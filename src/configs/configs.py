from src.prompts.prompts import FULL_BODY_GENERATION_PROMPT, FACT_EXTRACTION_PROMPT
from src.configs.settings import GOOGLE_API_KEY

LTM_CONFIG = {
    "llm": {
        "provider": "gemini",
        "config": {
            "model": "gemini-2.5-flash-lite",
            "api_key": GOOGLE_API_KEY,
            "temperature": 0.2,
            "max_tokens": 2000,
            "top_p": 1.0
        },
        "custom_fact_extraction_prompt": FACT_EXTRACTION_PROMPT,
    },
    "embedder": {
        "provider": "huggingface",
        "config": {
            "model": "multi-qa-MiniLM-L6-cos-v1"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "collection_name": "ltm",
            "host": "localhost",
            "port": 6333,
            "embedding_model_dims":384
        }
    },
"version": "v1.1",
}

STM_CONFIG = {
    "llm": {
        "provider": "gemini",
        "config": {
            "model": "gemini-2.5-flash-lite",
            "api_key": GOOGLE_API_KEY,
            "temperature": 0.2,
            "max_tokens": 2000,
            "top_p": 1.0
        },
    },
    "embedder": {
        "provider": "huggingface",
        "config": {
            "model": "multi-qa-MiniLM-L6-cos-v1"
        }
    },
    "vector_store": {
            "provider": "qdrant",
            "config": {
                "collection_name": "stm",
                "host": "localhost",
                "port": 6333,
                "embedding_model_dims":384
            }
        }
}

FULL_BODY_GENERATION_CONFIG = {
    "prompt": FULL_BODY_GENERATION_PROMPT,
    "seed": 30,
    "output_format": "jpeg",
    "prompt_upsampling": True,
    "safety_tolerance": 2
}

POSE_VALIDATION_CONFIG = {
    "is_a_pose": False,
    "obstructions": {
        "torso": False,
        "hips": False,
        "legs": False,
        "arms_crossing": False,
        "legs_crossing": False
    },
    "comments": ""
    }