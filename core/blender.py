import cv2
import numpy as np

class Blender:
    def __init__(self):
        pass

    def seamless_clone(self, destination, source, mask, center):
        """
        Applies seamless cloning to blend the warped face onto the destination.
        
        destination: User face image (background)
        source: Warped target face image
        mask: Binary mask of the face
        center: Center of the face region
        """
        try:
            # Normal cloning
            output = cv2.seamlessClone(source, destination, mask, center, cv2.NORMAL_CLONE)
            return output
        except Exception as e:
            print(f"Blending failed: {e}")
            return destination

    def match_color(self, source, target):
        """
        Matches the color tone of source image to target image.
        Simple mean/std matching in LAB color space.
        """
        source_lab = cv2.cvtColor(source, cv2.COLOR_BGR2LAB).astype("float32")
        target_lab = cv2.cvtColor(target, cv2.COLOR_BGR2LAB).astype("float32")

        # Compute statistics
        src_mean, src_std = cv2.meanStdDev(source_lab)
        tgt_mean, tgt_std = cv2.meanStdDev(target_lab)

        src_mean = src_mean.flatten()
        src_std = src_std.flatten()
        tgt_mean = tgt_mean.flatten()
        tgt_std = tgt_std.flatten()

        # Subtract the means from the source
        source_lab -= src_mean

        # Scale by the standard deviations
        # Avoid division by zero
        scale = tgt_std / (src_std + 1e-5)
        source_lab *= scale

        # Add the target means
        source_lab += tgt_mean

        # Clip values
        source_lab = np.clip(source_lab, 0, 255).astype("uint8")
        
        return cv2.cvtColor(source_lab, cv2.COLOR_LAB2BGR)
