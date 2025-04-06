git_root_folder=$(git rev-parse --show-toplevel)
opt_folder="${git_root_folder}/stage1"
train_folder=$(realpath "${args[training_stls]}")
cd "${train_folder}" || { echo -e "\e[31m${train_folder}\e[0m not found."; exit 1; }
echo -e "Computing geometrical features of all STL files found in ${train_folder}"
uv run compute-geometric-features  "${train_folder}"
cd "${opt_folder}" || { echo -e "\e[31m${opt_folder}\e[0m not found. We rely on git to infer root folder!"; exit 1; }
echo -e "Running \e[32mstage 1 \e[0mfor training the generic surrogate model ${args[--stage1-name]}..."
uv run foamBO --config-name stage_1 \
    ++problem.name="${args[--stage1-name]}" \
    ++meta.n_trials="${args[--n-trials]}" \
    ++meta.n_parallel_trials="${args[--n-parallel-trials]}" \
    ++meta.ttl_trial="${args[--trial-ttl]}" \
    ++meta.stopping_strategy.improvement_bar="${args[--stopping-improvement]}" \
