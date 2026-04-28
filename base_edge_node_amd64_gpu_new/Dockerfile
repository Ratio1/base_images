FROM ubuntu:24.04 AS python-builder

ARG PYTHON_VERSION=3.13.11

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    curl \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libffi-dev \
    liblzma-dev \
    libgdbm-dev \
    libncursesw5-dev \
    uuid-dev \
    tk-dev \
    xz-utils \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /tmp/python-build

RUN set -eux; \
  curl -fsSLO "https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz"; \
  tar -xzf "Python-${PYTHON_VERSION}.tgz"; \
  cd "Python-${PYTHON_VERSION}"; \
  ./configure --prefix=/opt/python --enable-optimizations --with-lto --enable-shared; \
  make -j"$(nproc)"; \
  make install; \
  cd /tmp/python-build; \
  rm -rf "Python-${PYTHON_VERSION}" "Python-${PYTHON_VERSION}.tgz"; \
  LD_LIBRARY_PATH="/opt/python/lib" /opt/python/bin/python3 -m ensurepip; \
  LD_LIBRARY_PATH="/opt/python/lib" /opt/python/bin/python3 -m pip install --no-cache-dir --upgrade pip setuptools wheel

FROM ubuntu:24.04 AS ffmpeg-builder

ARG FFMPEG_VERSION=6.1.1

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    ca-certificates \
    git \
    curl \
    pkg-config \
    yasm \
    nasm \
    cmake \
    ninja-build \
    meson \
    libva-dev \
    vainfo \
    libgnutls28-dev \
    libaom-dev \
    libmp3lame-dev \
    libopus-dev \
    libvpx-dev \
    libx264-dev \
    libx265-dev \
    libxml2-dev \
    libass-dev \
    libfreetype6-dev \
    libfontconfig1-dev \
  && rm -rf /var/lib/apt/lists/*

COPY scripts/build-ffmpeg.sh /tmp/build-ffmpeg.sh

RUN chmod +x /tmp/build-ffmpeg.sh && \
  FFMPEG_VERSION="${FFMPEG_VERSION}" /tmp/build-ffmpeg.sh

FROM ubuntu:24.04

ARG PYTHON_VERSION=3.13.11
ARG TORCH_CHANNEL=https://download.pytorch.org/whl/cu128
ARG CUDA_DEVEL_VERSION=12-8
ARG FLASH_ATTN_MAX_JOBS=1
ARG ENABLE_BITSANDBYTES=true
ARG ENABLE_FLASH_ATTN=true

ENV CUDA_ROOT="/usr/local/cuda-12.8" \
    DEBIAN_FRONTEND=noninteractive \
    TZ=Etc/UTC \
    DOCKER_TLS_CERTDIR=/certs \
    EE_DD=false \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

COPY --from=python-builder /opt/python /opt/python
COPY --from=ffmpeg-builder /usr/local /usr/local
COPY base_edge_node_amd64_gpu_new/requirements.txt /tmp/requirements.txt
COPY scripts/entrypoint.sh /usr/local/bin/entrypoint.sh

RUN set -eux; \
  chmod +x /usr/local/bin/entrypoint.sh; \
  apt-get update; \
  apt-get install -y --no-install-recommends \
    ca-certificates \
    e2fsprogs \
    curl \
    tzdata \
    nano \
    openssl \
    gpg \
    mosquitto \
    mosquitto-clients \
    git \
    iptables \
    iproute2 \
    kmod \
    util-linux \
    xz-utils \
    pigz \
    unzip \
    lsb-release \
    fuse-overlayfs \
    uidmap \
    libaom3 \
    libass9 \
    libfontconfig1 \
    libfreetype6 \
    libgnutls30t64 \
    libmp3lame0 \
    libopus0 \
    libva2 \
    libva-drm2 \
    libvpx9 \
    libxcb1 \
    libx264-164 \
    libx265-199 \
    libxml2; \
  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime; echo $TZ > /etc/timezone; \
  curl -fsSL https://deb.nodesource.com/setup_20.x -o /tmp/nodesource_setup.sh; \
  bash /tmp/nodesource_setup.sh; \
  apt-get install -y --no-install-recommends nodejs; \
  rm -f /tmp/nodesource_setup.sh; \
  curl -fsSLo /tmp/ngrok.tgz https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz; \
  tar xf /tmp/ngrok.tgz -C /usr/local/bin; \
  rm -f /tmp/ngrok.tgz; \
  mkdir -p /etc/apt/keyrings; \
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg; \
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list; \
  apt-get update; \
  apt-get install -y --no-install-recommends docker-ce docker-ce-cli containerd.io; \
  curl -fsSLo /tmp/cuda-keyring.deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2404/x86_64/cuda-keyring_1.1-1_all.deb; \
  dpkg -i /tmp/cuda-keyring.deb; \
  rm -f /tmp/cuda-keyring.deb; \
  apt-get update; \
  apt-get install -y --no-install-recommends \
    libnvinfer10 \
    libnvinfer-plugin10 \
    libnvonnxparsers10 \
    libnvinfer-bin \
    "cuda-cudart-dev-${CUDA_DEVEL_VERSION}" \
    "cuda-nvcc-${CUDA_DEVEL_VERSION}" \
    "libcublas-dev-${CUDA_DEVEL_VERSION}"; \
  TRT_INSTALLED_VERSION="$(dpkg-query -W -f='${Version}' libnvinfer10 2>/dev/null || true)"; \
  if [ -z "${TRT_INSTALLED_VERSION}" ]; then \
    echo "TensorRT package libnvinfer10 not installed"; \
    exit 1; \
  fi; \
  echo "TensorRT installed: ${TRT_INSTALLED_VERSION}"; \
  if [ ! -x "${CUDA_ROOT}/bin/nvcc" ]; then \
    echo "CUDA nvcc not installed under ${CUDA_ROOT}"; \
    exit 1; \
  fi; \
  rm -rf /usr/local/include /usr/local/lib/pkgconfig /usr/local/share/doc /usr/local/share/man; \
  rm -rf /var/lib/apt/lists/*; \
  ldconfig

ENV CUDA_HOME="${CUDA_ROOT}" \
    PATH="/opt/python/bin:/usr/local/bin:/usr/src/tensorrt/bin:${CUDA_ROOT}/bin:$PATH" \
    LD_LIBRARY_PATH="/opt/python/lib:/usr/local/lib:${CUDA_ROOT}/lib64" \
    UV_HTTP_TIMEOUT=300 \
    AI_ENV="base_edge_node_amd64_gpu_new" \
    AI_ENV_VER="0.3.0"

RUN set -eux; \
  curl -Ls https://astral.sh/uv/install.sh | sh; \
  if [ -f /root/.local/bin/uv ]; then mv /root/.local/bin/uv /usr/local/bin/uv; fi; \
  if [ -f /root/.local/bin/uvx ]; then mv /root/.local/bin/uvx /usr/local/bin/uvx; fi; \
  rm -rf /root/.local; \
  apt-get update; \
  apt-get install -y --no-install-recommends build-essential cmake libopenblas-dev pkg-config; \
  uv pip install --system --no-cache --no-compile --no-binary numpy \
    -C 'setup-args=-Dcpu-baseline=none' \
    "numpy>=2.1"; \
  uv pip install --system --no-cache --no-compile \
    torch \
    torchvision \
    torchaudio \
    --extra-index-url ${TORCH_CHANNEL}; \
  uv pip install --system --no-cache --no-compile -r /tmp/requirements.txt; \
  LD_LIBRARY_PATH="/opt/python/lib" /opt/python/bin/python3 -m pip install --no-cache-dir --no-compile \
    --index-url https://pypi.nvidia.com \
    --extra-index-url https://pypi.org/simple \
    tensorrt-cu12-bindings; \
  LD_LIBRARY_PATH="/opt/python/lib" /opt/python/bin/python3 -c "import site; from pathlib import Path; trt_dir = Path(site.getsitepackages()[0]) / 'tensorrt'; trt_dir.mkdir(exist_ok=True); (trt_dir / '__init__.py').write_text('from tensorrt_bindings import *\nfrom tensorrt_bindings import __version__\n')"; \
  # bitsandbytes is a GPU-oriented optional extension; enable it for test builds without a Python-version guard.
  if [ "${ENABLE_BITSANDBYTES}" = "true" ]; then \
    uv pip install --system --no-cache --no-compile bitsandbytes; \
    LD_LIBRARY_PATH="/opt/python/lib" /opt/python/bin/python3 -c "import bitsandbytes"; \
  fi; \
  # flash-attn needs CUDA compiler support and substantial RAM at build time; keep it opt-in for larger builders.
  if [ "${ENABLE_FLASH_ATTN}" = "true" ]; then \
    if command -v nvcc >/dev/null 2>&1; then \
      uv pip install --system --no-cache --no-compile ninja packaging psutil; \
      MAX_JOBS="${FLASH_ATTN_MAX_JOBS}" uv pip install --system --no-cache --no-build-isolation flash-attn; \
      LD_LIBRARY_PATH="/opt/python/lib" /opt/python/bin/python3 -c "import flash_attn"; \
    else \
      echo "ENABLE_FLASH_ATTN=true but nvcc is not available in the GPU test image"; \
      exit 1; \
    fi; \
  fi; \
  PYTHON_MAJOR_MINOR="${PYTHON_VERSION%.*}"; \
  rm -rf "/opt/python/lib/python${PYTHON_MAJOR_MINOR}/test" \
    "/opt/python/lib/python${PYTHON_MAJOR_MINOR}/idlelib" \
    "/opt/python/lib/python${PYTHON_MAJOR_MINOR}/turtledemo" \
    "/opt/python/lib/python${PYTHON_MAJOR_MINOR}/ensurepip/_bundled"; \
  find "/opt/python/lib/python${PYTHON_MAJOR_MINOR}" -type d -name __pycache__ -prune -exec rm -rf '{}' +; \
  find "/opt/python/lib/python${PYTHON_MAJOR_MINOR}" -type f -name '*.pyc' -delete; \
  find /usr/local/lib -type f \( -name '*.a' -o -name '*.la' \) -delete; \
  strip --strip-unneeded /opt/python/bin/python3.13 /usr/local/bin/ffmpeg /usr/local/bin/ffprobe /usr/local/bin/ngrok || true; \
  find /opt/python/lib -type f -name '*.so' -exec strip --strip-unneeded '{}' + || true; \
  find /usr/local/lib -type f -name '*.so*' -exec strip --strip-unneeded '{}' + || true; \
  apt-get autoremove -y; \
  rm -rf /var/lib/apt/lists/*; \
  rm -rf /root/.cache

RUN mkdir -p /root/intel && echo 0 > /root/intel/openvino_telemetry
RUN mkdir -p /intel && echo 0 > /intel/openvino_telemetry && chmod o+r /intel/openvino_telemetry

WORKDIR /ai_edge_node

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["bash"]
