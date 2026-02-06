# Repository Guidelines

## Project Structure & Module Organization
- `base_edge_node_amd64_cpu/`: production AMD64 CPU image (`Dockerfile`, `requirements.txt`, `retag_and_push.sh`).
- `base_edge_node_amd64_gpu/`: production AMD64 GPU image (`Dockerfile`, `requirements.txt`, `retag_and_push.sh`).
- `scripts/`: shared build/runtime helpers (`build-ffmpeg.sh`, `entrypoint.sh`) used by image Dockerfiles.
- `build-and-push-amd64-cpu.sh` / `build-and-push-amd64-gpu.sh`: root entrypoints for build, push, and retag flows.
- `image_testing/`: runtime validation scripts for CPU/GPU images.
- `xperimental/`: non-production image variants under active experimentation.
- `_archive/`: legacy image definitions and historical workflows (including prior arm64/tegra/dind layouts).

## Build, Tag & Publish Commands
- Standard local builds:
  ```bash
  docker build -f base_edge_node_amd64_cpu/Dockerfile -t ratio1/base_edge_node_amd64_cpu:latest .
  docker build -f base_edge_node_amd64_gpu/Dockerfile -t ratio1/base_edge_node_amd64_gpu:latest .
  ```
- Standard build+push wrappers:
  ```bash
  ./build-and-push-amd64-cpu.sh
  ./build-and-push-amd64-gpu.sh
  ```
- Retagging:
  - CPU: `cd base_edge_node_amd64_cpu && ./retag_and_push.sh ratio1/base_edge_node_amd64_cpu:latest`
  - GPU: `cd base_edge_node_amd64_gpu && ./retag_and_push.sh ratio1/base_edge_node_amd64_gpu:latest`

## Coding Style & Naming Conventions
- Dockerfiles: chain commands with `&& \`, clean apt caches, and avoid extra layers without cleanup.
- Shell scripts: use `#!/bin/bash`, `set -euo pipefail`, and quoted variables.
- Tags must stay aligned with retag scripts:
  - CPU: `py<major.minor>-th<major.minor>-ox<major.minor>-tr<major.minor>`
  - GPU: `py<major.minor>-th<major.minor>-cu<major.minor>-trt<major.minor>-tr<major.minor>`

## Testing & Validation
- Run runtime validations before publishing:
  ```bash
  ./image_testing/test-cpu.sh ratio1/base_edge_node_amd64_cpu:latest
  ./image_testing/test-gpu.sh ratio1/base_edge_node_amd64_gpu:latest
  ```
- Verify media stack where relevant: `docker run --rm <img> ffmpeg -codecs | head`.
- Keep validation commands in PR description for reproducibility.

## Documentation Is Mandatory (AGENTS.md Is Alive)
- `AGENTS.md` is a living operations contract, not a static note.
- Any important project change MUST update `AGENTS.md` in the same branch/PR.
- Any critical horizontal change MUST also update `README.md` in the same branch/PR.
- Every important change must append one dated bullet in `## Change Ledger (Keep Updated)` with a concise summary of what changed and why.
- Critical horizontal aspects include:
  - Architecture/accelerator coverage matrix.
  - Base OS/runtime axis (Python, Torch, CUDA/TensorRT, ONNX/Transformers).
  - Build/publish entrypoints and tagging schema.
  - Shared runtime services and behavior (`entrypoint`, DIND flags, ffmpeg toolchain).
  - Validation expectations that define release readiness.
- PRs missing required documentation updates are incomplete and should not be merged.

## Change Ledger (Keep Updated)
- `2026-02-06`: Established living documentation policy, added mandatory AGENTS+README sync for critical horizontal changes, and aligned structure/build guidance with segregated AMD64 CPU/GPU image families.

## Commit & Pull Request Guidelines
- Match history style: short imperative subjects with type prefixes (`fix: ...`, `chore: ...`, `feat: ...`).
- PRs should include:
  - Purpose and impacted image families.
  - Build/retag commands used.
  - Produced tags.
  - Validation output from `image_testing/`.
  - Documentation updates (`AGENTS.md`, `README.md`) when required by policy.

## Security & Configuration Tips
- Builds fetch from external apt/git sources; do not embed credentials in Dockerfiles or scripts.
- Use local `docker login`/registry auth in CI secrets rather than hardcoded tokens.
- Keep `LD_LIBRARY_PATH`, Python runtime settings, and entrypoint env defaults consistent when adding dependencies.
