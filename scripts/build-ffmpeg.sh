#!/bin/bash
set -euo pipefail

FFMPEG_VERSION="${FFMPEG_VERSION:-6.1.1}"
DAV1D_VERSION="${DAV1D_VERSION:-1.4.1}"
OPENH264_VERSION="${OPENH264_VERSION:-2.2.0}"
SVT_AV1_VERSION="${SVT_AV1_VERSION:-2.0.0}"
PREFIX="/usr/local"

cd /tmp

# Build the dav1d codec.
git clone --depth 1 --branch "${DAV1D_VERSION}" https://code.videolan.org/videolan/dav1d.git dav1d
cd dav1d
mkdir -p build
cd build
meson setup \
  -Denable_tools=false \
  -Denable_tests=false \
  --default-library=static \
  .. \
  --prefix "${PREFIX}" \
  --libdir="${PREFIX}/lib"
ninja
ninja install
cd /tmp
rm -rf dav1d

# Build the openh264 codec.
git clone --depth 1 --branch "openh264v${OPENH264_VERSION}" https://github.com/cisco/openh264.git openh264
cd openh264
make -j"$(nproc)"
make install PREFIX="${PREFIX}"
cd /tmp
rm -rf openh264

# Build the SVT-AV1 codec.
git clone --depth 1 --branch "v${SVT_AV1_VERSION}" https://gitlab.com/AOMediaCodec/SVT-AV1.git svt-av1
cd svt-av1
mkdir -p build
cd build
cmake -GNinja -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX="${PREFIX}" ../
ninja
ninja install
cd /tmp
rm -rf svt-av1

# Build ffmpeg from a pinned release.
cd /tmp
curl -fsSLO "https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.xz"
tar -xf "ffmpeg-${FFMPEG_VERSION}.tar.xz"
cd "ffmpeg-${FFMPEG_VERSION}"
./configure \
  --prefix="${PREFIX}" \
  --disable-doc \
  --disable-openssl \
  --enable-demuxer=dash \
  --enable-hardcoded-tables \
  --enable-libfreetype \
  --enable-libfontconfig \
  --enable-libopenh264 \
  --enable-libdav1d \
  --enable-gnutls \
  --enable-libmp3lame \
  --enable-libvpx \
  --enable-libass \
  --enable-pthreads \
  --enable-vaapi \
  --enable-gpl \
  --enable-libx264 \
  --enable-libx265 \
  --enable-libaom \
  --enable-libsvtav1 \
  --enable-libxml2 \
  --enable-pic \
  --enable-shared \
  --disable-static \
  --enable-version3 \
  --enable-zlib \
  --enable-libopus
make -j"$(nproc)"
make install
cd /tmp
rm -rf "ffmpeg-${FFMPEG_VERSION}" "ffmpeg-${FFMPEG_VERSION}.tar.xz"
