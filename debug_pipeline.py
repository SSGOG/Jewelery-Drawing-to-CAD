# debug_pipeline.py
import cv2
import numpy as np
import matplotlib.pyplot as plt
from contour_processor import ContourProcessor
from cad_generator import CADGenerator
import os

def debug_image_processing(image_path):
    print(f"Debugging: {image_path}")
    
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"ERROR: Could not load image from {image_path}")
        return
    
    print(f"Image shape: {image.shape}")
    
    # Preprocess
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(blurred)
    _, binary = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    kernel = np.ones((3, 3), np.uint8)
    cleaned = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_OPEN, kernel)
    
    # Show preprocessing steps
    plt.figure(figsize=(15, 5))
    
    plt.subplot(1, 4, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Original")
    
    plt.subplot(1, 4, 2)
    plt.imshow(binary, cmap='gray')
    plt.title("Binary")
    
    plt.subplot(1, 4, 3)
    plt.imshow(cleaned, cmap='gray')
    plt.title("Cleaned")
    
    # Process contours
    processor = ContourProcessor()
    contours = processor.detect_contours(cleaned)
    refined = processor.refine_contours(contours)
    curves = processor.vectorize_contours(refined)
    
    # Draw contours
    contour_img = image.copy()
    for i, contour in enumerate(refined):
        color = (0, 255, 0) if i == 0 else (0, 0, 255)  # First contour green, others red
        cv2.drawContours(contour_img, [contour], -1, color, 2)
    
    plt.subplot(1, 4, 4)
    plt.imshow(cv2.cvtColor(contour_img, cv2.COLOR_BGR2RGB))
    plt.title("Contours")
    
    plt.tight_layout()
    plt.savefig("debug_preprocessing.png")
    plt.show()
    
    # Try to create CAD geometry
    cad_gen = CADGenerator()
    polygons = cad_gen.create_cad_geometry(curves)
    
    print(f"Created {len(polygons)} polygons")
    for i, poly in enumerate(polygons):
        print(f"Polygon {i}: area={poly.area:.2f}, valid={poly.is_valid}")
    
    return len(polygons) > 0

if __name__ == "__main__":
    # Test with your images
    images = ["test_images/ring.png", "test_images/pendant.png"]
    
    for img_path in images:
        if os.path.exists(img_path):
            success = debug_image_processing(img_path)
            print(f"{img_path}: {'SUCCESS' if success else 'FAILED'}")
        else:
            print(f"File not found: {img_path}")
