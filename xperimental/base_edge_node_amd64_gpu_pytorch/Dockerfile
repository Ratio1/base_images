FROM pytorch/pytorch:2.9.1-cuda12.8-cudnn9-runtime AS ffmpeg-builder

ARG FFMPEG_VERSION=6.1.1

ENV DEBIAN_FRONTEND=noninteractive
ENV PATH="/usr/bin:/bin:${PATH}"

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

FROM pytorch/pytorch:2.9.1-cuda12.8-cudnn9-runtime

ARG TORCH_VERSION=2.9.1
ARG TORCHVISION_VERSION=0.24.1
ARG TORCHAUDIO_VERSION=2.9.1
ARG TENSORRT_VERSION=10.14.1.48.post1
ARG ENABLE_BITSANDBYTES=false
ARG ENABLE_FLASH_ATTN=false

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Etc/UTC \
    DOCKER_TLS_CERTDIR=/certs \
    EE_DD=false \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

COPY --from=ffmpeg-builder /usr/local /usr/local
COPY base_edge_node_amd64_gpu_pytorch/requirements.txt /tmp/requirements.txt
COPY scripts/entrypoint.sh /usr/local/bin/entrypoint.sh

RUN set -eux; \
  chmod +x /usr/local/bin/entrypoint.sh; \
  apt-get update; \
  UBUNTU_VERSION="$(. /etc/os-release; echo ${VERSION_ID})"; \
  if [ "${UBUNTU_VERSION}" = "22.04" ]; then \
    GNUTLS_PKG=libgnutls30; \
    VPX_PKG=libvpx7; \
    X264_PKG=libx264-163; \
  elif [ "${UBUNTU_VERSION}" = "24.04" ]; then \
    GNUTLS_PKG=libgnutls30t64; \
    VPX_PKG=libvpx9; \
    X264_PKG=libx264-164; \
  else \
    echo "Unsupported Ubuntu version: ${UBUNTU_VERSION}"; \
    exit 1; \
  fi; \
  apt-get install -y --no-install-recommends \
    ca-certificates \
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
    ${GNUTLS_PKG} \
    libmp3lame0 \
    libopus0 \
    libva2 \
    libva-drm2 \
    ${VPX_PKG} \
    ${X264_PKG} \
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
  UBUNTU_REPO="ubuntu$(printf '%s' "${UBUNTU_VERSION}" | tr -d '.')"; \
  curl -fsSLo /tmp/cuda-keyring.deb "https://developer.download.nvidia.com/compute/cuda/repos/${UBUNTU_REPO}/x86_64/cuda-keyring_1.1-1_all.deb"; \
  dpkg -i /tmp/cuda-keyring.deb; \
  rm -f /tmp/cuda-keyring.deb; \
  apt-get update; \
  apt-get install -y --no-install-recommends \
    libnvinfer10 \
    libnvinfer-plugin10 \
    libnvonnxparsers10 \
    libnvinfer-bin; \
  TRT_INSTALLED_VERSION="$(dpkg-query -W -f='${Version}' libnvinfer10 2>/dev/null || true)"; \
  if [ -z "${TRT_INSTALLED_VERSION}" ]; then \
    echo "TensorRT package libnvinfer10 not installed"; \
    exit 1; \
  fi; \
  echo "TensorRT installed: ${TRT_INSTALLED_VERSION}"; \
  rm -rf /usr/local/include /usr/local/lib/pkgconfig /usr/local/share/doc /usr/local/share/man; \
  rm -rf /var/lib/apt/lists/*; \
  ldconfig

ENV PATH="/opt/conda/bin:/usr/local/bin:$PATH" \
    LD_LIBRARY_PATH="/opt/conda/lib:/usr/local/lib" \
    UV_HTTP_TIMEOUT=300 \
    AI_ENV="base_edge_node_amd64_gpu_pytorch" \
    AI_ENV_VER="0.2.0"

RUN set -eux; \
  curl -Ls https://astral.sh/uv/install.sh | sh; \
  if [ -f /root/.local/bin/uv ]; then mv /root/.local/bin/uv /usr/local/bin/uv; fi; \
  if [ -f /root/.local/bin/uvx ]; then mv /root/.local/bin/uvx /usr/local/bin/uvx; fi; \
  rm -rf /root/.local; \
  uv pip install --system --no-cache --no-compile -r /tmp/requirements.txt; \
  if ! /opt/conda/bin/python -c "import torchvision, torchaudio" >/dev/null 2>&1; then \
    uv pip install --system --no-cache --no-compile \
      torchvision==${TORCHVISION_VERSION} \
      torchaudio==${TORCHAUDIO_VERSION}; \
  fi; \
  /opt/conda/bin/python -m pip install --no-cache-dir --no-compile \
    --index-url https://pypi.nvidia.com \
    --extra-index-url https://pypi.org/simple \
    tensorrt-cu12-bindings==${TENSORRT_VERSION}; \
  /opt/conda/bin/python -c "import site; from pathlib import Path; trt_dir = Path(site.getsitepackages()[0]) / 'tensorrt'; trt_dir.mkdir(exist_ok=True); (trt_dir / '__init__.py').write_text('from tensorrt_bindings import *\\nfrom tensorrt_bindings import __version__\\n')"; \
  PYTHON_MAJOR_MINOR="$(/opt/conda/bin/python -c 'import sys; print(f"{sys.version_info[0]}.{sys.version_info[1]}")')"; \
  if [ "${ENABLE_BITSANDBYTES}" = "true" ]; then \
    if [ "${PYTHON_MAJOR_MINOR}" = "3.13" ]; then \
      echo "Skipping bitsandbytes on Python ${PYTHON_MAJOR_MINOR}"; \
    else \
      uv pip install --system --no-cache --no-compile bitsandbytes; \
    fi; \
  fi; \
  if [ "${ENABLE_FLASH_ATTN}" = "true" ]; then \
    if [ "${PYTHON_MAJOR_MINOR}" = "3.13" ]; then \
      echo "Skipping flash-attn on Python ${PYTHON_MAJOR_MINOR}"; \
    else \
      uv pip install --system --no-cache --no-compile flash-attn; \
    fi; \
  fi; \
  rm -rf /root/.cache

RUN mkdir -p /root/intel && echo 0 > /root/intel/openvino_telemetry
RUN mkdir -p /intel && echo 0 > /intel/openvino_telemetry && chmod o+r /intel/openvino_telemetry

WORKDIR /ai_edge_node

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["bash"]
