import pandas as pd
import numpy as np
import argparse
from pathlib import Path
from typing import List, Tuple
from foambo.core import *
from ax.service.ax_client import AxClient
from ax.storage.json_store.load import load_experiment
from ax.core.observation import ObservationFeatures
import json
from compute_objectives import get_feature_cell_size
#from geo_features import compute_all_features

def client_state(problem_name):
    cl = AxClient(verbose_logging=False).load_from_json_file(f'{problem_name}_client_state.json')
    exp = load_experiment(f"{problem_name}_experiment.json")
    cl._experiment = exp
    return cl

def pick_best_pareto_point(problem_name):
    df = pd.read_csv(f"{problem_name}_frontier_report.csv")
    _, _, decay_inverse = get_feature_cell_size()
    uncertainty = abs(decay_inverse(df["CellSizeDecayed"] + df["CellSizeDecayed_sems"]) - decay_inverse(df["CellSizeDecayed"]))
    return df.loc[uncertainty.idxmin()].to_dict()

def predict(problem_name, coeffs_path):
    cl = client_state(problem_name)
    print(f"Picking a pareto front point: ")
    print(json.dumps(pick_best_pareto_point(problem_name), indent=4))
    with open(coeffs_path, "r") as file:
        pred_data = pick_best_pareto_point(problem_name) | json.load(file)
    print(f"Predicting Objectives for the following point with {len(pred_data.keys())} parameters:")
    print(json.dumps(pred_data, indent=4))
    print(f"Predicted Objective: mean +- 95%_interval , (95%_relative_interval)")
    Y = cl.get_model_predictions_for_parameterizations([pred_data])
    for yi in Y:
        cell_count = (yi["CellCount"][0] , yi["CellCount"][1])
        _, _, decay_inverse = get_feature_cell_size()
        uncertainty_on_original_cell_size = abs(decay_inverse(yi["CellSizeDecayed"][0] + yi["CellSizeDecayed"][1]) - decay_inverse(yi["CellSizeDecayed"][0]))
        original_cell_size = (decay_inverse(yi["CellSizeDecayed"][0]), uncertainty_on_original_cell_size)
        surface_diff = yi["SurfaceDifference"]
        issues = (yi["MeshIssues"][0], yi["MeshIssues"][1]) 
        rel_issues = 1.96*issues[1]/issues[0] if issues[0] != 0 else 1.96*issues[1]
        print(
            f"Cell Size: {original_cell_size[0]:.6g} +/- {1.96*original_cell_size[1]:.6g}, ({1.96*original_cell_size[1]/original_cell_size[0]:.6g})\n"
            f"Cell Count: {cell_count[0]:.6g} +/- {1.96*cell_count[1]:.6g}, ({1.96*cell_count[1]/cell_count[0]:.6g})\n"
            f"Surface to mesh difference: {surface_diff[0]:.6g} +/- {1.96*surface_diff[1]:.6g}, ({1.96*surface_diff[1]/surface_diff[0]:.6g})\n"
            f"Mesh issues: {issues[0]:.6g} +/- {1.96*issues[1]:.6g}, ({rel_issues:.6g})"
        )


def main():
    parser = argparse.ArgumentParser(description='Predict best cell size and cell count for an STL file using a trained model.')
    parser.add_argument('--name', required=True, type=str, help='Problem name used in problem.name for the optimizer configuration')
    parser.add_argument('--coeffs', required=True, type=str, help='JSON filehaving *Coeff parameter values')
    
    args = parser.parse_args()
    coeffs_path = Path(args.coeffs)
    if not coeffs_path.exists():
        raise ValueError(f"{coeffs_path} does not exist")
    predict(args.name, coeffs_path)

if __name__ == "__main__":
    main()
