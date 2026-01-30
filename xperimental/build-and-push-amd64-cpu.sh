#!/bin/bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
image_repo="${IMAGE_REPO:-ratio1/base_edge_node_amd64_cpu}"
image_tag="${IMAGE_TAG:-${image_repo}:latest}"

docker build \
  -f "${script_dir}/base_edge_node_amd64_cpu/Dockerfile" \
  -t "${image_tag}" \
  "${script_dir}"

docker push "${image_tag}"

"${script_dir}/base_edge_node_amd64_cpu/retag_and_push.sh" "${image_tag}"
