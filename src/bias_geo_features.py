import pandas as pd
import argparse, os, base64, struct
from predict_cell_size import client_state
from foambo.core import *
from ax.service.ax_client import AxClient
from ax.storage.json_store.load import load_experiment
from ax.plot.feature_importances import plot_feature_importance_by_feature

def generate_feature_importances(problem_name):
    cl = client_state(problem_name)
    exp = cl._experiment
    cl.generation_strategy._fit_current_model(data=exp.lookup_data())
    cur_model = cl.generation_strategy.model
    feature_importance = plot_feature_importance_by_feature(cur_model, relative=True)
    metrics=[ j['label'] for m in feature_importance.data['layout']['updatemenus'] for j in m['buttons'] ]
    dt = [
        {
            "parameter": feature_importance.data['data'][i]['y'][0],
            "metric": metrics[i//len(exp.parameters)],
            "importance": struct.unpack("d", base64.b64decode(feature_importance.data['data'][i]['x']['bdata']))[0]
        } for i in range(len(feature_importance.data['data']))
    ]
    importances = pd.DataFrame(dt)
    importances.to_csv(f"{problem_name}_feature_importance_report.csv")

def check_importance_similarity(df, parameters, objective, threshold):
    """
    Checks if the surrogate model is biased towards any of the geometric features
    
    Args:
        df (Dataframe): Pandas Dataframe containing feature importances
        parameters (List): List of parameters to consider for the check
        objective (str): Objective to check for
        threshold (float): Bar to consider the model to be biased
        
    Returns:
        bool: whether the bias check passes or not
    """
    filtered_df = df[df['metric'] == objective]
    if filtered_df.empty:
        raise ValueError(f"Objective {objective} not found in Dataframe.")
    values = {row['parameter']: row['importance'] for _, row in filtered_df.iterrows() if row['parameter'] in parameters}
    if len(values) < 2:
        raise ValueError("Not enough parameters found for comparison.")
    print(f"Feature importances for {objective}:")
    for param, value in values.items():
        print(f"{param}: {value*100:.2f}%")
    sorted_values = sorted(values.items(), key=lambda x: x[1], reverse=True)
    max_param, max_value = sorted_values[0]
    least_param, least_value = sorted_values[-1]

    max_diff = max(values.values()) - min(values.values())
    if max_diff < threshold:
        print("The model has minimal bias towards all geometric features.")
        return True
    else:
        print(f"The model is significantly biased towards {max_param} ({max_value*100:.2f}%).")
        print(f"The least important parameter is: {least_param} ({least_value*100:.2f}%)")
        return False

    
    
def main():

    parser = argparse.ArgumentParser(description='Check model bias towards geometric features')
    parser.add_argument('name', type=str, help='Problem name used in problem.name for the optimizer configuration')
    parser.add_argument('--threshold', type=float, required=False, default=0.05, help='Tolerance between 0 and 1 for bias consideration')
    
    args = parser.parse_args()

    if not os.path.exists(f"{args.name}_feature_importance_report.csv"):
        print("feature importance database not found, trying to regenerate it...")
        generate_feature_importances(args.name)
    
    df = pd.read_csv(f"{args.name}_feature_importance_report.csv")
    return check_importance_similarity(df=df, parameters=["curvature", "sharpness", "SVR", "flatness"], objective="CellSizeDecayed", threshold=args.threshold)

if __name__ == "__main__":
    main()
