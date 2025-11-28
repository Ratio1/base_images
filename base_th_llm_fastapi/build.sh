#!/bin/bash

# Build the image
docker build -t temp_image .

# Extract version information
PYTHON_VERSION=$(docker run --rm temp_image python -c "import platform; print(platform.python_version())")
TORCH_VERSION=$(docker run --rm temp_image python -c "import torch; print(torch.__version__)")
TRANSFORMERS_VERSION=$(docker run --rm temp_image python -c "import transformers; print(transformers.__version__)")

# Normalize version information for tagging
PYTHON_VERSION_NORMALIZED="py$(echo $PYTHON_VERSION | tr -d '[:space:]')"
TORCH_VERSION_NORMALIZED="th$(echo $TORCH_VERSION | tr -d '[:space:]')"
TRANSFORMERS_VERSION_NORMALIZED="tr$(echo $TRANSFORMERS_VERSION | tr -d '[:space:]')"

# Construct tag
IMAGE_NAME="ratio1/base_th_llm_fastapi"
IMAGE_TAG="${PYTHON_VERSION_NORMALIZED}-${TORCH_VERSION_NORMALIZED}-${TRANSFORMERS_VERSION_NORMALIZED}"
FINAL_IMAGE_NAME="$IMAGE_NAME:$IMAGE_TAG"

echo "Retagging temp_image to $FINAL_IMAGE_NAME"
docker tag temp_image $FINAL_IMAGE_NAME

echo "Pushing Docker image $FINAL_IMAGE_NAME"
docker push $FINAL_IMAGE_NAME

echo "Retagging Docker image to ${IMAGE_NAME}:latest"
docker tag $FINAL_IMAGE_NAME $IMAGE_NAME:latest

echo "Pushing Docker image ${IMAGE_NAME}:latest"
docker push $IMAGE_NAME:latest

