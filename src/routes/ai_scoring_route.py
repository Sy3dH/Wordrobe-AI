from fastapi import APIRouter, UploadFile, File, HTTPException
from src.ai.scoring import score_outfit
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
