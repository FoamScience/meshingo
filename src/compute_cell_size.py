import numpy as np
import pandas as pd
import argparse

def compute_cell_size(features: dict, alpha: float, beta: float, gamma: float, delta: float, epsilon: float) -> float:
    """
    Compute cell size using the formula:
    h = min_edge_length x min(1+1/(1+max(curvature)), 1+e^(-β⋅sharpness), 1+e^(-γ⋅SVR), 1+flatness^0.5)
    
    All terms except min_edge_length are guaranteed to be greater than 1.
    
    Args:
        features (dict): Dictionary containing geometric features
        alpha (float): Min edge length coefficient
        beta (float): Curvature coefficient
        gamma (float): Sharpness coefficient
        delta (float): Surface-to-volume ratio coefficient
        epsilon (float): Flatness coefficient
        
    Returns:
        float: Computed cell size
    """
    min_edge_term = alpha*features['min_edge_length']
    curvature_term = 1.0 + beta / (1 + features['max_curvature'])
    sharpness_term = 1.0 + np.exp(-gamma * features['sharpness'])
    svr_term = 1.0 + np.exp(-delta * features['surface_volume_ratio'])
    flatness_term = 1.0 + np.sqrt(epsilon*features['flatness'])
    min_value = min_edge_term * min(curvature_term, sharpness_term, svr_term, flatness_term)
    return min_value
def main():

    parser = argparse.ArgumentParser(description='Compute mesh cell size based on geometric features')
    parser.add_argument('stl_name', type=str, help='Filename for STL to use')
    parser.add_argument('features_database', type=str, help='Path to the CSV file holding geometric features data')
    parser.add_argument('--alpha', type=float, default=0.5, help='Min edge length coefficient')
    parser.add_argument('--beta', type=float, default=1.0, help='Curvature coefficient')
    parser.add_argument('--gamma', type=float, default=0.1, help='Sharpness coefficient')
    parser.add_argument('--delta', type=float, default=0.5, help='Surface-to-volume ratio coefficient')
    parser.add_argument('--epsilon', type=float, default=0.5, help='Flatness coefficient')
    
    args = parser.parse_args()
    
    df = pd.read_csv(args.features_database)
    filter = df[df["filename"] == args.stl_name]
    if not filter.empty:
        features = filter.iloc[0].to_dict()
        cell_size = compute_cell_size(features, args.alpha, args.beta, args.gamma, args.delta, args.epsilon)
        print(f"{cell_size}")
    else:
        raise ValueError(f"{args.stl_name} data not found in {args.features_database}")

if __name__ == "__main__":
    main()
