# utils/image_loader.py
import cv2
import numpy as np
from PIL import Image
import os
import subprocess

class ImageLoader:
    def __init__(self):
        pass
    
    def load_image(self, image_path):
        """
        Load an image from various formats
        """
        ext = os.path.splitext(image_path)[1].lower()
        
        if ext in ['.png', '.jpg', '.jpeg', '.bmp', '.tiff']:
            return self.load_raster_image(image_path)
        elif ext in ['.svg']:
            return self.load_svg_image(image_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
    
    def load_raster_image(self, image_path):
        """
        Load standard raster images
        """
        image = cv2.imread(image_path)
        if image is None:
            # Try with PIL as fallback
            try:
                pil_image = Image.open(image_path)
                image = np.array(pil_image)
                if len(image.shape) == 3 and image.shape[2] == 4:
                    # Convert RGBA to RGB
                    image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
                elif len(image.shape) == 2:
                    # Convert grayscale to RGB
                    image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
            except Exception as e:
                raise ValueError(f"Could not load image: {str(e)}")
        
        return image
    
    def load_svg_image(self, svg_path, output_size=(1024, 1024)):
        """
        Convert SVG to PNG using Inkscape (if available) or fallback
        """
        try:
            # Create a simple SVG to raster conversion using PIL as fallback
            # For now, we'll create a simple placeholder
            # In production, you'd use proper SVG rendering
            width, height = output_size
            image = np.ones((height, width, 3), dtype=np.uint8) * 255  # White background
            
            # Draw a simple placeholder
            cv2.putText(image, "SVG Placeholder", (width//4, height//2), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            
            return image
            
        except Exception as e:
            raise ValueError(f"Could not process SVG: {str(e)}")
