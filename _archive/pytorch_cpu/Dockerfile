ARG PYTHON_VERSION=3.13-slim
FROM python:${PYTHON_VERSION}

ARG TORCH_INDEX_URL="https://download.pytorch.org/whl/cpu"

ENV PIP_NO_CACHE_DIR=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends ca-certificates && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip numpy && \
    python -m pip install --index-url "${TORCH_INDEX_URL}" torch && \
    python - <<'PY'
import torch
print(f"torch {torch.__version__} (cpu) installed")
PY

CMD ["python3", "-c", "import sys; print(f'Python {sys.version}'); import numpy; print(f'Numpy: {numpy.__version__}'); import torch; print(f'Torch: {torch.__version__}')"]
