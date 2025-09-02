from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from src.VTON.try_on_service import make_fitroom_request, get_fitroom_task_status

router = APIRouter()


@router.post("/tryon")
async def tryon(
    cloth_image: UploadFile = File(...),
    model_image: UploadFile = File(...),
    cloth_type: str = Form(...),
    hd_mode: bool = Form(True),
):
    """
    Create a try-on task in Fitroom.
    Returns task_id and status (CREATED).
    """
    try:
        cloth_bytes = await cloth_image.read()
        model_bytes = await model_image.read()

        result = make_fitroom_request(
            cloth_image=cloth_bytes,
            model_image=model_bytes,
            cloth_type=cloth_type,
            hd_mode=hd_mode,
        )
        return {"task": result}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tryon/status/{task_id}")
async def tryon_status(task_id: str):
    """
    Check the status of a try-on task.
    Returns progress and signed download URL if completed.
    """
    try:
        result = get_fitroom_task_status(task_id)

        response = {
            "task_id": result.get("task_id"),
            "status": result.get("status"),
            "progress": result.get("progress", 0),
        }

        # Only add signed URL if task completed
        if result.get("status") == "COMPLETED":
            response["download_signed_url"] = result.get("download_signed_url")

        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
