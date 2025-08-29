# test_pipeline.py
from main import JewelryCADPipeline
import os
import glob

def test_with_examples():
    pipeline = JewelryCADPipeline()
    
    # Create test directory
    os.makedirs("test_results", exist_ok=True)
    os.makedirs("test_images", exist_ok=True)
    
    # Find all image files
    image_extensions = ['*.png', '*.jpg', '*.jpeg', '*.bmp']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join("test_images", ext)))
    
    if not image_files:
        print("No image files found in test_images/ folder!")
        print("Please place your jewelry images in test_images/ folder")
        return
    
    print(f"Found {len(image_files)} image file(s) to process:")
    for file in image_files:
        print(f"  - {file}")
    
    # Test cases
    test_cases = []
    for img_file in image_files:
        base_name = os.path.splitext(os.path.basename(img_file))[0]
        test_cases.append({
            "name": base_name,
            "image_path": img_file,
            "thickness": 2.0  # Default thickness
        })
    
    for test_case in test_cases:
        print(f"\nProcessing {test_case['name']}...")
        
        try:
            result = pipeline.process_image(
                test_case["image_path"],
                f"test_results/{test_case['name']}.stl",
                thickness=test_case["thickness"]
            )
            
            print(f"✓ Completed {test_case['name']}")
            print(f"  Validation: {'PASS' if result['validation']['is_valid'] else 'FAIL'}")
            if result['validation']['issues']:
                print(f"  Issues: {result['validation']['issues']}")
            
        except Exception as e:
            print(f"✗ Error processing {test_case['name']}: {str(e)}")

if __name__ == "__main__":
    test_with_examples()
