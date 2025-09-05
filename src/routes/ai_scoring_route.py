from fastapi import APIRouter, UploadFile, File, HTTPException
from src.ai.scoring import score_outfit, score_outfit_with_clothing
import tempfile, os

router = APIRouter()

@router.post("/ai-style-score")
async def ai_style_score(image: UploadFile = File(...)):
    """
    Evaluate outfit image and return AI-powered fashion rating in JSON format.
    """
    suffix = os.path.splitext(image.filename or "")[1] or ".jpg"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp_path = tmp.name

    try:
        tmp.write(await image.read())
        tmp.close()

        result = score_outfit(image_path=tmp_path)
        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


@router.post("/ai-style-score_avatar_and_clothing")
async def ai_style_score_avatar_and_clothing(user_image: UploadFile = File(...), clothing_image: UploadFile = File(...)):
    """
    Evaluate outfit image and return AI-powered fashion rating in JSON format.
    """
    suffix = os.path.splitext(user_image.filename or "")[1] or ".jpg"
    tmp1 = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    suffix = os.path.splitext(clothing_image.filename or "")[1] or ".jpg"
    tmp2 = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    tmp_path1 = tmp1.name
    tmp_path2 = tmp2.name

    try:
        tmp1.write(await user_image.read())
        tmp1.close()

        tmp2.write(await clothing_image.read())
        tmp2.close()

        result = score_outfit_with_clothing(person_image_path=tmp_path1, clothing_image_path=tmp_path2)
        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    finally:
        if os.path.exists(tmp_path1):
            os.remove(tmp_path1)

        if os.path.exists(tmp_path2):
            os.remove(tmp_path2)