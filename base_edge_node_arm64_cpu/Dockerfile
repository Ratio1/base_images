FROM ubuntu:22.04

COPY requirements.txt /tmp/requirements.txt
COPY scripts/build-ffmpeg.sh /tmp/build-ffmpeg.sh
WORKDIR /tmp

# Set a default value for the TZ environment variable
ENV TZ=Etc/UTC

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
    tzdata \
    nano && \
  apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev && \
  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
  cd /tmp && \
  pip3 install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu \
    torch \
    torchvision \
    torchaudio && \
  apt-get install -y --no-install-recommends \
    wget \
    build-essential \
    curl \
    git \
    nasm \
    cmake \
    pkg-config \
    ninja-build \
    libhdf5-dev && \
  pip install --no-cache-dir --upgrade -r /tmp/requirements.txt && \
  pip install --no-cache-dir meson && \
  bash build-ffmpeg.sh && \
  apt-get purge -y \
    build-essential \
    wget \
    curl \
    git \
    cmake \
    ninja-build && \
  apt-get -y autoremove && \
  apt-get -y autoclean && \
  rm -rf /var/lib/apt/lists/* && \
  pip uninstall -y meson

# Download and install ngrok
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
  curl https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz > /tmp/ngrok.tgz && \
  tar xf /tmp/ngrok.tgz -C /usr/local/bin && \
  rm /tmp/ngrok.tgz && \
  apt-get purge -y curl && \
  apt-get -y autoremove && \
  apt-get -y autoclean && \
  rm -rf /var/lib/apt/lists/*

# Make sure we look for shared objects in /usr/local/lib
ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/lib"

# Set up workdir and the various env variables.
WORKDIR /exe_eng_base
ENV AI_ENV="base_edge_node_arm64_cpu"
ENV AI_ENV_VER = "0.1.2"
