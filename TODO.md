# TODO list for future base images refactoring
## Any of these may change the base image(which is preferred to be done as rarely as possible)

- maybe unify `base_edge_node` and the rest of base images using some environment variables
- in `base_edge_node_cpu` check if it necessary to install python 3.10 and the go through
the process of having a virtual environment, since ubuntu 22.04 already has python 3.10
(maybe only get python-pip and python-dev)
- in `base_edge_node_cpu` maybe keep curl
- in `base_edge_node_cpu` maybe change workdir to ai_edge_node
- in all images check if it is necessary to purge git the first time(since it is reinstalled later) or at all
- in `base_edge_node_cpu` check if the cache should be removed similarly to the gpu version(rm -rf /root/.cache)
- check if 'build_ffmpeg.sh' needs to be in 3 different base images
- `retag_and_push_arm64_tegra.sh` needs to be tested on arm64 architecture(github actions uses x86)
- maybe review 'Cleanup space' section in `.github/workflows` files
- maybe add "RUN sed -i 's/\r$//' build-ffmpeg.sh" in base_edge_node/Dockerfile for windows image building