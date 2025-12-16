# Upgrade and Refactor Plan (reviewed)
Target: modernize all base images while keeping per-arch repos intact, move to Ubuntu 24.04 + Python 3.13 where feasible, embed DinD into every image (reusing the existing entrypoint and `EE_DD` toggle), and align installs/tests with `uv pip`.

## 1) Scope and repository reality
- Actively target three images: `base_edge_node_amd64_gpu`, `base_edge_node_amd64_cpu`, and `base_edge_node_arm64_cpu` (Pi/arm64v8). Keep directories/tags stable; tags should follow the existing scheme (pyX.Y.Z-thA.B.C-trD.E.F) without arch in the tag, since the repo already encodes arch.
- All active images should start from `ubuntu:24.04` (or `arm64v8/ubuntu:24.04`) with Python 3.13 layered on top.
- DinD must be integrated into every active image (not a separate image), but the current `base_edge_node_dind/entrypoint.sh` and the `EE_DD` environment flag must be preserved verbatim as the opt-in switch for privileged docker-in-docker mode.

## 2) Python 3.13 feasibility and installer changes
- Ubuntu 24.04 ships Python 3.12; Python 3.13 is not in apt yet. Plan to compile 3.13 or use a builder stage with `uv python install 3.13` and copy it in. Expect longer build times and extra build deps; keep a build arg to temporarily fall back to 3.12 if wheels are missing.
- Assume current releases (torch/torchvision/torchaudio, transformers, tokenizers, tensorrt, flash-attn, bitsandbytes) all publish cp313 wheels and are compatible. Treat 3.13 as the default target; keep a guarded fallback to 3.12 only if build-time validation surfaces a gap.
- Replace all `pip install`/venv usage with `uv pip install --system --no-cache --no-compile ...` (including `--extra-index-url` for torch). No virtualenvs are needed; drop the venv created in `Dockerfile_cpu`.

## 3) Core package versions and compatibility guardrails
- PyTorch: assume cp313 wheels (CPU and cu124) are available at current versions (e.g., torch 2.9.x + cu124, matching torchvision/torchaudio). Use 3.13 as default; keep a build arg to fall back to 3.12 if a wheel is missing for a specific arch/variant.
- Transformers/tokenizers: assume latest releases (e.g., transformers 4.57.x+, tokenizers 0.22.x) ship cp313 wheels. Default to these on Python 3.13; only pin down or fall back to 3.12 if validation shows gaps.
- Bitsandbytes/flash-attn: both are CUDA-only and currently limited to specific Python/CUDA combos (generally Py<=3.11). Keep them behind build args per arch; disable when Python 3.13 is enabled or when the target SM/CUDA pair lacks wheels.
- TensorRT: the existing pin (`tensorrt==8.6.1`) only supports older Python versions. TRT 10.x PyPI targets Py3.11 + CUDA 12.x; no Py3.13 wheels yet. For amd64 GPU, gate TRT behind a build arg and default to off until a matching wheel is confirmed. CPU images should omit TRT.
- ffmpeg: stop building from git head; pin to a released version (6.1.1 or 7.0.x) via a shared multi-stage builder. Trim codecs for Pi to reduce heat/size. Ensure dev deps are purged to keep layers small and consistent across arches.
- Node/ngrok: keep Node 20 LTS (or 22 if 24.04 apt is preferred) and retain the arch-specific ngrok tarballs already used.

## 4) DinD integration requirements
- Install Docker CE (27/28) + `fuse-overlayfs` + `uidmap` inside every image, set `DOCKER_TLS_CERTDIR=/certs`, and keep `EE_DD` as the switch to launch dockerd. The preserved `entrypoint.sh` must remain the dockerd launcher; the normal app entrypoint should stay available when `EE_DD=false`.
- Verify overlayfs availability per arch; document the requirement and allow a non-DinD path when missing.
- After all images embed DinD, keep a compatibility tag for users expecting `ratio1/base_edge_node_dind:*` but avoid maintaining a duplicate Dockerfile.

## 5) Architecture-specific guidance
- amd64 GPU: base `ubuntu:24.04`, CUDA 12.4 wheels, torch 2.9.x + cu124 (cp313 assumed), transformers 4.57.x+ + tokenizers 0.22.x (cp313 assumed), ffmpeg 6.1.1/7.0.x builder. Default to Python 3.13; keep a fallback to 3.12 only if validation shows missing wheels.
- amd64 CPU: base `ubuntu:24.04`, torch 2.9.x CPU wheels (cp313 assumed) with current transformers/tokenizers on 3.13; fall back to 3.12 only on validation failures. Remove the venv, keep installs system-wide via `uv pip --system`.
- arm64 CPU (Pi): base `arm64v8/ubuntu:24.04`, torch 2.9.x CPU wheels (cp313 assumed for aarch64), slim ffmpeg (drop heavy codecs), and the same transformers/tokenizers pins on 3.13; fall back to 3.12 only if aarch64 cp313 wheels are missing.

## 6) Tests and platform detection updates
- Update `test_image.sh` scripts to auto-detect the host arch (`uname -m` and `docker info --format '{{.Architecture}}'`) and run only the matching tests. Skip GPU checks unless `nvidia-smi`/`--gpus all` is available; skip arm64 nested runs on amd64 hosts unless QEMU is configured.
- Keep nested Docker smoke tests behind `SKIP_NESTED`; require `/var/run/docker.sock` or start the image with `EE_DD=true` to exercise the embedded dockerd.
- Assert versions in tests (torch/transformers/ffmpeg) instead of only printing them, and include a quick `uv pip check` to validate the installer switch.

## 7) CI/CD refactor
- Use a single buildx matrix over the existing directories (no renames) with arch-aware tags. Include `UV_CACHE_DIR` to speed installs.
- Gate runtime GPU tests to hardware runners; CI on amd64 should run only amd64 CPU/GPU smoke tests. Cross-built arm64 jobs should stop after import/ffmpeg smoke unless a device runner is available.
- Replace manual retag scripts with metadata action tags but keep the legacy tag names for compatibility.

## 8) Execution sequence
1. Add shared snippets for `uv` installation, Python 3.13 builder/copy, and the DinD entrypoint reuse. Update AGENTS.md accordingly.
2. Convert amd64 GPU/CPU Dockerfiles to Ubuntu 24.04 + `uv pip --system`, pin torch/transformers/ffmpeg, and embed DinD with the preserved entrypoint.
3. Port the arm64 CPU image to 24.04 with the same installer/version scheme and a trimmed ffmpeg stage.
4. Rewrite test scripts with platform detection and version assertions; ensure they honor `SKIP_NESTED` and `EE_DD`.
5. Refactor CI to the matrix layout, wiring the new tests and tags, and run staged builds per arch.

## 9) Risks and mitigations
- Python 3.13: proceeding under the assumption that current releases provide cp313 wheels across torch/transformers/tokenizers/CUDA and related deps. Keep a guarded fallback to 3.12 and add CI checks to fail fast if any arch/variant lacks cp313 wheels.
- DinD integration increases size and privilege needs; ensure overlayfs/iptables modules exist per arch and keep `EE_DD=false` as a safe default.
- ffmpeg source builds on 24.04 may be slower; use pinned releases and multi-stage builds to reduce timeouts and layer bloat.
- Cross-arch tests must not run the wrong nested images; enforce host-arch detection to avoid false failures.
