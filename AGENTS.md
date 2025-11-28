# Repository Guidelines

## Project Structure & Module Organization
- `base_edge_node/`: Ubuntu 22.04 GPU base with ffmpeg build, Torch/Transformers, ngrok, and helpers (`scripts/build-ffmpeg.sh`, `scripts/flash_attn_package.py`, `retag_and_push.sh`); `Dockerfile_cpu` is CPU-only.
- `base_edge_node_arm64_cpu/`: Raspberry Pi image with dedicated `Dockerfile`, `requirements.txt`, and ffmpeg build script.
- `base_edge_node_arm64_tegra/`: Jetson/Tegra GPU image; `retag_and_push_arm64_tegra.sh` normalizes tags.
- `base_edge_node_dind/`: Docker-in-Docker layer (GPU and CPU `Dockerfile*`, `entrypoint.sh`) built on edge node images.
- `base_fastapi/`, `base_th_llm_fastapi/`: FastAPI bases with `Dockerfile`, `requirements.txt`, and `build.sh` for tagging/pushing.

## Build, Tag & Publish Commands
- Standard builds:  
  ```bash
  docker build -t ratio1/base_edge_node:dev base_edge_node
  docker build -f base_edge_node/Dockerfile_cpu -t ratio1/base_edge_node:cpu-dev base_edge_node
  docker build -t ratio1/base_edge_node_dind:dev base_edge_node_dind
  ```
- FastAPI bases auto-tag/push: `cd base_fastapi && ./build.sh 3.10.13-slim` or `cd base_th_llm_fastapi && ./build.sh`.
- Arm64 Tegra retagging (after building/pulling): `cd base_edge_node_arm64_tegra && ./retag_and_push_arm64_tegra.sh <image>`; tags follow `<arch>-py<ver>-th<ver>-tr<ver>`.
- Edge node GPU retagging: `cd base_edge_node && ./retag_and_push.sh <image>`.

## Coding Style & Naming Conventions
- Dockerfiles: chain commands with `&& \`, clean `apt` caches, keep pinned versions already used, and avoid extra layers without cleanup.
- Shell scripts: prefer `#!/bin/bash`, `set -euo pipefail`, and quoted variables; keep comments minimal but purposeful.
- Tags: follow existing scheme (`pyX.Y.Z`, `th2.4.0.cpu`, `tr4.43.3`, or `<arch>-py*-th*-tr*>`) so retag scripts stay aligned.

## Testing & Validation
- No formal unit tests; validate images with runtime checks:  
  ```bash
  docker run --rm <img> python3 - <<'PY'
  import torch, transformers, platform; print(platform.machine(), torch.__version__, transformers.__version__)
  PY
  ```
- Verify media stack where relevant: `docker run --rm <img> ffmpeg -codecs | head`.
- For DIND images, confirm daemon reachability: `docker run --privileged -e EE_DD=true <img> docker info`.

## Commit & Pull Request Guidelines
- Match history: short, imperative subjects with a type (`fix: ...`, `chore: ...`, `feat: ...`).
- PRs should list purpose, build/retag commands, resulting tags, target arch, and runtime verification output. Link issues when relevant and flag external deps (CUDA/TensorRT, ngrok, Node).
- Update READMEs or this guide when workflows change; keep scripts executable and paths accurate.

## Security & Configuration Tips
- Builds hit external apt/git sources; avoid embedding credentials. Use `docker login` locally rather than baking tokens.
- DIND defaults to TLS (`DOCKER_TLS_CERTDIR`); for local testing set `EE_DD=false` to skip daemon startup. Keep `LD_LIBRARY_PATH` and Python env vars aligned when adding packages.
