---
type: Source
title: Oracle Container Registry database/free — anonymous pull probe and image sizes (registry v2 API)
description: "Result of querying container-registry.oracle.com's Docker Registry v2 API without credentials on 2026-09-02: an anonymous pull token is issued, tags are listed, and the per-architecture compressed sizes were summed from the manifests."
resource: https://container-registry.oracle.com/v2/database/free/tags/list
tags:
- oracle
- container-registry
- oracle-database-free
- measurement
status: stable
trust: verified
stale_after: "2026-12-01"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://container-registry.oracle.com/auth?service=Oracle%20Registry&scope=repository:database/free:pull
  title: Token endpoint (anonymous request)
  accessed: "2026-09-02"
- resource: https://container-registry.oracle.com/v2/database/free/manifests/latest
  title: OCI image index for :latest and per-arch manifests for 23.26.3.0
  accessed: "2026-09-02"
---

# What was read
Commands run on 2026-09-02 (read-only HTTP, no image layers downloaded):
```
curl -sI https://container-registry.oracle.com/v2/database/free/manifests/latest   # 401 + WWW-Authenticate: Bearer realm="https://container-registry.oracle.com/auth",service="Oracle Registry",scope="repository:database/free:pull"
curl -s "https://container-registry.oracle.com/auth?service=Oracle%20Registry&scope=repository:database/free:pull"   # returned a token without any credentials
curl -s -H "Authorization: Bearer $TOK" https://container-registry.oracle.com/v2/database/free/tags/list
curl -s -H "Authorization: Bearer $TOK" -H "Accept: application/vnd.oci.image.index.v1+json, ..." https://container-registry.oracle.com/v2/database/free/manifests/<tag>
```

# Relevant excerpt
* Tags: `23.2.0.0, 23.3.0.0, 23.4.0.0(-lite), 23.5.0.0 … 23.9.0.0` and `23.26.0.0 … 23.26.3.0`, each with `-amd64`, `-arm64`, `-lite`, `-lite-amd64`, `-lite-arm64` variants; `RDBMS_23.26.3.0.0DBRU_LINUX.X64_260704[-arm64][-lite]`; `latest`; `latest-lite`.
* `latest` and `latest-lite` are OCI image indexes with `linux/amd64` and `linux/arm64` entries (**arm64 is available**).
* Compressed layer totals: `23.26.3.0-amd64` 29 layers, **3,709 MB**; `23.26.3.0-arm64` 29 layers, 3,528 MB; `23.26.3.0-lite-amd64` 7 layers, **896 MB**.
* An anonymous bearer token was granted and honoured for `pull` scope, so `docker pull container-registry.oracle.com/database/free:latest` works **without `docker login`** at the API level as of the access date. **Inferred:** the OCR web UI may still present the Free Use Terms page for browsing; it was not readable (redirect loop) and is irrelevant to the pull.

# What it was used to decide
[Oracle Database Free container tool record](/tools/oracle-database-free-container.md); [conversion path](/decisions/oracle-conversion-path.md) (image size is a cost argument against running Oracle in the build).
