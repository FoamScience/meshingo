import pandas as pd
import numpy as np
import argparse, os, shutil
from pathlib import Path
from foambo.core import *
from ax.core.arm import Arm
from ax.core.generator_run import GeneratorRun
from ax.core.trial import Trial
from ax.service.scheduler import Scheduler, SchedulerOptions
from sklearn.preprocessing import MinMaxScaler
from ax.global_stopping.strategies.improvement import ImprovementGlobalStoppingStrategy
import json
from predict_cell_size import client_state

def get_best_parameters_per_objectives(problem_name):
    print(f"Loading model {problem_name}")
    cl = client_state(problem_name)
    df = pd.read_csv(f"{problem_name}_frontier_report.csv")
    cols = [obj.metric.name for obj in cl._experiment._optimization_config._objective.objectives]
    sems = [col + '_sems' for col in cols]
    scaler = MinMaxScaler()
    normalized = pd.DataFrame(scaler.fit_transform(df[cols + sems]), columns=cols + sems)
    scores = pd.DataFrame()
    for col, sem_col in zip(cols, sems):
        scores[col] = normalized[col] + normalized[sem_col]
    best_indices = scores.idxmin()
    parameter_sets = []
    for idx in np.unique(best_indices.values):
        parameter_sets.append((df.loc[idx], best_indices[best_indices == idx].index.tolist()))
    return parameter_sets

def run_trials_with_target_stl(problem_name, target_stl):
    params = get_best_parameters_per_objectives(problem_name)
    cl = client_state(problem_name)
    print(f"Client state and experiment for {problem_name} reloaded")
    objectives = [obj.metric.name for obj in cl._experiment._optimization_config._objective.objectives]
    exp = cl._experiment
    cfg = exp.runner.cfg
    print(f"Fitting generation strategy to old experiment data ({int(exp.lookup_data().df.shape[0]/exp.lookup_data().df.shape[1])} entries)")
    cl.generation_strategy._fit_current_model(data=exp.lookup_data())
    scheduler = Scheduler(
        experiment=exp,
        generation_strategy=cl.generation_strategy,
        options=SchedulerOptions(
            log_filepath="validator",
            ttl_seconds_for_trials=cfg.meta.trial_ttl
                if "trial_ttl" in cfg.meta.keys() else None,
            init_seconds_between_polls=cfg.meta.init_poll_wait
                if "init_poll_wait" in cfg.meta.keys() else 1,
            seconds_between_polls_backoff_factor=cfg.meta.poll_factor
                if "poll_factor" in cfg.meta.keys() else 1.5,
            timeout_hours=cfg.meta.timeout_hours
                if "timeout_hours" in cfg.meta.keys() else None,
            global_stopping_strategy=ImprovementGlobalStoppingStrategy(
                min_trials=int(cfg.meta.stopping_strategy.min_trials),
                window_size=cfg.meta.stopping_strategy.window_size,
                improvement_bar=cfg.meta.stopping_strategy.improvement_bar,
            ),
        ),
    )
    print("Scheduler recreated")
    full_parameters = [p for p in exp.search_space.parameters]
    trials = []
    # TODO: recompute testing_dataset/geometric_features.csv
    # TODO: get data from target STL and inject it into the trials
    target = pd.read_csv(f"{os.path.dirname(target_stl)}/geometric_features.csv")
    target_bn = os.path.basename(target_stl)
    target_col = target[target['filename'] == target_bn].index.to_list()
    feature_map = {
        "surface_volume_ratio": "SVR",
        "max_curvature": "curvature",
        "flatness": "flatness",
        "sharpness": "sharpness",
    }
    if len(target_col) != 1:
        raise ValueError(f"Expected to exactly one {target_col} file")
    target_col = target_col[0]
    for param in params:
        pr = param[0]
        for k,v in feature_map.items():
            pr[v] = target.loc[target_col][k]
        objs = param[1]
        trial = Trial(
            experiment=exp,
            generator_run=GeneratorRun(
                arms=[Arm(parameters=pr[full_parameters])],
                optimization_config=exp.optimization_config,
                search_space=exp.optimization_config,
            )
        )
        trials.append((trial, objs, param[0][objectives]))
    # merging test db with training set, and retracting it later
    # so Allrun can find the target STL
    print(f"Temporarily adding {target_bn} to training_dataset...")
    training = pd.read_csv(f"training_dataset/geometric_features.csv")
    merged = pd.concat([training, target], ignore_index=True)
    merged.to_csv(f"training_dataset/geometric_features.csv")
    print(f"{target_bn} added to training_dataset/geometric_features.csv")
    shutil.copy(target_stl, f"training_dataset/{target_bn}")
    stem = str(target_bn.replace(".stl",""))
    shutil.copy( f"{os.path.dirname(target_stl)}/feature_lines/{stem}_features.obj",
                f"training_dataset/{str(target_bn).replace('.stl','.obj')}")
    print(f"{target_stl} and its feature edges copied to training_dataset/")
    # run cases
    cwd = os.getcwd()
    os.chdir(os.path.dirname(target_stl))
    runs = {}
    print(f"Running {len(trials)} validation trials")
    try:
        runs = scheduler.run_trials([t[0] for t in trials])
        for k, o in zip(runs.keys(), [t[1] for t in trials]):
            runs[k]["best_for_objectives"] = o
        for k, o in zip(runs.keys(), [t[2] for t in trials]):
            runs[k]["predictions"] = o.to_dict()
    except:
        os.chdir(cwd)
        os.remove(f"training_dataset/{target_bn}")
        os.remove(f"training_dataset/{str(target_bn).replace('.stl','.obj')}")
        training.to_csv(f"training_dataset/geometric_features.csv")
        raise RuntimeError("Running validation trials failed...")
    os.chdir(cwd)
    os.remove(f"training_dataset/{target_bn}")
    os.remove(f"training_dataset/{str(target_bn).replace('.stl','.obj')}")
    training.to_csv(f"training_dataset/geometric_features.csv")
    print(f" == == !!! Make sure the running trials say that {target_bn} was picked in their logs...")
    print("Training dataset cleaned up of validation entries")
    return runs
    

def main():
    parser = argparse.ArgumentParser(description='Validate model by running on a test STL and comparing with predictions')
    parser.add_argument('--name', required=True, type=str, help='Problem name used in problem.name for the optimizer configuration')
    parser.add_argument('--target-stl', required=True, type=str, help='Path to validation STL')
    
    args = parser.parse_args()
    target_stl = Path(args.target_stl)
    if not target_stl.exists():
        raise ValueError(f"{target_stl} does not exist")
    runs = run_trials_with_target_stl(args.name, target_stl)
    print(json.dumps(runs, indent=4))

if __name__ == "__main__":
    main()
