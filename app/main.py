from fastapi import FastAPI, Header, BackgroundTasks, HTTPException
from datetime import datetime
from app.export_service import export_full, export_incremental, export_delta
from app.database import engine
from sqlalchemy import text

app = FastAPI()

@app.get("/health")
def health():
    return {"status":"ok","timestamp":datetime.utcnow()}

@app.post("/exports/full")
def full_export(bg:BackgroundTasks, X_Consumer_ID:str=Header(...)):
    bg.add_task(export_full, X_Consumer_ID)
    return {"status":"started","exportType":"full"}

@app.post("/exports/incremental")
def inc_export(bg:BackgroundTasks, X_Consumer_ID:str=Header(...)):
    bg.add_task(export_incremental, X_Consumer_ID)
    return {"status":"started","exportType":"incremental"}

@app.post("/exports/delta")
def delta_export(bg:BackgroundTasks, X_Consumer_ID:str=Header(...)):
    bg.add_task(export_delta, X_Consumer_ID)
    return {"status":"started","exportType":"delta"}

@app.get("/exports/watermark")
def get_watermark(X_Consumer_ID:str=Header(...)):
    with engine.connect() as conn:
        res = conn.execute(text("SELECT last_exported_at FROM watermarks WHERE consumer_id=:c"),{"c":X_Consumer_ID}).fetchone()
    if not res:
        raise HTTPException(404,"Not Found")
    return {"consumerId":X_Consumer_ID,"lastExportedAt":str(res[0])}