git_root_folder=$(git rev-parse --show-toplevel)
pred_folder="${git_root_folder}/stage2"
testing_stls="${git_root_folder}/testing_dataset"
if [ "$(readlink -f "${args[target_stl]}")" != "$(readlink -f "$testing_stls/$(basename ${args[target_stl]})")" ]; then
    cp "${args[target_stl]}" "$testing_stls"
fi
echo -e "Computing geometrical features of all STL files found in ${testing_stls}"
uv run compute-geometric-features  "${testing_stls}"
cd "${pred_folder}" || { echo -e "\e[31m${pred_folder}\e[0m not found. We rely on git to infer root folder!"; exit 1; }
echo -e "Running \e[32mstage 2 \e[0mfor fine-tuning the generic surrogate model ${args[--stage1-name]} model"
stl_name=$(basename "${args[target_stl]}")
stl_name="${stl_name%.*}"
uv run foamBO --config-name stage_2 \
    ++problem.name="${args[--stage2-name]}" \
    ++meta.n_trials="${args[--n-trials]}" \
    ++meta.n_parallel_trials="${args[--n-parallel-trials]}" \
    ++meta.ttl_trial="${args[--trial-ttl]}" \
    ++meta.case_run_command='["./Allrun.stage2", "'${stl_name}'", "'${args[--stage1-name]}'"]' \
    ++meta.stopping_strategy.improvement_bar="${args[--stopping-improvement]}"
uv run validate --name "${args[--stage2-name]}" --target_stl "${args[target_stl]}"
