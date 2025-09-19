from google import genai
from google.genai import types
from src.prompts.prompts import AI_SCORING_WITH_CLOTHING_PROMPT, AI_SCORING_PROMPT, AI_SCORING_PROMPT_WITH_MEMORY
from src.configs.settings import GOOGLE_API_KEY
from src.memory.memory_manager import MemoryManager
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
    system_prompt = AI_SCORING_WITH_CLOTHING_PROMPT

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
    system_prompt = AI_SCORING_PROMPT
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

def memory_score_outfit(image_path: str, user_id: str, user_prompt: str = "") -> dict:
    m = MemoryManager()
    system_prompt = AI_SCORING_PROMPT_WITH_MEMORY

    # 🔹 Search for specific memories
    score_related_memories = m.ltm.memory.search(
        "How scoring should be done?",
        user_id=user_id,
        filters={"category": "scoring"}
    )
    score_mem_texts = [
        mem.get("memory", "") for mem in score_related_memories.get("results", [])
    ]
    score_memories_str = " ".join(score_mem_texts) if score_mem_texts else ""

    # 🔹 Get all memories
    existing_memories = m.ltm.memory.get_all(user_id=user_id)
    memories = ["The user memories are as follows:"]
    for mem in existing_memories.get("results", []):
        mem_text = mem.get("memory")
        if mem_text:
            memories.append(mem_text)
    memories_str = "\n".join(memories)

    # 🔹 Load image
    with open(image_path, "rb") as f:
        img_bytes = f.read()

    # 🔹 Send request
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            system_prompt,
            user_prompt or "",
            memories_str,
            score_memories_str,
            types.Part.from_bytes(data=img_bytes, mime_type="image/jpeg")
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
        )
    )

    try:
        return json.loads(response.text)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON", "raw_output": response.text}


def feedback_score(feedback:str, user_id:str):
    return m.ltm.apply_feedback(user_feedback=feedback, user_id=user_id, filters="scoring")

if __name__ == "__main__":
    print(m.ltm.memory.get_all(user_id="user_7"))
    # print(memory_score_outfit("C:\\Users\Hamza\Downloads\\tmp57fo91m1_out-ezgif.com-webp-to-jpg-converter.jpg",
    #                           "user_7", ""))