# app/routes.py

from fastapi import APIRouter, Header, HTTPException, BackgroundTasks
from datetime import datetime
import uuid
from app.export_service import run_export_job
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import Watermark

router = APIRouter()

# ================= HEALTH CHECK ================= #

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat()
    }


# ================= FULL EXPORT ================= #

@router.post("/exports/full", status_code=202)
def full_export(
    background_tasks: BackgroundTasks,
    x_consumer_id: str = Header(..., alias="X-Consumer-ID")
):
    job_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"full_{x_consumer_id}_{timestamp}.csv"

    background_tasks.add_task(run_export_job, job_id, x_consumer_id, "full", filename)

    return {
        "jobId": job_id,
        "status": "started",
        "exportType": "full",
        "outputFilename": filename
    }


# ================= INCREMENTAL EXPORT ================= #

@router.post("/exports/incremental", status_code=202)
def incremental_export(
    background_tasks: BackgroundTasks,
    x_consumer_id: str = Header(..., alias="X-Consumer-ID")
):
    job_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"incremental_{x_consumer_id}_{timestamp}.csv"

    background_tasks.add_task(run_export_job, job_id, x_consumer_id, "incremental", filename)

    return {
        "jobId": job_id,
        "status": "started",
        "exportType": "incremental",
        "outputFilename": filename
    }


# ================= DELTA EXPORT ================= #

@router.post("/exports/delta", status_code=202)
def delta_export(
    background_tasks: BackgroundTasks,
    x_consumer_id: str = Header(..., alias="X-Consumer-ID")
):
    job_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filename = f"delta_{x_consumer_id}_{timestamp}.csv"

    background_tasks.add_task(run_export_job, job_id, x_consumer_id, "delta", filename)

    return {
        "jobId": job_id,
        "status": "started",
        "exportType": "delta",
        "outputFilename": filename
    }


# ================= GET WATERMARK ================= #

@router.get("/exports/watermark")
def get_watermark(
    x_consumer_id: str = Header(..., alias="X-Consumer-ID"),
    db: Session = next(get_db())
):
    watermark = db.query(Watermark).filter(Watermark.consumer_id == x_consumer_id).first()

    if not watermark:
        raise HTTPException(status_code=404, detail="Watermark not found")

    return {
        "consumerId": watermark.consumer_id,
        "lastExportedAt": watermark.last_exported_at.isoformat()
    }