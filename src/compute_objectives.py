import pyvista as pv
import os
import subprocess
import re
import argparse
import numpy as np

def get_feature_cell_size(size_scale: float = 0.1, decay_strength: float = 1.5):
    """Get minEdgeLength from featuresDict.
    
    Returns:
        float: Decay for the feature detection cell size
    """

    decay = lambda x : size_scale*np.log(1+decay_strength/x) 
    decay_inverse = lambda x : decay_strength/(np.exp(x/size_scale)-1)

    if not os.path.exists('featuresDict'):
        return np.nan, decay, decay_inverse
        
    with open('featuresDict', 'r') as f:
        content = f.read()
    
    match = re.search(r'minEdgeLength\s+([^\s;]+);', content)
    if not match:
        raise ValueError("minEdgeLength not found in featuresDict")

    
    return decay(float(match.group(1))), decay, decay_inverse 

def get_mesh_surface_difference():
    """Compute normalized maximum distance between OpenFOAM mesh surface points and reference STL surface.
    
    The difference is computed by:
    1. Extracting surface mesh from OpenFOAM case using PyVista
    2. Computing distances from each surface mesh point to the nearest point on STL surface
    3. Normalizing by the STL's characteristic length (diagonal of bounding box)
    4. Taking the maximum normalized distance as the final score
    
    Returns:
        float: Maximum normalized distance between mesh surface points and STL surface
    """
    stl_path = 'constant/triSurface/surface.stl'
    if not os.path.exists(stl_path):
        raise ValueError(f"STL file not found: {stl_path}")
    stl_surface = pv.read(stl_path)
    
    bounds = np.array(stl_surface.bounds).reshape(3, 2)
    stl_diagonal = np.sqrt(np.sum((bounds[:, 1] - bounds[:, 0])**2))
    
    if not os.path.exists('case.foam'):
        open('case.foam', 'w').close()
    foam_mesh = pv.OpenFOAMReader('case.foam')
    foam_grid = foam_mesh.read()
    if len(foam_grid) == 0:
        raise ValueError("No mesh was found")
        
    main_grid = foam_grid[0]
    foam_surface = main_grid.extract_surface()
    cloud = pv.PolyData(foam_surface.points)
    distance_mesh = cloud.compute_implicit_distance(stl_surface)
    distances = distance_mesh.point_data['implicit_distance']
    
    normalized_distances = np.abs(distances) / stl_diagonal
    max_normalized_distance = float(np.max(normalized_distances))
    
    return max_normalized_distance

def get_mesh_issues():
    """Run checkMesh and analyze its output for mesh issues.
    
    Returns:
        int: Weighted count of mesh issues (*** issues count 5x more than **)
    """
    try:
        result = subprocess.run(['checkMesh'], capture_output=True, text=True)
        output = result.stdout + result.stderr
        two_star_count = len(re.findall(r'(?<!\*)\*{2}(?!\*)[^\s]', output))
        three_star_count = len(re.findall(r'(?<!\*)\*{3}(?!\*)[^\s]', output))
        return two_star_count + (three_star_count * 5)
    except subprocess.CalledProcessError as e:
        raise(ValueError(f"Error running checkMesh: {e}"))

def get_total_cell_count():
    """Read OpenFOAM case and return cell count normalized by STL surface area.
    
    Returns:
        float: Cell density (cells per unit surface area of STL)
    """
    stl_path = 'constant/triSurface/surface.stl'
    if not os.path.exists(stl_path):
        raise ValueError(f"STL file not found: {stl_path}")
    stl_surface = pv.read(stl_path)
    surface_area = stl_surface.area
    
    if not os.path.exists('case.foam'):
        open('case.foam', 'w').close()
    foam_mesh = pv.OpenFOAMReader('case.foam')
    foam_grid = foam_mesh.read()
    if len(foam_grid) == 0:
        raise ValueError(f"No mesh was found")
    
    mesh = foam_grid.GetBlock(0)
    if hasattr(mesh, 'n_cells'):
        total_cells = mesh.n_cells
    else:
        total_cells = 0
        for i in range(len(mesh)):
            block = mesh.GetBlock(i)
            if hasattr(block, 'n_cells'):
                total_cells += block.n_cells
    
    return (float(total_cells) / surface_area) / 1000 if surface_area > 0 else float('inf')

def main():
    parser = argparse.ArgumentParser(description='Compute mesh objectives')
    parser.add_argument('--cell-count', action='store_true', help='Count mesh cells')
    parser.add_argument('--issues', action='store_true', help='Run checkMesh and count mesh issues')
    parser.add_argument('--difference', action='store_true', help='Compute difference from reference STL')
    parser.add_argument('--cell-size', action='store_true', help='Get feature detection cell size from featuresDict')
    args = parser.parse_args()
    
    if args.issues:
        print(f"{get_mesh_issues()}")
    if args.cell_count:
        print(f"{get_total_cell_count()}")
    if args.difference:
        print(f"{get_mesh_surface_difference()}")
    if args.cell_size:
        decayed_size, _,_ = get_feature_cell_size()
        print(f"{decayed_size}")

if __name__ == '__main__':
    main()
