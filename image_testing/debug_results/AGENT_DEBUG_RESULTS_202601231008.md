# Debug Results - Fri Jan 23 10:08:10 EET 2026

TLS environment detected. Generating certs...
/certs/server/cert.pem: OK
/certs/client/cert.pem: OK
iptables v1.8.10 (nf_tables)
Launching dockerd in the background...
Waiting for dockerd to respond...
dockerd is now running.
TLS environment detected. Generating certs...
/certs/server/cert.pem: OK
/certs/client/cert.pem: OK
iptables v1.8.10 (nf_tables)
Launching dockerd in the background...
Waiting for dockerd to respond...
dockerd is now running.
[01/23/2026-08:08:56] [TRT] [W] Unable to determine GPU memory usage: In getGpuMemStatsInBytes at /_src/common/extended/resources.cpp:1175
[01/23/2026-08:08:56] [TRT] [E] createInferBuilder: Error Code 6: API Usage Error (CUDA initialization failure with error: 35. Please check your CUDA installation: http://docs.nvidia.com/cuda/cuda-installation-guide-linux/index.html In operator() at /_src/optimizer/api/builder.cpp:1360)
[01/23/2026-08:08:56] [TRT] [E] [checkMacros.cpp::catchCudaError::229] Error Code 1: Cuda Runtime (In catchCudaError at /_src/common/dispatch/checkMacros.cpp:229)
== torch cuda ==
torch=2.9.1+cu129
torch_cuda=12.9
gpu=NVIDIA GeForce RTX 2080 Ti
cc=7.5 sm_hex=0x75
cudnn=91002
== transformers ==
transformers=4.57.1 out=(1, 2, 16)
== web3 ==
web3=7.14.0 connected=False
== tensorrt build ==
tensorrt=10.14.1.48.post1
TLS environment detected. Generating certs...
/certs/server/cert.pem: OK
/certs/client/cert.pem: OK
iptables v1.8.10 (nf_tables)
Launching dockerd in the background...
Waiting for dockerd to respond...
dockerd is now running.
== torch ==
torch=2.9.1+cpu
== torchscript ==
torchscript max_abs_diff=0
== onnx / onnxruntime ==
onnxruntime=1.23.0 max_abs_diff=0
== openvino ==
openvino=2025.1.0-18503-6fec06580ab-releases/2025/1 max_abs_diff=0
== speed (ms/iter) ==
torchscript_ms=0.033 onnxruntime_ms=0.012 openvino_ms=0.088
OK
== dind hello-world ==
EE_DD not set - skipping docker daemon initialization
Fri Jan 23 08:09:52 2026       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 560.35.02              Driver Version: 560.94         CUDA Version: 12.6     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 2080 Ti     On  |   00000000:65:00.0  On |                  N/A |
| 33%   41C    P8             37W /  260W |    3519MiB /  11264MiB |     39%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
                                                                                         
+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A        23      G   /Xwayland                                   N/A      |
+-----------------------------------------------------------------------------------------+
EE_DD not set - skipping docker daemon initialization
EE_DD not set - skipping docker daemon initialization
platform Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.39
torch 2.9.1+cpu
onnxruntime 1.23.0
openvino 2025.1.0-18503-6fec06580ab-releases/2025/1

## Scope
- GPU image: ratio1/base_edge_node_amd64_gpu:dev
- CPU image: ratio1/base_edge_node_amd64_cpu:dev
- Commands:
  - /home/andrei/work/base_images/image_testing/test-gpu.sh
  - /home/andrei/work/base_images/image_testing/test-cpu.sh
  - docker run --rm --gpus=all ratio1/base_edge_node_amd64_gpu:dev nvidia-smi
  - docker run --rm -i ratio1/base_edge_node_amd64_cpu:dev python3 - <<'PY' ...

## Results
- GPU test: FAIL (TensorRT builder init failed with CUDA error 35; pybind11::init() returned nullptr).
- CPU test: Python checks OK; DIND hello-world FAIL (overlay mount invalid argument).

## Logs (key excerpts only)
- GPU:
  - createInferBuilder: CUDA initialization failure with error 35
  - TypeError: pybind11::init(): factory function returned nullptr
- CPU:
  - docker run failed: failed to mount overlay ... err: invalid argument

## Diagnostics
- GPU host (nvidia-smi): Driver 560.94, CUDA 12.6, GPU RTX 2080 Ti.
- GPU container stack: torch 2.9.1+cu129 (CUDA 12.9 runtime), TensorRT 10.14.1.48.post1.
- CPU container stack: torch 2.9.1+cpu, onnxruntime 1.23.0, openvino 2025.1.0.
- Note: The CPU diagnostic here-doc required docker run -i to pass stdin.

## Root cause analysis (with sources)
1) CUDA error 35 means the installed NVIDIA driver is older than the CUDA runtime and must be updated to run newer runtimes.
   Source: https://docs.nvidia.com/cuda/archive/12.9.1/cuda-runtime-api/group__CUDART__TYPES.html
   Rationale: Host driver reports CUDA 12.6 while the container runtime is CUDA 12.9 (torch 2.9.1+cu129). That mismatch is consistent with cudaErrorInsufficientDriver (error 35) during TensorRT builder initialization.

2) OverlayFS/overlay2 requires kernel support and compatible backing filesystem; when unsupported, overlay mounts can fail.
   Source: https://docs.docker.com/engine/storage/drivers/overlayfs-driver/
   Rationale: The DIND hello-world failure shows overlay mount "invalid argument". This is consistent with overlay2 prerequisites not being met in the nested environment (e.g., overlay-on-overlay or backing FS constraints).

3) Docker recommends vfs only for testing or when no copy-on-write storage driver is supported; fuse-overlayfs is an alternative for hosts without overlay2 support.
   Source: https://docs.docker.com/engine/storage/drivers/select-storage-driver/
   Rationale: For DIND tests in constrained environments, forcing vfs (or fuse-overlayfs when applicable) can avoid overlay mount failures at the cost of performance.

## Proposed fixes (ranked)
1) GPU: Align CUDA runtime with host driver (e.g., rebuild image for CUDA 12.6) or upgrade host driver to a version that supports CUDA 12.9. Reinstall matching TensorRT if needed.
2) CPU/DIND: Configure inner dockerd to use a fallback storage driver (vfs or fuse-overlayfs) when overlay2 is unavailable. This is acceptable for test images but slower.
3) CPU/DIND: Verify host kernel and backing filesystem meet overlay2 prerequisites if overlay2 must be used.

## Retest results
- No fixes applied yet; no retest beyond the initial runs.
