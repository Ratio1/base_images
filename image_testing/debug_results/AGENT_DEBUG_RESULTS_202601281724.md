# Debug Results - Wed Jan 28 17:24:40 EET 2026

## Scope
- Image: ratio1/base_edge_node_amd64_cpu:py3.13.11-th2.9.1-cpu
- Command: docker run --rm -e EE_DD=1 -e DOCKER_DRIVER=fuse-overlayfs --privileged -v /home/itn/WORK/r1/base_images/image_testing:/image_testing:ro ratio1/base_edge_node_amd64_cpu:py3.13.11-th2.9.1-cpu python3 /image_testing/cpu_image_test.py
- Host: Linux TILaptop 6.6.87.2-microsoft-standard-WSL2 #1 SMP PREEMPT_DYNAMIC Thu Jun  5 18:30:46 UTC 2025 x86_64 x86_64 x86_64 GNU/Linux

## Results
- CPU test: PASS

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
time="2026-01-28T15:24:44.885940796Z" level=info msg="Starting up"
time="2026-01-28T15:24:44.889530493Z" level=info msg="containerd not running, starting managed containerd"
time="2026-01-28T15:24:44.891664535Z" level=info msg="started new containerd process" address=/var/run/docker/containerd/containerd.sock module=libcontainerd pid=64
time="2026-01-28T15:24:44.909073577Z" level=info msg="starting containerd" revision=dea7da592f5d1d2b7755e3a161be07f43fad8f75 version=v2.2.1
time="2026-01-28T15:24:44.916821394Z" level=warning msg="Configuration migrated from version 2, use `containerd config migrate` to avoid migration" t="5.422µs"
time="2026-01-28T15:24:44.916883220Z" level=info msg="loading plugin" id=io.containerd.content.v1.content type=io.containerd.content.v1
time="2026-01-28T15:24:44.916959522Z" level=info msg="loading plugin" id=io.containerd.image-verifier.v1.bindir type=io.containerd.image-verifier.v1
time="2026-01-28T15:24:44.916970609Z" level=info msg="loading plugin" id=io.containerd.internal.v1.opt type=io.containerd.internal.v1
time="2026-01-28T15:24:44.918563090Z" level=info msg="loading plugin" id=io.containerd.warning.v1.deprecations type=io.containerd.warning.v1
time="2026-01-28T15:24:44.918613019Z" level=info msg="loading plugin" id=io.containerd.mount-handler.v1.erofs type=io.containerd.mount-handler.v1
time="2026-01-28T15:24:44.918620953Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.blockfile type=io.containerd.snapshotter.v1
time="2026-01-28T15:24:44.918783868Z" level=info msg="skip loading plugin" error="no scratch file generator: skip plugin" id=io.containerd.snapshotter.v1.blockfile type=io.containerd.snapshotter.v1
time="2026-01-28T15:24:44.918801351Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.btrfs type=io.containerd.snapshotter.v1
time="2026-01-28T15:24:44.919034820Z" level=info msg="skip loading plugin" error="path /var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.btrfs (overlay) must be a btrfs filesystem to be used with the btrfs snapshotter: skip plugin" id=io.containerd.snapshotter.v1.btrfs type=io.containerd.snapshotter.v1
time="2026-01-28T15:24:44.919054543Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.devmapper type=io.containerd.snapshotter.v1
time="2026-01-28T15:24:44.919060951Z" level=info msg="skip loading plugin" error="devmapper not configured: skip plugin" id=io.containerd.snapshotter.v1.devmapper type=io.containerd.snapshotter.v1
time="2026-01-28T15:24:44.919064761Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.erofs type=io.containerd.snapshotter.v1
time="2026-01-28T15:24:44.919264189Z" level=info msg="skip loading plugin" error="EROFS unsupported, please `modprobe erofs`: skip plugin" id=io.containerd.snapshotter.v1.erofs type=io.containerd.snapshotter.v1
time="2026-01-28T15:24:44.919270903Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.native type=io.containerd.snapshotter.v1
time="2026-01-28T15:24:44.919481331Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.overlayfs type=io.containerd.snapshotter.v1
time="2026-01-28T15:24:44.919880526Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.zfs type=io.containerd.snapshotter.v1
time="2026-01-28T15:24:44.919924702Z" level=info msg="skip loading plugin" error="lstat /var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.zfs: no such file or directory: skip plugin" id=io.containerd.snapshotter.v1.zfs type=io.containerd.snapshotter.v1
time="2026-01-28T15:24:44.919929377Z" level=info msg="loading plugin" id=io.containerd.event.v1.exchange type=io.containerd.event.v1
time="2026-01-28T15:24:44.919986424Z" level=info msg="loading plugin" id=io.containerd.monitor.task.v1.cgroups type=io.containerd.monitor.task.v1
time="2026-01-28T15:24:44.920153596Z" level=info msg="loading plugin" id=io.containerd.metadata.v1.bolt type=io.containerd.metadata.v1
time="2026-01-28T15:24:44.920324541Z" level=info msg="metadata content store policy set" policy=shared
time="2026-01-28T15:24:44.930157617Z" level=info msg="loading plugin" id=io.containerd.gc.v1.scheduler type=io.containerd.gc.v1
time="2026-01-28T15:24:44.930275063Z" level=info msg="loading plugin" id=io.containerd.nri.v1.nri type=io.containerd.nri.v1
time="2026-01-28T15:24:44.930302421Z" level=info msg="built-in NRI default validator is disabled"
time="2026-01-28T15:24:44.930314397Z" level=info msg="runtime interface created"
time="2026-01-28T15:24:44.930316958Z" level=info msg="created NRI interface"
time="2026-01-28T15:24:44.930321707Z" level=info msg="loading plugin" id=io.containerd.differ.v1.erofs type=io.containerd.differ.v1
time="2026-01-28T15:24:44.930425490Z" level=info msg="skip loading plugin" error="failed to check mkfs.erofs availability: failed to run mkfs.erofs --help: exec: \"mkfs.erofs\": executable file not found in $PATH: skip plugin" id=io.containerd.differ.v1.erofs type=io.containerd.differ.v1
time="2026-01-28T15:24:44.930439253Z" level=info msg="loading plugin" id=io.containerd.differ.v1.walking type=io.containerd.differ.v1
time="2026-01-28T15:24:44.930446580Z" level=info msg="loading plugin" id=io.containerd.lease.v1.manager type=io.containerd.lease.v1
time="2026-01-28T15:24:44.930452657Z" level=info msg="loading plugin" id=io.containerd.mount-manager.v1.bolt type=io.containerd.mount-manager.v1
time="2026-01-28T15:24:44.932552711Z" level=info msg="loading plugin" id=io.containerd.service.v1.containers-service type=io.containerd.service.v1
time="2026-01-28T15:24:44.932585443Z" level=info msg="loading plugin" id=io.containerd.service.v1.content-service type=io.containerd.service.v1
time="2026-01-28T15:24:44.932596023Z" level=info msg="loading plugin" id=io.containerd.service.v1.diff-service type=io.containerd.service.v1
time="2026-01-28T15:24:44.932604796Z" level=info msg="loading plugin" id=io.containerd.service.v1.images-service type=io.containerd.service.v1
time="2026-01-28T15:24:44.932632609Z" level=info msg="loading plugin" id=io.containerd.service.v1.introspection-service type=io.containerd.service.v1
time="2026-01-28T15:24:44.932649585Z" level=info msg="loading plugin" id=io.containerd.service.v1.namespaces-service type=io.containerd.service.v1
time="2026-01-28T15:24:44.932655617Z" level=info msg="loading plugin" id=io.containerd.service.v1.snapshots-service type=io.containerd.service.v1
time="2026-01-28T15:24:44.932668366Z" level=info msg="loading plugin" id=io.containerd.shim.v1.manager type=io.containerd.shim.v1
time="2026-01-28T15:24:44.932697997Z" level=info msg="loading plugin" id=io.containerd.runtime.v2.task type=io.containerd.runtime.v2
time="2026-01-28T15:24:44.933028494Z" level=info msg="loading plugin" id=io.containerd.service.v1.tasks-service type=io.containerd.service.v1
time="2026-01-28T15:24:44.933055742Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.containers type=io.containerd.grpc.v1
time="2026-01-28T15:24:44.933065349Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.content type=io.containerd.grpc.v1
time="2026-01-28T15:24:44.933070979Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.diff type=io.containerd.grpc.v1
time="2026-01-28T15:24:44.933076405Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.events type=io.containerd.grpc.v1
time="2026-01-28T15:24:44.933081510Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.images type=io.containerd.grpc.v1
time="2026-01-28T15:24:44.933088934Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.introspection type=io.containerd.grpc.v1
time="2026-01-28T15:24:44.933093584Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.leases type=io.containerd.grpc.v1
time="2026-01-28T15:24:44.933114053Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.mounts type=io.containerd.grpc.v1
time="2026-01-28T15:24:44.933136367Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.namespaces type=io.containerd.grpc.v1
time="2026-01-28T15:24:44.933152647Z" level=info msg="loading plugin" id=io.containerd.sandbox.store.v1.local type=io.containerd.sandbox.store.v1
time="2026-01-28T15:24:44.933169965Z" level=info msg="loading plugin" id=io.containerd.transfer.v1.local type=io.containerd.transfer.v1
time="2026-01-28T15:24:44.933189605Z" level=info msg="loading plugin" id=io.containerd.cri.v1.images type=io.containerd.cri.v1
time="2026-01-28T15:24:44.933222700Z" level=info msg="Get image filesystem path \"/var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.overlayfs\" for snapshotter \"overlayfs\""
time="2026-01-28T15:24:44.933228630Z" level=info msg="Start snapshots syncer"
time="2026-01-28T15:24:44.933254207Z" level=info msg="loading plugin" id=io.containerd.cri.v1.runtime type=io.containerd.cri.v1
time="2026-01-28T15:24:44.933514620Z" level=info msg="starting cri plugin" config="{\"containerd\":{\"defaultRuntimeName\":\"runc\",\"runtimes\":{\"runc\":{\"runtimeType\":\"io.containerd.runc.v2\",\"runtimePath\":\"\",\"PodAnnotations\":null,\"ContainerAnnotations\":null,\"options\":{\"BinaryName\":\"\",\"CriuImagePath\":\"\",\"CriuWorkPath\":\"\",\"IoGid\":0,\"IoUid\":0,\"NoNewKeyring\":false,\"Root\":\"\",\"ShimCgroup\":\"\",\"SystemdCgroup\":false},\"privileged_without_host_devices\":false,\"privileged_without_host_devices_all_devices_allowed\":false,\"cgroupWritable\":false,\"baseRuntimeSpec\":\"\",\"cniConfDir\":\"\",\"cniMaxConfNum\":0,\"snapshotter\":\"\",\"sandboxer\":\"podsandbox\",\"io_type\":\"\"}},\"ignoreBlockIONotEnabledErrors\":false,\"ignoreRdtNotEnabledErrors\":false},\"cni\":{\"binDir\":\"\",\"binDirs\":[\"/opt/cni/bin\"],\"confDir\":\"/etc/cni/net.d\",\"maxConfNum\":1,\"setupSerially\":false,\"confTemplate\":\"\",\"ipPref\":\"\",\"useInternalLoopback\":false},\"enableSelinux\":false,\"selinuxCategoryRange\":1024,\"maxContainerLogLineSize\":16384,\"disableApparmor\":false,\"restrictOOMScoreAdj\":false,\"disableProcMount\":false,\"unsetSeccompProfile\":\"\",\"tolerateMissingHugetlbController\":true,\"disableHugetlbController\":true,\"device_ownership_from_security_context\":false,\"ignoreImageDefinedVolumes\":false,\"netnsMountsUnderStateDir\":false,\"enableUnprivilegedPorts\":true,\"enableUnprivilegedICMP\":true,\"enableCDI\":true,\"cdiSpecDirs\":[\"/etc/cdi\",\"/var/run/cdi\"],\"drainExecSyncIOTimeout\":\"0s\",\"ignoreDeprecationWarnings\":null,\"containerdRootDir\":\"/var/lib/docker/containerd/daemon\",\"containerdEndpoint\":\"/var/run/docker/containerd/containerd.sock\",\"rootDir\":\"/var/lib/docker/containerd/daemon/io.containerd.grpc.v1.cri\",\"stateDir\":\"/var/run/docker/containerd/daemon/io.containerd.grpc.v1.cri\"}"
time="2026-01-28T15:24:44.933566429Z" level=info msg="loading plugin" id=io.containerd.podsandbox.controller.v1.podsandbox type=io.containerd.podsandbox.controller.v1
time="2026-01-28T15:24:44.933711550Z" level=info msg="loading plugin" id=io.containerd.sandbox.controller.v1.shim type=io.containerd.sandbox.controller.v1
time="2026-01-28T15:24:44.934490837Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.sandbox-controllers type=io.containerd.grpc.v1
time="2026-01-28T15:24:44.934558021Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.sandboxes type=io.containerd.grpc.v1
time="2026-01-28T15:24:44.934580809Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.snapshots type=io.containerd.grpc.v1
time="2026-01-28T15:24:44.934590560Z" level=info msg="loading plugin" id=io.containerd.streaming.v1.manager type=io.containerd.streaming.v1
time="2026-01-28T15:24:44.934604423Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.streaming type=io.containerd.grpc.v1
time="2026-01-28T15:24:44.934613103Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.tasks type=io.containerd.grpc.v1
time="2026-01-28T15:24:44.934621443Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.transfer type=io.containerd.grpc.v1
time="2026-01-28T15:24:44.934635677Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.version type=io.containerd.grpc.v1
time="2026-01-28T15:24:44.934672283Z" level=info msg="loading plugin" id=io.containerd.monitor.container.v1.restart type=io.containerd.monitor.container.v1
time="2026-01-28T15:24:44.934744788Z" level=info msg="loading plugin" id=io.containerd.tracing.processor.v1.otlp type=io.containerd.tracing.processor.v1
time="2026-01-28T15:24:44.934788149Z" level=info msg="skip loading plugin" error="skip plugin: tracing endpoint not configured" id=io.containerd.tracing.processor.v1.otlp type=io.containerd.tracing.processor.v1
time="2026-01-28T15:24:44.934798208Z" level=info msg="loading plugin" id=io.containerd.internal.v1.tracing type=io.containerd.internal.v1
time="2026-01-28T15:24:44.934806735Z" level=info msg="skip loading plugin" error="skip plugin: tracing endpoint not configured" id=io.containerd.internal.v1.tracing type=io.containerd.internal.v1
time="2026-01-28T15:24:44.934812683Z" level=info msg="loading plugin" id=io.containerd.ttrpc.v1.otelttrpc type=io.containerd.ttrpc.v1
time="2026-01-28T15:24:44.934819630Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.healthcheck type=io.containerd.grpc.v1
time="2026-01-28T15:24:44.935220033Z" level=info msg=serving... address=/var/run/docker/containerd/containerd-debug.sock
time="2026-01-28T15:24:44.935309182Z" level=info msg=serving... address=/var/run/docker/containerd/containerd.sock.ttrpc
time="2026-01-28T15:24:44.935339856Z" level=info msg=serving... address=/var/run/docker/containerd/containerd.sock
time="2026-01-28T15:24:44.935364121Z" level=info msg="containerd successfully booted in 0.027914s"
time="2026-01-28T15:24:44.946273546Z" level=info msg="OTEL tracing is not configured, using no-op tracer provider"
time="2026-01-28T15:24:44.946394053Z" level=info msg="CDI directory does not exist, skipping: failed to monitor for changes: no such file or directory" dir=/etc/cdi
time="2026-01-28T15:24:44.946401311Z" level=info msg="CDI directory does not exist, skipping: failed to monitor for changes: no such file or directory" dir=/var/run/cdi
time="2026-01-28T15:24:44.958190838Z" level=info msg="Creating a containerd client" address=/var/run/docker/containerd/containerd.sock timeout=1m0s
time="2026-01-28T15:24:44.974852136Z" level=info msg="Loading containers: start."
time="2026-01-28T15:24:44.974935946Z" level=info msg="NRI is disabled"
time="2026-01-28T15:24:44.974946413Z" level=info msg="Setting the storage driver from the $DOCKER_DRIVER environment variable (fuse-overlayfs)"
time="2026-01-28T15:24:44.974955761Z" level=info msg="[graphdriver] trying configured driver: fuse-overlayfs"
time="2026-01-28T15:24:44.979629590Z" level=info msg="Restoring containers: start."
time="2026-01-28T15:24:45.015063419Z" level=info msg="Deleting nftables IPv4 rules" error="exit status 1"
time="2026-01-28T15:24:45.042949298Z" level=info msg="Deleting nftables IPv6 rules" error="exit status 1"
time="2026-01-28T15:24:45.224385208Z" level=info msg="Loading containers: done."
time="2026-01-28T15:24:45.234470250Z" level=info msg="Docker daemon" commit=9c62384 containerd-snapshotter=false storage-driver=fuse-overlayfs version=29.2.0
time="2026-01-28T15:24:45.235423173Z" level=info msg="Initializing buildkit"
time="2026-01-28T15:24:45.298217679Z" level=info msg="Completed buildkit initialization"
time="2026-01-28T15:24:45.306072384Z" level=info msg="Daemon has completed initialization"
time="2026-01-28T15:24:45.306635103Z" level=info msg="API listen on [::]:2376"
time="2026-01-28T15:24:45.306758707Z" level=info msg="API listen on /var/run/docker.sock"
dockerd is now running.
time="2026-01-28T15:25:16.465195094Z" level=info msg="connecting to shim 2271d16fb88d08707924ebce4cbfa41aced5a92455d6d12053559d1fb50b85ec" address="unix:///run/containerd/s/9ee276efdda6542a41f3537e0c5e310a8d88323682c7849e9886448d5f79db76" namespace=moby protocol=ttrpc version=3
time="2026-01-28T15:25:16.620137981Z" level=error msg="failed to enable controllers ([cpuset cpu io memory hugetlb pids rdma])" error="failed to write subtree controllers [cpuset cpu io memory hugetlb pids rdma] to \"/sys/fs/cgroup/docker/cgroup.subtree_control\": write /sys/fs/cgroup/docker/cgroup.subtree_control: no such file or directory" runtime=io.containerd.runc.v2
time="2026-01-28T15:25:16.621357461Z" level=warning msg="error from *cgroupsv2.Manager.EventChan" error="failed to add inotify watch for \"/sys/fs/cgroup/docker/2271d16fb88d08707924ebce4cbfa41aced5a92455d6d12053559d1fb50b85ec/memory.events\": no such file or directory"
time="2026-01-28T15:25:16.712556012Z" level=info msg="sbJoin: gwep4 ''->'0087036d2571', gwep6 ''->''" eid=0087036d2571 ep=loving_mcnulty net=bridge nid=dbf6ee816787
time="2026-01-28T15:25:16.802311680Z" level=info msg="shim disconnected" id=2271d16fb88d08707924ebce4cbfa41aced5a92455d6d12053559d1fb50b85ec namespace=moby
time="2026-01-28T15:25:16.802426172Z" level=info msg="cleaning up after shim disconnected" id=2271d16fb88d08707924ebce4cbfa41aced5a92455d6d12053559d1fb50b85ec namespace=moby
time="2026-01-28T15:25:16.802439296Z" level=info msg="cleaning up dead shim" id=2271d16fb88d08707924ebce4cbfa41aced5a92455d6d12053559d1fb50b85ec namespace=moby
time="2026-01-28T15:25:16.802556407Z" level=info msg="ignoring event" container=2271d16fb88d08707924ebce4cbfa41aced5a92455d6d12053559d1fb50b85ec module=libcontainerd namespace=moby topic=/tasks/delete type="*events.TaskDelete"
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
torchscript_median_ms=50.703 torchscript_p95_ms=87.471 torchscript_mean_ms=55.242 torchscript_iters=109 torchscript_throughput=4632.9/s
onnxruntime_median_ms=47.303 onnxruntime_p95_ms=76.130 onnxruntime_mean_ms=49.695 onnxruntime_iters=121 onnxruntime_throughput=5148.4/s
openvino_median_ms=41.182 openvino_p95_ms=52.428 openvino_mean_ms=41.802 openvino_iters=144 openvino_throughput=6122.6/s
OK
== dind hello-world ==
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
17eec7bbc9d7: Pulling fs layer
17eec7bbc9d7: Verifying Checksum
17eec7bbc9d7: Download complete
17eec7bbc9d7: Pull complete
Digest: sha256:05813aedc15fb7b4d732e1be879d3252c1c9c25d885824f6295cab4538cb85cd
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
====== Done CPU image test... =======

## Diagnostics

######## Extra non-python diagnostics: #########
EE_DD not set - skipping docker daemon initialization
platform Linux-6.6.87.2-microsoft-standard-WSL2-x86_64-with-glibc2.39
torch 2.9.1+cpu
onnxruntime 1.23.0
openvino 2025.1.0-18503-6fec06580ab-releases/2025/1
########## Done extra non-python diagnostics ##########
