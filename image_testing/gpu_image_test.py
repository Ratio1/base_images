#!/usr/bin/env python3
import os
import platform
import subprocess
import tempfile
import time
import warnings

import inspect
import torch


def log_section(title: str) -> None:
    print(f"== {title} ==")


def log_kv(key: str, value: object) -> None:
    print(f"{key}={value}")


def benchmark_gpu(
    fn,
    target_sec: float = 6.0,
    max_sec: float = 10.0,
    warmup: int = 10,
) -> dict:
    for _ in range(warmup):
        fn()
    torch.cuda.synchronize()
    times_ms = []
    iters = 0
    start = time.perf_counter()
    while True:
        start_evt = torch.cuda.Event(enable_timing=True)
        end_evt = torch.cuda.Event(enable_timing=True)
        start_evt.record()
        fn()
        end_evt.record()
        torch.cuda.synchronize()
        times_ms.append(start_evt.elapsed_time(end_evt))
        iters += 1
        elapsed = time.perf_counter() - start
        if elapsed >= target_sec or elapsed >= max_sec:
            break
    if not times_ms:
        return {
            "iters": 0,
            "total_s": elapsed,
            "mean_ms": float("nan"),
            "median_ms": float("nan"),
            "p95_ms": float("nan"),
        }
    arr = torch.tensor(times_ms, dtype=torch.float64)
    p95 = float(torch.quantile(arr, 0.95).item())
    mean = float(arr.mean().item())
    median = float(arr.median().item())
    return {
        "iters": iters,
        "total_s": elapsed,
        "mean_ms": mean,
        "median_ms": median,
        "p95_ms": p95,
    }


def print_bench_stats(label: str, stats: dict, batch: int) -> None:
    throughput = float("nan")
    if stats["total_s"] > 0:
        throughput = (batch * stats["iters"]) / stats["total_s"]
    print(
        f"{label}_median_ms={stats['median_ms']:.3f} "
        f"{label}_p95_ms={stats['p95_ms']:.3f} "
        f"{label}_mean_ms={stats['mean_ms']:.3f} "
        f"{label}_iters={stats['iters']} "
        f"{label}_throughput={throughput:.1f}/s"
    )


def warn_perf(name: str, faster: dict, slower: dict, threshold: float = 1.10) -> None:
    if slower["median_ms"] > faster["median_ms"] * threshold:
        print(
            f"PERF_WARN: {name} slower than baseline "
            f"(median {slower['median_ms']:.3f}ms vs {faster['median_ms']:.3f}ms)"
        )


def log_environment() -> None:
    log_section("environment")
    log_kv("python", platform.python_version())
    log_kv("platform", platform.platform())
    log_kv("torch", torch.__version__)
    log_kv("torch_cuda", torch.version.cuda)


def print_dind_diagnostics() -> None:
    log_section("dind diagnostics")
    log_kv(
        "dind_env",
        {
            "EE_DD": os.getenv("EE_DD"),
            "DOCKER_TLS_CERTDIR": os.getenv("DOCKER_TLS_CERTDIR"),
            "DOCKER_HOST": os.getenv("DOCKER_HOST"),
            "DOCKER_DRIVER": os.getenv("DOCKER_DRIVER"),
        },
    )
    try:
        info = subprocess.run(
            ["docker", "info"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=20,
        )
        if info.returncode == 0:
            keys = (
                "Storage Driver",
                "Backing Filesystem",
                "Cgroup Version",
                "Kernel Version",
                "Operating System",
            )
            for line in info.stdout.splitlines():
                if any(key in line for key in keys):
                    print(line.strip())
        else:
            print(info.stdout.strip())
    except Exception as exc:
        print(f"docker info failed: {exc}")
    for cmd in (["docker", "version"], ["uname", "-a"]):
        try:
            diag = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=20,
            )
            print(f"$ {' '.join(cmd)}")
            print(diag.stdout.strip())
        except Exception as exc:
            print(f"diag failed for {' '.join(cmd)}: {exc}")


def main() -> None:
    log_section("torch cuda")
    log_environment()
    if not torch.cuda.is_available():
        raise SystemExit("CUDA not available in torch")
    dev = torch.device("cuda:0")
    props = torch.cuda.get_device_properties(dev)
    cc = torch.cuda.get_device_capability(dev)
    sm_hex = (cc[0] << 4) | cc[1]
    log_kv("gpu", props.name)
    log_kv("cc", f"{cc[0]}.{cc[1]} sm_hex=0x{sm_hex:02x}")
    log_kv("cudnn", torch.backends.cudnn.version())
    x = torch.randn(8, device=dev)
    y = x * 2
    torch.cuda.synchronize()
    if y.device.type != "cuda":
        raise SystemExit("Tensor not on CUDA device")

    log_section("transformers")
    import transformers
    from transformers import BertConfig, BertModel

    cfg = BertConfig(
        hidden_size=16,
        num_hidden_layers=1,
        num_attention_heads=2,
        intermediate_size=32,
    )
    model = BertModel(cfg).to(dev).eval()
    input_ids = torch.zeros(1, 2, dtype=torch.long, device=dev)
    attention_mask = torch.ones_like(input_ids)
    with torch.inference_mode():
        out = model(input_ids, attention_mask=attention_mask)
    log_kv("transformers", transformers.__version__)
    log_kv("transformers_device", out.last_hidden_state.device.type)
    log_kv("transformers_out", tuple(out.last_hidden_state.shape))

    log_section("web3")
    import web3
    from web3 import Web3

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    log_kv("web3", web3.__version__)
    log_kv("web3_connected", w3.is_connected())

    log_section("tensorrt build")
    import tensorrt as trt
    import onnx  # noqa: F401

    log_kv("tensorrt", trt.__version__)
    logger = trt.Logger(trt.Logger.WARNING)
    builder = trt.Builder(logger)
    flags = 1 << int(trt.NetworkDefinitionCreationFlag.EXPLICIT_BATCH)
    network = builder.create_network(flags)
    parser = trt.OnnxParser(network, logger)

    class Tiny(torch.nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.fc1 = torch.nn.Linear(4, 8)
            self.act = torch.nn.ReLU()
            self.fc2 = torch.nn.Linear(8, 2)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return self.fc2(self.act(self.fc1(x)))

    model = Tiny().eval()
    dummy = torch.randn(1, 4)

    with tempfile.NamedTemporaryFile(suffix=".onnx", delete=False) as f:
        onnx_path = f.name
    try:
        export_kwargs = dict(
            opset_version=17,
            input_names=["input"],
            output_names=["output"],
        )
        if "dynamo" in inspect.signature(torch.onnx.export).parameters:
            export_kwargs["dynamo"] = False
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", category=DeprecationWarning)
            torch.onnx.export(model, dummy, onnx_path, **export_kwargs)
        with open(onnx_path, "rb") as f:
            if not parser.parse(f.read()):
                msgs = [str(parser.get_error(i)) for i in range(parser.num_errors)]
                raise SystemExit("ONNX parse failed:\n" + "\n".join(msgs))
        config = builder.create_builder_config()
        config.set_memory_pool_limit(trt.MemoryPoolType.WORKSPACE, 1 << 28)
        if builder.platform_has_fast_fp16:
            config.set_flag(trt.BuilderFlag.FP16)
        if hasattr(builder, "build_serialized_network"):
            serialized = builder.build_serialized_network(network, config)
            if serialized is None:
                raise SystemExit("TensorRT build_serialized_network returned None")
            runtime = trt.Runtime(logger)
            engine = runtime.deserialize_cuda_engine(serialized)
        else:
            engine = builder.build_engine(network, config)
        if engine is None:
            raise SystemExit("TensorRT engine build failed")
        print("TensorRT engine build: OK")
    finally:
        try:
            os.remove(onnx_path)
        except OSError:
            pass

    if cc[0] >= 12:
        print("SM 12.x detected; TensorRT build verified on this device")
    else:
        print("SM 12.x not detected; TensorRT build verified on this device's SM")

    log_section("speed (ms/iter)")
    trt_dtype_map = {
        trt.DataType.FLOAT: torch.float32,
        trt.DataType.HALF: torch.float16,
        trt.DataType.INT8: torch.int8,
        trt.DataType.INT32: torch.int32,
        trt.DataType.BOOL: torch.bool,
    }
    context = engine.create_execution_context()
    io_names = [engine.get_tensor_name(i) for i in range(engine.num_io_tensors)]
    input_names = [n for n in io_names if engine.get_tensor_mode(n) == trt.TensorIOMode.INPUT]
    output_names = [n for n in io_names if engine.get_tensor_mode(n) == trt.TensorIOMode.OUTPUT]
    if not input_names or not output_names:
        raise SystemExit("TensorRT engine missing input/output tensors")
    input_name = input_names[0]
    output_name = output_names[0]

    input_shape = tuple(dummy.shape)
    try:
        if -1 in tuple(context.get_tensor_shape(input_name)):
            context.set_input_shape(input_name, input_shape)
    except Exception:
        pass
    output_shape = tuple(context.get_tensor_shape(output_name))
    if -1 in output_shape:
        with torch.no_grad():
            output_shape = tuple(model(dummy).shape)
    input_dtype = trt_dtype_map.get(engine.get_tensor_dtype(input_name), torch.float32)
    output_dtype = trt_dtype_map.get(engine.get_tensor_dtype(output_name), torch.float32)

    trt_input = torch.randn(*input_shape, device=dev, dtype=input_dtype)
    trt_output = torch.empty(*output_shape, device=dev, dtype=output_dtype)
    context.set_tensor_address(input_name, trt_input.data_ptr())
    context.set_tensor_address(output_name, trt_output.data_ptr())
    stream = torch.cuda.current_stream()

    def trt_run() -> None:
        context.execute_async_v3(stream.cuda_stream)

    ts_model = torch.jit.trace(model.to(dev).to(input_dtype), trt_input)
    ts_model.eval()

    with torch.inference_mode():
        ts_stats = benchmark_gpu(lambda: ts_model(trt_input))
    trt_stats = benchmark_gpu(trt_run)
    batch = int(trt_input.shape[0])
    print_bench_stats("torchscript", ts_stats, batch)
    print_bench_stats("tensorrt", trt_stats, batch)
    warn_perf("tensorrt", ts_stats, trt_stats)

    log_section("dind hello-world")
    try:
        run = subprocess.run(
            ["docker", "run", "--rm", "hello-world"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        print(run.stdout.strip())
    except FileNotFoundError as exc:
        raise SystemExit("docker CLI not found inside container") from exc
    except subprocess.CalledProcessError:
        pull = subprocess.run(
            ["docker", "pull", "hello-world"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if pull.returncode != 0:
            raise SystemExit(f"docker pull failed:\n{pull.stdout.strip()}")
        run = subprocess.run(
            ["docker", "run", "--rm", "hello-world"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if run.returncode != 0:
            print("docker run failed; collecting diagnostics...")
            print_dind_diagnostics()
            raise SystemExit(f"docker run failed:\n{run.stdout.strip()}")
        print(run.stdout.strip())


if __name__ == "__main__":
    print("========================================")
    print("====== Running GPU image test... =======")
    print("========================================")
    main()
    print("====== Done GPU image test... =======")
