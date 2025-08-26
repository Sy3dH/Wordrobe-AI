from src.prompts.prompts import FULL_BODY_GENERATION_PROMPT

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