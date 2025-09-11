import tempfile
import shutil
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
    Saves uploaded files to temp paths and calls make_fitroom_request.
    Returns task_id and status (CREATED).
    """
    try:
        # Save uploaded images to temp files
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as cloth_tmp:
            shutil.copyfileobj(cloth_image.file, cloth_tmp)
            cloth_path = cloth_tmp.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as model_tmp:
            shutil.copyfileobj(model_image.file, model_tmp)
            model_path = model_tmp.name

        # Call your existing function (expects file paths)
        result = make_fitroom_request(
            cloth_image=cloth_path,
            model_image=model_path,
            cloth_type=cloth_type,
            hd_mode=hd_mode,
        )

        return result

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

        if result.get("status") == "COMPLETED":
            response["download_signed_url"] = result.get("download_signed_url")

        return response

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))