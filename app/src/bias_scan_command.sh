git_root_folder=$(git rev-parse --show-toplevel)
opt_folder="${git_root_folder}/stage1"
ignore=""
if [[ -n "${args[--ignore]}" ]]; then
  ignore="--ignore"
fi
uv run bias-geo-features --threshold "${args[--threshold]}" $ignore "${opt_folder}/${args[--stage1-name]}"
