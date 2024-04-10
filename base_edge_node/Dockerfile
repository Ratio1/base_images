FROM ubuntu:22.04

COPY requirements.txt /tmp/requirements.txt
COPY ./scripts/build-ffmpeg.sh /tmp/build-ffmpeg.sh
WORKDIR /tmp
ENV TZ=Etc/UTC

# Note we're leaving build-essential behind because torch compile
# needs a system compiler.

RUN apt-get update && \
  apt-get install -y --no-install-recommends software-properties-common gpg-agent && \
  add-apt-repository ppa:deadsnakes/ppa && \
  apt-get update && \
  apt-get install -y --no-install-recommends \
    tzdata \
    nano \
    vim && \
  ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone && \
  apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-venv && \
  cd /opt && python3.10 -m venv venv && \
  . /opt/venv/bin/activate && \
  cd /tmp && \
  pip install --no-cache-dir --upgrade -r /tmp/requirements.txt && \
  pip install --no-cache-dir tensorrt --extra-index-url https://pypi.nvidia.com && \
  apt-get install -y --no-install-recommends \
    wget \
    build-essential \
    curl \
    git \
    nasm \
    cmake \
    pkg-config \
    ninja-build && \
  pip install --no-cache-dir meson && \
  bash build-ffmpeg.sh && \
  apt-get purge -y curl cmake wget git ninja-build && \
  apt-get -y autoremove && \
  apt-get -y autoclean && \
  rm -rf /var/lib/apt/lists/* && \
  pip uninstall -y meson

# Disable openvino telemetry
RUN mkdir -p /root/intel && echo 0 > "/root/intel/openvino_telemetry"
RUN mkdir -p /intel && echo 0 > "/intel/openvino_telemetry" && chmod o+r /intel/openvino_telemetry

# Use the created venv by default
ENV PATH="/opt/venv/bin:$PATH"
# Make sure we look for shared objects in /usr/local/lib
ENV LD_LIBRARY_PATH="$LD_LIBRARY_PATH:/usr/local/lib"

# Set up workdir and the various env variables.
WORKDIR /ai_edge_node

ENV AI_ENV="base_edge_node"
ENV AI_ENV_VER = "0.1.2"
