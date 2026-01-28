# Debug Results - Wed Jan 28 17:16:20 EET 2026

## Scope
- Image: ratio1/base_edge_node_amd64_cpu:py3.13.11-th2.9.1-cpu
- Command: ./image_testing/test-cpu.sh ratio1/base_edge_node_amd64_cpu:py3.13.11-th2.9.1-cpu
- Host: Linux TILaptop 6.6.87.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun  5 18:30:46 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux

## Results
- CPU test: FAIL (dind hello-world)

## Logs
TLS environment detected. Generating certs...
Certificate request self-signature ok
subject=CN = R1-dind server
/certs/server/cert.pem: OK
Certificate request self-signature ok
subject=CN = R1-dind client
/certs/client/cert.pem: OK
iptables v1.8.10 (nf_tables)
Launching dockerd in the background...
Waiting for dockerd to respond...
time="2026-01-28T15:16:25.796542841Z" level=info msg="Starting up"
time="2026-01-28T15:16:25.806495825Z" level=info msg="containerd not running, starting managed containerd"
time="2026-01-28T15:16:25.809406084Z" level=info msg="started new containerd process" address=/var/run/docker/containerd/containerd.sock module=libcontainerd pid=64
time="2026-01-28T15:16:25.848961489Z" level=info msg="starting containerd" revision=dea7da592f5d1d2b7755e3a161be07f43fad8f75 version=v2.2.1
time="2026-01-28T15:16:25.864562691Z" level=warning msg="Configuration migrated from version 2, use `containerd config migrate` to avoid migration" t="10.67µs"
time="2026-01-28T15:16:25.864668760Z" level=info msg="loading plugin" id=io.containerd.content.v1.content type=io.containerd.content.v1
time="2026-01-28T15:16:25.864893989Z" level=info msg="loading plugin" id=io.containerd.image-verifier.v1.bindir type=io.containerd.image-verifier.v1
time="2026-01-28T15:16:25.865008755Z" level=info msg="loading plugin" id=io.containerd.internal.v1.opt type=io.containerd.internal.v1
time="2026-01-28T15:16:25.870844131Z" level=info msg="loading plugin" id=io.containerd.warning.v1.deprecations type=io.containerd.warning.v1
time="2026-01-28T15:16:25.871136592Z" level=info msg="loading plugin" id=io.containerd.mount-handler.v1.erofs type=io.containerd.mount-handler.v1
time="2026-01-28T15:16:25.871177977Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.blockfile type=io.containerd.snapshotter.v1
time="2026-01-28T15:16:25.871988963Z" level=info msg="skip loading plugin" error="no scratch file generator: skip plugin" id=io.containerd.snapshotter.v1.blockfile type=io.containerd.snapshotter.v1
time="2026-01-28T15:16:25.872056657Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.btrfs type=io.containerd.snapshotter.v1
time="2026-01-28T15:16:25.872732518Z" level=info msg="skip loading plugin" error="path /var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.btrfs (overlay) must be a btrfs filesystem to be used with the btrfs snapshotter: skip plugin" id=io.containerd.snapshotter.v1.btrfs type=io.containerd.snapshotter.v1
time="2026-01-28T15:16:25.872799490Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.devmapper type=io.containerd.snapshotter.v1
time="2026-01-28T15:16:25.872815723Z" level=info msg="skip loading plugin" error="devmapper not configured: skip plugin" id=io.containerd.snapshotter.v1.devmapper type=io.containerd.snapshotter.v1
time="2026-01-28T15:16:25.872824187Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.erofs type=io.containerd.snapshotter.v1
time="2026-01-28T15:16:25.873397949Z" level=info msg="skip loading plugin" error="EROFS unsupported, please `modprobe erofs`: skip plugin" id=io.containerd.snapshotter.v1.erofs type=io.containerd.snapshotter.v1
time="2026-01-28T15:16:25.873450734Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.native type=io.containerd.snapshotter.v1
time="2026-01-28T15:16:25.874281496Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.overlayfs type=io.containerd.snapshotter.v1
time="2026-01-28T15:16:25.875738173Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.zfs type=io.containerd.snapshotter.v1
time="2026-01-28T15:16:25.875847969Z" level=info msg="skip loading plugin" error="lstat /var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.zfs: no such file or directory: skip plugin" id=io.containerd.snapshotter.v1.zfs type=io.containerd.snapshotter.v1
time="2026-01-28T15:16:25.875858863Z" level=info msg="loading plugin" id=io.containerd.event.v1.exchange type=io.containerd.event.v1
time="2026-01-28T15:16:25.875970457Z" level=info msg="loading plugin" id=io.containerd.monitor.task.v1.cgroups type=io.containerd.monitor.task.v1
time="2026-01-28T15:16:25.876350450Z" level=info msg="loading plugin" id=io.containerd.metadata.v1.bolt type=io.containerd.metadata.v1
time="2026-01-28T15:16:25.876787209Z" level=info msg="metadata content store policy set" policy=shared
time="2026-01-28T15:16:25.890073935Z" level=info msg="loading plugin" id=io.containerd.gc.v1.scheduler type=io.containerd.gc.v1
time="2026-01-28T15:16:25.890216364Z" level=info msg="loading plugin" id=io.containerd.nri.v1.nri type=io.containerd.nri.v1
time="2026-01-28T15:16:25.890284645Z" level=info msg="built-in NRI default validator is disabled"
time="2026-01-28T15:16:25.890290207Z" level=info msg="runtime interface created"
time="2026-01-28T15:16:25.890293323Z" level=info msg="created NRI interface"
time="2026-01-28T15:16:25.890300987Z" level=info msg="loading plugin" id=io.containerd.differ.v1.erofs type=io.containerd.differ.v1
time="2026-01-28T15:16:25.890480291Z" level=info msg="skip loading plugin" error="failed to check mkfs.erofs availability: failed to run mkfs.erofs --help: exec: \"mkfs.erofs\": executable file not found in $PATH: skip plugin" id=io.containerd.differ.v1.erofs type=io.containerd.differ.v1
time="2026-01-28T15:16:25.890512051Z" level=info msg="loading plugin" id=io.containerd.differ.v1.walking type=io.containerd.differ.v1
time="2026-01-28T15:16:25.891448577Z" level=info msg="loading plugin" id=io.containerd.lease.v1.manager type=io.containerd.lease.v1
time="2026-01-28T15:16:25.891901418Z" level=info msg="loading plugin" id=io.containerd.mount-manager.v1.bolt type=io.containerd.mount-manager.v1
time="2026-01-28T15:16:25.897309935Z" level=info msg="loading plugin" id=io.containerd.service.v1.containers-service type=io.containerd.service.v1
time="2026-01-28T15:16:25.897402513Z" level=info msg="loading plugin" id=io.containerd.service.v1.content-service type=io.containerd.service.v1
time="2026-01-28T15:16:25.897415615Z" level=info msg="loading plugin" id=io.containerd.service.v1.diff-service type=io.containerd.service.v1
time="2026-01-28T15:16:25.897431497Z" level=info msg="loading plugin" id=io.containerd.service.v1.images-service type=io.containerd.service.v1
time="2026-01-28T15:16:25.897442006Z" level=info msg="loading plugin" id=io.containerd.service.v1.introspection-service type=io.containerd.service.v1
time="2026-01-28T15:16:25.897451202Z" level=info msg="loading plugin" id=io.containerd.service.v1.namespaces-service type=io.containerd.service.v1
time="2026-01-28T15:16:25.897461369Z" level=info msg="loading plugin" id=io.containerd.service.v1.snapshots-service type=io.containerd.service.v1
time="2026-01-28T15:16:25.897469932Z" level=info msg="loading plugin" id=io.containerd.shim.v1.manager type=io.containerd.shim.v1
time="2026-01-28T15:16:25.897480657Z" level=info msg="loading plugin" id=io.containerd.runtime.v2.task type=io.containerd.runtime.v2
time="2026-01-28T15:16:25.898168743Z" level=info msg="loading plugin" id=io.containerd.service.v1.tasks-service type=io.containerd.service.v1
time="2026-01-28T15:16:25.898224166Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.containers type=io.containerd.grpc.v1
time="2026-01-28T15:16:25.898237456Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.content type=io.containerd.grpc.v1
time="2026-01-28T15:16:25.898252990Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.diff type=io.containerd.grpc.v1
time="2026-01-28T15:16:25.898263343Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.events type=io.containerd.grpc.v1
time="2026-01-28T15:16:25.898271373Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.images type=io.containerd.grpc.v1
time="2026-01-28T15:16:25.898282080Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.introspection type=io.containerd.grpc.v1
time="2026-01-28T15:16:25.898289853Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.leases type=io.containerd.grpc.v1
time="2026-01-28T15:16:25.898310171Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.mounts type=io.containerd.grpc.v1
time="2026-01-28T15:16:25.898322916Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.namespaces type=io.containerd.grpc.v1
time="2026-01-28T15:16:25.898333753Z" level=info msg="loading plugin" id=io.containerd.sandbox.store.v1.local type=io.containerd.sandbox.store.v1
time="2026-01-28T15:16:25.898343034Z" level=info msg="loading plugin" id=io.containerd.transfer.v1.local type=io.containerd.transfer.v1
time="2026-01-28T15:16:25.898383149Z" level=info msg="loading plugin" id=io.containerd.cri.v1.images type=io.containerd.cri.v1
time="2026-01-28T15:16:25.898469153Z" level=info msg="Get image filesystem path \"/var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.overlayfs\" for snapshotter \"overlayfs\""
time="2026-01-28T15:16:25.898511168Z" level=info msg="Start snapshots syncer"
time="2026-01-28T15:16:25.898579776Z" level=info msg="loading plugin" id=io.containerd.cri.v1.runtime type=io.containerd.cri.v1
time="2026-01-28T15:16:25.899380861Z" level=info msg="starting cri plugin" config="{\"containerd\":{\"defaultRuntimeName\":\"runc\",\"runtimes\":{\"runc\":{\"runtimeType\":\"io.containerd.runc.v2\",\"runtimePath\":\"\",\"PodAnnotations\":null,\"ContainerAnnotations\":null,\"options\":{\"BinaryName\":\"\",\"CriuImagePath\":\"\",\"CriuWorkPath\":\"\",\"IoGid\":0,\"IoUid\":0,\"NoNewKeyring\":false,\"Root\":\"\",\"ShimCgroup\":\"\",\"SystemdCgroup\":false},\"privileged_without_host_devices\":false,\"privileged_without_host_devices_all_devices_allowed\":false,\"cgroupWritable\":false,\"baseRuntimeSpec\":\"\",\"cniConfDir\":\"\",\"cniMaxConfNum\":0,\"snapshotter\":\"\",\"sandboxer\":\"podsandbox\",\"io_type\":\"\"}},\"ignoreBlockIONotEnabledErrors\":false,\"ignoreRdtNotEnabledErrors\":false},\"cni\":{\"binDir\":\"\",\"binDirs\":[\"/opt/cni/bin\"],\"confDir\":\"/etc/cni/net.d\",\"maxConfNum\":1,\"setupSerially\":false,\"confTemplate\":\"\",\"ipPref\":\"\",\"useInternalLoopback\":false},\"enableSelinux\":false,\"selinuxCategoryRange\":1024,\"maxContainerLogLineSize\":16384,\"disableApparmor\":false,\"restrictOOMScoreAdj\":false,\"disableProcMount\":false,\"unsetSeccompProfile\":\"\",\"tolerateMissingHugetlbController\":true,\"disableHugetlbController\":true,\"device_ownership_from_security_context\":false,\"ignoreImageDefinedVolumes\":false,\"netnsMountsUnderStateDir\":false,\"enableUnprivilegedPorts\":true,\"enableUnprivilegedICMP\":true,\"enableCDI\":true,\"cdiSpecDirs\":[\"/etc/cdi\",\"/var/run/cdi\"],\"drainExecSyncIOTimeout\":\"0s\",\"ignoreDeprecationWarnings\":null,\"containerdRootDir\":\"/var/lib/docker/containerd/daemon\",\"containerdEndpoint\":\"/var/run/docker/containerd/containerd.sock\",\"rootDir\":\"/var/lib/docker/containerd/daemon/io.containerd.grpc.v1.cri\",\"stateDir\":\"/var/run/docker/containerd/daemon/io.containerd.grpc.v1.cri\"}"
time="2026-01-28T15:16:25.899579148Z" level=info msg="loading plugin" id=io.containerd.podsandbox.controller.v1.podsandbox type=io.containerd.podsandbox.controller.v1
time="2026-01-28T15:16:25.899858211Z" level=info msg="loading plugin" id=io.containerd.sandbox.controller.v1.shim type=io.containerd.sandbox.controller.v1
time="2026-01-28T15:16:25.900855583Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.sandbox-controllers type=io.containerd.grpc.v1
time="2026-01-28T15:16:25.900921286Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.sandboxes type=io.containerd.grpc.v1
time="2026-01-28T15:16:25.900933244Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.snapshots type=io.containerd.grpc.v1
time="2026-01-28T15:16:25.900964738Z" level=info msg="loading plugin" id=io.containerd.streaming.v1.manager type=io.containerd.streaming.v1
time="2026-01-28T15:16:25.900980255Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.streaming type=io.containerd.grpc.v1
time="2026-01-28T15:16:25.900989928Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.tasks type=io.containerd.grpc.v1
time="2026-01-28T15:16:25.900999559Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.transfer type=io.containerd.grpc.v1
time="2026-01-28T15:16:25.901013541Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.version type=io.containerd.grpc.v1
time="2026-01-28T15:16:25.901038710Z" level=info msg="loading plugin" id=io.containerd.monitor.container.v1.restart type=io.containerd.monitor.container.v1
time="2026-01-28T15:16:25.901146502Z" level=info msg="loading plugin" id=io.containerd.tracing.processor.v1.otlp type=io.containerd.tracing.processor.v1
time="2026-01-28T15:16:25.901190747Z" level=info msg="skip loading plugin" error="skip plugin: tracing endpoint not configured" id=io.containerd.tracing.processor.v1.otlp type=io.containerd.tracing.processor.v1
time="2026-01-28T15:16:25.901200732Z" level=info msg="loading plugin" id=io.containerd.internal.v1.tracing type=io.containerd.internal.v1
time="2026-01-28T15:16:25.901212038Z" level=info msg="skip loading plugin" error="skip plugin: tracing endpoint not configured" id=io.containerd.internal.v1.tracing type=io.containerd.internal.v1
time="2026-01-28T15:16:25.901218717Z" level=info msg="loading plugin" id=io.containerd.ttrpc.v1.otelttrpc type=io.containerd.ttrpc.v1
time="2026-01-28T15:16:25.901227826Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.healthcheck type=io.containerd.grpc.v1
time="2026-01-28T15:16:25.901690952Z" level=info msg=serving... address=/var/run/docker/containerd/containerd-debug.sock
time="2026-01-28T15:16:25.902073981Z" level=info msg=serving... address=/var/run/docker/containerd/containerd.sock.ttrpc
time="2026-01-28T15:16:25.902348285Z" level=info msg=serving... address=/var/run/docker/containerd/containerd.sock
time="2026-01-28T15:16:25.902394120Z" level=info msg="containerd successfully booted in 0.056311s"
time="2026-01-28T15:16:25.912544996Z" level=info msg="OTEL tracing is not configured, using no-op tracer provider"
time="2026-01-28T15:16:25.912873190Z" level=info msg="CDI directory does not exist, skipping: failed to monitor for changes: no such file or directory" dir=/etc/cdi
time="2026-01-28T15:16:25.912905037Z" level=info msg="CDI directory does not exist, skipping: failed to monitor for changes: no such file or directory" dir=/var/run/cdi
time="2026-01-28T15:16:25.943337274Z" level=info msg="Creating a containerd client" address=/var/run/docker/containerd/containerd.sock timeout=1m0s
time="2026-01-28T15:16:25.970905691Z" level=info msg="Loading containers: start."
time="2026-01-28T15:16:25.971057334Z" level=info msg="NRI is disabled"
time="2026-01-28T15:16:25.971070535Z" level=info msg="Starting daemon with containerd snapshotter integration enabled"
time="2026-01-28T15:16:25.975793592Z" level=info msg="Restoring containers: start."
time="2026-01-28T15:16:26.018212716Z" level=info msg="Deleting nftables IPv4 rules" error="exit status 1"
time="2026-01-28T15:16:26.054154895Z" level=info msg="Deleting nftables IPv6 rules" error="exit status 1"
time="2026-01-28T15:16:26.424871799Z" level=info msg="Loading containers: done."
time="2026-01-28T15:16:26.435790077Z" level=info msg="Docker daemon" commit=9c62384 containerd-snapshotter=true storage-driver=overlayfs version=29.2.0
time="2026-01-28T15:16:26.436119580Z" level=info msg="Initializing buildkit"
time="2026-01-28T15:16:26.459108808Z" level=info msg="Completed buildkit initialization"
time="2026-01-28T15:16:26.462761733Z" level=info msg="Daemon has completed initialization"
time="2026-01-28T15:16:26.462966706Z" level=info msg="API listen on /var/run/docker.sock"
time="2026-01-28T15:16:26.463002849Z" level=info msg="API listen on [::]:2376"
dockerd is now running.
time="2026-01-28T15:16:56.178313680Z" level=info msg="image pulled" digest="sha256:05813aedc15fb7b4d732e1be879d3252c1c9c25d885824f6295cab4538cb85cd" remote="docker.io/library/hello-world:latest"
time="2026-01-28T15:16:56.353599867Z" level=error msg="Error saving dying container to disk: invalid output path: stat /var/lib/docker/containers/f712763eb54e3ffd7b89f3f5388d561c64a48a766894edb127724756621bfb4f: no such file or directory"
time="2026-01-28T15:16:56.354408979Z" level=error msg="Handler for POST /v1.53/containers/create returned error: failed to mount /tmp/containerd-mount190509172: mount source: \"overlay\", target: \"/tmp/containerd-mount190509172\", fstype: overlay, flags: 0, data: \"workdir=/var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.overlayfs/snapshots/2/work,upperdir=/var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.overlayfs/snapshots/2/fs,lowerdir=/var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.overlayfs/snapshots/1/fs,index=off\", err: invalid argument"
time="2026-01-28T15:16:57.630087797Z" level=info msg="image pulled" digest="sha256:05813aedc15fb7b4d732e1be879d3252c1c9c25d885824f6295cab4538cb85cd" remote="docker.io/library/hello-world:latest"
time="2026-01-28T15:16:57.829531700Z" level=error msg="Error saving dying container to disk: invalid output path: stat /var/lib/docker/containers/2b16bac2b94ba1132035bbe2577678d171aa26cb364db6fa1ed7ed4a670ddbbe: no such file or directory"
time="2026-01-28T15:16:57.830242151Z" level=error msg="Handler for POST /v1.53/containers/create returned error: failed to mount /tmp/containerd-mount3909361867: mount source: \"overlay\", target: \"/tmp/containerd-mount3909361867\", fstype: overlay, flags: 0, data: \"workdir=/var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.overlayfs/snapshots/3/work,upperdir=/var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.overlayfs/snapshots/3/fs,lowerdir=/var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.overlayfs/snapshots/1/fs,index=off\", err: invalid argument"
========================================
====== Running CPU image test... =======
========================================
== torch ==
torch=2.9.1+cpu
model_shape=batch=256, in=1024, hidden=2048, out=1024, layers=3
== environment ==
python=3.13.11
platform=Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.39
threads_env={'CPU_TEST_THREADS': None, 'OMP_NUM_THREADS': None, 'MKL_NUM_THREADS': None, 'NUMEXPR_NUM_THREADS': None}
torch_threads=8
torch_interop_threads=7
torch_set_threads=8
== torchscript ==
torchscript max_abs_diff=0
== onnx / onnxruntime ==
onnxruntime=1.23.0
onnxruntime max_abs_diff=2.08616e-07
== openvino ==
openvino=2025.1.0-18503-6fec06580ab-releases/2025/1
openvino max_abs_diff=4.14439e-07
== speed (ms/iter) ==
torchscript_median_ms=43.071 torchscript_p95_ms=59.975 torchscript_mean_ms=42.308 torchscript_iters=142 torchscript_throughput=6048.6/s
onnxruntime_median_ms=34.463 onnxruntime_p95_ms=43.148 onnxruntime_mean_ms=35.308 onnxruntime_iters=170 onnxruntime_throughput=7248.1/s
openvino_median_ms=37.875 openvino_p95_ms=42.501 openvino_mean_ms=38.258 openvino_iters=157 openvino_throughput=6689.9/s
OK
== dind hello-world ==
docker run failed; collecting diagnostics...
== dind diagnostics ==
dind_env={'EE_DD': '1', 'DOCKER_TLS_CERTDIR': '/certs', 'DOCKER_HOST': None, 'DOCKER_DRIVER': None}
Storage Driver: overlayfs
Cgroup Version: 2
Kernel Version: 6.6.87.2-microsoft-standard-WSL2
Operating System: Ubuntu 24.04.3 LTS
$ docker version
Client: Docker Engine - Community
 Version:           29.2.0
 API version:       1.53
 Go version:        go1.25.6
 Git commit:        0b9d198
 Built:             Mon Jan 26 19:27:07 2026
 OS/Arch:           linux/amd64
 Context:           default

Server: Docker Engine - Community
 Engine:
  Version:          29.2.0
  API version:      1.53 (minimum version 1.44)
  Go version:       go1.25.6
  Git commit:       9c62384
  Built:            Mon Jan 26 19:27:07 2026
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          v2.2.1
  GitCommit:        dea7da592f5d1d2b7755e3a161be07f43fad8f75
 runc:
  Version:          1.3.4
  GitCommit:        v1.3.4-0-gd6d73eb8
 docker-init:
  Version:          0.19.0
  GitCommit:        de40ad0
$ uname -a
Linux afd207d159c2 6.6.87.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun  5 18:30:46 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
docker run failed:
docker: Error response from daemon: failed to mount /tmp/containerd-mount3909361867: mount source: "overlay", target: "/tmp/containerd-mount3909361867", fstype: overlay, flags: 0, data: "workdir=/var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.overlayfs/snapshots/3/work,upperdir=/var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.overlayfs/snapshots/3/fs,lowerdir=/var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.overlayfs/snapshots/1/fs,index=off", err: invalid argument

Run 'docker run --help' for more information

## Diagnostics

######## Extra non-python diagnostics: #########
EE_DD not set - skipping docker daemon initialization
platform Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.39
torch 2.9.1+cpu
onnxruntime 1.23.0
openvino 2025.1.0-18503-6fec06580ab-releases/2025/1
########## Done extra non-python diagnostics ##########
EE_DD not set - skipping docker daemon initialization
Client: Docker Engine - Community
 Version:    29.2.0
 Context:    default
 Debug Mode: false

Server:
######## DIND follow-up diagnostics (docker version / uname) #########
EE_DD not set - skipping docker daemon initialization
Client: Docker Engine - Community
 Version:           29.2.0
 API version:       1.53
 Go version:        go1.25.6
 Git commit:        0b9d198
 Built:             Mon Jan 26 19:27:07 2026
 OS/Arch:           linux/amd64
 Context:           default
----
EE_DD not set - skipping docker daemon initialization
Linux 4a2341081e42 6.6.87.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun  5 18:30:46 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
########## Done DIND follow-up diagnostics ##########
######## DIND diagnostics (stderr captured) #########
EE_DD not set - skipping docker daemon initialization
Client: Docker Engine - Community
 Version:    29.2.0
 Context:    default
 Debug Mode: false

Server:
failed to connect to the docker API at unix:///var/run/docker.sock; check if the path is correct and if the daemon is running: dial unix /var/run/docker.sock: connect: no such file or directory
EE_DD not set - skipping docker daemon initialization
Client: Docker Engine - Community
 Version:           29.2.0
 API version:       1.53
 Go version:        go1.25.6
 Git commit:        0b9d198
 Built:             Mon Jan 26 19:27:07 2026
 OS/Arch:           linux/amd64
 Context:           default
failed to connect to the docker API at unix:///var/run/docker.sock; check if the path is correct and if the daemon is running: dial unix /var/run/docker.sock: connect: no such file or directory
EE_DD not set - skipping docker daemon initialization
Linux 80e8f310156e 6.6.87.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun  5 18:30:46 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux
########## Done DIND diagnostics (stderr captured) ##########

## Root cause analysis
- DIND `hello-world` failed with `failed to mount ... fstype: overlay ... err: invalid argument` (see Logs).
- Inference: the inner Docker daemon is using OverlayFS with an upper layer on a filesystem that does not meet OverlayFS requirements (upper must support `trusted.*`/`user.*` xattrs and provide valid `d_type` in `readdir`). In nested containers, the upperdir often resides on an overlayfs mount, which can violate these requirements and trigger EINVAL. Source: https://www.kernel.org/doc/html/latest/filesystems/overlayfs.html

## Proposed fixes
1) Configure DIND to use the `vfs` storage driver (`DOCKER_DRIVER=vfs` or daemon.json). Docker docs note `vfs` is intended for testing / when no copy-on-write filesystem can be used and works in every environment (slower). Sources: https://docs.docker.com/engine/storage/drivers/select-storage-driver/ and https://docs.docker.com/engine/storage/drivers/vfs-driver/
2) Use `fuse-overlayfs` where available (e.g., install and set `DOCKER_DRIVER=fuse-overlayfs`). Docker docs note it’s preferred when `overlay2` isn’t supported (especially rootless) and works on any filesystem. Source: https://docs.docker.com/engine/storage/drivers/select-storage-driver/
3) Ensure `/var/lib/docker` inside DIND is backed by a compatible filesystem (e.g., ext4/xfs with required features) instead of overlayfs-on-overlayfs; this aligns with OverlayFS upper-layer requirements and Docker backing filesystem guidance. Sources: https://www.kernel.org/doc/html/latest/filesystems/overlayfs.html and https://docs.docker.com/engine/storage/drivers/select-storage-driver/

## Retest results
- Not retested; no changes applied.
