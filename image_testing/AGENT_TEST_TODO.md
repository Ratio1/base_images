# Agent Test TODO (Image Regression)

Goal: enable any fresh agent to run the GPU/CPU image tests iteratively, investigate failures using online docs, and record findings in a timestamped report:
`./image_testing/AGENT_DEBUG_RESULTS_[YYYYmmddHHMM].md`

## Inputs
- GPU image name (default inside script): `ratio1/base_edge_node_amd64_gpu:dev`
- CPU image name (default inside script): `ratio1/base_edge_node_amd64_cpu:dev`
- Scripts:
  - `./image_testing/test-gpu.sh`
  - `./image_testing/test-cpu.sh`
- Python tests:
  - `./image_testing/gpu_image_test.py`
  - `./image_testing/cpu_image_test.py`

## Quick Run (one pass)
```bash
./image_testing/test-gpu.sh <gpu_image_tag>
./image_testing/test-cpu.sh <cpu_image_tag>
```
If no tag is provided, each script uses its default.

## Iterative Debug Loop (repeat until clean)
1) **Create a report file with timestamp**
```bash
TS="$(date +%Y%m%d%H%M)"
REPORT="./image_testing/AGENT_DEBUG_RESULTS_${TS}.md"
printf "# Debug Results - %s\n\n" "$(date)" > "${REPORT}"
```

2) **Run tests and capture logs**
```bash
./image_testing/test-gpu.sh <gpu_image_tag> | tee -a "${REPORT}"
./image_testing/test-cpu.sh <cpu_image_tag> | tee -a "${REPORT}"
```

3) **If a test fails, collect diagnostics**
Add the output of the following to the report:
```bash
docker run --rm --gpus=all <gpu_image_tag> nvidia-smi | tee -a "${REPORT}"
docker run --rm <cpu_image_tag> python3 - <<'PY' | tee -a "${REPORT}"
import torch, transformers, platform
print("platform", platform.platform())
print("torch", torch.__version__)
try:
    import onnxruntime as ort
    print("onnxruntime", ort.__version__)
except Exception as e:
    print("onnxruntime err", e)
try:
    import openvino
    print("openvino", getattr(openvino, "__version__", "unknown"))
except Exception as e:
    print("openvino err", e)
PY
```

4) **Use online documentation to interpret errors**
- Look up error codes/messages (CUDA/TensorRT/driver compatibility, Docker overlay issues, etc.).
- Record the exact sources and rationale in the report.

5) **Propose fixes**
- For each failure, add clear actionable fixes (e.g., driver upgrade, CUDA version alignment, DIND storage driver change).
- Note which fix you applied and retest.

6) **Retest after each change**
Repeat steps 2–5 until both scripts pass or you have a documented blocker.

## Suggested Report Structure
Include the following sections in each `AGENT_DEBUG_RESULTS_*.md`:
- Scope (images tested, commands run)
- Results (pass/fail for each test)
- Logs (key excerpts only)
- Diagnostics (driver versions, CUDA versions, storage driver)
- Root cause analysis (with links to docs)
- Proposed fixes (ranked, with expected impact)
- Retest results

## Notes
- These scripts expect privileged DIND operation; they will attempt to run `hello-world` inside the container.
- Keep edits to the test scripts minimal; prefer documenting the issue and fixing the image instead.
