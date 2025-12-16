#!/bin/bash
set -euo pipefail

if [[ "${EE_DD:-false}" =~ ^(false|0|False)$ ]]; then
  exec "$@"
fi

CERTDIR="${DOCKER_TLS_CERTDIR:-/certs}"
mkdir -p "${CERTDIR}"/{ca,client,server}

_tls_san() {
  {
    ip -oneline address | awk '{ gsub(/\/.+$/, "", $4); print "IP:" $4 }'
    hostname -f 2>/dev/null || true
    hostname -s 2>/dev/null || true
    echo "DNS:localhost"
  } | sort -u | paste -sd, -
}

_generate_certs() {
  local dir="$1"
  [ -s "$dir/ca/key.pem" ] || openssl genrsa -out "$dir/ca/key.pem" 4096
  [ -s "$dir/ca/cert.pem" ] || openssl req -new -x509 -days 825 -key "$dir/ca/key.pem" -subj "/CN=r1-dind CA" -out "$dir/ca/cert.pem"

  [ -s "$dir/server/key.pem" ] || openssl genrsa -out "$dir/server/key.pem" 4096
  openssl req -new -key "$dir/server/key.pem" -subj "/CN=r1-dind server" -out "$dir/server/csr.pem"
  cat > "$dir/server/ext.cnf" <<EOF
[x509_exts]
subjectAltName = $(_tls_san)
EOF
  openssl x509 -req -days 825 -in "$dir/server/csr.pem" -CA "$dir/ca/cert.pem" -CAkey "$dir/ca/key.pem" -CAcreateserial \
    -out "$dir/server/cert.pem" -extfile "$dir/server/ext.cnf" -extensions x509_exts
  cp "$dir/ca/cert.pem" "$dir/server/ca.pem"

  [ -s "$dir/client/key.pem" ] || openssl genrsa -out "$dir/client/key.pem" 4096
  openssl req -new -key "$dir/client/key.pem" -subj "/CN=r1-dind client" -out "$dir/client/csr.pem"
  cat > "$dir/client/ext.cnf" <<EOF
[x509_exts]
extendedKeyUsage = clientAuth
EOF
  openssl x509 -req -days 825 -in "$dir/client/csr.pem" -CA "$dir/ca/cert.pem" -CAkey "$dir/ca/key.pem" -CAcreateserial \
    -out "$dir/client/cert.pem" -extfile "$dir/client/ext.cnf" -extensions x509_exts
  cp "$dir/ca/cert.pem" "$dir/client/ca.pem"
}

_generate_certs "$CERTDIR"

storage_opts=()
if command -v fuse-overlayfs >/dev/null 2>&1; then
  storage_opts+=(--storage-driver=overlay2 --storage-opt overlay2.use_oci=1 --storage-opt overlay2.fuse-overlayfs=1)
fi

DOCKERD_ARGS=(
  --host=unix:///var/run/docker.sock
  --host=tcp://0.0.0.0:2376
  --tlsverify
  --tlscacert="${CERTDIR}/server/ca.pem"
  --tlscert="${CERTDIR}/server/cert.pem"
  --tlskey="${CERTDIR}/server/key.pem"
  "${storage_opts[@]}"
)

find /run /var/run -name 'docker*.pid' -delete || true
dockerd "${DOCKERD_ARGS[@]}" >/var/log/dockerd.log 2>&1 &

for _ in $(seq 1 30); do
  if docker info >/dev/null 2>&1; then break; fi
  sleep 1
done

exec "$@"
