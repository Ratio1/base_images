#!/bin/bash
set -euo pipefail

IMAGE="${1:-ratio1/base_edge_node_amd64_cpu:dev}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

docker run --rm -e EE_DD=1 -e DOCKER_DRIVER=fuse-overlayfs --privileged \
  -v "${SCRIPT_DIR}:/image_testing:ro" \
  "${IMAGE}" \
  python3 /image_testing/cpu_image_test.py
