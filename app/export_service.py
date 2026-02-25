import pandas as pd
from datetime import datetime
import uuid
from sqlalchemy import text
from app.database import engine

def export_full(consumer):
    job_id = str(uuid.uuid4())
    filename = f"output/full_{consumer}_{datetime.utcnow().timestamp()}.csv"

    df = pd.read_sql("SELECT * FROM users WHERE is_deleted=false", engine)
    df.to_csv(filename, index=False)

    max_time = df["updated_at"].max()
    with engine.begin() as conn:
        conn.execute(text("""
        INSERT INTO watermarks(consumer_id,last_exported_at,updated_at)
        VALUES(:c,:t,:t)
        ON CONFLICT (consumer_id)
        DO UPDATE SET last_exported_at=:t, updated_at=:t
        """), {"c":consumer,"t":max_time})

    return job_id, filename


def export_incremental(consumer):
    with engine.connect() as conn:
        res = conn.execute(text("SELECT last_exported_at FROM watermarks WHERE consumer_id=:c"),{"c":consumer}).fetchone()
        last = res[0] if res else '1970-01-01'

    query = f"SELECT * FROM users WHERE updated_at > '{last}' AND is_deleted=false"
    df = pd.read_sql(query, engine)

    filename = f"output/incremental_{consumer}_{datetime.utcnow().timestamp()}.csv"
    df.to_csv(filename, index=False)

    if len(df)>0:
        max_time = df["updated_at"].max()
        with engine.begin() as conn:
            conn.execute(text("""
            UPDATE watermarks SET last_exported_at=:t, updated_at=:t WHERE consumer_id=:c
            """), {"c":consumer,"t":max_time})

    return filename


def export_delta(consumer):
    with engine.connect() as conn:
        res = conn.execute(text("SELECT last_exported_at FROM watermarks WHERE consumer_id=:c"),{"c":consumer}).fetchone()
        last = res[0] if res else '1970-01-01'

    df = pd.read_sql(f"SELECT * FROM users WHERE updated_at > '{last}'", engine)

    ops=[]
    for _,r in df.iterrows():
        if r["is_deleted"]:
            ops.append("DELETE")
        elif r["created_at"]==r["updated_at"]:
            ops.append("INSERT")
        else:
            ops.append("UPDATE")
    df.insert(0,"operation",ops)

    filename = f"output/delta_{consumer}_{datetime.utcnow().timestamp()}.csv"
    df.to_csv(filename, index=False)

    if len(df)>0:
        max_time = df["updated_at"].max()
        with engine.begin() as conn:
            conn.execute(text("""
            INSERT INTO watermarks(consumer_id,last_exported_at,updated_at)
            VALUES(:c,:t,:t)
            ON CONFLICT (consumer_id)
            DO UPDATE SET last_exported_at=:t, updated_at=:t
            """), {"c":consumer,"t":max_time})

    return filename