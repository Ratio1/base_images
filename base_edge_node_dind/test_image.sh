#!/bin/bash
set -euo pipefail

# Build and validate the Docker-in-Docker layer. By default this targets the GPU
# Dockerfile and exercises the embedded Docker daemon plus a nested torch
# container.

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
image_tag="${IMAGE_TAG:-ratio1/base_edge_node_dind:test}"
dockerfile="Dockerfile"
variant="gpu"
nested_torch_image="${NESTED_TORCH_IMAGE:-ratio1/pytorch:cpu-latest}"
nested_use_gpu="${NESTED_USE_GPU:-0}"
skip_nested="${SKIP_NESTED:-0}"

usage() {
  cat <<'USAGE'
Usage: ./test_image.sh [--cpu] [--image <tag>] [--nested-image <image>] [--nested-use-gpu] [--skip-nested]
  --cpu             Use Dockerfile_cpu and CPU torch defaults
  --image           Override the image tag (default: ratio1/base_edge_node_dind:test or cpu-test)
  --nested-image    Override the torch container used for the nested Docker run
  --nested-use-gpu  Use a GPU torch image for the nested container (requires NVIDIA runtime in dind)
  --skip-nested     Skip the nested torch container check
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --cpu)
      variant="cpu"
      dockerfile="Dockerfile_cpu"
      image_tag="${IMAGE_TAG:-ratio1/base_edge_node_dind:cpu-test}"
      shift
      ;;
    --image)
      image_tag="$2"
      shift 2
      ;;
    --nested-image)
      nested_torch_image="$2"
      shift 2
      ;;
    --nested-use-gpu)
      nested_use_gpu=1
      shift
      ;;
    --skip-nested)
      skip_nested=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      usage
      exit 1
      ;;
  esac
done

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is required but not found on the host."
  exit 1
fi

run_flags=(--shm-size 2g)
if [[ "$variant" == "gpu" ]]; then
  run_flags+=(--gpus all)
fi

if [[ "$variant" == "gpu" && "${nested_use_gpu}" -eq 1 && "${NESTED_TORCH_IMAGE:-}" == "" ]]; then
  nested_torch_image="pytorch/pytorch:2.9.1-cuda12.8-cudnn9-runtime"
fi

echo "Building ${image_tag} using ${dockerfile}..."
docker build -f "${script_dir}/${dockerfile}" -t "${image_tag}" "${script_dir}"

container_name="dind-test-$(date +%s)"
volume_name="${container_name}-data"
cleanup() {
  docker rm -f "${container_name}" >/dev/null 2>&1 || true
  docker volume rm -f "${volume_name}" >/dev/null 2>&1 || true
}
trap cleanup EXIT

docker volume create "${volume_name}" >/dev/null

container_flags=(--name "${container_name}" --rm --privileged --tmpfs /run --tmpfs /run/lock -v "${volume_name}:/var/lib/docker" -e EE_DD=true)
container_flags+=("${run_flags[@]}")

echo "Starting dind container and running checks..."
docker run "${container_flags[@]}" "${image_tag}" bash -lc '
set -e
echo "=== Inner dockerd info ==="
docker info --format "Server Version: {{.ServerVersion}}, Storage: {{.Driver}}"
docker version --format "Client: {{.Client.Version}}, API: {{.Client.APIVersion}}"
echo
echo "=== Python stack (inside dind) ==="
python3 - <<'"'"'PY'"'"'
import platform

import torch
import transformers

print(f"platform: {platform.machine()}")
print(f"torch: {torch.__version__}, cuda: {torch.version.cuda}")
print(f"torch cuda available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"device: {torch.cuda.get_device_name(0)}")
print(f"transformers: {transformers.__version__}")
PY
echo
echo "=== Inner docker smoke test ==="
docker run --rm alpine:3.19 echo "inner docker ok"

if [ '"${skip_nested}"' -eq 1 ]; then
  echo "Skipping nested torch container check."
  exit 0
fi

nested_flags=(--rm --ipc=host)
if [ '"${variant}"' = "gpu" ] && [ '"${nested_use_gpu}"' -eq 1 ]; then
  nested_flags+=(--gpus all)
fi

echo "=== Nested torch container (${nested_torch_image}) ==="
docker run "${nested_flags[@]}" '"${nested_torch_image}"' python3 - <<'"'"'PY'"'"'
import torch

print(f"nested torch: {torch.__version__}")
print(f"cuda available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"device: {torch.cuda.get_device_name(0)}")
PY
'
