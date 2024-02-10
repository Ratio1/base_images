#!/bin/bash

# Default Python version
PYTHON_VERSION=${1:-3.10.13}-slim

IMAGE_NAME="aidamian/base_fastapi"

# Replace dots with underscores and remove minor version if it's zero, for tagging purposes
IMAGE_TAG="py${PYTHON_VERSION}"
FULL_IMAGE_NAME="$IMAGE_NAME:$IMAGE_TAG"

# Build the Docker image with a dynamic tag based on the Python version
echo "Building Docker image with Python version $PYTHON_VERSION"
docker build --build-arg PYTHON_VERSION=${PYTHON_VERSION} -t $FULL_IMAGE_NAME .

# # Push the Docker image with the dynamic tag
echo "Pushing Docker image $FULL_IMAGE_NAME"
docker push $FULL_IMAGE_NAME

echo "Retagging Docker image as latest"
docker tag $FULL_IMAGE_NAME $IMAGE_NAME:latest

echo "Pushing Docker image $IMAGE_NAME:latest"
docker push $IMAGE_NAME:latest


