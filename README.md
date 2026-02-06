# Ratio1 Edge Node Base Images
This repository maintains segregated base images for Ratio1 Edge Node containers, split by architecture and accelerator profile.

## Objective
- Keep CPU and GPU image families isolated so dependency/runtime choices remain explicit per target.
- Enable independent build, tagging, validation, and release flows for each image family.
- Track production-ready recipes separately from experimental and archived variants.
- Preserve architecture segregation across generations: active `amd64` lines in root, historical `arm64/tegra` lines in `_archive/`.

## Repository Layout
- `base_edge_node_amd64_cpu/`: production AMD64 CPU base image.
- `base_edge_node_amd64_gpu/`: production AMD64 GPU base image (CUDA/TensorRT stack).
- `scripts/`: shared helpers used by image builds (`build-ffmpeg.sh`, `entrypoint.sh`).
- `image_testing/`: CPU/GPU validation suites.
- `xperimental/`: experimental image variants (not production baseline).
- `_archive/`: historical image layouts (including arm64/tegra/dind generations).

## Image Matrix
- `ratio1/base_edge_node_amd64_cpu`: AMD64 CPU runtime for edge node services and model inference.
- `ratio1/base_edge_node_amd64_gpu`: AMD64 NVIDIA GPU runtime with TensorRT-capable stack.
- `xperimental/*`: candidate variants under evaluation.
- `_archive/*`: deprecated or superseded definitions preserved for reference.

## Build, Push, Retag
```bash
# Build locally
docker build -f base_edge_node_amd64_cpu/Dockerfile -t ratio1/base_edge_node_amd64_cpu:latest .
docker build -f base_edge_node_amd64_gpu/Dockerfile -t ratio1/base_edge_node_amd64_gpu:latest .

# Build + push + retag
./build-and-push-amd64-cpu.sh
./build-and-push-amd64-gpu.sh

# Retag existing latest images
(cd base_edge_node_amd64_cpu && ./retag_and_push.sh ratio1/base_edge_node_amd64_cpu:latest)
(cd base_edge_node_amd64_gpu && ./retag_and_push.sh ratio1/base_edge_node_amd64_gpu:latest)
```

## Tagging Conventions
- CPU tags: `py<major.minor>-th<major.minor>-ox<major.minor>-tr<major.minor>`
- GPU tags: `py<major.minor>-th<major.minor>-cu<major.minor>-trt<major.minor>-tr<major.minor>`

## Validation
```bash
./image_testing/test-cpu.sh ratio1/base_edge_node_amd64_cpu:latest
./image_testing/test-gpu.sh ratio1/base_edge_node_amd64_gpu:latest
docker run --rm ratio1/base_edge_node_amd64_cpu:latest ffmpeg -codecs | head
docker run --rm ratio1/base_edge_node_amd64_gpu:latest ffmpeg -codecs | head
```

## Documentation Policy
- `AGENTS.md` is the living operations contract for this repo.
- Critical horizontal changes must update both `AGENTS.md` and `README.md` in the same change set.
- Horizontal changes include architecture coverage, core runtime stack, build/release workflow, tag schema, and validation contract.

## Citation
```bibtex
@misc{base_images,
  title  = {Ratio1 -- Base Images for Edge Node},
  author = {Traian Ispir and Andrei Damian and Cristian Bleotiu},
  year   = {2024},
  url    = {https://github.com/Ratio1/base_images}
}

@misc{damian2025ratio1aimetaos,
  title        = {Ratio1 -- AI meta-OS},
  author       = {Andrei Damian and Petrica Butusina and Alessandro De Franceschi and Vitalii Toderian and Marius Grigoras and Cristian Bleotiu},
  DOI          = {10.48550/ARXIV.2509.12223},
  year         = {2025},
  eprint       = {2509.12223},
  archivePrefix= {arXiv},
  primaryClass = {cs.OS},
  url          = {https://arxiv.org/abs/2509.12223}
}

@inproceedings{Damian_2025,
  title      = {Ratio1 meta-OS - decentralized MLOps and beyond},
  url        = {http://dx.doi.org/10.1109/cscs66924.2025.00046},
  DOI        = {10.1109/cscs66924.2025.00046},
  booktitle  = {2025 25th International Conference on Control Systems and Computer Science (CSCS)},
  publisher  = {IEEE},
  author     = {Damian, Andrei Ionut and Bleotiu, Cristian and Grigoras, Marius and Butusina, Petrica and De Franceschi, Alessandro and Toderian, Vitalii and Tapus, Nicolae},
  year       = {2025},
  month      = {may},
  pages      = {258--265}
}
```
