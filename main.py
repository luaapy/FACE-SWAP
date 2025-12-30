import cv2
import sys
import os
import numpy as np
from config import CONFIG
from core.face_detector import FaceDetector
from core.face_swapper import FaceSwapper
from core.blender import Blender
from core.utils import get_face_mask

class FaceSwapApp:
    def __init__(self, config):
        self.config = config
        self.detector = FaceDetector()
        self.swapper = FaceSwapper()
        self.blender = Blender()
        
        self.target_img = None
        self.target_landmarks = None
        self.target_triangles = None
        
        self.load_target_face(self.config['target_face'])

    def load_target_face(self, path):
        if not os.path.exists(path):
            print(f"Target face not found: {path}")
            return
            
        self.target_img = cv2.imread(path)
        self.target_landmarks = self.detector.get_landmarks(self.target_img)
        
        if self.target_landmarks is None:
            print(f"No face detected in target image: {path}")
            return

        self.target_triangles = self.swapper.get_triangles(self.target_landmarks)
        print(f"Loaded target face: {path} with {len(self.target_landmarks)} landmarks.")

    def process_frame(self, frame):
        if self.target_img is None or self.target_landmarks is None:
            return frame

        # Detect face in current frame (User)
        user_landmarks = self.detector.get_landmarks(frame)
        
        if user_landmarks is None:
            # No face found, return original frame
            return frame

        # Prepare images
        img_target = self.target_img
        img_user = frame
        img_new_face = np.zeros_like(img_user)
        
        # Warp triangles
        for t_indices in self.target_triangles:
            t1 = [self.target_landmarks[i] for i in t_indices]
            t2 = [user_landmarks[i] for i in t_indices]
            
            self.swapper.warp_triangle(img_target, img_new_face, t1, t2)

        # Generate Mask for Seamless Cloning
        # Create a mask of the new face (warped)
        face_mask = np.zeros_like(img_user, dtype=np.uint8)
        face_mask_gray = get_face_mask((img_user.shape[0], img_user.shape[1]), user_landmarks)
        
        # Refine mask: convex hull of user landmarks
        # The simple warping puts content into img_new_face.
        # We need a mask to blend img_new_face onto img_user
        
        # Calculate center for seamlessClone
        rect = cv2.boundingRect(cv2.convexHull(np.array(user_landmarks)))
        center = (int(rect[0] + rect[2] / 2), int(rect[1] + rect[3] / 2))

        # Color Correction
        if self.config.get('color_correction', False):
            # We perform color transfer from the user face (roi) to the target face texture
            # But since img_target is the full image, we should probably do it on the warped result or the source texture
            # Simpler approach: Match the global tone of the target image to the user image
            # Or better: Match the target face pixels to the user face pixels
            
            # Since we are warping 'img_target' into 'img_new_face', we should ideally color correct img_target first
            # But for simplicity in this pipeline, we can try to color match the texture being warped.
            # However, `warp_triangle` reads from `img_target` directly.
            
            # Let's do a simple global match on the target image before warping (if it hasn't been done)
            # Note: This is computationally expensive to do every frame if we did it on the whole image.
            # A better place would be on load, but lighting changes per frame.
            
            # Alternative: Match the warped result before blending? 
            # No, 'img_new_face' has black background.
            
            # We will use a flag to do it once or optimize. For now, let's match the target image to the current frame.
            # To avoid modifying the cached self.target_img, we work on a copy or just the texture.
            
            # Optimization: Only match if significant lighting change?
            # For this implementation, we will apply it to the source texture `img_target` before warping.
            # But `img_target` is shared. 
            
            # Let's create a temporary color-corrected target for this frame.
            img_target = self.blender.match_color(img_target, img_user)

        # Blending
        output = self.blender.seamless_clone(img_user, img_new_face, face_mask_gray, center)
        
        return output

    def run(self):
        mode = self.config['mode']
        
        if mode == 'file':
            from io_module.file_processor import FileProcessor
            processor = FileProcessor(self.config['input_source'], self.config['output_path'], self.process_frame)
            processor.run()
            
        elif mode == 'webcam':
            from io_module.webcam_capture import WebcamCapture
            cap = WebcamCapture(0, self.config['width'], self.config['height'], self.config['fps'])
            if cap.start():
                while True:
                    ret, frame = cap.read()
                    if not ret: break
                    
                    output = self.process_frame(frame)
                    cv2.imshow("Face Swap", output)
                    
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                cap.release()
                cv2.destroyAllWindows()

        elif mode == 'virtual':
            from io_module.webcam_capture import WebcamCapture
            from io_module.virtual_camera import VirtualCamera
            
            cap = WebcamCapture(0, self.config['width'], self.config['height'], self.config['fps'])
            vcam = VirtualCamera(self.config['width'], self.config['height'], self.config['fps'])
            
            if cap.start() and vcam.start():
                print("Running in Virtual Camera Mode. Press Ctrl+C to stop.")
                try:
                    while True:
                        ret, frame = cap.read()
                        if not ret: break
                        
                        output = self.process_frame(frame)
                        vcam.send(output)
                except KeyboardInterrupt:
                    pass
                finally:
                    cap.release()
                    vcam.stop()

if __name__ == "__main__":
    app = FaceSwapApp(CONFIG)
    app.run()
