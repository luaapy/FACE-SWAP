import cv2
import time

class WebcamCapture:
    def __init__(self, camera_id=0, width=640, height=480, fps=30):
        self.camera_id = camera_id
        self.width = width
        self.height = height
        self.fps = fps
        self.cap = None

    def start(self):
        self.cap = cv2.VideoCapture(self.camera_id)
        if not self.cap.isOpened():
            print(f"Error: Could not open webcam {self.camera_id}")
            return False
            
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cap.set(cv2.CAP_PROP_FPS, self.fps)
        return True

    def read(self):
        if self.cap:
            return self.cap.read()
        return False, None

    def release(self):
        if self.cap:
            self.cap.release()
