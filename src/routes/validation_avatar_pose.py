import os
import tempfile
import cv2
from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from src.pose.validate import validate_a_pose
from src.manager.jobs_manager import create_job, update_job, get_job

router = APIRouter()

def run_validation(job_id: str, file_path: str):
    try:
        update_job(job_id, "running", 50)  # halfway
        cv_image = cv2.imread(file_path)
        result = validate_a_pose(cv_image)
        update_job(job_id, "completed", 100, result=result)
    except Exception as e:
        update_job(job_id, "failed", 100, error=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@router.post("/validate-pose")
async def validate_pose(background_tasks: BackgroundTasks, image: UploadFile = File(...)):
    suffix = os.path.splitext(image.filename or "")[1] or ".jpg"
    tmp_input = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)

    tmp_input.write(await image.read())
    tmp_input.close()

    job_id = create_job()
    background_tasks.add_task(run_validation, job_id, tmp_input.name)

    return {"job_id": job_id, "status": "queued"}
