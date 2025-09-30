import os
import tempfile
from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks
from src.upscale.upscale_full_image import upscale_realesrgan
from src.manager.jobs_manager import create_job, update_job
from src.notify.fcm_server import send_notification

router = APIRouter()

def run_upscale(job_id: str, file_path: str, outscale: float, face_enhance: bool, token: Optional[str] = None):
    try:
        update_job(job_id, "running", 50)
        results = upscale_realesrgan(
            input_path=file_path,
            outscale=outscale,
            face_enhance=face_enhance
        )
        update_job(job_id, "completed", 100, result={"processed_images": results})

        if token:
            data = {
                "title": "Upscale Completed",
                "body": "Your image has been upscaled successfully!",
                "job_id": job_id,
                "tag": "upscaling",
                "processed_images": f"{results[0]}"
            }
            send_notification(token, data)

    except Exception as e:
        update_job(job_id, "failed", 100, error=str(e))
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


@router.post("/upscale-image")
async def upscale_image(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    outscale: float = Form(4.0),
    face_enhance: bool = Form(True),
    token: Optional[str] = Form(None)
):
    suffix = os.path.splitext(image.filename or "")[1] or ".jpg"
    tmp_input = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)

    tmp_input.write(await image.read())
    tmp_input.close()

    job_id = create_job()
    background_tasks.add_task(run_upscale, job_id, tmp_input.name, outscale, face_enhance, token)

    return {
        "job_id": job_id,
        "status": "queued",
        "notification": "enabled" if token else "not provided"
    }
