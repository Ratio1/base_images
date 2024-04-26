#!/bin/bash

# Bail out on errors.
set -e

# This builds ffmpeg 6.1 from source. We're matching the same configuration
# of ffmpeg as that that we would get from conda. Note there are pottentially
# more codecs that we could build (including proprietary ones), but these are
# clearly not used at this point.

# apt-get install all codecs that we can actually install on 20.04.
apt-get install -y --no-install-recommends \
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
  libass-dev

# Build the dav1d codec.
git clone https://code.videolan.org/videolan/dav1d.git dav1d
cd dav1d
git checkout 1.4.1
mkdir -p build
cd build
meson setup \
  -Denable_tools=false \
  -Denable_tests=false \
  --default-library=static \
  .. \
  --prefix "/usr/lib" \
  --libdir="/usr/lib"
ninja
ninja install
cd /tmp
rm -rf dav1d

# Build the openh264 codec.
git clone https://github.com/cisco/openh264.git openh264
cd openh264
git checkout openh264v2.2.0
make -j8
make install
cd /tmp
rm -rf openh264

# Build the SVT-AV1 codec
git clone https://gitlab.com/AOMediaCodec/SVT-AV1/
cd SVT-AV1/
git checkout v2.0.0
mkdir build
cd build/
cmake  -GNinja -DCMAKE_BUILD_TYPE=Release ../
ninja install
cd /tmp
rm -rf SVT-AV1

# Now build ffmpeg. Use the same configuration options as
# used in the conda-forge build.
git clone https://github.com/FFmpeg/FFmpeg.git ffmpeg
cd ffmpeg
git checkout release/6.1
./configure \
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
make -j16
make install
cd /tmp
rm -rf ffmpeg
