FROM ubuntu:22.04

COPY requirements.txt /tmp/requirements.txt
COPY ./scripts/build-ffmpeg.sh /tmp/build-ffmpeg.sh
WORKDIR /tmp
ENV TZ=Etc/UTC

# Note we're leaving build-essential behind because torch compile
# needs a system compiler.
# Note: tensor-rt forced to 8.6.1 to avoid the new 10.0 experimental release.
RUN apt-get update && \
  apt-get install -y --no-install-recommends software-properties-common gpg-agent && \
  apt-get install -y --no-install-recommends \
    tzdata \
    nano \
    vim && \
  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
  apt-get install -y --no-install-recommends \
    python3-pip \
    python3-dev && \
  cd /tmp && \
  pip3 install --no-cache-dir --upgrade -r /tmp/requirements.txt && \
  pip3 install --no-cache-dir "tensorrt==8.6.1" --extra-index-url https://pypi.nvidia.com && \
  apt-get install -y --no-install-recommends \
    wget \
    build-essential \
    git \
    nasm \
    cmake \
    pkg-config \
    ninja-build \
    curl && \
  pip3 install --no-cache-dir meson && \
  bash build-ffmpeg.sh && \
  apt-get purge -y cmake wget git ninja-build && \
  apt-get -y autoremove && \
  apt-get -y autoclean && \
  rm -rf /var/lib/apt/lists/* && \
  pip3 uninstall -y meson && \
  rm -rf /root/.cache

# Download and install ngrok
RUN curl https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz > /tmp/ngrok.tgz && \
  tar xf /tmp/ngrok.tgz -C /usr/local/bin && \
  rm /tmp/ngrok.tgz

# Disable openvino telemetry
RUN mkdir -p /root/intel && echo 0 > "/root/intel/openvino_telemetry"
RUN mkdir -p /intel && echo 0 > "/intel/openvino_telemetry" && chmod o+r /intel/openvino_telemetry

# Make sure we look for shared objects in /usr/local/lib
ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/lib"

# Set up workdir and the various env variables.
WORKDIR /ai_edge_node


ENV AI_ENV="base_edge_node"
ENV AI_ENV_VER = "0.1.3"
