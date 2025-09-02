import requests
from src.configs.settings import FITROOM_API_KEY

FITROOM_API_URL = "https://platform.fitroom.app/api/tryon/v2/tasks"

def make_fitroom_request(cloth_image, model_image, cloth_type: str, hd_mode: bool = True):
    """
    Sends a request to the Fitroom API with given images and parameters.
    """
    files = {
        "cloth_image": ("cloth.jpg", cloth_image, "image/jpeg"),
        "model_image": ("model.jpg", model_image, "image/jpeg"),
    }
    data = {
        "cloth_type": cloth_type,
        "hd_mode": str(hd_mode).lower(),
    }
    headers = {"X-API-KEY": FITROOM_API_KEY}

    response = requests.post(FITROOM_API_URL, headers=headers, files=files, data=data)

    if response.status_code != 200:
        raise Exception(f"Fitroom API error: {response.status_code} {response.text}")

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
