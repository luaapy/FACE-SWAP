import cv2
import time
import os

class FileProcessor:
    def __init__(self, input_path, output_dir, process_frame_callback):
        self.input_path = input_path
        self.output_dir = output_dir
        self.process_frame_callback = process_frame_callback

    def run(self):
        if not os.path.exists(self.input_path):
            print(f"Error: File {self.input_path} not found.")
            return

        # Check if image or video
        ext = os.path.splitext(self.input_path)[1].lower()
        if ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            self.process_image()
        else:
            self.process_video()

    def process_image(self):
        frame = cv2.imread(self.input_path)
        if frame is None:
            print("Error reading image.")
            return
            
        start_time = time.time()
        processed_frame = self.process_frame_callback(frame)
        duration = time.time() - start_time
        
        output_path = os.path.join(self.output_dir, f"output_{os.path.basename(self.input_path)}")
        cv2.imwrite(output_path, processed_frame)
        print(f"Processed image saved to {output_path} (Time: {duration:.3f}s)")

    def process_video(self):
        cap = cv2.VideoCapture(self.input_path)
        if not cap.isOpened():
            print("Error opening video file.")
            return

        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        output_path = os.path.join(self.output_dir, f"output_{os.path.basename(self.input_path)}")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_count = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            processed_frame = self.process_frame_callback(frame)
            out.write(processed_frame)
            
            frame_count += 1
            if frame_count % 30 == 0:
                print(f"Processed {frame_count} frames...")

        cap.release()
        out.release()
        print(f"Video processing complete. Saved to {output_path}")
