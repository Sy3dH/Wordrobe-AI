from src.utils import get_xy, point_in_polygon

def check_arms_crossing_midline(mp_pose, landmarks, w, h):

    lw, _ = get_xy(landmarks[mp_pose.PoseLandmark.LEFT_WRIST], w, h)
    rw, _ = get_xy(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST], w, h)
    ls, _ = get_xy(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER], w, h)
    rs, _ = get_xy(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER], w, h)

    mid_x = (ls + rs) // 2
    return (lw < mid_x) and (rw > mid_x)


def check_wrists_on_torso(mp_pose,landmarks, w, h):

    ls = get_xy(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER], w, h)
    rs = get_xy(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER], w, h)
    lh = get_xy(landmarks[mp_pose.PoseLandmark.LEFT_HIP], w, h)
    rh = get_xy(landmarks[mp_pose.PoseLandmark.RIGHT_HIP], w, h)

    torso_poly = [ls, rs, rh, lh]
    wrists = [
        get_xy(landmarks[mp_pose.PoseLandmark.LEFT_WRIST], w, h),
        get_xy(landmarks[mp_pose.PoseLandmark.RIGHT_WRIST], w, h)
    ]
    elbows = [
        get_xy(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW], w, h),
        get_xy(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW], w, h)
    ]

    for pt in wrists + elbows:
        if point_in_polygon(pt, torso_poly):
            return True
    return False


def check_legs_obstructing_torso(mp_pose, landmarks, w, h):

    ls = get_xy(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER], w, h)
    rs = get_xy(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER], w, h)
    lh = get_xy(landmarks[mp_pose.PoseLandmark.LEFT_HIP], w, h)
    rh = get_xy(landmarks[mp_pose.PoseLandmark.RIGHT_HIP], w, h)
    torso_poly = [ls, rs, rh, lh]

    knees = [
        get_xy(landmarks[mp_pose.PoseLandmark.LEFT_KNEE], w, h),
        get_xy(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE], w, h)
    ]
    for pt in knees:
        if point_in_polygon(pt, torso_poly):
            return True
    return False


def check_legs_crossed(mp_pose, landmarks, w, h):

    lk = get_xy(landmarks[mp_pose.PoseLandmark.LEFT_KNEE], w, h)
    rk = get_xy(landmarks[mp_pose.PoseLandmark.RIGHT_KNEE], w, h)
    la = get_xy(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE], w, h)
    ra = get_xy(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE], w, h)

    knees_crossed = lk[0] < rk[0]
    ankles_crossed = la[0] < ra[0]

    return knees_crossed or ankles_crossed
