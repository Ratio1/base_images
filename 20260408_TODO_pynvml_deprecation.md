# TODO: Fix pynvml deprecation warning in base images

## Date
2026-04-08

## Priority
Low (warning only, no functional impact yet)

## Problem

When PyTorch initializes CUDA on the edge node, it emits this warning:

```
/opt/python/lib/python3.13/site-packages/torch/cuda/__init__.py:63: FutureWarning:
The pynvml package is deprecated. Please install nvidia-ml-py instead.
If you did not install pynvml directly, please report this to the maintainers
of the package that installed pynvml for you.
    import pynvml  # type: ignore[import]
```

Observed in container `dvi-1` running the R1FS Manager API plugin on the Python 3.13 base image.

## Root cause

The base images correctly install `nvidia-ml-py>=11.4` (the modern replacement). However, a transitive dependency in the pip dependency chain also installs the old `pynvml` package. When both are present, PyTorch's `torch/cuda/__init__.py` imports `pynvml` and triggers the deprecation warning because it detects the old package.

Both packages expose the same `pynvml` Python module, but the deprecated `pynvml` PyPI package shadows the `nvidia-ml-py` one when both are installed.

## Affected files

- `base_edge_node_amd64_cpu/requirements.txt` (line 5: `nvidia-ml-py>=11.4`)
- `base_edge_node_amd64_gpu/requirements.txt` (line 3: `nvidia-ml-py>=11.4`)
- `base_edge_node_amd64_cpu/Dockerfile` (pip install step)
- `base_edge_node_amd64_gpu/Dockerfile` (pip install step)

## Proposed fix

After the pip install step in both Dockerfiles, add an explicit uninstall of the deprecated `pynvml` package:

```dockerfile
# Remove deprecated pynvml if pulled in transitively (nvidia-ml-py provides the same module)
pip uninstall -y pynvml 2>/dev/null || true
```

Alternatively, add a pip constraint to prevent `pynvml` from being installed:

```
# In a constraints file or inline
--constraint "pynvml==0.0.0"  # force resolution failure for the old package
```

## Verification

After the fix, run inside the container:

```bash
python3 -c "import pynvml; print(pynvml.__file__)"
# Should point to nvidia-ml-py's pynvml, not the standalone pynvml package

pip list | grep -i nvml
# Should show nvidia-ml-py only, NOT pynvml
```

And confirm the warning no longer appears:

```bash
python3 -c "import torch; torch.cuda.is_available()"
# Should produce no FutureWarning about pynvml
```

## Investigation needed

- Identify which transitive dependency pulls in the old `pynvml` package (run `pip show pynvml` to check `Required-by`)
- If it's a direct dependency of something we install, file an issue upstream
