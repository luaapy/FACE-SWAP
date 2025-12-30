import tkinter as tk
from tkinter import ttk, filedialog
import cv2
import threading
from PIL import Image, ImageTk
from config import CONFIG

class MainWindow:
    def __init__(self, root, app_logic):
        self.root = root
        self.app_logic = app_logic
        self.root.title("Real-Time Face Swap")
        self.root.geometry("1000x700")
        
        # Style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Layout
        self.create_widgets()
        
        # Video Loop
        self.running = False
        self.video_thread = None
        
    def create_widgets(self):
        # Top Bar
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill=tk.X)
        
        ttk.Label(top_frame, text="Face Swap Control Panel", font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        
        # Main Content - Split into Video and Controls
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Video Display (Left)
        self.video_frame = ttk.Frame(content_frame, borderwidth=2, relief="sunken")
        self.video_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.video_label = ttk.Label(self.video_frame, text="Video Output")
        self.video_label.pack(expand=True)
        
        # Controls (Right)
        control_panel = ttk.Frame(content_frame, width=300, padding=10)
        control_panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Face Selection
        ttk.Label(control_panel, text="Target Face:").pack(anchor=tk.W, pady=(0, 5))
        self.face_path_var = tk.StringVar(value=CONFIG['target_face'])
        ttk.Entry(control_panel, textvariable=self.face_path_var).pack(fill=tk.X, pady=5)
        ttk.Button(control_panel, text="Browse...", command=self.browse_face).pack(fill=tk.X, pady=5)
        ttk.Button(control_panel, text="Load Face", command=self.load_face).pack(fill=tk.X, pady=5)
        
        # Settings
        ttk.Label(control_panel, text="Settings", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(20, 10))
        
        self.blend_var = tk.DoubleVar(value=1.0)
        ttk.Label(control_panel, text="Blending Strength:").pack(anchor=tk.W)
        ttk.Scale(control_panel, variable=self.blend_var, from_=0.0, to=1.0).pack(fill=tk.X, pady=5)
        
        self.color_correct_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(control_panel, text="Color Correction", variable=self.color_correct_var).pack(anchor=tk.W, pady=5)
        
        # Mode Selection
        ttk.Label(control_panel, text="Mode:").pack(anchor=tk.W, pady=(10, 5))
        self.mode_var = tk.StringVar(value="webcam")
        ttk.Radiobutton(control_panel, text="Webcam", variable=self.mode_var, value="webcam").pack(anchor=tk.W)
        ttk.Radiobutton(control_panel, text="Virtual Camera", variable=self.mode_var, value="virtual").pack(anchor=tk.W)
        
        # Start/Stop
        self.btn_start = ttk.Button(control_panel, text="START", command=self.toggle_video)
        self.btn_start.pack(fill=tk.X, pady=20)
        
    def browse_face(self):
        filename = filedialog.askopenfilename(filetypes=[("Images", "*.jpg *.png")])
        if filename:
            self.face_path_var.set(filename)
            
    def load_face(self):
        path = self.face_path_var.get()
        if path:
            self.app_logic.load_target_face(path)
            
    def toggle_video(self):
        if not self.running:
            self.start_video()
        else:
            self.stop_video()
            
    def start_video(self):
        self.running = True
        self.btn_start.configure(text="STOP")
        self.video_thread = threading.Thread(target=self.video_loop)
        self.video_thread.daemon = True
        self.video_thread.start()
        
    def stop_video(self):
        self.running = False
        self.btn_start.configure(text="START")
        
    def video_loop(self):
        # Simplified video loop for UI demo
        # In real integration, this would connect to FaceSwapApp's capture
        cap = cv2.VideoCapture(0)
        while self.running:
            ret, frame = cap.read()
            if ret:
                # Process frame
                output = self.app_logic.process_frame(frame)
                
                # Convert to ImageTk
                frame_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # Update Label (thread safe way usually requires queue, but this is simple demo)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
            
            # Simple FPS control
            cv2.waitKey(30)
            
        cap.release()

if __name__ == "__main__":
    # If run directly, try to import the real app logic
    try:
        # Add parent directory to path to import core/io modules
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        
        from main import FaceSwapApp
        from config import CONFIG
        
        # Override config for UI control if needed
        # CONFIG['mode'] = 'webcam' 
        
        app_logic = FaceSwapApp(CONFIG)
        
        root = tk.Tk()
        app = MainWindow(root, app_logic)
        print("UI started with Real App Logic.")
        # root.mainloop() # Commented out for headless env
        
    except ImportError as e:
        print(f"Could not import real app logic: {e}")
        # Fallback to Dummy
        class DummyApp:
            def load_target_face(self, path): print(f"Load {path}")
            def process_frame(self, frame): return frame
            
        root = tk.Tk()
        app = MainWindow(root, DummyApp())
        print("UI started with Dummy App Logic.")
