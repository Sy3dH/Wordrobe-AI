from google import genai
from google.genai import types
from src.configs.settings import GOOGLE_API_KEY
import json


def score_outfit(image_path: str, user_prompt: str = "") -> dict:
    """
    Evaluate an outfit image and return structured JSON rating.
    """
    client = genai.Client()

    system_prompt = """
    You are a fashion assistant. 
    Evaluate the outfit in the image based on:
    Color Harmony, Fit & Proportion, Style Consistency,
    Trend Alignment, Occasion Appropriateness, Accessories & Detailing.

    Return JSON with:
    {
      "ratings": {
        "color_harmony": {"score": int, "explanation": str},
        "fit_proportion": {"score": int, "explanation": str},
        "style_consistency": {"score": int, "explanation": str},
        "trend_alignment": {"score": int, "explanation": str},
        "occasion_appropriateness": {"score": int, "explanation": str},
        "accessories_detailing": {"score": int, "explanation": str}
      },
      "average_score": float,
      "overall_summary": str
    }
    """

    with open(image_path, "rb") as f:
        img_bytes = f.read()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            system_prompt,
            user_prompt or "",  # ensures no None
            types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg")
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON", "raw_output": response.text}
