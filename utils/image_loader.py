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
        Convert SVG to PNG using Inkscape (if available) or fallback to cairosvg
        """
        try:
            # Try using Inkscape first (more reliable)
            png_path = os.path.splitext(svg_path)[0] + "_converted.png"
            
            # Run Inkscape command to convert SVG to PNG
            cmd = [
                "inkscape", 
                svg_path, 
                "--export-type=png",
                f"--export-filename={png_path}",
                f"--export-width={output_size[0]}",
                f"--export-height={output_size[1]}"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(png_path):
                return self.load_raster_image(png_path)
            else:
                # Fallback to cairosvg if available
                try:
                    import cairosvg
                    png_data = cairosvg.svg2png(url=svg_path, output_width=output_size[0], output_height=output_size[1])
                    with open(png_path, 'wb') as f:
                        f.write(png_data)
                    return self.load_raster_image(png_path)
                except ImportError:
                    raise ImportError("Neither Inkscape nor cairosvg is available for SVG conversion")
                    
        except Exception as e:
            raise ValueError(f"Could not convert SVG to raster: {str(e)}")
