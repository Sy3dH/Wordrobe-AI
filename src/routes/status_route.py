from fastapi import APIRouter
from src.manager.jobs_manager import get_job

router = APIRouter()

@router.get("/status/{job_id}")
async def get_status(job_id: str):
    """
    Retrieve the status and result of a background job.
    """
    return get_job(job_id)
