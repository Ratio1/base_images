FROM ubuntu:24.04

ARG PYTHON_VERSION=3.12
ARG PYTHON_FALLBACK=3.12
ARG TORCH_VERSION=2.6.0
ARG TORCHVISION_VERSION=0.21.0
ARG TORCHAUDIO_VERSION=2.6.0
ARG TORCH_CHANNEL=https://download.pytorch.org/whl/cpu
ARG DOCKER_VERSION=7.1.0

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Etc/UTC \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    DOCKER_TLS_CERTDIR=/certs \
    EE_DD=false

WORKDIR /tmp
COPY scripts/build-ffmpeg.sh /tmp/build-ffmpeg.sh
COPY base_edge_node_amd64_cpu/requirements.txt /tmp/requirements.txt
COPY scripts/dockerd-entrypoint.sh /usr/local/bin/dockerd-entrypoint.sh

RUN set -eux; \
  chmod +x /usr/local/bin/dockerd-entrypoint.sh; \
  apt-get update; \
  apt-get install -y --no-install-recommends software-properties-common gpg-agent ca-certificates curl wget tzdata nano openssl; \
  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime; echo $TZ > /etc/timezone; \
  add-apt-repository ppa:deadsnakes/ppa; \
  apt-get update; \
  if ! apt-get install -y --no-install-recommends python${PYTHON_VERSION} python${PYTHON_VERSION}-dev python${PYTHON_VERSION}-venv python3-pip; then \
    apt-get install -y --no-install-recommends python${PYTHON_FALLBACK} python${PYTHON_FALLBACK}-dev python${PYTHON_FALLBACK}-venv python3-pip; \
  fi; \
  PY_BIN="python${PYTHON_VERSION}"; if [ ! -x "/usr/bin/${PY_BIN}" ]; then PY_BIN="python${PYTHON_FALLBACK}"; fi; \
  ${PY_BIN} -m venv /opt/venv; \
  . /opt/venv/bin/activate; pip install --upgrade pip setuptools; \
  apt-get install -y --no-install-recommends \
    build-essential git nasm cmake pkg-config ninja-build \
    libva-dev vainfo libgnutls28-dev libaom-dev libmp3lame-dev libopus-dev \
    libvpx-dev libx264-dev libx265-dev libxml2-dev libass-dev; \
  pip install --no-cache-dir meson; \
  bash /tmp/build-ffmpeg.sh; \
  pip uninstall -y meson; \
  apt-get purge -y build-essential git nasm cmake pkg-config ninja-build software-properties-common; \
  apt-get autoremove -y; \
  rm -rf /var/lib/apt/lists/* /root/.cache

RUN set -eux; \
  apt-get update; \
  apt-get install -y --no-install-recommends \
    mosquitto mosquitto-clients git iptables iproute2 xz-utils pigz unzip lsb-release \
    fuse-overlayfs uidmap curl; \
  curl -fsSL https://deb.nodesource.com/setup_20.x -o nodesource_setup.sh; \
  bash nodesource_setup.sh; \
  apt-get install -y --no-install-recommends nodejs; \
  rm -f nodesource_setup.sh; \
  curl -fsSLo /tmp/ngrok.tgz https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz; \
  tar xf /tmp/ngrok.tgz -C /usr/local/bin; rm /tmp/ngrok.tgz; \
  rm -rf /var/lib/apt/lists/*

RUN set -eux; \
  apt-get update; \
  mkdir -p /etc/apt/keyrings; \
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg; \
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list; \
  apt-get update; \
  apt-get install -y --no-install-recommends docker-ce docker-ce-cli containerd.io; \
  rm -rf /var/lib/apt/lists/*

ENV PATH="/opt/venv/bin:$PATH" \
    LD_LIBRARY_PATH="/usr/local/lib" \
    AI_ENV="base_edge_node_amd64_cpu" \
    AI_ENV_VER="0.2.0"

WORKDIR /ai_edge_node

RUN set -eux; \
  . /opt/venv/bin/activate; \
  pip install --no-cache-dir \
    torch==${TORCH_VERSION} \
    torchvision==${TORCHVISION_VERSION} \
    torchaudio==${TORCHAUDIO_VERSION} \
    --extra-index-url ${TORCH_CHANNEL}; \
  apt-get update; \
  apt-get install -y --no-install-recommends build-essential cmake; \
  pip install --no-cache-dir -r /tmp/requirements.txt; \
  pip install --no-cache-dir docker==${DOCKER_VERSION}; \
  apt-get purge -y build-essential cmake; \
  apt-get autoremove -y; \
  rm -rf /var/lib/apt/lists/*; \
  rm -rf /root/.cache

ENTRYPOINT ["/usr/local/bin/dockerd-entrypoint.sh"]
CMD ["bash"]
