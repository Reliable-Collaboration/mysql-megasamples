---
type: Source
title: "Internet Archive Developer Portal: ias3 S3-like API"
description: "s3.us.archive.org endpoint, LOW auth header, x-archive-meta-* headers, auto-make-bucket, queue-derive, size hint, 503 SlowDown."
resource: https://archive.org/developers/ias3.html
tags: [archive-org, mirroring, api]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
sources:
  - resource: https://archive.org/developers/ias3.html
    title: "Internet Archive Developer Portal: ias3 S3-like API"
    accessed: "2026-09-02"
---

# What was read
https://archive.org/developers/ias3.html, accessed 2026-09-02.

# Relevant excerpt
* Endpoint `s3.us.archive.org`; items are buckets and files are keys; header `authorization: LOW $accesskey:$secret` over HTTPS.
* New items: `x-archive-auto-make-bucket:1`, `x-archive-meta-mediatype`, `x-archive-meta-collection`, `x-archive-meta-title`, arbitrary `x-archive-meta-$name:$value`; `x-archive-queue-derive:0` skips derivative generation; `x-archive-size-hint:$bytes` for large items; `x-archive-interactive-priority:1`.
* Overload returns 503 SlowDown; availability check `https://s3.us.archive.org/?check_limit=1&accesskey=$key&bucket=$bucket`.

# What it was used to decide
[Internet Archive mirroring](/tools/internet-archive-mirroring.md): uploads must set `mediatype:data`, disable derive, and handle 503 SlowDown with retries.
