# main.py
import cv2
import numpy as np
import matplotlib.pyplot as plt
import trimesh
from contour_processor import ContourProcessor
from cad_generator import CADGenerator
from mesh_validator import MeshValidator
import os

class JewelryCADPipeline:
    def __init__(self):
        self.contour_processor = ContourProcessor()
        self.cad_generator = CADGenerator()
        self.mesh_validator = MeshValidator()
        
    def process_image(self, image_path, output_stl_path, thickness=2.0):
        # Load and preprocess image
        print("Loading and preprocessing image...")
        
        # Fix file path for Windows
        image_path = os.path.normpath(image_path)
        if not os.path.exists(image_path):
            raise ValueError(f"File not found: {image_path}")
            
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image from {image_path}")
            
        processed = self.preprocess_image(image)
        
        # Extract and process contours
        print("Extracting contours...")
        contours = self.contour_processor.detect_contours(processed)
        refined_contours = self.contour_processor.refine_contours(contours)
        vector_curves = self.contour_processor.vectorize_contours(refined_contours)
        
        # Generate CAD geometry
        print("Generating CAD geometry...")
        cad_geometry = self.cad_generator.create_cad_geometry(vector_curves)
        
        # Extrude to 3D
        print("Extruding to 3D...")
        mesh = self.cad_generator.extrude_to_3d(cad_geometry, thickness=thickness)
        
        # Validate mesh
        print("Validating mesh...")
        is_valid, issues = self.mesh_validator.validate_mesh(mesh)
        
        if not is_valid:
            print(f"Mesh validation issues: {issues}")
            # Apply fixes if possible
            mesh = self.mesh_validator.fix_mesh(mesh)
            is_valid, issues = self.mesh_validator.validate_mesh(mesh)
            if not is_valid:
                print("Warning: Mesh still has issues after fixing attempts")
        
        # Export STL
        print(f"Exporting STL to {output_stl_path}...")
        output_stl_path = os.path.normpath(output_stl_path)
        mesh.export(output_stl_path)
        
        return {
            "image": image,
            "processed": processed,
            "contours": contours,
            "refined_contours": refined_contours,
            "vector_curves": vector_curves,
            "mesh": mesh,
            "validation": {
                "is_valid": is_valid,
                "issues": issues
            }
        }
    
    def preprocess_image(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Try different blur settings
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)  # Increased from (5,5)
        
        # Try without CLAHE (sometimes it causes issues)
        # clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        # enhanced = clahe.apply(blurred)
        enhanced = blurred  # Skip CLAHE
        
        # Try different thresholding
        _, binary = cv2.threshold(enhanced, 127, 255, cv2.THRESH_BINARY)  # Simple threshold
        
        # Morphological operations
        kernel = np.ones((5, 5), np.uint8)  # Larger kernel
        cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
        cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
        
        return cleaned

if __name__ == "__main__":
    pipeline = JewelryCADPipeline()
    
    # Test with a simple image first
    try:
        # Create a simple test image if needed
        test_img = np.ones((200, 200, 3), dtype=np.uint8) * 255
        cv2.circle(test_img, (100, 100), 50, (0, 0, 0), -1)  # Solid circle
        cv2.imwrite('simple_test.png', test_img)
        
        result = pipeline.process_image('simple_test.png', 'test_output.stl', thickness=2.0)
        print("Simple test completed successfully!")
        
    except Exception as e:
        print(f"Error in simple test: {e}")
