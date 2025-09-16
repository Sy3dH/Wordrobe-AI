import os
import tempfile
from fastapi import APIRouter, UploadFile, File, BackgroundTasks
from src.crop.object_crop import crop_image
from src.manager.jobs_manager import create_job, update_job
from src.notify.fcm_server import send_notification

router = APIRouter()

#TODO: testing the notification

def run_crop(job_id: str, file_path: str, filename: str, token: str):
    try:
        update_job(job_id, "running", 50)
        cropped_path = crop_image(file_path, filename)
        update_job(job_id, "completed", 100, result={"cropped_image_path": cropped_path})
        data =  {
                "title": "Crop Completed",
                "body": f"Your cropped avatar is ready!",
                "job_id": job_id,
                "cropped_image_path": cropped_path
                }
        send_notification(token, data)
    except Exception as e:
        update_job(job_id, "failed", 100, error=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@router.post("/crop-avatar")
async def crop_avatar(background_tasks: BackgroundTasks, image: UploadFile = File(...), token: str = ""):
    suffix = os.path.splitext(image.filename or "")[1] or ".jpg"
    tmp_input = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)

    tmp_input.write(await image.read())
    tmp_input.close()

    job_id = create_job()
    background_tasks.add_task(run_crop, job_id, tmp_input.name, image.filename, token)

    return {"job_id": job_id, "status": "queued"}
