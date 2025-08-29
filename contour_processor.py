# contour_processor.py
import cv2
import numpy as np
from scipy import interpolate

class ContourProcessor:
    def __init__(self, min_contour_length=50, epsilon_factor=0.01):
        self.min_contour_length = min_contour_length
        self.epsilon_factor = epsilon_factor
    
    def detect_contours(self, binary_image):
        contours, hierarchy = cv2.findContours(
            binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
        )
        
        print(f"Found {len(contours)} contours initially")
        
        # Filter small contours
        filtered_contours = [
            cnt for cnt in contours 
            if cv2.arcLength(cnt, True) > self.min_contour_length
        ]
        
        print(f"After filtering: {len(filtered_contours)} contours")
        return filtered_contours
    
    def refine_contours(self, contours):
        refined_contours = []
        for i, contour in enumerate(contours):
            # Approximate contour with fewer points
            epsilon = self.epsilon_factor * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Only keep contours with enough points
            if len(approx) >= 3:
                refined_contours.append(approx)
        
        print(f"After refinement: {len(refined_contours)} contours")
        return refined_contours
    
    def vectorize_contours(self, contours):
        vector_curves = []
        
        for i, contour in enumerate(contours):
            points = contour.reshape(-1, 2)
            if len(points) >= 3:  # Ensure we have at least 3 points
                # Check if contour is closed (first and last points are close)
                if np.linalg.norm(points[0] - points[-1]) < 10:
                    is_closed = True
                else:
                    is_closed = False
                
                curve = {
                    "type": "polyline",
                    "points": points.tolist(),
                    "is_closed": is_closed,
                    "contour_index": i
                }
                vector_curves.append(curve)
                print(f"Contour {i}: {len(points)} points, closed: {is_closed}")
        
        print(f"Vectorized {len(vector_curves)} curves")
        return vector_curves
