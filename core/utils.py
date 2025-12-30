import numpy as np
import cv2

def normalize_landmarks(landmarks, width, height):
    """
    Convert normalized landmarks (0.0 - 1.0) to pixel coordinates.
    """
    points = []
    for lm in landmarks:
        x = int(lm.x * width)
        y = int(lm.y * height)
        points.append((x, y))
    return points

def get_face_mask(size, points):
    """
    Create a binary mask for the face region.
    """
    mask = np.zeros(size, dtype=np.uint8)
    if points is not None:
        cv2.fillConvexPoly(mask, cv2.convexHull(np.array(points)), 255)
    return mask
