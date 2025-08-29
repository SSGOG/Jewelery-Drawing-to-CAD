# run_png_images.py
from main import JewelryCADPipeline
import os
import glob

def process_png_images():
    pipeline = JewelryCADPipeline()
    
    # Create output directory
    os.makedirs("test_results", exist_ok=True)
    
    # Find all PNG files in test_images folder
    png_files = glob.glob("test_images/*.png")
    
    if not png_files:
        print("No PNG files found in test_images/ folder!")
        print("Please place your jewelry sketch images in test_images/ folder")
        return
    
    print(f"Found {len(png_files)} PNG file(s) to process:")
    for file in png_files:
        print(f"  - {file}")
    
    # Process each PNG file
    for png_file in png_files:
        try:
            # Get the base name without extension
            base_name = os.path.splitext(os.path.basename(png_file))[0]
            output_file = f"test_results/{base_name}.stl"
            
            print(f"\nProcessing {png_file}...")
            
            # Process with appropriate thickness based on jewelry type
            thickness = 2.0  # Default thickness
            
            # Adjust thickness based on filename
            if "ring" in base_name.lower():
                thickness = 2.0
            elif "pendant" in base_name.lower():
                thickness = 1.5
            elif "earring" in base_name.lower():
                thickness = 1.0
            elif "bracelet" in base_name.lower():
                thickness = 3.0
            
            result = pipeline.process_image(png_file, output_file, thickness=thickness)
            
            print(f"✓ Completed: {output_file}")
            print(f"  Validation: {'PASS' if result['validation']['is_valid'] else 'FAIL'}")
            if result['validation']['issues']:
                print(f"  Issues: {result['validation']['issues']}")
                
        except Exception as e:
            print(f"✗ Error processing {png_file}: {str(e)}")

if __name__ == "__main__":
    process_png_images()
