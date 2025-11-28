#!/bin/bash
set -euo pipefail

# Build and push a CPU-only PyTorch image. The final tag is
# ratio1/pytorch:<torch>-py<python>-<os>, where values are read from the built image.

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
image_base="${IMAGE_BASE:-ratio1/pytorch}"
tmp_tag="${image_base}:cpu-tmp"
alias_tag="${ALIAS_TAG:-cpu-latest}"

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is required but not found."
  exit 1
fi

echo "Building ${tmp_tag} from ${script_dir}/Dockerfile..."
docker build -t "${tmp_tag}" "${script_dir}"

echo "Reading torch/python/OS versions from the built image..."
readarray -t versions < <(docker run --rm -i "${tmp_tag}" python - <<'PY'
import platform
import torch

def os_slug():
    data = {}
    try:
        with open("/etc/os-release") as fh:
            for line in fh:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    data[k] = v.strip('"')
    except FileNotFoundError:
        return "unknown"
    return f"{data.get('ID','unknown')}{data.get('VERSION_ID','')}"

torch_ver = torch.__version__.split("+", 1)[0]
print(torch_ver)
print(platform.python_version())
print(os_slug())
PY
)

torch_version="$(echo "${versions[0]:-}" | tr -d '[:space:]')"
python_version="$(echo "${versions[1]:-}" | tr -d '[:space:]')"
os_version="$(echo "${versions[2]:-}" | tr -d '[:space:]')"

if [[ -z "${torch_version}" || -z "${python_version}" || -z "${os_version}" ]]; then
  echo "Unable to determine versions from ${tmp_tag} (torch='${torch_version}', python='${python_version}', os='${os_version}')"
  exit 1
fi

echo "Found torch=${torch_version}, python=${python_version}, os=${os_version}"

final_tag="${image_base}:${torch_version}-py${python_version}-${os_version}"
echo "Tagging ${tmp_tag} as ${final_tag}"
docker tag "${tmp_tag}" "${final_tag}"

echo "Pushing ${final_tag}"
docker push "${final_tag}"

published="${final_tag}"

if [[ -n "${alias_tag}" ]]; then
  alias_full="${image_base}:${alias_tag}"
  echo "Tagging ${tmp_tag} as ${alias_full}"
  docker tag "${tmp_tag}" "${alias_full}"
  echo "Pushing ${alias_full}"
  docker push "${alias_full}"
  published="${final_tag} and ${alias_full}"
fi

echo "Done. Published ${published}"
