# Jewelry Design to 3D CAD Pipeline

This project implements an AI-driven pipeline that converts jewelry design images into 3D CAD models suitable for manufacturing.

## Features

- Image preprocessing and enhancement
- Precise contour detection and vectorization
- CAD-compatible geometry generation
- 3D extrusion with customizable thickness
- Mesh validation and manufacturability checking
- STL export for 3D printing

## Installation

1. Clone this repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Usage

1. Place your jewelry design images in the `test_images` folder
2. Run the pipeline: `python test_pipeline.py`
3. Check the `test_results` folder for generated STL files

## Pipeline Architecture

1. **Image Preprocessing**: 
   - Grayscale conversion
   - Noise reduction
   - Contrast enhancement
   - Thresholding and morphological operations

2. **Contour Processing**:
   - Contour detection using OpenCV
   - Contour refinement and smoothing
   - Vectorization for CAD compatibility

3. **CAD Generation**:
   - Conversion to NURBS curves
   - Handling of nested contours (holes)
   - 3D extrusion with specified thickness

4. **Mesh Validation**:
   - Watertightness checking
   - Self-intersection detection
   - Thickness validation
   - Automatic mesh repair

## Alternative Approaches Considered

### Computer Vision Techniques
- **Canny Edge Detection**: Good for general edge detection but lacks precision for complex jewelry designs
- **Hough Transforms**: Effective for simple shapes but struggles with organic curves
- **Deep Learning-based segmentation**: Potentially more accurate but requires extensive training data

### 3D Reconstruction Methods
- **Neural Implicit Surfaces**: Promising for complex shapes but computationally intensive
- **Diffusion-based methods**: Emerging technology but not yet mature for precision applications
- **Multi-view reconstruction**: Not applicable to single-view sketches

### Why This Approach Was Chosen
This pipeline combines traditional computer vision techniques with CAD-aware processing to ensure:
- High precision for manufacturing requirements
- Watertight mesh generation
- Controllable parameters for different jewelry types
- Reasonable computational requirements

## Manufacturability Considerations

The pipeline ensures manufacturability through:

1. **Watertight Meshes**: All output meshes are checked and repaired to be watertight
2. **Minimum Thickness**: Validation ensures all parts meet minimum thickness requirements
3. **No Self-Intersections**: Meshes are checked and repaired to eliminate self-intersections
4. **Consistent Normals**: All face normals are consistently oriented for 3D printing

## Examples

The repository includes two test cases:
1. Ring design with uniform thickness
2. Pendant design with complex contours

## Future Improvements

1. Integration with Rhino.Compute for more advanced CAD operations
2. Machine learning-based contour classification
3. Support for color images and texture extraction
4. Parameter optimization based on jewelry type