import pyvirtualcam
import numpy as np
import cv2

class VirtualCamera:
    def __init__(self, width=640, height=480, fps=30):
        self.width = width
        self.height = height
        self.fps = fps
        self.cam = None
        self.active = False

    def start(self):
        try:
            self.cam = pyvirtualcam.Camera(width=self.width, height=self.height, fps=self.fps)
            self.active = True
            print(f"Virtual Camera started: {self.cam.device}")
            return True
        except Exception as e:
            print(f"Error starting virtual camera: {e}")
            print("Ensure OBS Virtual Camera or v4l2loopback is installed and active.")
            self.active = False
            return False

    def send(self, frame):
        if self.active and self.cam:
            # pyvirtualcam expects RGB, OpenCV uses BGR
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Ensure size matches
            if frame.shape[1] != self.width or frame.shape[0] != self.height:
                frame_rgb = cv2.resize(frame_rgb, (self.width, self.height))
                
            self.cam.send(frame_rgb)
            self.cam.sleep_until_next_frame()

    def stop(self):
        if self.cam:
            self.cam.close()
            self.active = False
