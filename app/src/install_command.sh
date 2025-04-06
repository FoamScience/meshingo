git_root_folder=$(git rev-parse --show-toplevel)
cd "${git_root_folder}" || { echo -e "\e[31m${git_root_folder}\e[0m not found. We rely on git to infer root folder!"; exit 1; }
echo -e "Installing dependencies to \e[32m${git_root_folder}\e[0m"
uv sync
uv pip install -e .
