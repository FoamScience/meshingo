git_root_folder=$(git rev-parse --show-toplevel)
testing_stls="${git_root_folder}/testing_dataset"
if [ "$(readlink -f "${args[target_stl]}")" != "$(readlink -f "$testing_stls/$(basename ${args[target_stl]})")" ]; then
    cp "${args[target_stl]}" "$testing_stls"
fi
echo -e "Computing geometrical features of all STL files found in ${testing_stls}"
uv run compute-geometric-features  "${testing_stls}"
echo -e "\e[32mValidation run \e[0mfor ${args[--model]} surrogate model..."
uv run validate --name ${args[--model]} --target-stl ${args[target_stl]}
