#!/usr/bin/env python3
import os
import platform
import subprocess
import tempfile
import time
import warnings

import inspect
import numpy as np
import torch


def log_section(title: str) -> None:
    print(f"== {title} ==")


def log_kv(key: str, value: object) -> None:
    print(f"{key}={value}")


def max_abs_diff(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.max(np.abs(a - b)))


def benchmark(
    fn,
    target_sec: float = 6.0,
    max_sec: float = 10.0,
    warmup: int = 10,
) -> dict:
    for _ in range(warmup):
        fn()
    times_ms = []
    iters = 0
    start = time.perf_counter()
    while True:
        t0 = time.perf_counter()
        fn()
        t1 = time.perf_counter()
        times_ms.append((t1 - t0) * 1000.0)
        iters += 1
        elapsed = time.perf_counter() - start
        if elapsed >= target_sec or elapsed >= max_sec:
            break
    arr = np.asarray(times_ms, dtype=np.float64)
    p95 = float(np.percentile(arr, 95)) if arr.size else float("nan")
    mean = float(arr.mean()) if arr.size else float("nan")
    median = float(np.median(arr)) if arr.size else float("nan")
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


def log_environment(threads: int) -> None:
    log_section("environment")
    log_kv("python", platform.python_version())
    log_kv("platform", platform.platform())
    log_kv("threads_env", {
        "CPU_TEST_THREADS": os.getenv("CPU_TEST_THREADS"),
        "OMP_NUM_THREADS": os.getenv("OMP_NUM_THREADS"),
        "MKL_NUM_THREADS": os.getenv("MKL_NUM_THREADS"),
        "NUMEXPR_NUM_THREADS": os.getenv("NUMEXPR_NUM_THREADS"),
    })
    log_kv("torch_threads", torch.get_num_threads())
    log_kv("torch_interop_threads", torch.get_num_interop_threads())
    log_kv("torch_set_threads", threads)


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
    threads = int(os.getenv("CPU_TEST_THREADS", str(min(8, os.cpu_count() or 1))))
    torch.set_num_threads(threads)

    log_section("torch")
    log_kv("torch", torch.__version__)
    torch.manual_seed(0)

    batch = int(os.getenv("CPU_TEST_BATCH", "256"))
    in_features = int(os.getenv("CPU_TEST_IN", "1024"))
    hidden = int(os.getenv("CPU_TEST_HIDDEN", "2048"))
    out_features = int(os.getenv("CPU_TEST_OUT", "1024"))
    layers = int(os.getenv("CPU_TEST_LAYERS", "3"))
    log_kv(
        "model_shape",
        f"batch={batch}, in={in_features}, hidden={hidden}, out={out_features}, layers={layers}",
    )

    log_environment(threads)

    class MLP(torch.nn.Module):
        def __init__(self) -> None:
            super().__init__()
            mods = []
            dim = in_features
            for _ in range(max(layers - 1, 1)):
                mods.append(torch.nn.Linear(dim, hidden))
                mods.append(torch.nn.ReLU())
                dim = hidden
            mods.append(torch.nn.Linear(dim, out_features))
            self.net = torch.nn.Sequential(*mods)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return self.net(x)

    model = MLP().eval()
    x = torch.randn(batch, in_features)
    with torch.inference_mode():
        y_ref = model(x).numpy()

    log_section("torchscript")
    ts = torch.jit.trace(model, x)
    with torch.inference_mode():
        y_ts = ts(x).numpy()
    log_kv("torchscript max_abs_diff", f"{max_abs_diff(y_ref, y_ts):.6g}")

    log_section("onnx / onnxruntime")
    import onnx  # noqa: F401
    import onnxruntime as ort

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
            torch.onnx.export(model, x, onnx_path, **export_kwargs)
        sess_options = ort.SessionOptions()
        sess_options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        sess_options.intra_op_num_threads = threads
        sess = ort.InferenceSession(
            onnx_path,
            providers=["CPUExecutionProvider"],
            sess_options=sess_options,
        )
        x_np = x.numpy()
        ort_inputs = {"input": x_np}
        y_ort = sess.run(None, ort_inputs)[0]
        log_kv("onnxruntime", ort.__version__)
        log_kv("onnxruntime max_abs_diff", f"{max_abs_diff(y_ref, y_ort):.6g}")

        log_section("openvino")
        try:
            import openvino
            from openvino import Core

            core = Core()
            try:
                core.set_property("CPU", {"INFERENCE_NUM_THREADS": threads})
            except Exception as exc:
                print(f"openvino threads config warn: {exc}")
            ov_model = core.read_model(onnx_path)
            compiled = core.compile_model(
                ov_model,
                "CPU",
                {
                    "PERFORMANCE_HINT": "LATENCY",
                    "NUM_STREAMS": "1",
                },
            )
            try:
                input_name = compiled.inputs[0].get_any_name()
            except Exception:
                input_name = "input"
            infer_request = compiled.create_infer_request()
            ov_inputs = {input_name: x_np}
            infer_request.infer(ov_inputs)
            y_ov = infer_request.get_output_tensor(0).data
            ov_ver = getattr(openvino, "__version__", "unknown")
            y_ov = np.array(y_ov)
        except ImportError:
            from openvino.inference_engine import IECore

            core = IECore()
            net = core.read_network(model=onnx_path)
            exec_net = core.load_network(net, "CPU")
            ov_inputs = {"input": x_np}
            ov_out = exec_net.infer(ov_inputs)
            y_ov = next(iter(ov_out.values()))
            ov_ver = "inference_engine"
            y_ov = np.array(y_ov)

        log_kv("openvino", ov_ver)
        log_kv("openvino max_abs_diff", f"{max_abs_diff(y_ref, y_ov):.6g}")

        log_section("speed (ms/iter)")
        with torch.inference_mode():
            ts_stats = benchmark(lambda: ts(x))
        ort_stats = benchmark(lambda: sess.run(None, ort_inputs))
        if "ov_inputs" in locals():
            if "infer_request" in locals():
                ov_stats = benchmark(lambda: infer_request.infer(ov_inputs))
            else:
                ov_stats = benchmark(lambda: exec_net.infer(ov_inputs))
            print_bench_stats("torchscript", ts_stats, batch)
            print_bench_stats("onnxruntime", ort_stats, batch)
            print_bench_stats("openvino", ov_stats, batch)
            warn_perf("openvino", ts_stats, ov_stats)
        else:
            print_bench_stats("torchscript", ts_stats, batch)
            print_bench_stats("onnxruntime", ort_stats, batch)
            print("openvino=NA")
    finally:
        try:
            os.remove(onnx_path)
        except OSError:
            pass

    np.testing.assert_allclose(y_ref, y_ts, rtol=1e-3, atol=1e-4)
    np.testing.assert_allclose(y_ref, y_ort, rtol=1e-3, atol=1e-4)
    np.testing.assert_allclose(y_ref, y_ov, rtol=1e-3, atol=1e-4)
    print("OK")

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
    print("====== Running CPU image test... =======")
    print("========================================")
    main()
    print("====== Done CPU image test... =======")
