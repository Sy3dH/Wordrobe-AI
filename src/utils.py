import base64
import cv2
import numpy as np

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
