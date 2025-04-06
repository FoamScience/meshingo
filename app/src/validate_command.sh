git_root_folder=$(git rev-parse --show-toplevel)
echo -e "\e[32mValidation run \e[0mfor ${args[--model]} surrogate model..."
uv run validate --name ${args[--model]} --target-stl ${args[target_stl]}
