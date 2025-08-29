# utils/visualization.py
import matplotlib.pyplot as plt
import cv2
import numpy as np
import open3d as o3d

class Visualization:
    def __init__(self):
        pass
    
    def draw_processing_steps(self, results, output_path):
        """
        Create a visualization of the processing pipeline steps
        """
        plt.figure(figsize=(15, 10))
        
        # Original image
        plt.subplot(2, 3, 1)
        plt.imshow(cv2.cvtColor(results["image"], cv2.COLOR_BGR2RGB))
        plt.title("Original Image")
        plt.axis('off')
        
        # Processed image
        plt.subplot(2, 3, 2)
        plt.imshow(results["processed"], cmap='gray')
        plt.title("Processed Image")
        plt.axis('off')
        
        # Detected contours
        plt.subplot(2, 3, 3)
        contour_img = results["image"].copy()
        cv2.drawContours(contour_img, results["contours"], -1, (0, 255, 0), 2)
        plt.imshow(cv2.cvtColor(contour_img, cv2.COLOR_BGR2RGB))
        plt.title("Detected Contours")
        plt.axis('off')
        
        # Refined contours
        plt.subplot(2, 3, 4)
        refined_img = results["image"].copy()
        for contour in results["refined_contours"]:
            cv2.drawContours(refined_img, [contour], -1, (0, 255, 0), 2)
        plt.imshow(cv2.cvtColor(refined_img, cv2.COLOR_BGR2RGB))
        plt.title("Refined Contours")
        plt.axis('off')
        
        # Vector curves (simplified visualization)
        plt.subplot(2, 3, 5)
        vector_img = np.ones_like(results["image"]) * 255
        for curve in results["vector_curves"]:
            points = np.array(curve["points"], dtype=np.int32)
            cv2.polylines(vector_img, [points], curve["is_closed"], (0, 0, 255), 2)
        plt.imshow(cv2.cvtColor(vector_img, cv2.COLOR_BGR2RGB))
        plt.title("Vector Curves")
        plt.axis('off')
        
        # 3D mesh preview
        plt.subplot(2, 3, 6)
        try:
            # Create a simple 2D projection of the 3D mesh
            mesh = results["mesh"]
            if mesh is not None:
                # Get the 2D outline of the mesh (top-down view)
                vertices_2d = mesh.vertices[:, :2]  # Ignore Z coordinate
                plt.scatter(vertices_2d[:, 0], vertices_2d[:, 1], s=1, alpha=0.5)
                plt.title("3D Mesh Outline")
        except:
            plt.text(0.5, 0.5, "3D Preview\nNot Available", 
                    ha='center', va='center', transform=plt.gca().transAxes)
        plt.axis('off')
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
    
    def visualize_3d_mesh(self, mesh):
        """
        Interactive 3D visualization using Open3D
        """
        if mesh is None:
            print("No mesh to visualize")
            return
        
        # Convert trimesh to open3d
        vertices = np.array(mesh.vertices)
        faces = np.array(mesh.faces)
        
        o3d_mesh = o3d.geometry.TriangleMesh()
        o3d_mesh.vertices = o3d.utility.Vector3dVector(vertices)
        o3d_mesh.triangles = o3d.utility.Vector3iVector(faces)
        o3d_mesh.compute_vertex_normals()
        
        # Create visualization
        o3d.visualization.draw_geometries([o3d_mesh])
    
    def create_validation_report(self, mesh, output_path):
        """
        Create a visualization of mesh validation results
        """
        fig, axes = plt.subplots(2, 2, figsize=(10, 10))
        
        # Mesh overview
        if mesh is not None:
            # Get the 2D projection from different angles
            vertices = mesh.vertices
            
            # Top view (XY plane)
            axes[0, 0].scatter(vertices[:, 0], vertices[:, 1], s=1, alpha=0.5)
            axes[0, 0].set_title("Top View (XY)")
            axes[0, 0].set_aspect('equal')
            
            # Front view (XZ plane)
            axes[0, 1].scatter(vertices[:, 0], vertices[:, 2], s=1, alpha=0.5)
            axes[0, 1].set_title("Front View (XZ)")
            axes[0, 1].set_aspect('equal')
            
            # Side view (YZ plane)
            axes[1, 0].scatter(vertices[:, 1], vertices[:, 2], s=1, alpha=0.5)
            axes[1, 0].set_title("Side View (YZ)")
            axes[1, 0].set_aspect('equal')
            
            # Statistics
            stats_text = f"""
            Mesh Statistics:
            - Vertices: {len(vertices)}
            - Faces: {len(mesh.faces)}
            - Volume: {mesh.volume:.2f}
            - Bounds: {mesh.bounds}
            - Watertight: {mesh.is_watertight}
            """
            axes[1, 1].text(0.1, 0.9, stats_text, fontsize=10, va='top')
            axes[1, 1].set_title("Mesh Statistics")
            axes[1, 1].set_axis_off()
        
        plt.tight_layout()
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        plt.close()
