# Debug Results - 2026-01-23

## Scope
- Images under test:
  - ratio1/base_edge_node_amd64_gpu:dev
  - ratio1/base_edge_node_amd64_cpu:dev
- Tests added:
  - image_tests/gpu_image_test.py
  - image_tests/cpu_image_test.py
  - test-gpu.sh
  - test-cpu.sh

## Test Runs (local)
### CPU
Command:
`./test-cpu.sh`

Outcome:
- Torch OK
- TorchScript vs ONNX vs OpenVINO: outputs match (max abs diff = 0)
- Docker-in-Docker (hello-world): FAILED

Error (DIND):
- dockerd starts, but `docker run hello-world` fails with:
  - "failed to mount ... fstype overlay ... err: invalid argument"

### GPU
Command:
`./test-gpu.sh`

Outcome:
- Torch CUDA OK (GPU visible, simple op works)
- Transformers OK
- Web3 OK
- TensorRT build: FAILED

Error (TensorRT):
- "CUDA initialization failure with error: 35"
- Builder creation returns nullptr (TypeError)

Additional diagnostics:
- `nvidia-smi` inside container shows:
  - Driver 560.94, CUDA 12.6
- libcudart reports:
  - runtime 12090 (CUDA 12.9)
  - driver 12060 (CUDA 12.6)

## Findings
1) TensorRT failure is consistent with CUDA runtime > driver.
   - Error 35 maps to "cudaErrorInsufficientDriver" (driver too old for runtime). citeturn6open0
   - CUDA 12.9 GA requires driver >= 575.51.03 for full compatibility. citeturn9open0
   - Current driver 560.94 (CUDA 12.6) is below that requirement.

2) DIND overlay mount failure indicates overlay2 cannot be used with the backing filesystem.
   - Docker overlay2 requires specific kernel/filesystem support (e.g., backing FS must support d_type) and proper kernel support. citeturn11open0
   - In nested docker-in-docker, overlay-on-overlay frequently triggers "invalid argument" during mount; use a different storage driver or a proper backing filesystem. (Inference based on Docker overlay2 requirements.) citeturn11open0

## Recommended Fixes
### TensorRT / CUDA mismatch
Option A (preferred): Upgrade host NVIDIA driver to >= 575.51.03 (or newer 575+ driver that supports CUDA 12.9). citeturn9open0

Option B: Rebuild the GPU image to match CUDA 12.6 (driver capability), using PyTorch/TensorRT builds that target CUDA 12.6.

Option C: Install CUDA compatibility package for 12.9 (cuda-compat-12-9) inside the image and ensure it is on the library path, then retest. This can enable forward compatibility on newer 12.x drivers, but still requires a driver new enough for CUDA 12.x. citeturn6open0turn9open0

### Docker-in-Docker overlay failure
Option A: Run DIND with a non-overlay storage driver (e.g., set `DOCKER_DRIVER=vfs`).
Option B: Mount a volume backed by a filesystem that supports overlay2 requirements (xfs with d_type=1 or ext4), and point `/var/lib/docker` to it. citeturn11open0
Option C: Use fuse-overlayfs if available and configured for the inner dockerd. citeturn11open0

## Notes
- The TensorRT error occurs before the DIND test step in the GPU test, so DIND status for GPU is unknown until TensorRT is fixed or skipped.
