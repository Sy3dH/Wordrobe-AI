import requests
from src.configs.settings import FITROOM_API_KEY
from typing import Dict, Any

FITROOM_API_URL = "https://platform.fitroom.app/api/tryon/v2/tasks"

def make_fitroom_request(cloth_image: str, model_image: str, cloth_type: str, hd_mode: bool = True) -> Dict[str, Any]:
    """
    Sends a request to the Fitroom API with the given images and parameters.

    Args:
        cloth_image (str): Path to the cloth image file.
        model_image (str): Path to the model image file.
        cloth_type (str): Type of clothing (e.g., "upper", "lower").
        hd_mode (bool, optional): Whether to enable HD mode. Defaults to True.

    Returns:
        Dict[str, Any]: The JSON response from the Fitroom API.

    Raises:
        Exception: If the API returns a non-200 status code.
    """
    headers = {"X-API-KEY": FITROOM_API_KEY}
    data = {
        "cloth_type": cloth_type,
        "hd_mode": str(hd_mode).lower(),
    }

    with open(cloth_image, "rb") as c, open(model_image, "rb") as m:
        files = {
            "cloth_image": ("cloth.jpg", c, "image/jpeg"),
            "model_image": ("model.jpg", m, "image/jpeg"),
        }
        response = requests.post(FITROOM_API_URL, headers=headers, files=files, data=data)

    if response.status_code != 200:
        raise Exception(f"Fitroom API error {response.status_code}: {response.text}")

    return response.json()

def get_fitroom_task_status(task_id: str):
    """
    Fetch the status of a Fitroom try-on task.
    """
    url = f"{FITROOM_API_URL}/{task_id}"
    headers = {"X-API-KEY": FITROOM_API_KEY}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Fitroom API error: {response.status_code} {response.text}")

    return response.json()