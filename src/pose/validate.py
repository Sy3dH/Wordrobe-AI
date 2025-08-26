import cv2
import mediapipe as mp
from src.pose.checks import (check_arms_crossing_midline,check_legs_crossed,check_legs_obstructing_torso,
                             check_wrists_on_torso)
from src.configs.configs import POSE_VALIDATION_CONFIG
from logging import getLogger

logging = getLogger(__name__)

def validate_a_pose(image):
    h, w, _ = image.shape

    with mp_pose.Pose(static_image_mode=True) as pose:
        results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if not results.pose_landmarks:
            POSE_VALIDATION_CONFIG["comments"] = "No person detected"
            return POSE_VALIDATION_CONFIG

        lms = results.pose_landmarks.landmark

        # Run checks
        arms_crossing = check_arms_crossing_midline(mp_pose,lms, w, h)
        wrists_on_torso = check_wrists_on_torso(mp_pose,lms, w, h)
        legs_on_torso = check_legs_obstructing_torso(mp_pose,lms, w, h)
        legs_crossed = check_legs_crossed(mp_pose,lms, w, h)

        POSE_VALIDATION_CONFIG["obstructions"]["arms_crossing"] = arms_crossing
        POSE_VALIDATION_CONFIG["obstructions"]["torso"] = wrists_on_torso
        POSE_VALIDATION_CONFIG["obstructions"]["legs_on_torso"] = legs_on_torso
        POSE_VALIDATION_CONFIG["obstructions"]["legs_crossing"] = legs_crossed

        # Decision: A-pose only if no obstructions
        if not any([arms_crossing, wrists_on_torso, legs_on_torso, legs_crossed]):
            POSE_VALIDATION_CONFIG["is_a_pose"] = True
            POSE_VALIDATION_CONFIG["comments"] = "Pose is acceptable; clothing visible."
        else:
            POSE_VALIDATION_CONFIG["comments"] = "Obstructions detected."

        return POSE_VALIDATION_CONFIG

if __name__ == "__main__":
    mp_pose = mp.solutions.pose
    image_path = "D:\9D Tech Work\Wardrobe-POC\POC\sample\\validation_check\criss cross arms\\2.jpg"
    image = cv2.imread(image_path)
    print(validate_a_pose(image))