import os
import tempfile
from fastapi import APIRouter, UploadFile, File
from src.crop.object_crop import crop_image

router = APIRouter()

@router.post("/crop-avatar")
async def crop_avatar(image: UploadFile = File(...)):
    """
    Crops an uploaded avatar image by removing its background.
    Saves output in src/output/cropped directory.
    """
    suffix = os.path.splitext(image.filename or "")[1] or ".jpg"
    tmp_input = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)

    try:
        tmp_input.write(await image.read())
        tmp_input.close()

        cropped_path = crop_image(tmp_input.name, image.filename)
        return {"status": "success", "cropped_image_path": cropped_path}
    finally:
        if os.path.exists(tmp_input.name):
            os.remove(tmp_input.name)