import os
import tempfile
import cv2
from fastapi import APIRouter, UploadFile, File
from src.pose.validate import validate_a_pose

router = APIRouter()

@router.post("/validate-pose")
async def validate_pose(image: UploadFile = File(...)):
    """
    Validates if the uploaded image shows a valid A-pose.
    Returns pose validation results.
    """
    suffix = os.path.splitext(image.filename or "")[1] or ".jpg"
    tmp_input = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)

    try:
        # Save uploaded file to temp path
        tmp_input.write(await image.read())
        tmp_input.close()

        # Read image with OpenCV
        cv_image = cv2.imread(tmp_input.name)

        # Validate pose
        result = validate_a_pose(cv_image)

        return {"status": "success", "validation": result}

    finally:
        if os.path.exists(tmp_input.name):
            os.remove(tmp_input.name)
