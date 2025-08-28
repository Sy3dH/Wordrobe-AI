import os
import tempfile
from fastapi import APIRouter, UploadFile, File, Form
from src.upscale.upscale_full_image import upscale_realesrgan

router = APIRouter()

@router.post("/upscale-image")
async def upscale_image(
    image: UploadFile = File(...),
    outscale: float = Form(4.0),
    face_enhance: bool = Form(True)
):
    suffix = os.path.splitext(image.filename or "")[1] or ".jpg"
    tmp_input = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)

    try:
        # Stream upload to temp file
        with open(tmp_input.name, "wb") as buffer:
            while chunk := await image.read(1024 * 1024):
                buffer.write(chunk)

        # Process upscale
        results = upscale_realesrgan(
            input_path=tmp_input.name,
            outscale=outscale,
            face_enhance=face_enhance
        )

        return {"status": "success", "processed_images": results}
    finally:
        if os.path.exists(tmp_input.name):
            os.remove(tmp_input.name)
