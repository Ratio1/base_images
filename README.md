# Base Images for Edge
Minimal, versioned Docker bases for GPU/CPU edge workloads.

## Layout at a Glance
- `base_edge_node/`: Ubuntu 22.04 GPU base with ffmpeg build, Torch/Transformers/TensorRT, ngrok; `Dockerfile_cpu` is CPU-only.
- `base_edge_node_arm64_cpu/`: Raspberry Pi–focused image with its own ffmpeg build script.
- `base_edge_node_arm64_tegra/`: Jetson/Tegra GPU base; `retag_and_push_arm64_tegra.sh` normalizes tags after cross-arch builds.
- `base_edge_node_dind/`: Docker-in-Docker layers (GPU and CPU) built atop edge node images; includes `entrypoint.sh`.

## Quick Start (build & tag)
```bash
# Edge node
docker build -t ratio1/base_edge_node:dev base_edge_node
docker build -f base_edge_node/Dockerfile_cpu -t ratio1/base_edge_node:cpu-dev base_edge_node
./base_edge_node/retag_and_push.sh ratio1/base_edge_node:dev             # retag by versions

# Arm64 variants
docker build -t ratio1/base_edge_node_arm64_cpu:dev base_edge_node_arm64_cpu
(cd base_edge_node_arm64_tegra && ./retag_and_push_arm64_tegra.sh <image>) # sets up qemu, retags, pushes

# Docker-in-Docker
docker build -t ratio1/base_edge_node_dind:dev base_edge_node_dind
```
Tag patterns: `<arch>-py<ver>-th<ver>-tr<ver>` for edge images.

## Validate Images (spot checks)
```bash
docker run --rm <img> python3 - <<'PY'
import torch, transformers, platform; print(platform.machine(), torch.__version__, transformers.__version__)
PY
docker run --rm <img> ffmpeg -codecs | head
docker run --privileged -e EE_DD=true ratio1/base_edge_node_dind:dev docker info
```

## Contributing Notes
- Keep Dockerfile layers compact (`&& \`), clean apt caches, and match existing pinned versions unless you must bump them.
- Scripts should use `#!/bin/bash`, `set -euo pipefail`, and quoted vars; keep them executable.
- Follow commit style seen in history (`fix: ...`, `chore: ...`). Update READMEs/AGENTS.md when workflows change.

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
