# test_pipeline.py
from main import JewelryCADPipeline
import os

def test_with_examples():
    pipeline = JewelryCADPipeline()
    
    # Create test directory
    os.makedirs("test_results", exist_ok=True)
    
    # Test cases - now including SVG
    test_cases = [
        {
            "name": "ring",
            "image_path": "test_images/ring.svg",
            "thickness": 2.0
        },
        {
            "name": "pendant",
            "image_path": "test_images/pendant.svg",
            "thickness": 1.5
        },
        # You can still use PNG files
        {
            "name": "ring_sketch",
            "image_path": "test_images/ring_sketch.png",
            "thickness": 2.0
        }
    ]
    
    for test_case in test_cases:
        print(f"Processing {test_case['name']}...")
        
        try:
            result = pipeline.process_image(
                test_case["image_path"],
                f"test_results/{test_case['name']}.stl",
                thickness=test_case["thickness"]
            )
            
            print(f"Completed {test_case['name']}")
            print(f"Validation: {result['validation']}")
            
        except Exception as e:
            print(f"Error processing {test_case['name']}: {str(e)}")

if __name__ == "__main__":
    # First create sample SVG files if they don't exist
    if not os.path.exists("test_images/ring.svg") or not os.path.exists("test_images/pendant.svg"):
        print("Creating sample SVG files...")
        from create_sample_svg import create_ring_svg, create_pendant_svg
        os.makedirs("test_images", exist_ok=True)
        create_ring_svg()
        create_pendant_svg()
    
    test_with_examples()