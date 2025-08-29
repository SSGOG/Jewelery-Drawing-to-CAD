# mesh_validator.py
import trimesh
import numpy as np

class MeshValidator:
    def __init__(self):
        pass
    
    def validate_mesh(self, mesh):
        issues = []
        
        if mesh is None:
            return False, ["Mesh is None"]
        
        # Check if mesh is watertight
        if hasattr(mesh, 'is_watertight') and not mesh.is_watertight:
            issues.append("Mesh is not watertight")
        
        # Check for degenerate faces
        if hasattr(mesh, 'faces') and mesh.faces.shape[0] > 0:
            if hasattr(mesh, 'area') and mesh.area < 1e-6:
                issues.append("Mesh area is too small")
            
            # Check for non-manifold edges
            if hasattr(mesh, 'is_winding_consistent') and not mesh.is_winding_consistent:
                issues.append("Mesh has inconsistent winding")
            
            # Check for self-intersections (only if available)
            if hasattr(mesh, 'self_intersecting') and mesh.self_intersecting:
                issues.append("Mesh has self-intersections")
        
        # Check thickness (minimum dimension)
        if hasattr(mesh, 'bounds'):
            bounds = mesh.bounds
            size = bounds[1] - bounds[0]
            if min(size) < 0.1:  # Minimum thickness check
                issues.append(f"Mesh is too thin in one dimension: {min(size):.3f}")
        
        is_valid = len(issues) == 0
        return is_valid, issues
    
    def fix_mesh(self, mesh):
        if mesh is None:
            return None
            
        # Try to fix common mesh issues
        try:
            # Remove duplicate vertices
            if hasattr(mesh, 'merge_vertices'):
                mesh.merge_vertices()
            
            # Fix winding
            if hasattr(mesh, 'fix_normals'):
                mesh.fix_normals()
            
            # Fill holes if possible
            if hasattr(mesh, 'fill_holes'):
                mesh.fill_holes()
            
            # Remove unreferenced vertices
            if hasattr(mesh, 'remove_unreferenced_vertices'):
                mesh.remove_unreferenced_vertices()
            
            return mesh
            
        except Exception as e:
            print(f"Mesh fixing failed: {e}")
            return mesh
