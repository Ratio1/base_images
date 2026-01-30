#!/bin/bash

# Build the image
IMAGE_NAME_BASE="ratio1/base_edge_node"
IMAGE_NAME=$1

# Extract version information
PYTHON_VERSION=$(docker run --rm $IMAGE_NAME python3 -c "import platform; print(platform.python_version())")
TORCH_VERSION=$(docker run --rm $IMAGE_NAME python3 -c "import torch; print(torch.__version__.split('+')[0])")
ONNX_VERSION=$(docker run --rm $IMAGE_NAME python3 -c "import onnx; print(onnx.__version__)")
TRANSFORMERS_VERSION=$(docker run --rm $IMAGE_NAME python3 -c "import transformers; print(transformers.__version__)")

# Normalize version information for tagging
normalize_version() {
  echo "$1" | tr -d '[:space:]' | sed -r 's/\+/\./g'
}

PYTHON_VERSION_NORMALIZED="py$(normalize_version "$PYTHON_VERSION")"
TORCH_VERSION_NORMALIZED="th$(normalize_version "$TORCH_VERSION")"
ONNX_VERSION_NORMALIZED="ox$(normalize_version "$ONNX_VERSION")"
TRANSFORMERS_VERSION_NORMALIZED="tr$(normalize_version "$TRANSFORMERS_VERSION")"

# Construct tag
FINAL_IMAGE_TAG="${PYTHON_VERSION_NORMALIZED}-${TORCH_VERSION_NORMALIZED}-${ONNX_VERSION_NORMALIZED}-${TRANSFORMERS_VERSION_NORMALIZED}"
FINAL_IMAGE_NAME="$IMAGE_NAME_BASE:$FINAL_IMAGE_TAG"

echo "Retagging $IMAGE_NAME to $FINAL_IMAGE_NAME"
docker tag $IMAGE_NAME $FINAL_IMAGE_NAME

echo "Pushing Docker image $FINAL_IMAGE_NAME"
docker push $FINAL_IMAGE_NAME
