import base64
import cv2
from typing import Dict, Any
import numpy as np

def get_combined_config(llm_config: Dict[str,Any], embedding_config: Dict[str,Any], memory_config:Dict[str,Any]) -> Dict[str, Any]:
    """
    Merge all configs into one unified dictionary.
    """
    combined = {}
    combined.update(llm_config)
    combined.update(embedding_config)
    combined.update(memory_config)
    return combined

def encode_image_to_base64(image_path: str) -> str:
    """
    Encode an image file to a base64 string.
    """
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def get_xy(lm, image_w, image_h):
    return int(lm.x * image_w), int(lm.y * image_h)

def point_in_polygon(point, polygon):
    """Check if point lies inside polygon using cv2"""
    return cv2.pointPolygonTest(np.array(polygon, np.int32), point, False) >= 0


def angle_between_points(a, b, c):
        """Returns angle ABC in degrees."""
        ba = np.array(a) - np.array(b)
        bc = np.array(c) - np.array(b)
        cos_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        cos_angle = np.clip(cos_angle, -1.0, 1.0)
        return np.degrees(np.arccos(cos_angle))