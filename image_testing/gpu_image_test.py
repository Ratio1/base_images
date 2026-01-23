#!/usr/bin/env python3
import os
import subprocess
import tempfile
import time

import inspect
import torch


def benchmark_gpu(fn, target_sec: float = 6.0, max_sec: float = 10.0, warmup: int = 20) -> float:
    for _ in range(warmup):
        fn()
    torch.cuda.synchronize()
    iters = 0
    start = time.perf_counter()
    while True:
        fn()
        iters += 1
        torch.cuda.synchronize()
        elapsed = time.perf_counter() - start
        if elapsed >= target_sec:
            break
        if elapsed >= max_sec:
            break
    return (elapsed * 1000.0) / max(iters, 1)


def main() -> None:
    print("== torch cuda ==")
    print(f"torch={torch.__version__}")
    print(f"torch_cuda={torch.version.cuda}")
    if not torch.cuda.is_available():
        raise SystemExit("CUDA not available in torch")
    dev = torch.device("cuda:0")
    props = torch.cuda.get_device_properties(dev)
    cc = torch.cuda.get_device_capability(dev)
    sm_hex = (cc[0] << 4) | cc[1]
    print(f"gpu={props.name}")
    print(f"cc={cc[0]}.{cc[1]} sm_hex=0x{sm_hex:02x}")
    print(f"cudnn={torch.backends.cudnn.version()}")
    x = torch.randn(8, device=dev)
    y = x * 2
    torch.cuda.synchronize()
    if y.device.type != "cuda":
        raise SystemExit("Tensor not on CUDA device")

    print("== transformers ==")
    import transformers
    from transformers import BertConfig, BertModel

    cfg = BertConfig(
        hidden_size=16,
        num_hidden_layers=1,
        num_attention_heads=2,
        intermediate_size=32,
    )
    model = BertModel(cfg)
    with torch.no_grad():
        out = model(torch.zeros(1, 2, dtype=torch.long))
    print(f"transformers={transformers.__version__} out={tuple(out.last_hidden_state.shape)}")

    print("== web3 ==")
    import web3
    from web3 import Web3

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    print(f"web3={web3.__version__} connected={w3.is_connected()}")

    print("== tensorrt build ==")
    import tensorrt as trt
    import onnx  # noqa: F401

    print(f"tensorrt={trt.__version__}")
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

    print("== speed (ms/iter) ==")
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

    with torch.no_grad():
        ts_ms = benchmark_gpu(lambda: ts_model(trt_input))
    trt_ms = benchmark_gpu(trt_run)
    print(f"torchscript_ms={ts_ms:.3f} tensorrt_ms={trt_ms:.3f}")

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
  print("====== Running GPU image test... =======")
  print("========================================") 
  main()
  print("====== Done GPU image test... =======")
