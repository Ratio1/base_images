# Upgrade and Refactor Plan
Target: modernize all base images (OS, Python, PyTorch), converge on consistent DinD support, and streamline CI/CD for multi-arch delivery.

## 1) Objectives & Scope
- Replace `base_edge_node` with explicit variants: `base_edge_node_amd64_gpu`, `base_edge_node_amd64_cpu`, `base_edge_node_arm64_cpu` (Pi-optimized), `base_edge_node_arm64_tegra` (Jetson-optimized). Drop `base_edge_node_dind` after DinD is built into each image as an opt-in entrypoint.
- Move all eligible images to Ubuntu 24.04 LTS and Python 3.13; keep exceptions documented (Jetson base images tied to NVIDIA L4T/JetPack).
- Upgrade PyTorch to the latest stable release per arch (CPU, CUDA 12.x for amd64, JetPack-matched for Tegra).
- Harden Docker-in-Docker (TLS by default, rootless where possible, fuse-overlayfs, uidmap) and align with the latest Docker CE release.
- Optimize arm64 Pi and Jetson builds for size, thermal headroom, and hardware-accelerated codecs.
- Refactor GitHub Actions to a unified, cache-aware matrix pipeline with consistent tagging and provenance metadata.

## 2) Current Baseline Snapshot
- amd64: `base_edge_node` (GPU/CPU Dockerfiles), `base_edge_node_dind` (DinD wrapper), FastAPI bases.
- arm64: `base_edge_node_arm64_cpu` (generic Pi), `base_edge_node_arm64_tegra` (FROM `dustynv/l4t-pytorch:r36.2.0`), FastAPI is amd64-only today.
- CI: per-directory workflows using Buildx cloud drivers, minimal caching, manual retag scripts.

## 3) Image Matrix & Naming
- New canonical names:  
  - `base_edge_node_amd64_gpu` (CUDA 12.x)  
  - `base_edge_node_amd64_cpu`  
  - `base_edge_node_arm64_cpu` (Pi-optimized)  
  - `base_edge_node_arm64_tegra` (JetPack-aligned)  
  - Remove `base_edge_node` (legacy alias) and `base_edge_node_dind`.
- Tag pattern: `<arch>-py<ver>-th<ver>[-tr<ver>][-dind]` plus `latest`. Use Docker metadata action to add `sha`, `date`, and `v*` semver tags when present.

## 4) OS & Python Upgrade Strategy
- amd64 GPU/CPU and Pi: move to `ubuntu:24.04` (or `arm64v8/ubuntu:24.04`). Validate glibc compatibility with bundled libs (ffmpeg, flash-attn).
- Jetson: stay on the official L4T base matching the target JetPack (r36.2 == Ubuntu 22.04). 24.04 is not yet supported by NVIDIA; document this exception.
- Python 3.13: use `ppa:deadsnakes/ppa` or `python:3.13-slim` stage for amd64/arm64 CPU; confirm PyTorch wheel availability. If PyTorch for 3.13 is gated, set a feature flag to fall back to 3.12 while keeping Dockerfile ready for 3.13 once released.

## 5) PyTorch Upgrade Path
- Target PyTorch ≥ 2.4.x (or the latest stable) for amd64 CPU/GPU with CUDA 12.4 wheels from `https://download.pytorch.org/whl/cu124`.
- FastAPI + LLM base: align with the same torch/transformers versions to reduce cache misses and dependency drift.
- Jetson: match NVIDIA’s L4T PyTorch release for r36.2 (JetPack 6). If a newer L4T-PyTorch tag exists, bump to it; otherwise keep r36.2 torch and document pinning.
- Add a small smoke test script per image (`python - <<'PY'` printing platform, torch, transformers, cuda availability) for CI validation.
  - References: PyTorch install matrix https://pytorch.org/get-started/locally/; CUDA 12.4 wheels https://download.pytorch.org/whl/cu124; L4T PyTorch container catalog https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-pytorch.

## 6) TensorRT Upgrade Path
- amd64 GPU: evaluate the latest stable TensorRT (10.x) from NVIDIA PyPI (`--extra-index-url https://pypi.nvidia.com`). Keep a hard pin (e.g., `tensorrt==10.0.x`) matching CUDA 12.x and the chosen torch version; add a build arg to fall back to 8.6.1 if regressions appear.
- Jetson: rely on JetPack-bundled TensorRT (apt packages `libnvinfer*`); do not pip-upgrade. Document the JetPack/TRT version and expose it via an image label.
- FastAPI/CPU-only images: omit TensorRT to reduce size; keep the install optional behind a build arg.
- Testing: run `trtexec --version` and a minimal engine build to verify CUDA/cuDNN alignment in CI for amd64; for Jetson mark runtime validation as on-device only.
  - Reference: TensorRT release notes https://docs.nvidia.com/deeplearning/tensorrt/release-notes/.

## 7) DinD Integration (all images)
- Embed Docker CE (rootless preferred) inside each edge image with opt-in via `EE_DD=true`. Provide two entrypoints: normal app entrypoint and `dockerd-entrypoint.sh`.
- Upgrade Docker CE to the latest LTS (e.g., 27.x+), use `fuse-overlayfs` and `uidmap`, set `DOCKER_TLS_CERTDIR` with auto-generated certs, and allow `EE_DD=false` to skip daemon start.
- Harden: drop capabilities where possible, purge build tools after install, and enable log rotation defaults.
- Remove the standalone `base_edge_node_dind` directory after migration; keep a compatibility tag that points to the new amd64 DinD-enabled GPU image.
  - References: Docker CE release notes https://docs.docker.com/engine/release-notes/; Rootless mode https://docs.docker.com/engine/security/rootless/; DinD security guidance https://docs.docker.com/engine/security/protect-access/#docker-in-docker.

## 8) arm64 Pi Optimization
- Base: `arm64v8/ubuntu:24.04` (or `debian:bookworm-slim` if smaller) with `--platform=linux/arm64/v8` buildx.
- Python: from deadsnakes 3.13 or compiled once in a builder stage; install minimal build deps then purge. Prefer `pip --no-cache-dir` and `--extra-index-url https://download.pytorch.org/whl/cpu` if using torch CPU wheels.
- ffmpeg: reuse a common multi-stage builder; copy only binaries and libs. Consider disabling heavy codecs on Pi to save space.
- Enable `arm_64bit=1` expectation, ensure `pi` friendly sysctl not assumed; keep `nano/vim` optional.
  - References: Ubuntu arm64 images https://hub.docker.com/_/ubuntu; Raspberry Pi Docker build guidance https://docs.docker.com/build/arm/.

## 9) arm64 Tegra Optimization
- Stay on `dustynv/l4t-pytorch:<matching JP>`; confirm JetPack 6.0 GA tag and CUDA/cuDNN versions. Only rebuild ffmpeg if the base lacks needed codecs; otherwise rely on NVIDIA-provided multimedia stack.
- Avoid upgrading to Ubuntu 24.04 until NVIDIA ships it. Note that Python 3.13 may not be supported; keep Python version tied to the L4T image (likely 3.10/3.11). If 3.13 is required, document it as blocked and add a conditional build arg.
- Use `--runtime nvidia` expectations; test on-device or via QEMU for syntax only, with runtime tests marked “manual on Jetson”.
  - References: JetPack downloads/compatibility https://developer.nvidia.com/embedded/jetpack; L4T PyTorch container https://catalog.ngc.nvidia.com/orgs/nvidia/containers/l4t-pytorch.

## 10) FastAPI Bases Alignment
- Rebase `base_fastapi` and `base_th_llm_fastapi` onto the new amd64 CPU base to inherit Python 3.13 and system deps. Switch to `pip install --no-cache-dir` and drop redundant package installs.
- Pin transformers to a version compatible with the upgraded torch; add minimal healthcheck script (import torch/transformers/uvicorn).
  - References: FastAPI Docker deployment guide https://fastapi.tiangolo.com/deployment/docker/.

## 11) CI/CD Refactor
- Consolidate workflows into a matrix: axes for `{arch: amd64, arm64, tegra}` and `{variant: gpu, cpu, dind}` where applicable; reuse a single workflow with conditional include/exclude rules.
- Use `docker/setup-buildx-action@v3` with `driver: docker-container` and `cache-from/cache-to: type=gha,mode=max`.
- Add QEMU setup for cross builds, and leverage `docker/metadata-action` for tags/labels and SBOM/attestations (`docker/build-push-action` supports `provenance`).
- Integrate the new smoke tests post-build (run containers, print torch/transformers/cuda info). For Jetson, gate runtime tests behind a manual “device” job.
- Replace manual retag scripts with buildx-driven multi-tag outputs; keep legacy tags via `--tag` list in a single build step.
  - References: Buildx docs https://docs.docker.com/build/buildx/; QEMU setup https://github.com/docker/setup-qemu-action; metadata/provenance https://github.com/docker/metadata-action.

## 12) Execution Sequence (phased)
1. Define common base snippets (Python install, ffmpeg builder, DinD entrypoint) and update AGENTS.md with the new matrix and tag scheme.
2. Implement amd64 CPU/GPU Dockerfiles on Ubuntu 24.04 + Python 3.13; upgrade torch/transformers; embed DinD entrypoint; deprecate `base_edge_node` alias.
3. Port Pi image to 24.04 (or Debian slim), add multi-stage ffmpeg, Python 3.13, torch CPU wheels, and size/boot-time trims.
4. Update Tegra image to latest L4T-PyTorch tag; reconcile ffmpeg needs; document Python/OS constraints.
5. Rebase FastAPI images on the new amd64 CPU base and retest.
6. Replace `base_edge_node_dind` with new DinD-enabled images; maintain temporary compatibility tags.
7. Refactor GitHub Actions into a matrix workflow with caching, metadata, SBOM, and smoke tests.
8. Run end-to-end builds (amd64, arm64 via QEMU; Jetson syntax-only) and push to staging tags; verify runtime on actual devices for Pi/Jetson before promoting `latest`.

## 13) Risk & Mitigation Notes
- Python 3.13 + PyTorch: watch official wheel availability; keep a toggle to fall back to 3.12 without blocking the refactor.
- Jetson OS jump: blocked until NVIDIA publishes 24.04-based L4T; document the exception and avoid forced upgrade.
- DinD in all images: ensure it remains optional to avoid bloating non-Docker use cases; keep entrypoint selectable.
- Cross-build drift: rely on buildx + QEMU; validate with smoke tests and device runs before tagging `latest`.
