#!/bin/bash
set -euo pipefail

# Build and validate the Jetson/Tegra edge node image. Assumes the host uses
# the NVIDIA Container Runtime (JetPack) and exposes /var/run/docker.sock.

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
image_tag="${IMAGE_TAG:-ratio1/base_edge_node_arm64_tegra:test}"
nested_torch_image="${NESTED_TORCH_IMAGE:-dustynv/l4t-pytorch:r36.2.0}"
runtime_flag="${NVIDIA_RUNTIME_FLAG:---runtime nvidia}"
skip_nested="${SKIP_NESTED:-0}"

usage() {
  cat <<'USAGE'
Usage: ./test_image.sh [--image <tag>] [--nested-image <image>] [--runtime-flag "<flag>"] [--skip-nested]
  --image           Override the image tag (default: ratio1/base_edge_node_arm64_tegra:test)
  --nested-image    Override the torch container used for the nested Docker run
  --runtime-flag    Runtime flag passed to docker run for GPU access (default: --runtime nvidia)
  --skip-nested     Skip the nested torch container check
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --image)
      image_tag="$2"
      shift 2
      ;;
    --nested-image)
      nested_torch_image="$2"
      shift 2
      ;;
    --runtime-flag)
      runtime_flag="$2"
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

if ! command -v docker >/dev/null 2>&1; then
  echo "docker is required but not found on the host."
  exit 1
fi

run_flags=(--shm-size 2g ${runtime_flag})

echo "Building ${image_tag}..."
docker build -t "${image_tag}" "${script_dir}"

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
import platform

import torch
import transformers

print(f"platform: {platform.machine()}")
print(f"torch: {torch.__version__}, cuda: {torch.version.cuda}")
print(f"torch cuda available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"device: {torch.cuda.get_device_name(0)}")
    try:
        print(f"capability: {torch.cuda.get_device_capability(0)}")
    except Exception as exc:
        print(f"capability lookup failed: {exc}")
print(f"transformers: {transformers.__version__}")
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

nested_flags=(--rm ${runtime_flag})

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
