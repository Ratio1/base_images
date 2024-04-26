FROM dustynv/l4t-pytorch:r36.2.0

COPY requirements.txt /tmp/requirements.txt
WORKDIR /tmp
ENV TZ=Etc/UTC

RUN git clone git://source.ffmpeg.org/ffmpeg.git ffmpeg && \
  cd ffmpeg && \
  ./configure && \
  make -j8 && \
  make install && \
  cd /tmp && \
  rm -rf /tmp/ffmpeg

WORKDIR /ai_edge_node

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

# Install tzdata if it's not available in your base image.
RUN apt-get update && apt-get install -y -no-install-recommends tzdata nano vim

# Use the TZ variable to set the timezone
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENV AI_ENV="base_edge_node_tegra"
ENV AI_ENV_VER = "0.2.1"
