#!/usr/bin/env python3
import os
import subprocess
import tempfile
import time

import inspect
import numpy as np
import torch


def max_abs_diff(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.max(np.abs(a - b)))


def benchmark(fn, target_sec: float = 6.0, max_sec: float = 10.0, warmup: int = 20) -> float:
    for _ in range(warmup):
        fn()
    iters = 0
    start = time.perf_counter()
    while True:
        fn()
        iters += 1
        elapsed = time.perf_counter() - start
        if elapsed >= target_sec:
            break
        if elapsed >= max_sec:
            break
    return (elapsed * 1000.0) / max(iters, 1)


def main() -> None:
    print("== torch ==")
    print(f"torch={torch.__version__}")
    torch.manual_seed(0)

    class Tiny(torch.nn.Module):
        def __init__(self) -> None:
            super().__init__()
            self.fc1 = torch.nn.Linear(4, 8)
            self.act = torch.nn.ReLU()
            self.fc2 = torch.nn.Linear(8, 2)

        def forward(self, x: torch.Tensor) -> torch.Tensor:
            return self.fc2(self.act(self.fc1(x)))

    model = Tiny().eval()
    x = torch.randn(1, 4)
    with torch.no_grad():
        y_ref = model(x).numpy()

    print("== torchscript ==")
    ts = torch.jit.trace(model, x)
    y_ts = ts(x).detach().numpy()
    print(f"torchscript max_abs_diff={max_abs_diff(y_ref, y_ts):.6g}")

    print("== onnx / onnxruntime ==")
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
        torch.onnx.export(model, x, onnx_path, **export_kwargs)
        sess = ort.InferenceSession(onnx_path, providers=["CPUExecutionProvider"])
        x_np = x.numpy()
        ort_inputs = {"input": x_np}
        y_ort = sess.run(None, ort_inputs)[0]
        print(f"onnxruntime={ort.__version__} max_abs_diff={max_abs_diff(y_ref, y_ort):.6g}")

        print("== openvino ==")
        try:
            import openvino
            from openvino.runtime import Core

            core = Core()
            ov_model = core.read_model(onnx_path)
            compiled = core.compile_model(ov_model, "CPU")
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

        print(f"openvino={ov_ver} max_abs_diff={max_abs_diff(y_ref, y_ov):.6g}")

        print("== speed (ms/iter) ==")
        with torch.no_grad():
            ts_ms = benchmark(lambda: ts(x))
        ort_ms = benchmark(lambda: sess.run(None, ort_inputs))
        if "ov_inputs" in locals():
            if "infer_request" in locals():
                ov_ms = benchmark(lambda: infer_request.infer(ov_inputs))
            else:
                ov_ms = benchmark(lambda: exec_net.infer(ov_inputs))
            print(f"torchscript_ms={ts_ms:.3f} onnxruntime_ms={ort_ms:.3f} openvino_ms={ov_ms:.3f}")
        else:
            print(f"torchscript_ms={ts_ms:.3f} onnxruntime_ms={ort_ms:.3f} openvino_ms=NA")
    finally:
        try:
            os.remove(onnx_path)
        except OSError:
            pass

    np.testing.assert_allclose(y_ref, y_ts, rtol=1e-3, atol=1e-4)
    np.testing.assert_allclose(y_ref, y_ort, rtol=1e-3, atol=1e-4)
    np.testing.assert_allclose(y_ref, y_ov, rtol=1e-3, atol=1e-4)
    print("OK")

    print("== dind hello-world ==")
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
            raise SystemExit(f"docker run failed:\n{run.stdout.strip()}")
        print(run.stdout.strip())


if __name__ == "__main__":
  print("========================================")
  print("====== Running CPU image test... =======")
  print("========================================")
  main()
  print("====== Done CPU image test... =======")
