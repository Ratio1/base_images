# Review and Optimization Plan (AMD64 CPU/GPU Base Images)

## 0) Mission and Scope
This plan defines the execution path for a full technical review and optimization of:
- `base_edge_node_amd64_gpu/Dockerfile`
- `base_edge_node_amd64_cpu/Dockerfile`
- `.github/workflows/base_edge_node_amd64_cpu.yaml.paused`
- `.github/workflows/base_edge_node_amd64_gpu.yaml.paused`
- `build-and-push-amd64-cpu.sh`
- `build-and-push-amd64-gpu.sh`

The goal is to improve correctness, security posture, reproducibility, image size, and build time while preserving intended workloads.

## 1) Current State Snapshot (as analyzed)

### 1.1 Image construction patterns
- Both CPU/GPU images already use multi-stage builds:
  - `python-builder` (builds CPython from source)
  - `ffmpeg-builder` (builds FFmpeg + codecs from source)
  - runtime stage (Ubuntu 24.04)
- Both images install Docker Engine (`docker-ce`, `docker-ce-cli`, `containerd.io`) and use shared `scripts/entrypoint.sh` with optional DIND behavior (`EE_DD=false` default).
- Both images install Node.js via NodeSource setup script and `ngrok` via tarball download.

### 1.2 Key pinned versions in repo right now
- Python: `3.13.11`
- Torch stack: `2.9.1 / 0.24.1 / 2.9.1`
- GPU Torch channel: `cu128`
- TensorRT Python bindings: `10.14.1.48.post1`
- FFmpeg: `6.1.1`
- OpenVINO: `2025.1.0`
- ONNX Runtime OpenVINO EP: `1.23.0`
- Cryptography: `42.0.7`

### 1.3 Immediate review hotspots
- Workflow files are disabled by extension (`*.yaml.paused`).
- Workflows trigger only on image-folder changes, but build context is repo root (`context: .`) and Dockerfiles depend on `scripts/*`; script changes currently would not trigger CI.
- Workflows use older action majors (`actions/checkout@v4`, `docker/build-push-action@v5`) and cloud buildx mode (`driver: cloud`, `endpoint: naeural/naeural-builder`) that needs explicit readiness checks.
- No root `.dockerignore` file exists while build context is `.`.
- GPU TensorRT system libs are installed from apt, while Python TensorRT bindings are separately pinned; compatibility should be explicitly verified.
- CPU/GPU `requirements.txt` include many unpinned packages; drift risk and reproducibility risk are high.

## 2) Target Outcomes and Acceptance Criteria

### 2.1 Functional parity (must pass)
- CPU image:
  - `./image_testing/test-cpu.sh <image>` passes
  - `ffmpeg -codecs` check passes
- GPU image:
  - `./image_testing/test-gpu.sh <image>` passes on CUDA-capable host
  - TensorRT engine build smoke test passes
  - `ffmpeg -codecs` check passes

### 2.2 Optimization targets
- Runtime image size reduction target: at least 10% without functionality loss, or provide explicit justification if not achievable.
- Cold build-time reduction target: at least 15% on CI baseline, or provide explicit justification.
- Warm/cached build-time reduction target: at least 25% with BuildKit cache strategy.

### 2.3 Security and reproducibility gates
- No unresolved critical CVEs introduced by direct dependency changes.
- Dependency version policy documented (pinned vs range, and why).
- External downloads for installers/binaries have checksum/signature verification where practical.

### 2.4 Documentation gate (mandatory)
- Dockerfiles must receive thorough, stage-by-stage comments explaining:
  - Stage purpose
  - Inputs and outputs
  - Why a dependency group exists
  - Tradeoffs (size, performance, compatibility)
- Every nontrivial `RUN` block should include intent-focused comments (reasoning, not just command restatement).

## 3) Tools and Data Collection

### 3.1 Static and linting tools
- `hadolint` for Dockerfile quality and anti-pattern detection.
- `shellcheck` for shell scripts (`build-and-push-*`, `retag_and_push.sh`, `scripts/*`).
- `actionlint` and `yamllint` for GitHub Actions.

### 3.2 Dependency and security analysis
- `pip-audit` for Python dependency vulnerability review.
- `trivy image` (or `grype`) for container CVE scan.
- `syft` for SBOM generation before/after.
- `docker scout cves` (optional, if available in environment).

### 3.3 Size and layer analysis
- `docker history --no-trunc <image>` to identify heavy layers.
- `dive <image>` to inspect wasted bytes and layer composition.
- `docker image inspect` for final image size and metadata.

### 3.4 Build performance analysis
- `docker buildx build --progress=plain` with timing capture.
- Compare `--no-cache` and warm-cache builds.
- Inspect build cache hit rates in CI logs.

### 3.5 Runtime verification
- Existing scripts in `image_testing/`.
- Additional targeted import checks for crypto/web3/media stack.
- GPU runtime checks: CUDA availability, TensorRT Python import/version, minimal engine build.

## 4) Reference Sources to Verify “Latest Best Practice”
Use these sources during execution for version and compatibility checks:
- CUDA release notes: `https://docs.nvidia.com/cuda/cuda-toolkit-release-notes/index.html`
- TensorRT releases: `https://github.com/NVIDIA/TensorRT/releases`
- TensorRT support matrix: `https://docs.nvidia.com/deeplearning/tensorrt/support-matrix/index.html`
- PyTorch version/channel guidance: `https://pytorch.org/get-started/previous-versions/`
- OpenVINO release notes: `https://docs.openvino.ai/releasenotes`
- ONNX Runtime release servicing: `https://onnxruntime.ai/docs/reference/releases-servicing.html`
- FFmpeg releases: `https://ffmpeg.org/download.html`
- Docker build best practices: `https://docs.docker.com/build/building/best-practices/`
- Docker build cache optimization: `https://docs.docker.com/build/cache/optimize/`
- GitHub workflow syntax: `https://docs.github.com/en/actions/writing-workflows/workflow-syntax-for-github-actions`
- Docker build-push action docs: `https://github.com/docker/build-push-action`

## 5) Execution Plan by Workstream

### Workstream A: GPU image deep review and optimization (`base_edge_node_amd64_gpu/`)

#### A1. Version and compatibility audit
- Validate and document current vs latest for:
  - CUDA toolkit/runtime compatibility with selected Torch wheels
  - TensorRT apt libs vs `tensorrt-cu12-bindings`
  - cuDNN package strategy (`nvidia-cudnn-cu12`) vs transitive dependency behavior
  - FFmpeg version and required codecs
  - `cryptography`, `web3`, and GPU-critical Python dependencies
- Produce a compatibility table with tested combinations.

#### A2. Dependency necessity audit
- Classify each apt and pip package as:
  - Required runtime
  - Required build-time only
  - Optional by workload profile
  - Unused/dead weight
- Verify usage by grep/import scan plus runtime tests.
- Explicitly evaluate heavy inclusions: Docker Engine, Node.js, ngrok, developer utilities.

#### A3. Build and size optimization candidates
- Evaluate switching GPU runtime base to an NVIDIA CUDA runtime image vs current Ubuntu base + manual CUDA repo setup.
- Keep/build multi-stage strategy but reduce copied artifacts:
  - Copy only required FFmpeg runtime files instead of full `/usr/local` where possible.
  - Minimize Python runtime footprint with safe pruning policy.
- Introduce BuildKit cache mounts for apt/pip where safe.
- Review high-cost compile flags (`--enable-optimizations` CPython build) for build-time impact.

#### A4. Security and supply-chain hardening
- Replace or harden `curl | sh` and unauthenticated tarball flows using checksums/signatures where practical.
- Ensure apt key handling and repository pinning are deterministic.

#### A5. Validation and performance benchmark
- Run GPU image tests (`image_testing/test-gpu.sh`).
- Capture image size/build time deltas and publish before/after report.

### Workstream B: CPU image deep review and optimization (`base_edge_node_amd64_cpu/`)

#### B1. Version and compatibility audit
- Validate and document current vs latest for:
  - Python, Torch CPU wheel channel
  - ONNX / OpenVINO / ONNX Runtime OpenVINO compatibility
  - FFmpeg and codec stack
  - `cryptography`, `web3`, and other runtime libraries

#### B2. Dependency necessity audit
- Same classification model as GPU (required/optional/build-only/unused).
- Verify whether DIND stack is needed in CPU base or should be split into flavor variants.

#### B3. Build and size optimization candidates
- Re-evaluate CPython source-build strategy vs alternatives (while preserving compatibility and determinism).
- Apply pruning/strip strategy parity with GPU image where safe.
- Optimize layer composition and remove redundant runtime packages.

#### B4. Validation and benchmark
- Run CPU image tests (`image_testing/test-cpu.sh`).
- Collect build-time and size deltas with the same methodology as GPU.

### Workstream C: Workflow unpause and CI hardening (`.github/workflows/*.paused`)

#### C1. Unpause prerequisites
- Rename:
  - `base_edge_node_amd64_cpu.yaml.paused` -> `base_edge_node_amd64_cpu.yaml`
  - `base_edge_node_amd64_gpu.yaml.paused` -> `base_edge_node_amd64_gpu.yaml`
- Confirm repo-level Actions settings allow workflow execution.

#### C2. Trigger correctness
- Expand trigger paths to include all build inputs, at minimum:
  - `base_edge_node_amd64_cpu/**` or `base_edge_node_amd64_gpu/**`
  - `scripts/**`
  - relevant root scripts (`build-and-push-*`)
- Add `workflow_dispatch` for manual runs.

#### C3. Workflow modernization
- Update action versions to current supported majors (validate before final pin):
  - `actions/checkout`
  - `docker/build-push-action`
  - `docker/login-action`
  - `docker/setup-buildx-action`
- Add explicit `permissions` and `concurrency` controls.
- Add BuildKit cache strategy (`cache-from/cache-to`) for repeat builds.
- Validate whether `driver: cloud` + endpoint should remain or fallback to standard driver for reliability.

#### C4. CI/Manual parity
- Ensure workflow build args, tags, and retag behavior match manual scripts.
- Ensure both paths produce equivalent tags and metadata.

### Workstream D: Manual build-and-push scripts alignment

#### D1. Behavior alignment
- Align scripts with workflow behavior for:
  - build context and Dockerfile paths
  - build args
  - tagging and push order
  - retag invocation and error handling

#### D2. Reliability improvements
- Add explicit `--pull` and optional buildx mode.
- Add consistent logging and deterministic defaults.
- Add dry-run mode for safe validation.

#### D3. Contract definition
- Document environment variables accepted by scripts (e.g., `IMAGE_REPO`, `IMAGE_TAG`, optional `BUILD_ARGS`).
- Ensure scripts fail fast on missing prerequisites.

## 6) Detailed Commenting Plan for Dockerfiles (Mandatory)

### 6.1 Stage-level comment template
For each Dockerfile stage, add a header comment block:
- `Stage name`
- `Purpose`
- `Inputs (ARG/COPY)`
- `Outputs (artifacts copied to next stage)`
- `Why this design was chosen`
- `Main risks/constraints`

### 6.2 RUN block comment requirements
Before each meaningful `RUN` block, add comments describing:
- Why this package group exists
- Why the install method was chosen
- Whether dependencies are runtime or build-only
- Cleanup rationale and impact

### 6.3 Dependency rationale comments
- For non-obvious dependencies (e.g., DIND, web3, crypto, media codecs), include short rationale comments tied to supported workloads/tests.

### 6.4 Review criteria for comments
- Comments must explain intent and tradeoffs, not restate commands.
- Comment quality will be part of merge acceptance.

## 7) Measurement and Reporting Format

### 7.1 Baseline report artifacts
Generate for both CPU and GPU:
- Build time (cold/warm)
- Final image size
- Top 10 largest layers
- CVE summary (critical/high/medium)
- Test pass/fail summary

### 7.2 Change proposal scoring rubric
Score each proposed optimization across:
- Compatibility risk (low/med/high)
- Size impact
- Build-time impact
- Security impact
- Maintenance complexity

Only implement changes with net positive score and acceptable risk.

## 8) Suggested Execution Order
1. Baseline measurement and SBOM/CVE capture.
2. GPU version compatibility and dependency audit.
3. CPU version compatibility and dependency audit.
4. Draft optimization candidates and run A/B benchmarks.
5. Implement selected Dockerfile optimizations with mandatory comments.
6. Unpause and modernize workflows.
7. Align manual build scripts with CI.
8. Final validation run and publish before/after report.

## 9) Deliverables Expected from the Executing Agent
- Updated Dockerfiles (CPU/GPU) with optimization changes and thorough stage comments.
- Updated workflow files (unpaused and hardened).
- Updated manual build scripts aligned with workflows.
- Benchmark report (size/time/security/functionality deltas).
- Clear compatibility matrix documenting validated version combinations.
