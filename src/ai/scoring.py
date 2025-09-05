from google import genai
from google.genai import types
from src.configs.settings import GOOGLE_API_KEY
import json

client = genai.Client(api_key=GOOGLE_API_KEY)

def score_outfit_with_clothing(person_image_path: str, clothing_image_path: str, user_prompt: str = "") -> dict:
    """
    Takes a person image + clothing image and evaluates the hypothetical outfit.
    Returns structured JSON with fashion ratings.
    """

    # Read images
    with open(person_image_path, "rb") as f:
        person_bytes = f.read()
    with open(clothing_image_path, "rb") as f:
        clothing_bytes = f.read()

    # Instructions for AI
    system_prompt = """
    You are a fashion assistant.
    The first image is a person. The second image is the clothing they will wear.
    Imagine the clothing on the person and evaluate the resulting outfit based on:
    - Color Harmony
    - Fit & Proportion
    - Style Consistency
    - Trend Alignment
    - Occasion Appropriateness
    - Accessories & Detailing

    For each category:
    - Give a score between 1 and 10.
    - Provide a 1–2 sentence explanation.

    Return JSON strictly in this format:
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

    # Generate content with interleaved images + text
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            system_prompt,
            "This is the person.",
            types.Part.from_bytes(data=person_bytes, mime_type="image/jpeg"),
            "This is the clothing the person will wear.",
            types.Part.from_bytes(data=clothing_bytes, mime_type="image/jpeg"),
            user_prompt or ""  # optional extra context from user
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    # Parse response
    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON", "raw_output": response.text}


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
