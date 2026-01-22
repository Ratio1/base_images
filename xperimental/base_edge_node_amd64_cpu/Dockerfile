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
ARG TORCH_VERSION=2.9.1
ARG TORCHVISION_VERSION=0.24.1
ARG TORCHAUDIO_VERSION=2.9.1
ARG TORCH_CHANNEL=https://download.pytorch.org/whl/cpu
ARG ENABLE_BITSANDBYTES=false
ARG ENABLE_FLASH_ATTN=false

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Etc/UTC \
    DOCKER_TLS_CERTDIR=/certs \
    EE_DD=false \
    PIP_DISABLE_PIP_VERSION_CHECK=1

COPY --from=python-builder /opt/python /opt/python
COPY --from=ffmpeg-builder /usr/local /usr/local
COPY base_edge_node_amd64_cpu/requirements.txt /tmp/requirements.txt
COPY scripts/entrypoint.sh /usr/local/bin/entrypoint.sh

RUN set -eux; \
  chmod +x /usr/local/bin/entrypoint.sh; \
  apt-get update; \
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
    libgnutls30t64 \
    libmp3lame0 \
    libopus0 \
    libva2 \
    libva-drm2 \
    libvpx9 \
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
  rm -rf /var/lib/apt/lists/*; \
  ldconfig

ENV PATH="/opt/python/bin:/usr/local/bin:$PATH" \
    LD_LIBRARY_PATH="/opt/python/lib:/usr/local/lib" \
    UV_HTTP_TIMEOUT=300 \
    AI_ENV="base_edge_node_amd64_cpu" \
    AI_ENV_VER="0.2.0"

RUN set -eux; \
  curl -Ls https://astral.sh/uv/install.sh | sh; \
  if [ -f /root/.local/bin/uv ]; then mv /root/.local/bin/uv /usr/local/bin/uv; fi; \
  if [ -f /root/.local/bin/uvx ]; then mv /root/.local/bin/uvx /usr/local/bin/uvx; fi; \
  rm -rf /root/.local; \
  apt-get update; \
  apt-get install -y --no-install-recommends build-essential cmake; \
  uv pip install --system --no-cache --no-compile \
    torch==${TORCH_VERSION} \
    torchvision==${TORCHVISION_VERSION} \
    torchaudio==${TORCHAUDIO_VERSION} \
    --extra-index-url ${TORCH_CHANNEL}; \
  uv pip install --system --no-cache --no-compile -r /tmp/requirements.txt; \
  if [ "${ENABLE_BITSANDBYTES}" = "true" ]; then \
    if echo "${PYTHON_VERSION}" | grep -q '^3\.13'; then \
      echo "Skipping bitsandbytes on Python ${PYTHON_VERSION}"; \
    else \
      uv pip install --system --no-cache --no-compile bitsandbytes; \
    fi; \
  fi; \
  if [ "${ENABLE_FLASH_ATTN}" = "true" ]; then \
    if echo "${PYTHON_VERSION}" | grep -q '^3\.13'; then \
      echo "Skipping flash-attn on Python ${PYTHON_VERSION}"; \
    else \
      uv pip install --system --no-cache --no-compile flash-attn; \
    fi; \
  fi; \
  apt-get purge -y build-essential cmake; \
  apt-get autoremove -y; \
  rm -rf /var/lib/apt/lists/*; \
  rm -rf /root/.cache

RUN mkdir -p /root/intel && echo 0 > /root/intel/openvino_telemetry
RUN mkdir -p /intel && echo 0 > /intel/openvino_telemetry && chmod o+r /intel/openvino_telemetry

WORKDIR /exe_eng_base

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["bash"]
