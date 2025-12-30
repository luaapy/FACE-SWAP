import cv2
import numpy as np

class FaceSwapper:
    def __init__(self):
        pass

    def get_triangles(self, landmarks):
        """
        Calculates the Delaunay triangulation for the given landmarks.
        Returns a list of triangle indices (pt1, pt2, pt3).
        """
        rect = (0, 0, 4000, 4000) # Arbitrary large rectangle
        subdiv = cv2.Subdiv2D(rect)
        
        # Insert landmarks into subdiv
        for i, (x, y) in enumerate(landmarks):
            subdiv.insert((x, y)) # (x, y)

        # Get the triangles
        triangle_list = subdiv.getTriangleList()
        
        triangles = []
        for t in triangle_list:
            pts = [(t[0], t[1]), (t[2], t[3]), (t[4], t[5])]
            
            # Find indices for these points in the landmarks list
            # This is slow O(N^2), but N=468 is small enough for now
            # Optimization: Pre-calculate triangulation for the canonical face mesh if topology is constant
            indices = []
            for pt in pts:
                for i, (lx, ly) in enumerate(landmarks):
                    if abs(pt[0] - lx) < 1.0 and abs(pt[1] - ly) < 1.0:
                        indices.append(i)
                        break
            
            if len(indices) == 3:
                triangles.append(tuple(indices))
        
        return triangles

    def warp_triangle(self, img1, img2, t1, t2):
        """
        Warps a rectangular region defined by triangle t1 in img1 
        to triangle t2 in img2 (actually warping t1 content into t2 shape).
        
        img1: Source Image (Target Face texture)
        img2: Destination Image (User Face canvas) - modified in place
        t1: Coordinates of triangle in img1
        t2: Coordinates of triangle in img2
        """
        
        # Find bounding rectangle for each triangle
        r1 = cv2.boundingRect(np.float32([t1]))
        r2 = cv2.boundingRect(np.float32([t2]))

        # Offset points by left top corner of the respective rectangles
        t1_rect = []
        t2_rect = []
        t2_rect_int = []

        for i in range(3):
            t1_rect.append(((t1[i][0] - r1[0]), (t1[i][1] - r1[1])))
            t2_rect.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))
            t2_rect_int.append(((t2[i][0] - r2[0]), (t2[i][1] - r2[1])))

        # Get mask by filling triangle
        mask = np.zeros((r2[3], r2[2], 3), dtype=np.float32)
        cv2.fillConvexPoly(mask, np.int32(t2_rect_int), (1.0, 1.0, 1.0), 16, 0)

        # Apply warpImage to small rectangular patches
        img1_rect = img1[r1[1]:r1[1] + r1[3], r1[0]:r1[0] + r1[2]]
        
        size = (r2[2], r2[3])

        # Affine Transform
        warp_mat = cv2.getAffineTransform(np.float32(t1_rect), np.float32(t2_rect))
        img2_rect = cv2.warpAffine(img1_rect, warp_mat, size, None, flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
        
        # Alpha blend the patch
        img2_rect = img2_rect * mask

        # Copy triangular region of the rectangular patch to the output image
        # We need to be careful with boundaries
        if r2[3] > 0 and r2[2] > 0:
            roi = img2[r2[1]:r2[1]+r2[3], r2[0]:r2[0]+r2[2]]
            
            # Simple alpha blending logic: 
            # Output = (1 - mask) * ROI + img2_rect
            # But roi might be smaller than img2_rect if near edges
            
            # Ensure sizes match (clipping)
            h_roi, w_roi = roi.shape[:2]
            img2_rect = img2_rect[:h_roi, :w_roi]
            mask = mask[:h_roi, :w_roi]
            
            img2[r2[1]:r2[1]+h_roi, r2[0]:r2[0]+w_roi] = img2[r2[1]:r2[1]+h_roi, r2[0]:r2[0]+w_roi] * ((1.0, 1.0, 1.0) - mask) + img2_rect

