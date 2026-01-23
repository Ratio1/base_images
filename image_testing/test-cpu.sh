#!/bin/bash
set -euo pipefail

IMAGE="${1:-ratio1/base_edge_node_amd64_cpu:dev}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

docker run --rm -e EE_DD=1 --privileged \
  -v "${SCRIPT_DIR}/image_tests:/image_tests:ro" \
  "${IMAGE}" \
  python3 /image_tests/cpu_image_test.py
