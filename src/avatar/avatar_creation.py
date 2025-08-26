import os
import time
import requests
from typing import Dict, Any
from src.utils import encode_image_to_base64
from src.configs.settings import BFL_API_KEY

OUTPUT_DIR = os.path.join("src", "output", "avatar_creation_service")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def validate_and_merge_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """Validate and merge user config with default FULL_BODY_GENERATION_CONFIG."""
    final_config = {**config}

    if not final_config.get("prompt"):
        raise ValueError("Config error: 'prompt' is required.")

    if final_config.get("output_format") not in ["jpeg", "png"]:
        raise ValueError("Config error: 'output_format' must be 'jpeg' or 'png'.")

    if not isinstance(final_config.get("seed"), int):
        raise ValueError("Config error: 'seed' must be an integer.")

    if not isinstance(final_config.get("safety_tolerance"), int):
        raise ValueError("Config error: 'safety_tolerance' must be an integer.")

    return final_config


def generate_flux_image_with_reference(
    image_path: str,
    config: Dict[str, Any],
    poll_interval: float = 1.0,
    output_dir: str = "output"
) -> Dict[str, Any]:
    """
    Generate image using FLUX API with reference image and config.
    Handles async polling until image is ready, and saves the result locally.
    """
    # Merge with defaults + validate
    final_config = validate_and_merge_config(config)

    # Encode image
    encoded_image = encode_image_to_base64(image_path)

    url = "https://api.bfl.ai/v1/flux-kontext-pro"
    headers = {
        "Content-Type": "application/json",
        "x-key": BFL_API_KEY,
    }

    payload = {
        "prompt": final_config["prompt"],
        "input_image": encoded_image,
        "seed": final_config["seed"],
        "output_format": final_config["output_format"],
        "prompt_upsampling": final_config["prompt_upsampling"],
        "safety_tolerance": final_config["safety_tolerance"],
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Initial request failed: {response.status_code}, {response.text}")

    job_data = response.json()
    polling_url = job_data.get("url") or job_data.get("polling_url")
    request_id = job_data.get("id")

    if not polling_url or not request_id:
        raise Exception(f"Missing polling details in response: {job_data}")

    # Step 2: Poll until ready
    while True:
        time.sleep(poll_interval)
        poll_response = requests.get(
            polling_url,
            headers={
                "accept": "application/json",
                "x-key": BFL_API_KEY,
            },
            params={"id": request_id},
        )

        if poll_response.status_code != 200:
            raise Exception(f"Polling failed: {poll_response.status_code}, {poll_response.text}")

        result = poll_response.json()
        status = result.get("status")

        if status == "Ready":
            image_url = result["result"]["sample"]

            # Step 3: Download the image
            os.makedirs(output_dir, exist_ok=True)
            output_filename = os.path.join(
                output_dir, f"flux_output_{request_id}.{final_config['output_format']}"
            )

            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                with open(output_filename, "wb") as f:
                    f.write(img_response.content)
                print(f"✅ Image saved at: {output_filename}")
            else:
                print(f"⚠️ Failed to download image from {image_url}")

            return {"status": "Ready", "image_url": image_url, "saved_path": output_filename, "raw": result}

        elif status in ["Error", "Failed"]:
            print(f"❌ Generation failed: {result}")
            return {"status": status, "error": result}
