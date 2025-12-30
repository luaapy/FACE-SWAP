# Face Swap Real-Time

A Python application for real-time face swapping using MediaPipe and OpenCV. Supports file-based processing, webcam, and virtual camera output for streaming (Discord/Zoom).

## Features

- **Real-time Face Swap:** Uses MediaPipe Face Mesh for high-performance detection and landmark alignment.
- **Multiple Modes:**
    - `file`: Process video files or images for testing.
    - `webcam`: Real-time swap on your local webcam.
    - `virtual`: Output the swapped video to a virtual camera (requires OBS Virtual Cam or v4l2loopback).
- **Core Technology:**
    - Delaunay Triangulation & Affine Warping for geometry adaptation.
    - Seamless Cloning for natural blending.
    - Color Correction to match skin tones.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/face_swap_realtime.git
    cd face_swap_realtime
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: The `requirements.txt` file includes `opencv-python` for local GUI support. If you are running on a headless server (like a cloud sandbox), you may need to switch to `opencv-python-headless` to avoid missing library errors.*
    
    *For Virtual Camera support, you may need to install OS-specific drivers (e.g., OBS Studio with Virtual Camera on Windows, or `v4l2loopback` on Linux).*

## Usage

1.  **Configure:**
    Edit `config.py` to select the mode and paths:
    ```python
    CONFIG = {
        'mode': 'webcam',  # Options: 'file', 'webcam', 'virtual'
        'target_face': 'faces/elon_musk.jpg', # The face you want to wear
        ...
    }
    ```

2.  **Run the Application:**
    ```bash
    python main.py
    ```

3.  **UI Control (Experimental):**
    A Tkinter-based UI is available for easier control (requires local display environment):
    ```bash
    python ui/main_window.py
    ```

## Adding New Faces

1.  Find a clear, frontal photo of the person you want to swap with.
2.  Save it to the `faces/` directory.
3.  Update `target_face` in `config.py` or use the UI to select it.

## Troubleshooting

-   **"No module named mediapipe"**: Ensure you installed requirements. If you have conflicts, try `pip install mediapipe==0.10.14`.
-   **Virtual Camera error**: Make sure the virtual camera driver is installed and active before running the script in `virtual` mode.
-   **Lighting**: For best results, ensure both the user and the target face have even lighting.

## Credits

-   **MediaPipe** by Google for Face Mesh.
-   **OpenCV** for image processing.
-   **pyvirtualcam** for virtual camera interfacing.

## Disclaimer

This software is for educational and entertainment purposes only. Do not use it for unethical activities such as deepfakes without consent or impersonation.
