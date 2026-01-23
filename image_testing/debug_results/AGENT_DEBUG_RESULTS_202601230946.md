# Debug Results - Fri Jan 23 09:46:30 EET 2026

TLS environment detected. Generating certs...
/certs/server/cert.pem: OK
/certs/client/cert.pem: OK
iptables v1.8.10 (nf_tables)
Launching dockerd in the background...
Waiting for dockerd to respond...
dockerd is now running.
TLS environment detected. Generating certs...
/certs/server/cert.pem: OK
/certs/client/cert.pem: OK
iptables v1.8.10 (nf_tables)
Launching dockerd in the background...
Waiting for dockerd to respond...
dockerd is now running.
EE_DD not set - skipping docker daemon initialization
Fri Jan 23 07:47:12 2026       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 560.35.02              Driver Version: 560.94         CUDA Version: 12.6     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 2080 Ti     On  |   00000000:65:00.0  On |                  N/A |
| 33%   41C    P8             32W /  260W |    3505MiB /  11264MiB |     15%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
                                                                                         
+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI        PID   Type   Process name                              GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A        23      G   /Xwayland                                   N/A      |
+-----------------------------------------------------------------------------------------+
EE_DD not set - skipping docker daemon initialization
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
time="2026-01-23T07:48:26.752978422Z" level=info msg="Starting up"
time="2026-01-23T07:48:26.765918052Z" level=info msg="containerd not running, starting managed containerd"
time="2026-01-23T07:48:26.767387379Z" level=info msg="started new containerd process" address=/var/run/docker/containerd/containerd.sock module=libcontainerd pid=61
time="2026-01-23T07:48:26.790523687Z" level=info msg="starting containerd" revision=dea7da592f5d1d2b7755e3a161be07f43fad8f75 version=v2.2.1
time="2026-01-23T07:48:26.800043599Z" level=warning msg="Configuration migrated from version 2, use `containerd config migrate` to avoid migration" t="4.536µs"
time="2026-01-23T07:48:26.800099774Z" level=info msg="loading plugin" id=io.containerd.content.v1.content type=io.containerd.content.v1
time="2026-01-23T07:48:26.800155966Z" level=info msg="loading plugin" id=io.containerd.image-verifier.v1.bindir type=io.containerd.image-verifier.v1
time="2026-01-23T07:48:26.800167909Z" level=info msg="loading plugin" id=io.containerd.internal.v1.opt type=io.containerd.internal.v1
time="2026-01-23T07:48:26.800992751Z" level=info msg="loading plugin" id=io.containerd.warning.v1.deprecations type=io.containerd.warning.v1
time="2026-01-23T07:48:26.801036747Z" level=info msg="loading plugin" id=io.containerd.mount-handler.v1.erofs type=io.containerd.mount-handler.v1
time="2026-01-23T07:48:26.801049541Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.blockfile type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:26.801216609Z" level=info msg="skip loading plugin" error="no scratch file generator: skip plugin" id=io.containerd.snapshotter.v1.blockfile type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:26.801250069Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.btrfs type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:26.801822528Z" level=info msg="skip loading plugin" error="path /var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.btrfs (overlay) must be a btrfs filesystem to be used with the btrfs snapshotter: skip plugin" id=io.containerd.snapshotter.v1.btrfs type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:26.801885333Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.devmapper type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:26.801904446Z" level=info msg="skip loading plugin" error="devmapper not configured: skip plugin" id=io.containerd.snapshotter.v1.devmapper type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:26.801916424Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.erofs type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:26.802513529Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.native type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:26.802835973Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.overlayfs type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:26.811516247Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.zfs type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:26.811610297Z" level=info msg="skip loading plugin" error="lstat /var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.zfs: no such file or directory: skip plugin" id=io.containerd.snapshotter.v1.zfs type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:26.811629308Z" level=info msg="loading plugin" id=io.containerd.event.v1.exchange type=io.containerd.event.v1
time="2026-01-23T07:48:26.811691320Z" level=info msg="loading plugin" id=io.containerd.monitor.task.v1.cgroups type=io.containerd.monitor.task.v1
time="2026-01-23T07:48:26.814821776Z" level=info msg="loading plugin" id=io.containerd.metadata.v1.bolt type=io.containerd.metadata.v1
time="2026-01-23T07:48:26.815207791Z" level=info msg="metadata content store policy set" policy=shared
time="2026-01-23T07:48:26.821995948Z" level=info msg="loading plugin" id=io.containerd.gc.v1.scheduler type=io.containerd.gc.v1
time="2026-01-23T07:48:26.822207288Z" level=info msg="loading plugin" id=io.containerd.nri.v1.nri type=io.containerd.nri.v1
time="2026-01-23T07:48:26.822388183Z" level=info msg="built-in NRI default validator is disabled"
time="2026-01-23T07:48:26.822456594Z" level=info msg="runtime interface created"
time="2026-01-23T07:48:26.822473392Z" level=info msg="created NRI interface"
time="2026-01-23T07:48:26.822609577Z" level=info msg="loading plugin" id=io.containerd.differ.v1.erofs type=io.containerd.differ.v1
time="2026-01-23T07:48:26.822719089Z" level=info msg="skip loading plugin" error="failed to check mkfs.erofs availability: failed to run mkfs.erofs --help: exec: \"mkfs.erofs\": executable file not found in $PATH: skip plugin" id=io.containerd.differ.v1.erofs type=io.containerd.differ.v1
time="2026-01-23T07:48:26.822755654Z" level=info msg="loading plugin" id=io.containerd.differ.v1.walking type=io.containerd.differ.v1
time="2026-01-23T07:48:26.822797880Z" level=info msg="loading plugin" id=io.containerd.lease.v1.manager type=io.containerd.lease.v1
time="2026-01-23T07:48:26.822810065Z" level=info msg="loading plugin" id=io.containerd.mount-manager.v1.bolt type=io.containerd.mount-manager.v1
time="2026-01-23T07:48:26.824960462Z" level=info msg="loading plugin" id=io.containerd.service.v1.containers-service type=io.containerd.service.v1
time="2026-01-23T07:48:26.825012117Z" level=info msg="loading plugin" id=io.containerd.service.v1.content-service type=io.containerd.service.v1
time="2026-01-23T07:48:26.825025248Z" level=info msg="loading plugin" id=io.containerd.service.v1.diff-service type=io.containerd.service.v1
time="2026-01-23T07:48:26.825038037Z" level=info msg="loading plugin" id=io.containerd.service.v1.images-service type=io.containerd.service.v1
time="2026-01-23T07:48:26.825049333Z" level=info msg="loading plugin" id=io.containerd.service.v1.introspection-service type=io.containerd.service.v1
time="2026-01-23T07:48:26.825070140Z" level=info msg="loading plugin" id=io.containerd.service.v1.namespaces-service type=io.containerd.service.v1
time="2026-01-23T07:48:26.825110312Z" level=info msg="loading plugin" id=io.containerd.service.v1.snapshots-service type=io.containerd.service.v1
time="2026-01-23T07:48:26.825123776Z" level=info msg="loading plugin" id=io.containerd.shim.v1.manager type=io.containerd.shim.v1
time="2026-01-23T07:48:26.825175034Z" level=info msg="loading plugin" id=io.containerd.runtime.v2.task type=io.containerd.runtime.v2
time="2026-01-23T07:48:26.825686372Z" level=info msg="loading plugin" id=io.containerd.service.v1.tasks-service type=io.containerd.service.v1
time="2026-01-23T07:48:26.825783833Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.containers type=io.containerd.grpc.v1
time="2026-01-23T07:48:26.825852285Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.content type=io.containerd.grpc.v1
time="2026-01-23T07:48:26.825891593Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.diff type=io.containerd.grpc.v1
time="2026-01-23T07:48:26.825903731Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.events type=io.containerd.grpc.v1
time="2026-01-23T07:48:26.825913350Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.images type=io.containerd.grpc.v1
time="2026-01-23T07:48:26.825943863Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.introspection type=io.containerd.grpc.v1
time="2026-01-23T07:48:26.825955183Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.leases type=io.containerd.grpc.v1
time="2026-01-23T07:48:26.825978388Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.mounts type=io.containerd.grpc.v1
time="2026-01-23T07:48:26.826019851Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.namespaces type=io.containerd.grpc.v1
time="2026-01-23T07:48:26.826060083Z" level=info msg="loading plugin" id=io.containerd.sandbox.store.v1.local type=io.containerd.sandbox.store.v1
time="2026-01-23T07:48:26.826128128Z" level=info msg="loading plugin" id=io.containerd.transfer.v1.local type=io.containerd.transfer.v1
time="2026-01-23T07:48:26.826190577Z" level=info msg="loading plugin" id=io.containerd.cri.v1.images type=io.containerd.cri.v1
time="2026-01-23T07:48:26.826320788Z" level=info msg="Get image filesystem path \"/var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.overlayfs\" for snapshotter \"overlayfs\""
time="2026-01-23T07:48:26.826373064Z" level=info msg="Start snapshots syncer"
time="2026-01-23T07:48:26.826411923Z" level=info msg="loading plugin" id=io.containerd.cri.v1.runtime type=io.containerd.cri.v1
time="2026-01-23T07:48:26.827087914Z" level=info msg="starting cri plugin" config="{\"containerd\":{\"defaultRuntimeName\":\"runc\",\"runtimes\":{\"runc\":{\"runtimeType\":\"io.containerd.runc.v2\",\"runtimePath\":\"\",\"PodAnnotations\":null,\"ContainerAnnotations\":null,\"options\":{\"BinaryName\":\"\",\"CriuImagePath\":\"\",\"CriuWorkPath\":\"\",\"IoGid\":0,\"IoUid\":0,\"NoNewKeyring\":false,\"Root\":\"\",\"ShimCgroup\":\"\",\"SystemdCgroup\":false},\"privileged_without_host_devices\":false,\"privileged_without_host_devices_all_devices_allowed\":false,\"cgroupWritable\":false,\"baseRuntimeSpec\":\"\",\"cniConfDir\":\"\",\"cniMaxConfNum\":0,\"snapshotter\":\"\",\"sandboxer\":\"podsandbox\",\"io_type\":\"\"}},\"ignoreBlockIONotEnabledErrors\":false,\"ignoreRdtNotEnabledErrors\":false},\"cni\":{\"binDir\":\"\",\"binDirs\":[\"/opt/cni/bin\"],\"confDir\":\"/etc/cni/net.d\",\"maxConfNum\":1,\"setupSerially\":false,\"confTemplate\":\"\",\"ipPref\":\"\",\"useInternalLoopback\":false},\"enableSelinux\":false,\"selinuxCategoryRange\":1024,\"maxContainerLogLineSize\":16384,\"disableApparmor\":false,\"restrictOOMScoreAdj\":false,\"disableProcMount\":false,\"unsetSeccompProfile\":\"\",\"tolerateMissingHugetlbController\":true,\"disableHugetlbController\":true,\"device_ownership_from_security_context\":false,\"ignoreImageDefinedVolumes\":false,\"netnsMountsUnderStateDir\":false,\"enableUnprivilegedPorts\":true,\"enableUnprivilegedICMP\":true,\"enableCDI\":true,\"cdiSpecDirs\":[\"/etc/cdi\",\"/var/run/cdi\"],\"drainExecSyncIOTimeout\":\"0s\",\"ignoreDeprecationWarnings\":null,\"containerdRootDir\":\"/var/lib/docker/containerd/daemon\",\"containerdEndpoint\":\"/var/run/docker/containerd/containerd.sock\",\"rootDir\":\"/var/lib/docker/containerd/daemon/io.containerd.grpc.v1.cri\",\"stateDir\":\"/var/run/docker/containerd/daemon/io.containerd.grpc.v1.cri\"}"
time="2026-01-23T07:48:26.827173764Z" level=info msg="loading plugin" id=io.containerd.podsandbox.controller.v1.podsandbox type=io.containerd.podsandbox.controller.v1
time="2026-01-23T07:48:26.827263970Z" level=info msg="loading plugin" id=io.containerd.sandbox.controller.v1.shim type=io.containerd.sandbox.controller.v1
time="2026-01-23T07:48:26.827774609Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.sandbox-controllers type=io.containerd.grpc.v1
time="2026-01-23T07:48:26.827823023Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.sandboxes type=io.containerd.grpc.v1
time="2026-01-23T07:48:26.827835240Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.snapshots type=io.containerd.grpc.v1
time="2026-01-23T07:48:26.827844608Z" level=info msg="loading plugin" id=io.containerd.streaming.v1.manager type=io.containerd.streaming.v1
time="2026-01-23T07:48:26.827862958Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.streaming type=io.containerd.grpc.v1
time="2026-01-23T07:48:26.827893903Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.tasks type=io.containerd.grpc.v1
time="2026-01-23T07:48:26.827940297Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.transfer type=io.containerd.grpc.v1
time="2026-01-23T07:48:26.827980705Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.version type=io.containerd.grpc.v1
time="2026-01-23T07:48:26.827995011Z" level=info msg="loading plugin" id=io.containerd.monitor.container.v1.restart type=io.containerd.monitor.container.v1
time="2026-01-23T07:48:26.828073734Z" level=info msg="loading plugin" id=io.containerd.tracing.processor.v1.otlp type=io.containerd.tracing.processor.v1
time="2026-01-23T07:48:26.828168716Z" level=info msg="skip loading plugin" error="skip plugin: tracing endpoint not configured" id=io.containerd.tracing.processor.v1.otlp type=io.containerd.tracing.processor.v1
time="2026-01-23T07:48:26.828210620Z" level=info msg="loading plugin" id=io.containerd.internal.v1.tracing type=io.containerd.internal.v1
time="2026-01-23T07:48:26.828233390Z" level=info msg="skip loading plugin" error="skip plugin: tracing endpoint not configured" id=io.containerd.internal.v1.tracing type=io.containerd.internal.v1
time="2026-01-23T07:48:26.828248405Z" level=info msg="loading plugin" id=io.containerd.ttrpc.v1.otelttrpc type=io.containerd.ttrpc.v1
time="2026-01-23T07:48:26.828274902Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.healthcheck type=io.containerd.grpc.v1
time="2026-01-23T07:48:26.828701455Z" level=info msg=serving... address=/var/run/docker/containerd/containerd-debug.sock
time="2026-01-23T07:48:26.828849168Z" level=info msg=serving... address=/var/run/docker/containerd/containerd.sock.ttrpc
time="2026-01-23T07:48:26.828939478Z" level=info msg=serving... address=/var/run/docker/containerd/containerd.sock
time="2026-01-23T07:48:26.829072903Z" level=info msg="containerd successfully booted in 0.040404s"
time="2026-01-23T07:48:26.836589516Z" level=info msg="OTEL tracing is not configured, using no-op tracer provider"
time="2026-01-23T07:48:26.836846476Z" level=info msg="CDI directory does not exist, skipping: failed to monitor for changes: no such file or directory" dir=/etc/cdi
time="2026-01-23T07:48:26.836877207Z" level=info msg="CDI directory does not exist, skipping: failed to monitor for changes: no such file or directory" dir=/var/run/cdi
time="2026-01-23T07:48:26.848986533Z" level=info msg="Creating a containerd client" address=/var/run/docker/containerd/containerd.sock timeout=1m0s
time="2026-01-23T07:48:26.861746433Z" level=info msg="Loading containers: start."
time="2026-01-23T07:48:26.861841069Z" level=info msg="Starting daemon with containerd snapshotter integration enabled"
time="2026-01-23T07:48:26.864404691Z" level=info msg="Restoring containers: start."
time="2026-01-23T07:48:26.932201575Z" level=info msg="Deleting nftables IPv4 rules" error="exit status 1"
time="2026-01-23T07:48:27.031014426Z" level=info msg="Deleting nftables IPv6 rules" error="exit status 1"
time="2026-01-23T07:48:27.300788915Z" level=info msg="Loading containers: done."
time="2026-01-23T07:48:27.313435212Z" level=warning msg="WARNING: No blkio throttle.read_bps_device support"
time="2026-01-23T07:48:27.313531468Z" level=warning msg="WARNING: No blkio throttle.write_bps_device support"
time="2026-01-23T07:48:27.313546096Z" level=warning msg="WARNING: No blkio throttle.read_iops_device support"
time="2026-01-23T07:48:27.313554490Z" level=warning msg="WARNING: No blkio throttle.write_iops_device support"
time="2026-01-23T07:48:27.313587979Z" level=warning msg="WARNING: Support for cgroup v1 is deprecated and planned to be removed by no later than May 2029 (https://github.com/moby/moby/issues/51111)"
time="2026-01-23T07:48:27.313622078Z" level=info msg="Docker daemon" commit=3b01d64 containerd-snapshotter=true storage-driver=overlayfs version=29.1.5
time="2026-01-23T07:48:27.315174629Z" level=info msg="Initializing buildkit"
time="2026-01-23T07:48:27.341701002Z" level=info msg="Completed buildkit initialization"
time="2026-01-23T07:48:27.349502458Z" level=info msg="Daemon has completed initialization"
time="2026-01-23T07:48:27.349636805Z" level=info msg="API listen on /var/run/docker.sock"
time="2026-01-23T07:48:27.349638909Z" level=info msg="API listen on [::]:2376"
dockerd is now running.
python3: can't open file '/image_tests/gpu_image_test.py': [Errno 2] No such file or directory
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
time="2026-01-23T07:48:36.048173956Z" level=info msg="Starting up"
time="2026-01-23T07:48:36.060930821Z" level=info msg="containerd not running, starting managed containerd"
time="2026-01-23T07:48:36.062621693Z" level=info msg="started new containerd process" address=/var/run/docker/containerd/containerd.sock module=libcontainerd pid=64
time="2026-01-23T07:48:36.081847876Z" level=info msg="starting containerd" revision=dea7da592f5d1d2b7755e3a161be07f43fad8f75 version=v2.2.1
time="2026-01-23T07:48:36.089717052Z" level=warning msg="Configuration migrated from version 2, use `containerd config migrate` to avoid migration" t="3.804µs"
time="2026-01-23T07:48:36.089885729Z" level=info msg="loading plugin" id=io.containerd.content.v1.content type=io.containerd.content.v1
time="2026-01-23T07:48:36.089989950Z" level=info msg="loading plugin" id=io.containerd.image-verifier.v1.bindir type=io.containerd.image-verifier.v1
time="2026-01-23T07:48:36.090487182Z" level=info msg="loading plugin" id=io.containerd.internal.v1.opt type=io.containerd.internal.v1
time="2026-01-23T07:48:36.092220665Z" level=info msg="loading plugin" id=io.containerd.warning.v1.deprecations type=io.containerd.warning.v1
time="2026-01-23T07:48:36.092290076Z" level=info msg="loading plugin" id=io.containerd.mount-handler.v1.erofs type=io.containerd.mount-handler.v1
time="2026-01-23T07:48:36.092306013Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.blockfile type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:36.092504710Z" level=info msg="skip loading plugin" error="no scratch file generator: skip plugin" id=io.containerd.snapshotter.v1.blockfile type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:36.092541428Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.btrfs type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:36.092996069Z" level=info msg="skip loading plugin" error="path /var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.btrfs (overlay) must be a btrfs filesystem to be used with the btrfs snapshotter: skip plugin" id=io.containerd.snapshotter.v1.btrfs type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:36.093037335Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.devmapper type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:36.093054099Z" level=info msg="skip loading plugin" error="devmapper not configured: skip plugin" id=io.containerd.snapshotter.v1.devmapper type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:36.093062435Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.erofs type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:36.093533345Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.native type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:36.093879905Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.overlayfs type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:36.102824480Z" level=info msg="loading plugin" id=io.containerd.snapshotter.v1.zfs type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:36.102957412Z" level=info msg="skip loading plugin" error="lstat /var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.zfs: no such file or directory: skip plugin" id=io.containerd.snapshotter.v1.zfs type=io.containerd.snapshotter.v1
time="2026-01-23T07:48:36.103014040Z" level=info msg="loading plugin" id=io.containerd.event.v1.exchange type=io.containerd.event.v1
time="2026-01-23T07:48:36.103090311Z" level=info msg="loading plugin" id=io.containerd.monitor.task.v1.cgroups type=io.containerd.monitor.task.v1
time="2026-01-23T07:48:36.104008568Z" level=info msg="loading plugin" id=io.containerd.metadata.v1.bolt type=io.containerd.metadata.v1
time="2026-01-23T07:48:36.104489585Z" level=info msg="metadata content store policy set" policy=shared
time="2026-01-23T07:48:36.111491650Z" level=info msg="loading plugin" id=io.containerd.gc.v1.scheduler type=io.containerd.gc.v1
time="2026-01-23T07:48:36.111624822Z" level=info msg="loading plugin" id=io.containerd.nri.v1.nri type=io.containerd.nri.v1
time="2026-01-23T07:48:36.111691339Z" level=info msg="built-in NRI default validator is disabled"
time="2026-01-23T07:48:36.111724772Z" level=info msg="runtime interface created"
time="2026-01-23T07:48:36.111734493Z" level=info msg="created NRI interface"
time="2026-01-23T07:48:36.111780096Z" level=info msg="loading plugin" id=io.containerd.differ.v1.erofs type=io.containerd.differ.v1
time="2026-01-23T07:48:36.111957290Z" level=info msg="skip loading plugin" error="failed to check mkfs.erofs availability: failed to run mkfs.erofs --help: exec: \"mkfs.erofs\": executable file not found in $PATH: skip plugin" id=io.containerd.differ.v1.erofs type=io.containerd.differ.v1
time="2026-01-23T07:48:36.112003422Z" level=info msg="loading plugin" id=io.containerd.differ.v1.walking type=io.containerd.differ.v1
time="2026-01-23T07:48:36.112047283Z" level=info msg="loading plugin" id=io.containerd.lease.v1.manager type=io.containerd.lease.v1
time="2026-01-23T07:48:36.112115856Z" level=info msg="loading plugin" id=io.containerd.mount-manager.v1.bolt type=io.containerd.mount-manager.v1
time="2026-01-23T07:48:36.114749418Z" level=info msg="loading plugin" id=io.containerd.service.v1.containers-service type=io.containerd.service.v1
time="2026-01-23T07:48:36.114811553Z" level=info msg="loading plugin" id=io.containerd.service.v1.content-service type=io.containerd.service.v1
time="2026-01-23T07:48:36.114827493Z" level=info msg="loading plugin" id=io.containerd.service.v1.diff-service type=io.containerd.service.v1
time="2026-01-23T07:48:36.114847366Z" level=info msg="loading plugin" id=io.containerd.service.v1.images-service type=io.containerd.service.v1
time="2026-01-23T07:48:36.114860415Z" level=info msg="loading plugin" id=io.containerd.service.v1.introspection-service type=io.containerd.service.v1
time="2026-01-23T07:48:36.114885613Z" level=info msg="loading plugin" id=io.containerd.service.v1.namespaces-service type=io.containerd.service.v1
time="2026-01-23T07:48:36.114929624Z" level=info msg="loading plugin" id=io.containerd.service.v1.snapshots-service type=io.containerd.service.v1
time="2026-01-23T07:48:36.114972888Z" level=info msg="loading plugin" id=io.containerd.shim.v1.manager type=io.containerd.shim.v1
time="2026-01-23T07:48:36.115017198Z" level=info msg="loading plugin" id=io.containerd.runtime.v2.task type=io.containerd.runtime.v2
time="2026-01-23T07:48:36.115595243Z" level=info msg="loading plugin" id=io.containerd.service.v1.tasks-service type=io.containerd.service.v1
time="2026-01-23T07:48:36.115653739Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.containers type=io.containerd.grpc.v1
time="2026-01-23T07:48:36.115681778Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.content type=io.containerd.grpc.v1
time="2026-01-23T07:48:36.115704541Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.diff type=io.containerd.grpc.v1
time="2026-01-23T07:48:36.115732244Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.events type=io.containerd.grpc.v1
time="2026-01-23T07:48:36.115753508Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.images type=io.containerd.grpc.v1
time="2026-01-23T07:48:36.115782082Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.introspection type=io.containerd.grpc.v1
time="2026-01-23T07:48:36.115809233Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.leases type=io.containerd.grpc.v1
time="2026-01-23T07:48:36.115830688Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.mounts type=io.containerd.grpc.v1
time="2026-01-23T07:48:36.115885755Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.namespaces type=io.containerd.grpc.v1
time="2026-01-23T07:48:36.115929635Z" level=info msg="loading plugin" id=io.containerd.sandbox.store.v1.local type=io.containerd.sandbox.store.v1
time="2026-01-23T07:48:36.115966166Z" level=info msg="loading plugin" id=io.containerd.transfer.v1.local type=io.containerd.transfer.v1
time="2026-01-23T07:48:36.116016558Z" level=info msg="loading plugin" id=io.containerd.cri.v1.images type=io.containerd.cri.v1
time="2026-01-23T07:48:36.116143763Z" level=info msg="Get image filesystem path \"/var/lib/docker/containerd/daemon/io.containerd.snapshotter.v1.overlayfs\" for snapshotter \"overlayfs\""
time="2026-01-23T07:48:36.116172950Z" level=info msg="Start snapshots syncer"
time="2026-01-23T07:48:36.116234523Z" level=info msg="loading plugin" id=io.containerd.cri.v1.runtime type=io.containerd.cri.v1
time="2026-01-23T07:48:36.116896038Z" level=info msg="starting cri plugin" config="{\"containerd\":{\"defaultRuntimeName\":\"runc\",\"runtimes\":{\"runc\":{\"runtimeType\":\"io.containerd.runc.v2\",\"runtimePath\":\"\",\"PodAnnotations\":null,\"ContainerAnnotations\":null,\"options\":{\"BinaryName\":\"\",\"CriuImagePath\":\"\",\"CriuWorkPath\":\"\",\"IoGid\":0,\"IoUid\":0,\"NoNewKeyring\":false,\"Root\":\"\",\"ShimCgroup\":\"\",\"SystemdCgroup\":false},\"privileged_without_host_devices\":false,\"privileged_without_host_devices_all_devices_allowed\":false,\"cgroupWritable\":false,\"baseRuntimeSpec\":\"\",\"cniConfDir\":\"\",\"cniMaxConfNum\":0,\"snapshotter\":\"\",\"sandboxer\":\"podsandbox\",\"io_type\":\"\"}},\"ignoreBlockIONotEnabledErrors\":false,\"ignoreRdtNotEnabledErrors\":false},\"cni\":{\"binDir\":\"\",\"binDirs\":[\"/opt/cni/bin\"],\"confDir\":\"/etc/cni/net.d\",\"maxConfNum\":1,\"setupSerially\":false,\"confTemplate\":\"\",\"ipPref\":\"\",\"useInternalLoopback\":false},\"enableSelinux\":false,\"selinuxCategoryRange\":1024,\"maxContainerLogLineSize\":16384,\"disableApparmor\":false,\"restrictOOMScoreAdj\":false,\"disableProcMount\":false,\"unsetSeccompProfile\":\"\",\"tolerateMissingHugetlbController\":true,\"disableHugetlbController\":true,\"device_ownership_from_security_context\":false,\"ignoreImageDefinedVolumes\":false,\"netnsMountsUnderStateDir\":false,\"enableUnprivilegedPorts\":true,\"enableUnprivilegedICMP\":true,\"enableCDI\":true,\"cdiSpecDirs\":[\"/etc/cdi\",\"/var/run/cdi\"],\"drainExecSyncIOTimeout\":\"0s\",\"ignoreDeprecationWarnings\":null,\"containerdRootDir\":\"/var/lib/docker/containerd/daemon\",\"containerdEndpoint\":\"/var/run/docker/containerd/containerd.sock\",\"rootDir\":\"/var/lib/docker/containerd/daemon/io.containerd.grpc.v1.cri\",\"stateDir\":\"/var/run/docker/containerd/daemon/io.containerd.grpc.v1.cri\"}"
time="2026-01-23T07:48:36.116990950Z" level=info msg="loading plugin" id=io.containerd.podsandbox.controller.v1.podsandbox type=io.containerd.podsandbox.controller.v1
time="2026-01-23T07:48:36.117084175Z" level=info msg="loading plugin" id=io.containerd.sandbox.controller.v1.shim type=io.containerd.sandbox.controller.v1
time="2026-01-23T07:48:36.117556935Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.sandbox-controllers type=io.containerd.grpc.v1
time="2026-01-23T07:48:36.117612939Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.sandboxes type=io.containerd.grpc.v1
time="2026-01-23T07:48:36.117628042Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.snapshots type=io.containerd.grpc.v1
time="2026-01-23T07:48:36.117640379Z" level=info msg="loading plugin" id=io.containerd.streaming.v1.manager type=io.containerd.streaming.v1
time="2026-01-23T07:48:36.117674192Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.streaming type=io.containerd.grpc.v1
time="2026-01-23T07:48:36.117715819Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.tasks type=io.containerd.grpc.v1
time="2026-01-23T07:48:36.117750059Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.transfer type=io.containerd.grpc.v1
time="2026-01-23T07:48:36.117766962Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.version type=io.containerd.grpc.v1
time="2026-01-23T07:48:36.117777601Z" level=info msg="loading plugin" id=io.containerd.monitor.container.v1.restart type=io.containerd.monitor.container.v1
time="2026-01-23T07:48:36.117869635Z" level=info msg="loading plugin" id=io.containerd.tracing.processor.v1.otlp type=io.containerd.tracing.processor.v1
time="2026-01-23T07:48:36.117891219Z" level=info msg="skip loading plugin" error="skip plugin: tracing endpoint not configured" id=io.containerd.tracing.processor.v1.otlp type=io.containerd.tracing.processor.v1
time="2026-01-23T07:48:36.117907327Z" level=info msg="loading plugin" id=io.containerd.internal.v1.tracing type=io.containerd.internal.v1
time="2026-01-23T07:48:36.117918252Z" level=info msg="skip loading plugin" error="skip plugin: tracing endpoint not configured" id=io.containerd.internal.v1.tracing type=io.containerd.internal.v1
time="2026-01-23T07:48:36.117927124Z" level=info msg="loading plugin" id=io.containerd.ttrpc.v1.otelttrpc type=io.containerd.ttrpc.v1
time="2026-01-23T07:48:36.117939022Z" level=info msg="loading plugin" id=io.containerd.grpc.v1.healthcheck type=io.containerd.grpc.v1
time="2026-01-23T07:48:36.118275417Z" level=info msg=serving... address=/var/run/docker/containerd/containerd-debug.sock
time="2026-01-23T07:48:36.118445596Z" level=info msg=serving... address=/var/run/docker/containerd/containerd.sock.ttrpc
time="2026-01-23T07:48:36.118594795Z" level=info msg=serving... address=/var/run/docker/containerd/containerd.sock
time="2026-01-23T07:48:36.118656130Z" level=info msg="containerd successfully booted in 0.038275s"
time="2026-01-23T07:48:36.127647242Z" level=info msg="OTEL tracing is not configured, using no-op tracer provider"
time="2026-01-23T07:48:36.127860784Z" level=info msg="CDI directory does not exist, skipping: failed to monitor for changes: no such file or directory" dir=/var/run/cdi
time="2026-01-23T07:48:36.127899893Z" level=info msg="CDI directory does not exist, skipping: failed to monitor for changes: no such file or directory" dir=/etc/cdi
time="2026-01-23T07:48:36.141598008Z" level=info msg="Creating a containerd client" address=/var/run/docker/containerd/containerd.sock timeout=1m0s
time="2026-01-23T07:48:36.155669828Z" level=info msg="Loading containers: start."
time="2026-01-23T07:48:36.155775900Z" level=info msg="Starting daemon with containerd snapshotter integration enabled"
time="2026-01-23T07:48:36.158577802Z" level=info msg="Restoring containers: start."
time="2026-01-23T07:48:36.241042676Z" level=info msg="Deleting nftables IPv4 rules" error="exit status 1"
time="2026-01-23T07:48:36.281422253Z" level=info msg="Deleting nftables IPv6 rules" error="exit status 1"
time="2026-01-23T07:48:36.542559168Z" level=info msg="Loading containers: done."
time="2026-01-23T07:48:36.558643335Z" level=warning msg="WARNING: No blkio throttle.read_bps_device support"
time="2026-01-23T07:48:36.558709243Z" level=warning msg="WARNING: No blkio throttle.write_bps_device support"
time="2026-01-23T07:48:36.558722978Z" level=warning msg="WARNING: No blkio throttle.read_iops_device support"
time="2026-01-23T07:48:36.558731453Z" level=warning msg="WARNING: No blkio throttle.write_iops_device support"
time="2026-01-23T07:48:36.558740955Z" level=warning msg="WARNING: Support for cgroup v1 is deprecated and planned to be removed by no later than May 2029 (https://github.com/moby/moby/issues/51111)"
time="2026-01-23T07:48:36.558775829Z" level=info msg="Docker daemon" commit=3b01d64 containerd-snapshotter=true storage-driver=overlayfs version=29.1.5
time="2026-01-23T07:48:36.559218972Z" level=info msg="Initializing buildkit"
time="2026-01-23T07:48:36.582809559Z" level=info msg="Completed buildkit initialization"
time="2026-01-23T07:48:36.589897722Z" level=info msg="Daemon has completed initialization"
time="2026-01-23T07:48:36.590044137Z" level=info msg="API listen on [::]:2376"
time="2026-01-23T07:48:36.590046728Z" level=info msg="API listen on /var/run/docker.sock"
dockerd is now running.
python3: can't open file '/image_tests/cpu_image_test.py': [Errno 2] No such file or directory
platform Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.39
torch 2.9.1+cpu
onnxruntime 1.23.0
openvino 2025.1.0-18503-6fec06580ab-releases/2025/1
total 8
drwxr-xr-x 2 root   root   4096 Jan 23 09:46 .
drwxr-xr-x 3 andrei andrei 4096 Jan 23 09:46 ..

## Scope
- Images: ratio1/base_edge_node_amd64_gpu:dev, ratio1/base_edge_node_amd64_cpu:dev
- Commands:
  - ./image_testing/test-gpu.sh (run twice, second time with stderr captured)
  - ./image_testing/test-cpu.sh (run twice, second time with stderr captured)
  - docker run --rm --gpus=all ratio1/base_edge_node_amd64_gpu:dev nvidia-smi
  - docker run --rm ratio1/base_edge_node_amd64_cpu:dev python3 - <<'PY' ... (no output; stdin not passed)
  - docker run --rm -i --entrypoint python3 ratio1/base_edge_node_amd64_cpu:dev - <<'PY' ... (captured output)

## Results
- GPU test: FAIL (missing /image_tests/gpu_image_test.py)
- CPU test: FAIL (missing /image_tests/cpu_image_test.py)

## Logs (key excerpts)
- GPU: python3: can't open file '/image_tests/gpu_image_test.py': [Errno 2] No such file or directory
- CPU: python3: can't open file '/image_tests/cpu_image_test.py': [Errno 2] No such file or directory

## Diagnostics
- nvidia-smi: Driver 560.94, CUDA 12.6, GPU NVIDIA GeForce RTX 2080 Ti
- CPU image python (with -i):
  - platform Linux-5.15.167.4-microsoft-standard-WSL2-x86_64-with-glibc2.39
  - torch 2.9.1+cpu
  - onnxruntime 1.23.0
  - openvino 2025.1.0-18503-6fec06580ab-releases/2025/1
- Host bind mount evidence: ./image_testing/image_tests exists and is empty (created by docker -v)

## Root Cause Analysis
- The test scripts mount "${SCRIPT_DIR}/image_tests" into /image_tests. In this repo, the tests live in ./image_testing/ (gpu_image_test.py, cpu_image_test.py), and ./image_testing/image_tests did not exist before running the scripts.
- Per Docker bind mount behavior, using -v with a non-existent host path auto-creates an empty directory. That means /image_tests inside the container is an empty directory, so the python files are missing and the tests exit immediately.
- Source: https://docs.docker.com/engine/storage/bind-mounts/ ("If you use --volume to bind-mount a file or directory that does not yet exist on the Docker host, Docker automatically creates the directory on the host for you. It's always created as a directory.")

## Proposed Fixes (ranked)
1) Create ./image_testing/image_tests and place/symlink gpu_image_test.py + cpu_image_test.py there. This keeps test scripts unchanged and aligns with the expected mount path.
2) Update test-gpu.sh and test-cpu.sh to mount "${SCRIPT_DIR}" directly (or change the container path to match the existing file locations). Example: -v "${SCRIPT_DIR}:/image_tests:ro".
3) Switch to --mount with an explicit missing-path error (safer signal if the host path is wrong) and update the scripts accordingly.

## Retest Results
- Reran both scripts with stderr capture; failures persist until mount path is corrected.
