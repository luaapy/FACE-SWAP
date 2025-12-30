import cv2
from core.face_detector import FaceDetector

def test_detector():
    img_path = 'test_assets/user_face.jpg'
    img = cv2.imread(img_path)
    if img is None:
        print(f"Error: Could not read {img_path}")
        return

    detector = FaceDetector()
    landmarks = detector.get_landmarks(img)

    if landmarks:
        print(f"Success! Detected {len(landmarks)} landmarks.")
        # Draw some landmarks to verify
        for (x, y) in landmarks:
            cv2.circle(img, (x, y), 1, (0, 255, 0), -1)
        cv2.imwrite('output/detected_face.jpg', img)
        print("Saved detection result to output/detected_face.jpg")
    else:
        print("Failed to detect face.")

if __name__ == "__main__":
    test_detector()
