# Tegra/Jetson TODO (archived)

All Jetson work is paused and tracked here; current focus is amd64 (CPU/GPU) and arm64 CPU. Re-enable when NVIDIA ships a newer L4T/JetPack base (ideally Ubuntu 24.04) and matching PyTorch wheels.

## Current baseline
- Latest public base: `dustynv/l4t-pytorch:r36.4.0` (JetPack 6.x, Ubuntu 22.04, NVIDIA-built PyTorch). CUDA 12.4-aligned option: `dustynv/l4t-pytorch:r36.3.0-cu124`.
- Python: vendor stack (Py3.10/3.11). Python 3.13 is not available on Jetson bases today; cp313 assumptions do not hold.
- DinD: not yet integrated; would need docker-ce + `EE_DD` entrypoint added without disturbing NVIDIA CUDA/TRT stack.

## Deferred actions
- Dockerfile: when resuming, start from `r36.4.0` (or newer), keep vendor Python/torch, add DinD (docker-ce, fuse-overlayfs, uidmap) while preserving CUDA/TRT libs. No attempt to force Ubuntu 24.04 until NVIDIA publishes it.
- Package strategy: stay with vendor torch/TRT; avoid forcing cp313. Continue using `uv pip --system` for Python deps that match the base Python.
- Tests: run only on-device with `--runtime nvidia`; keep nested Docker checks optional via `SKIP_NESTED` and `EE_DD=true`. CUDA/TensorRT smoke must be marked "on-device only" (no CI emulation).
- CI: exclude Tegra from the main matrix. Add a gated/manual job for device testing when hardware is available.
- Tagging: keep legacy `arm64_tegra` tags; consider `<arch>-py<th>-tr` style once a new base is chosen.

## Re-entry criteria
- NVIDIA publishes a Jetson base on Ubuntu 24.04 or a newer L4T with PyTorch/TensorRT supporting the target Python.
- Confirm matching wheels/apt packages for the desired Python/TensorRT/CUDA stack and availability of DinD prerequisites (overlayfs/iptables modules).
