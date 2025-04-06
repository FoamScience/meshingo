import numpy as np
import trimesh
import os.path
import pandas as pd
from pathlib import Path
import argparse
from tqdm import tqdm
import open3d as o3d
import subprocess
import time
import shutil
import re
import scipy.spatial

def refine_surface(mesh: trimesh.Trimesh, output_path: str, k : float, p : float) -> trimesh.Trimesh:
    """
    Refine input surface to achieve a minimum number of triangles per surface area
    that scales with model length.

    Args:
        mesh (trimesh.Trimesh): Input mesh
        filname (str): Output output_path for refined surface
        k (float): Base triangle density
        p (float): Scaling exponent
        
    Returns:
        float: Normalized surface-to-volume ratio (0 to 1)
    """
    bbox_min, bbox_max = mesh.bounds
    L = np.linalg.norm(bbox_max - bbox_min)
    A = mesh.area
    density = k * (L ** p)
    min_n_triangles = int(density * A)
    curr_n_triangles = len(mesh.faces)
    n_subdivides = 0
    while (curr_n_triangles < min_n_triangles):
        mesh = mesh.subdivide()
        curr_n_triangles = len(mesh.faces)
        n_subdivides += 1
    if (n_subdivides > 0):
        mesh.export(output_path)
    return mesh

def compute_surface_volume_ratio(mesh: trimesh.Trimesh) -> float:
    """
    Compute a normalized surface-to-volume ratio (SVR) of a mesh.
    Returns a value between 0 and 1, where higher values indicate a higher surface area
    relative to volume.
    
    Args:
        mesh (trimesh.Trimesh): Input mesh
        
    Returns:
        float: Normalized surface-to-volume ratio (0 to 1)
    """
    surface_area = mesh.area
    volume = abs(mesh.volume)
    if volume == 0:
        return 1.0
    svr = surface_area / (volume ** (2/3))
    normalized_svr = np.clip(svr / 20.0, 0.0, 1.0)
    return float(normalized_svr)

def compute_max_curvature(mesh: trimesh.Trimesh) -> float:
    """
    Compute a normalized approximation of the maximum curvature using dihedral angles
    between adjacent faces. The curvature is estimated based on how much adjacent faces
    deviate from being coplanar.
    
    Args:
        mesh (trimesh.Trimesh): Input mesh
        
    Returns:
        float: Normalized maximum curvature (0 to 1)
    """
    face_normals = mesh.face_normals
    face_pairs = mesh.face_adjacency
    if len(face_pairs) == 0:
        return 0.0
    
    normals_0 = face_normals[face_pairs[:, 0]]
    normals_1 = face_normals[face_pairs[:, 1]]
    dot_products = np.sum(normals_0 * normals_1, axis=1)
    dot_products = np.clip(dot_products, -1.0, 1.0)
    angles = np.arccos(dot_products)
    angles_deg = np.degrees(angles)
    if len(angles_deg) >= 20:
        p95 = np.percentile(angles_deg, 95)
        p50 = np.percentile(angles_deg, 50)
        if p50 > 0:
            ratio = p95 / p50
        else:
            ratio = p95 / 45.0
    else:
        max_angle = np.max(angles_deg)
        mean_angle = np.mean(angles_deg)
        if mean_angle > 0:
            ratio = max_angle / mean_angle
        else:
            ratio = max_angle / 45.0
    normalized = 2.0 / (1.0 + np.exp(-ratio/45.0)) - 1.0
    return float(np.clip(normalized, 0.0, 1.0))

def compute_flatness(mesh: trimesh.Trimesh) -> float:
    """
    Compute flatness as the ratio of minimum to maximum bounding box dimensions.
    
    Args:
        mesh (trimesh.Trimesh): Input mesh
        
    Returns:
        float: Flatness ratio (0 to 1, where 1 is a cube)
    """
    extents = mesh.bounding_box.extents
    max_length = np.max(extents)
    if max_length == 0:
        return 0.0
    return float(np.min(extents) / max_length)

def compute_sharpness(mesh: trimesh.Trimesh) -> float:
    """
    Compute normalized sharpness using a histogram-based approach that considers
    the distribution of dihedral angles. Sharp features are those with small
    dihedral angles (close to 0).
    
    Args:
        mesh (trimesh.Trimesh): Input mesh
        
    Returns:
        float: Normalized sharpness metric (0 to 1)
    """
    face_normals = mesh.face_normals
    face_pairs = mesh.face_adjacency
    if len(face_pairs) == 0:
        return 0.0
    
    normals_0 = face_normals[face_pairs[:, 0]]
    normals_1 = face_normals[face_pairs[:, 1]]
    dot_products = np.sum(normals_0 * normals_1, axis=1)
    dot_products = np.clip(dot_products, -1.0, 1.0)
    angles = np.arccos(dot_products)
    dihedral_angles = angles
    hist, bins = np.histogram(dihedral_angles, bins=20, range=(0, np.pi/2), density=True)
    bin_centers = (bins[:-1] + bins[1:]) / 2
    weights = 1 - (bin_centers / (np.pi/2))
    sharpness = np.sum(hist * weights) / np.sum(hist)
    
    return float(np.clip(sharpness, 0.0, 1.0))

def compute_min_edge_length(mesh: trimesh.Trimesh, n_samples: int = 1000) -> float:
    """
    Compute minimum edge length needed to capture all STL features.
    This considers:
    1. Local curvature
    2. Distance between non-adjacent faces
    3. Existing edge lengths
    4. Ray casting from surrounding sphere (as fallback)
    
    Args:
        mesh (trimesh.Trimesh): Input mesh
        n_samples (int): Number of sample points for curvature estimation
        
    Returns:
        float: Minimum edge length needed to capture all features
    """
    min_size = float('inf')
    
    edges = mesh.vertices[mesh.edges]
    edge_lengths = np.linalg.norm(edges[:, 0] - edges[:, 1], axis=1)
    min_size = min(min_size, np.percentile(edge_lengths, 1))  # Use 1st percentile to avoid outliers
    
    vertex_normals = mesh.vertex_normals
    for i, vertex in enumerate(mesh.vertices):
        connected = mesh.vertex_neighbors[i]
        if len(connected) > 0:
            # Get average distance to neighbors
            neighbor_verts = mesh.vertices[connected]
            avg_dist = np.mean(np.linalg.norm(neighbor_verts - vertex, axis=1))
            neighbor_normals = vertex_normals[connected]
            angles = np.arccos(np.clip(np.dot(neighbor_normals, vertex_normals[i]), -1, 1))
            max_angle = np.max(angles)
            if max_angle > 0:
                curve_radius = avg_dist / (2 * np.sin(max_angle/2))
                min_size = min(min_size, curve_radius/3)
    
    face_centers = mesh.triangles.mean(axis=1)
    face_normals = mesh.face_normals
    
    tree = scipy.spatial.cKDTree(face_centers)
    
    for i in range(len(mesh.faces)):
        adjacent = set()
        for vertex in mesh.faces[i]:
            adjacent.update(mesh.vertex_faces[vertex])
        distances, indices = tree.query(face_centers[i], k=10)
        for d, idx in zip(distances, indices):
            if idx not in adjacent and idx != i:
                angle = np.arccos(np.clip(np.dot(face_normals[i], face_normals[idx]), -1, 1))
                if angle > np.pi/6:
                    min_size = min(min_size, d/2)
                break
    
    if min_size == float('inf') or min_size <= 0:
        center = mesh.bounding_box.centroid
        radius = np.linalg.norm(mesh.bounding_box.extents) * 0.6
        theta = np.random.uniform(0, 2*np.pi, n_samples)
        phi = np.arccos(np.random.uniform(-1, 1, n_samples))
        x = radius * np.sin(phi) * np.cos(theta)
        y = radius * np.sin(phi) * np.sin(theta)
        z = radius * np.cos(phi)
        ray_origins = np.column_stack((x, y, z)) + center
        
        for origin in ray_origins:
            while True:
                random_point = np.random.uniform(-1, 1, 3)
                if np.linalg.norm(random_point) <= 1:
                    break
            target = center + random_point * radius
            direction = target - origin
            direction = direction / np.linalg.norm(direction)
            locations, _, _ = mesh.ray.intersects_location(
                ray_origins=[origin],
                ray_directions=[direction]
            )
            
            if len(locations) > 1:
                distances = np.linalg.norm(locations - origin, axis=1)
                sorted_indices = np.argsort(distances)
                locations = locations[sorted_indices]
                for i in range(1, len(locations)-1):
                    dist = np.linalg.norm(locations[i] - locations[i-1])
                    min_size = min(min_size, dist)
        
        if min_size == float('inf') or min_size <= 0:
            min_size = np.linalg.norm(mesh.bounding_box.extents) * 0.001
    
    return float(min_size)

def extract_feature_lines(mesh: trimesh.Trimesh, angle_threshold: float = 30.0) -> tuple:
    """
    Extract feature lines from mesh based on dihedral angles.
    
    Args:
        mesh (trimesh.Trimesh): Input mesh
        angle_threshold (float): Angle threshold in degrees for feature detection
        
    Returns:
        tuple: (vertices, lines) where vertices are the points and lines are the indices
    """
    face_normals = mesh.face_normals
    face_pairs = mesh.face_adjacency
    face_pair_edges = mesh.face_adjacency_edges
    
    if len(face_pairs) == 0:
        return np.array([]), np.array([])
    
    normals_0 = face_normals[face_pairs[:, 0]]
    normals_1 = face_normals[face_pairs[:, 1]]
    dot_products = np.sum(normals_0 * normals_1, axis=1)
    dot_products = np.clip(dot_products, -1.0, 1.0)
    angles = np.degrees(np.arccos(dot_products))
    feature_edges = face_pair_edges[angles > angle_threshold]
    unique_vertices = np.unique(feature_edges.reshape(-1))
    vertex_map = {old: new for new, old in enumerate(unique_vertices)}
    vertices = mesh.vertices[unique_vertices]
    lines = np.array([[vertex_map[edge[0]], vertex_map[edge[1]]] 
                     for edge in feature_edges])
    
    return vertices, lines

def write_feature_lines_obj(mesh: trimesh.Trimesh, output_path: str, angle_threshold: float = 30.0):
    """
    Extract feature lines and write them to an OBJ file manually since Open3D's line set 
    writer doesn't directly support OBJ format.
    
    Args:
        mesh (trimesh.Trimesh): Input mesh
        output_path (str): Path to save the OBJ file
        angle_threshold (float): Angle threshold in degrees for feature detection
    """
    vertices, lines = extract_feature_lines(mesh, angle_threshold)
    
    if len(vertices) == 0 or len(lines) == 0:
        raise ValueError(f"No feature lines found for threshold {angle_threshold} degrees")
        
    with open(output_path, 'w') as f:
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for line in lines:
            f.write(f"l {line[0] + 1} {line[1] + 1}\n")

def compute_all_features(stl_path: str, extract_features: bool, surface_k: float, surface_p: float):
    """
    Compute all geometric features for an STL file and optionally extract feature lines.
    First checks if the STL file is valid using surfaceCheck.
    
    Args:
        stl_path (str): Path to the STL file
        extract_features (bool): Whether to extract and save feature lines
        
    Returns:
        dict: Dictionary containing all computed features, or None if the file is invalid
    """
    try:
        start_time = time.time()
        process = subprocess.Popen(['surfaceCheck', stl_path], 
                                 stdout=subprocess.PIPE, 
                                 stderr=subprocess.PIPE,
                                 text=True)
        
        try:
            stdout, _ = process.communicate(timeout=180)
            if any(re.match(r'^\s*\*\*\*', line) for line in stdout.splitlines()):
                bad_path = f"{stl_path}.bad"
                shutil.move(stl_path, bad_path)
                print(f"File {stl_path} marked as bad due to surfaceCheck errors")
                return None
                
        except subprocess.TimeoutExpired:
            process.kill()
            bad_path = f"{stl_path}.bad"
            shutil.move(stl_path, bad_path)
            print(f"File {stl_path} marked as bad due to surfaceCheck timeout")
            return None
            
    except Exception as e:
        print(f"Error running surfaceCheck on {stl_path}: {str(e)}")
        return None

    try:
        mesh = trimesh.load_mesh(stl_path)
        if not isinstance(mesh, trimesh.Trimesh):
            raise ValueError(f"{stl_path} is not an STL model")

        #mesh = refine_surface(mesh, stl_path, surface_k, surface_p)
            
        features = {
            'filename': os.path.basename(stl_path),
            'surface_volume_ratio': compute_surface_volume_ratio(mesh),
            'max_curvature': compute_max_curvature(mesh),
            'flatness': compute_flatness(mesh),
            'sharpness': compute_sharpness(mesh),
            'min_edge_length': compute_min_edge_length(mesh)
        }
        
        if extract_features:
            feature_dir = os.path.join(os.path.dirname(stl_path), 'feature_lines')
            os.makedirs(feature_dir, exist_ok=True)
            base_name = os.path.splitext(os.path.basename(stl_path))[0]
            output_path = os.path.join(feature_dir, f"{base_name}_features.obj")
            write_feature_lines_obj(mesh, output_path)
            
        return features
        
    except Exception as e:
        print(f"Error processing {stl_path} so marking it as bad: {str(e)}")
        bad_path = f"{stl_path}.bad"
        shutil.move(stl_path, bad_path)
        return None

def main():
    parser = argparse.ArgumentParser(description='Compute geometric features for STL files in a folder')
    parser.add_argument('folder', type=str, help='Folder containing STL files')
    parser.add_argument('--extract-features', action='store_true', default=False,
                       help='Extract feature lines and save as OBJ files')
    parser.add_argument('--surface-density', type=float, default=500,
                       help='Base triangle density')
    parser.add_argument('--surface-density-scaling', type=float, default=1.5,
                       help='Base triangle density scaling factor')
    args = parser.parse_args()
    
    folder_path = Path(args.folder)
    if not folder_path.exists() or not folder_path.is_dir():
        print(f"Error: {folder_path} is not a valid directory")
        exit(1)
    
    stl_files = list(folder_path.glob('*.stl')) + list(folder_path.glob('*.STL'))
    if not stl_files:
        print(f"No STL files found in {folder_path}")
        exit(1)
    
    print(f"Found {len(stl_files)} STL files")
    
    all_features = []
    for stl_file in tqdm(stl_files, desc="Processing STL files"):
        try:
            features = compute_all_features(str(stl_file), args.extract_features, args.surface_density, args.surface_density_scaling)
            if features is not None:
                all_features.append(features)
        except Exception as e:
            print(f"\nError processing {stl_file.name}: {str(e)}")
    
    if all_features:
        df = pd.DataFrame(all_features)
        output_file = folder_path / 'geometric_features.csv'
        df.to_csv(output_file, index=False)
        print(f"\nFeatures saved to: {output_file}")
        
        print("\nDataset Description:")
        print("\nShape:", df.shape)
        print("\nColumns:", ", ".join(df.columns))
        print("\nNumerical Features Statistics:")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        print(df[numeric_cols].describe())

if __name__ == "__main__":
    main()
