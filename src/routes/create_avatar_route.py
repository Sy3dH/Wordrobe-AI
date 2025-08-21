from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from src.avatar.avatar_creation import generate_flux_image_with_reference
from src.configs.configs import FULL_BODY_GENERATION_CONFIG
import tempfile
import os

router = APIRouter()

@router.post("/avatar-creation")
async def avatar_creation(image: UploadFile = File(...)):
    """
    Generate an image using the default FULL_BODY_GENERATION_CONFIG.
    Only the image file is required.
    """
    suffix = os.path.splitext(image.filename or "")[1] or ".jpg"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp_path = tmp.name
    try:
        tmp.write(await image.read())
        if os.path.exists(tmp_path):
            print(f"✅ Temp file exists at: {tmp_path}")
        else:
            print(f"❌ Temp file was not created.")
        tmp.close()

        result = generate_flux_image_with_reference(
            image_path=tmp_path,
            config=FULL_BODY_GENERATION_CONFIG
        )
        return FileResponse(result["saved_path"])

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
