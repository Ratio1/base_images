#!/bin/bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
image_tag="${IMAGE_TAG:-ratio1/base_edge_node_amd64_gpu:dev}"

docker build \
  -f "${script_dir}/base_edge_node_amd64_gpu/Dockerfile" \
  -t "${image_tag}" \
  "${script_dir}"
