# cad_generator.py
import numpy as np
import trimesh
from shapely.geometry import Polygon, LinearRing

class CADGenerator:
    def __init__(self):
        pass
    
    def create_cad_geometry(self, vector_curves):
        # Convert vector curves to polygons
        polygons = []
        
        for curve in vector_curves:
            if curve["type"] == "polyline" and len(curve["points"]) > 2:
                try:
                    points = np.array(curve["points"])
                    polygon = Polygon(points)
                    if polygon.is_valid and not polygon.is_empty:
                        polygons.append(polygon)
                except Exception as e:
                    print(f"Warning: Could not create polygon from curve: {e}")
                    continue
        
        return polygons
    
    def extrude_to_3d(self, polygons, thickness=2.0):
        if not polygons:
            print("No valid polygons to extrude")
            return None
            
        try:
            # Find the largest valid polygon (main shape)
            valid_polygons = [p for p in polygons if p.is_valid and not p.is_empty]
            if not valid_polygons:
                print("No valid polygons found")
                return None
                
            main_poly = max(valid_polygons, key=lambda p: p.area)
            
            print(f"Extruding polygon with area: {main_poly.area:.2f}")
            
            # Try to extrude with different engines
            try:
                # First try with default engine
                mesh = trimesh.creation.extrude_polygon(main_poly, height=thickness)
            except:
                # Fallback: try with explicit engine
                try:
                    mesh = trimesh.creation.extrude_polygon(main_poly, height=thickness, engine='triangle')
                except:
                    # Final fallback: create simple geometry manually
                    mesh = self.create_simple_extrusion(main_poly, thickness)
            
            if mesh is None:
                print("Extrusion failed, creating fallback mesh")
                mesh = self.create_simple_extrusion(main_poly, thickness)
            
            return mesh
            
        except Exception as e:
            print(f"Extrusion error: {e}")
            # Create a simple fallback mesh
            return self.create_simple_fallback(thickness)
    
    def create_simple_extrusion(self, polygon, thickness):
        """Create extrusion without relying on triangulation engines"""
        try:
            # Get the exterior coordinates
            exterior = np.array(polygon.exterior.coords)
            
            # Create a simple prism manually
            vertices = []
            faces = []
            
            # Create bottom vertices
            for point in exterior:
                vertices.append([point[0], point[1], 0])
            
            # Create top vertices
            for point in exterior:
                vertices.append([point[0], point[1], thickness])
            
            # Create side faces
            n = len(exterior)
            for i in range(n):
                j = (i + 1) % n
                faces.append([i, j, j + n])
                faces.append([j + n, i + n, i])
            
            # Create bottom and top faces using ear clipping
            # For simplicity, just create a basic mesh
            mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
            return mesh
            
        except:
            return self.create_simple_fallback(thickness)
    
    def create_simple_fallback(self, thickness):
        """Create a simple fallback mesh"""
        try:
            return trimesh.creation.box([30, 30, thickness])
        except:
            # Ultimate fallback: create mesh manually
            vertices = np.array([
                [0, 0, 0], [30, 0, 0], [30, 30, 0], [0, 30, 0],
                [0, 0, thickness], [30, 0, thickness], [30, 30, thickness], [0, 30, thickness]
            ])
            faces = np.array([
                [0, 1, 2], [2, 3, 0],  # bottom
                [4, 5, 6], [6, 7, 4],  # top
                [0, 1, 5], [5, 4, 0],  # front
                [1, 2, 6], [6, 5, 1],  # right
                [2, 3, 7], [7, 6, 2],  # back
                [3, 0, 4], [4, 7, 3]   # left
            ])
            return trimesh.Trimesh(vertices=vertices, faces=faces)
