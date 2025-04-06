import pandas as pd
import numpy as np
import argparse
from pathlib import Path
from typing import List, Tuple

def normalize_features(df: pd.DataFrame, feature_cols: List[str]) -> pd.DataFrame:
    """
    Normalize features using min-max scaling.
    
    Args:
        df (pd.DataFrame): Input dataframe
        feature_cols (List[str]): List of feature column names
        
    Returns:
        pd.DataFrame: DataFrame with normalized features
    """
    result = df.copy()
    for feature in feature_cols:
        min_val = df[feature].min()
        max_val = df[feature].max()
        if max_val > min_val:
            result[feature] = (df[feature] - min_val) / (max_val - min_val)
        else:
            result[feature] = 0  # Handle constant features
    return result

def find_most_similar(df: pd.DataFrame, query_features: dict, 
                     feature_cols: List[str], n: int = 1) -> List[Tuple[str, float]]:
    """
    Find the n most similar surfaces based on Euclidean distance.
    
    Args:
        df (pd.DataFrame): DataFrame containing geometric features
        query_features (dict): Dictionary of query feature values
        feature_cols (List[str]): List of feature column names to consider
        n (int): Number of similar surfaces to return
        
    Returns:
        List[Tuple[str, float]]: List of (filename, distance) tuples
    """
    query_df = pd.DataFrame([query_features])
    combined_df = pd.concat([df[feature_cols], query_df[feature_cols]], ignore_index=True)
    normalized_df = normalize_features(combined_df, feature_cols)
    norm_database = normalized_df.iloc[:-1]
    norm_query = normalized_df.iloc[-1]
    distances = np.sqrt(((norm_database - norm_query) ** 2).sum(axis=1))
    closest_indices = distances.nsmallest(n).index
    return [(df.iloc[idx]['filename'], distances[idx]) for idx in closest_indices]

def main():
    parser = argparse.ArgumentParser(description='Find similar surfaces based on geometric features')
    parser.add_argument('csv_path', type=str, help='Path to the geometric features CSV file')
    parser.add_argument('--svr', type=float, help='Surface-to-Volume Ratio')
    parser.add_argument('--curvature', type=float, help='Maximum Curvature')
    parser.add_argument('--flatness', type=float, help='Flatness Ratio')
    parser.add_argument('--sharpness', type=float, help='Maximum Sharpness (Dihedral Angle)')
    parser.add_argument('--parts', type=int, help='Number of Parts')
    parser.add_argument('-n', type=int, default=1, help='Number of similar surfaces to return')
    
    args = parser.parse_args()
    csv_path = Path(args.csv_path)
    if not csv_path.exists():
        raise ValueError(f"{csv_path} does not exist")
    
    df = pd.read_csv(csv_path)
    feature_mapping = {
        'surface_volume_ratio': args.svr,
        'max_curvature': args.curvature,
        'flatness': args.flatness,
        'sharpness': args.sharpness,
        'num_parts': args.parts
    }
    
    query_features = {k: v for k, v in feature_mapping.items() if v is not None}
    if not query_features:
        raise ValueError(f"At least one feature must be provided")
    
    feature_cols = list(query_features.keys())
    similar_surfaces = find_most_similar(df, query_features, feature_cols, args.n)
    best_similarity = 1 / (1 + similar_surfaces[0][1])
    if best_similarity <= 0.3:
        raise ValueError(f"No sufficiently similar surfaces found. Best similarity score was {best_similarity:.3f}")
    
    for filename, distance in similar_surfaces:
        similarity = 1 / (1 + distance)
        print(f"{filename}, {similarity}")

if __name__ == "__main__":
    main()
