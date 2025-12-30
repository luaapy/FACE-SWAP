import cv2
import mediapipe as mp
import numpy as np
from core.utils import normalize_landmarks

class FaceDetector:
    def __init__(self, max_num_faces=1, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=max_num_faces,
            refine_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )

    def get_landmarks(self, image):
        """
        Detects face landmarks in the given image.
        Returns a list of (x, y) tuples for the first detected face.
        """
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(image_rgb)

        if results.multi_face_landmarks:
            # We only take the first face
            face_landmarks = results.multi_face_landmarks[0]
            h, w, _ = image.shape
            return normalize_landmarks(face_landmarks.landmark, w, h)
        return None
