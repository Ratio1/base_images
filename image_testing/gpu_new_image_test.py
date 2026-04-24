#!/usr/bin/env python3
import os
import platform
import shutil
import subprocess
import tempfile
from pathlib import Path


def log_section(title: str) -> None:
    print(f"== {title} ==")


def log_kv(key: str, value: object) -> None:
    print(f"{key}={value}")


def run(cmd: list[str], cwd: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )


def main() -> None:
    log_section("environment")
    log_kv("python", platform.python_version())
    log_kv("platform", platform.platform())
    log_kv("ai_env", os.getenv("AI_ENV"))
    log_kv("cuda_home", os.getenv("CUDA_HOME"))

    log_section("toolchain")
    nvcc = shutil.which("nvcc")
    if not nvcc:
        raise SystemExit("nvcc missing from PATH")
    cmake = shutil.which("cmake")
    if not cmake:
        raise SystemExit("cmake missing from PATH")
    log_kv("nvcc", nvcc)
    log_kv("cmake", cmake)
    print(run(["nvcc", "--version"]).stdout.strip())
    print(run(["cmake", "--version"]).stdout.splitlines()[0])

    log_section("python packages")
    import bitsandbytes  # noqa: F401
    import flash_attn  # noqa: F401
    import tensorrt as trt
    import torch
    import transformers

    if not torch.cuda.is_available():
        raise SystemExit("CUDA not available in torch")
    log_kv("torch", torch.__version__)
    log_kv("torch_cuda", torch.version.cuda)
    log_kv("transformers", transformers.__version__)
    log_kv("tensorrt", trt.__version__)
    log_kv("bitsandbytes", getattr(bitsandbytes, "__version__", "unknown"))
    log_kv("flash_attn", getattr(flash_attn, "__version__", "unknown"))

    log_section("cuda compile smoke")
    cuda_source = r"""
#include <cuda_runtime.h>
#include <cublas_v2.h>
#include <iostream>

int main() {
  int count = 0;
  if (cudaGetDeviceCount(&count) != cudaSuccess || count <= 0) {
    std::cerr << "cudaGetDeviceCount failed" << std::endl;
    return 1;
  }
  cublasHandle_t handle;
  if (cublasCreate(&handle) != CUBLAS_STATUS_SUCCESS) {
    std::cerr << "cublasCreate failed" << std::endl;
    return 1;
  }
  cublasDestroy(handle);
  std::cout << "CUDA compile smoke: OK devices=" << count << std::endl;
  return 0;
}
"""
    cmake_lists = r"""
cmake_minimum_required(VERSION 3.24)
project(cuda_smoke LANGUAGES CXX CUDA)
find_package(CUDAToolkit REQUIRED)
add_executable(cuda_smoke main.cu)
target_link_libraries(cuda_smoke PRIVATE CUDA::cudart CUDA::cublas)
set_target_properties(cuda_smoke PROPERTIES CUDA_STANDARD 17 CUDA_STANDARD_REQUIRED ON)
"""

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        (tmp / "main.cu").write_text(cuda_source)
        (tmp / "CMakeLists.txt").write_text(cmake_lists)
        build_dir = tmp / "build"
        run(["cmake", "-S", str(tmp), "-B", str(build_dir)], cwd=tmpdir)
        run(["cmake", "--build", str(build_dir), "-j2"], cwd=tmpdir)
        output = run([str(build_dir / "cuda_smoke")], cwd=tmpdir).stdout.strip()
        print(output)


if __name__ == "__main__":
    main()
