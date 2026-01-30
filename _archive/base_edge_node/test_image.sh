#!/bin/bash
set -euo pipefail

# Build and validate the base_edge_node image (GPU by default). It also runs a
# public torch container from inside the image via the host Docker socket.

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
image_tag="${IMAGE_TAG:-ratio1/base_edge_node:test}"
dockerfile="Dockerfile"
variant="gpu"
nested_torch_image="${NESTED_TORCH_IMAGE:-pytorch/pytorch:2.9.1-cuda12.8-cudnn9-runtime}"
skip_nested="${SKIP_NESTED:-0}"

usage() {
  cat <<'USAGE'
Usage: ./test_image.sh [--cpu] [--image <tag>] [--nested-image <image>] [--skip-nested]
  --cpu             Build and test the CPU variant (Dockerfile_cpu)
  --image           Override the image tag (default: ratio1/base_edge_node:test or cpu-test)
  --nested-image    Override the torch container used for the nested Docker run
  --skip-nested     Skip the nested torch container check (not recommended)
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --cpu)
      variant="cpu"
      dockerfile="Dockerfile_cpu"
      image_tag="${IMAGE_TAG:-ratio1/base_edge_node:cpu-test}"
      nested_torch_image="${NESTED_TORCH_IMAGE:-ratio1/pytorch:cpu-latest}"
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

require_docker() {
  if ! command -v docker >/dev/null 2>&1; then
    echo "docker is required but not found on the host."
    exit 1
  fi
}

require_docker

run_flags=(--shm-size 2g)
if [[ "$variant" == "gpu" ]]; then
  run_flags+=(--gpus all)
fi

echo "Building ${image_tag} using ${dockerfile}..."
docker build -f "${script_dir}/${dockerfile}" -t "${image_tag}" "${script_dir}"

echo "Running on-image checks..."
docker run --rm "${run_flags[@]}" "${image_tag}" bash -lc '
set -e
echo "=== Binary versions ==="
python3 --version
pip3 --version
ffmpeg -version | head -n 1
node -v
ngrok version
echo
echo "=== Python package sanity ==="
python3 - <<'"'"'PY'"'"'
import importlib
import platform

import torch
import transformers

print(f"platform: {platform.machine()}")
print(f"torch: {torch.__version__}, cuda: {torch.version.cuda}")
print(f"torch cuda available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"cuda device: {torch.cuda.get_device_name(0)}")

print(f"transformers: {transformers.__version__}")

for name in ("onnx", "onnxruntime", "openvino"):
    try:
        mod = importlib.import_module(name)
        ver = getattr(mod, "__version__", "unknown")
        print(f"{name}: {ver}")
    except Exception as exc:
        print(f"{name}: MISSING ({exc})")

try:
    import tensorrt
    print(f"tensorrt: {tensorrt.__version__}")
except Exception as exc:
    print(f"tensorrt: not available ({exc})")
PY
echo
echo "=== ffmpeg codecs (top 5) ==="
ffmpeg -codecs | head -n 5
'

if [[ "${skip_nested}" -eq 1 ]]; then
  echo "Skipping nested torch container check."
  exit 0
fi

if [[ ! -S /var/run/docker.sock ]]; then
  echo "Docker socket /var/run/docker.sock is missing; cannot run nested container."
  exit 1
fi

nested_flags=(--rm)
if [[ "$variant" == "gpu" ]]; then
  nested_flags+=(--gpus all --ipc=host)
fi

echo "Running nested torch container (${nested_torch_image}) from inside ${image_tag}..."
docker run --rm "${run_flags[@]}" \
  -e DOCKER_HOST=unix:///var/run/docker.sock \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v "$(command -v docker)":/usr/bin/docker:ro \
  "${image_tag}" bash -lc '
set -e
docker run '"${nested_flags[*]}"' '"${nested_torch_image}"' python3 - <<'"'"'PY'"'"'
import torch

print(f"nested torch: {torch.__version__}")
print(f"cuda available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"device: {torch.cuda.get_device_name(0)}")
PY
'
