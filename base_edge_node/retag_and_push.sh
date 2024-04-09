#!/bin/bash

# Build the image
IMAGE_NAME_BASE="aidamian/base_edge_node"
IMAGE_NAME=$1

# Extract version information
PYTHON_VERSION=$(docker run --rm $IMAGE_NAME python -c "import platform; print(platform.python_version())")
TORCH_VERSION=$(docker run --rm $IMAGE_NAME python -c "import torch; print(torch.__version__)")
TRANSFORMERS_VERSION=$(docker run --rm $IMAGE_NAME python -c "import transformers; print(transformers.__version__)")
MACHINE_VERSION=$(docker run --rm $IMAGE_NAME python -c "import platform; print(platform.machine())")

# Normalize version information for tagging
PYTHON_VERSION_NORMALIZED="py$(echo $PYTHON_VERSION | tr -d '[:space:]' | sed -r 's/\+/\./g')"
TORCH_VERSION_NORMALIZED="th$(echo $TORCH_VERSION | tr -d '[:space:]' | sed -r 's/\+/\./g')"
TRANSFORMERS_VERSION_NORMALIZED="tr$(echo $TRANSFORMERS_VERSION | tr -d '[:space:]' | sed -r 's/\+/\./g')"

# Construct tag
FINAL_IMAGE_TAG="${MACHINE_VERSION}-${PYTHON_VERSION_NORMALIZED}-${TORCH_VERSION_NORMALIZED}-${TRANSFORMERS_VERSION_NORMALIZED}"
FINAL_IMAGE_NAME="$IMAGE_NAME_BASE:$FINAL_IMAGE_TAG"

echo "Retagging $IMAGE_NAME to $FINAL_IMAGE_NAME"
docker tag $IMAGE_NAME $FINAL_IMAGE_NAME

echo "Pushing Docker image $FINAL_IMAGE_NAME"
docker push $FINAL_IMAGE_NAME

