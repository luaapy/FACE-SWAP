import cv2
import numpy as np

def create_face_image(filename, color_bg, color_face):
    # Create a blank image
    img = np.zeros((480, 640, 3), dtype=np.uint8)
    img[:] = color_bg
    
    # Draw a face (circle)
    center = (320, 240)
    radius = 100
    cv2.circle(img, center, radius, color_face, -1)
    
    # Draw eyes
    eye_radius = 15
    eye_color = (255, 255, 255)
    cv2.circle(img, (280, 210), eye_radius, eye_color, -1)
    cv2.circle(img, (360, 210), eye_radius, eye_color, -1)
    
    # Draw pupils
    pupil_radius = 5
    pupil_color = (0, 0, 0)
    cv2.circle(img, (280, 210), pupil_radius, pupil_color, -1)
    cv2.circle(img, (360, 210), pupil_radius, pupil_color, -1)
    
    # Draw nose
    nose_pts = np.array([[320, 220], [300, 260], [340, 260]], np.int32)
    cv2.fillPoly(img, [nose_pts], (100, 100, 100))
    
    # Draw mouth (rectangle)
    cv2.rectangle(img, (280, 280), (360, 300), (0, 0, 150), -1)
    
    cv2.imwrite(filename, img)
    print(f"Created {filename}")

# Create "User" face (Blue background, Skin color face)
create_face_image('test_assets/user_face.jpg', (50, 50, 50), (200, 200, 255))

# Create "Target" face (Green background, Different skin color)
create_face_image('faces/target_face.jpg', (50, 100, 50), (180, 220, 255))
