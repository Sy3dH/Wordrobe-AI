import tempfile
import os
from typing import Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Form
from src.ai.scoring import score_outfit, score_outfit_with_clothing
from src.manager.jobs_manager import update_job, create_job
from src.notify.fcm_server import send_notification

router = APIRouter()

def run_ai_style_score(job_id: str, tmp_path: str, token: Optional[str] = None):
    try:
        update_job(job_id, "running", 50)
        result = score_outfit(image_path=tmp_path)
        update_job(job_id, "completed", 100, result=result)

        if token:
            data = {
                "title": "Style Score Completed",
                "body": "Your outfit score is ready!",
                "job_id": job_id,
                "tag": "scoring"
            }
            send_notification(token, data)

    except Exception as e:
        update_job(job_id, "failed", 100, error=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def run_ai_style_score_avatar_and_clothing(job_id: str, tmp_path1: str, tmp_path2: str, token: Optional[str] = None):
    try:
        update_job(job_id, "running", 50)
        result = score_outfit_with_clothing(
            person_image_path=tmp_path1,
            clothing_image_path=tmp_path2
        )
        update_job(job_id, "completed", 100, result=result)

        if token:
            data = {
                "title": "Style Score Completed",
                "body": "Your avatar + clothing score is ready!",
                "job_id": job_id,
                "tag": "scoring"
            }
            send_notification(token, data)

    except Exception as e:
        update_job(job_id, "failed", 100, error=str(e))
    finally:
        if os.path.exists(tmp_path1):
            os.remove(tmp_path1)
        if os.path.exists(tmp_path2):
            os.remove(tmp_path2)


@router.post("/ai-style-score")
async def ai_style_score(
    background_tasks: BackgroundTasks,
    image: UploadFile = File(...),
    token: Optional[str] = Form(None)
):
    """
    Queue an AI-powered style score job for a single outfit image.
    """
    suffix = os.path.splitext(image.filename or "")[1] or ".jpg"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp_path = tmp.name
    tmp.write(await image.read())
    tmp.close()

    job_id = create_job()
    background_tasks.add_task(run_ai_style_score, job_id, tmp_path, token)

    return {
        "job_id": job_id,
        "status": "queued",
        "notification": "enabled" if token else "not provided"
    }


@router.post("/ai-style-score-avatar-and-clothing")
async def ai_style_score_avatar_and_clothing(
    background_tasks: BackgroundTasks,
    user_image: UploadFile = File(...),
    clothing_image: UploadFile = File(...),
    token: Optional[str] = Form(None)
):
    """
    Queue an AI-powered style score job for avatar + clothing images.
    """
    suffix = os.path.splitext(user_image.filename or "")[1] or ".jpg"
    tmp1 = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp_path1 = tmp1.name
    tmp1.write(await user_image.read())
    tmp1.close()

    suffix = os.path.splitext(clothing_image.filename or "")[1] or ".jpg"
    tmp2 = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp_path2 = tmp2.name
    tmp2.write(await clothing_image.read())
    tmp2.close()

    job_id = create_job()
    background_tasks.add_task(
        run_ai_style_score_avatar_and_clothing, job_id, tmp_path1, tmp_path2, token
    )

    return {
        "job_id": job_id,
        "status": "queued",
        "notification": "enabled" if token else "not provided"
    }
