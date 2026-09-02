---
type: Source
title: simplewiki-latest-md5sums.txt and -sha1sums.txt (20260901)
description: Published checksums for every simplewiki dump file; the files list dated names, so the executor must map latest-* to 20260901-*.
resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-sha1sums.txt
tags:
- source
- wikipedia
- checksums
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
stale_after: "2026-10-05"
sources:
- resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-md5sums.txt
  title: md5sums (38 lines)
  accessed: "2026-09-02"
- resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-sha1sums.txt
  title: sha1sums
  accessed: "2026-09-02"
---

# What was read
Both checksum files on 2026-09-02.

# Relevant excerpt (20260901)
md5: pages-articles.xml.bz2 `066f0b2e8d6cf5504abf26b8b86027bb`; page.sql.gz `f48dc42e43e50c5e31a5641118de2a6d`; categorylinks `49218fc0877e3568eabbd0d5c62252e8`; pagelinks `2e07c9e1b90e16c3cf00a814b55ec448`; linktarget `ee227cfc6d3e28a004080eb86ea56fe4`; redirect `7cd7c35b7aaa6f8f861e42b29de5f8f3`; category `073743f17b4d7391e98d34070b873be2`; site_stats `af0898a45c9e589153ac523030654fa3`.
sha1: pages-articles.xml.bz2 `1bdd97642b5f511def336cce8afd34996db52d49`; page.sql.gz `c2b88ecbc7e0e440cf541e54f5cf53c1129b9468`; categorylinks `3139fe67ba6105ba0829b321bf80f552b4f26466`; pagelinks `b900518ce197c72f01cdf2f38f8e2514d8e7c6af`; linktarget `3b84a923cb157f4d4cbcc538516aa866b53d27f0`; redirect `46fabd49fc5a18c0ce2e2338743b596806279b92`; category `c57b1f2b8d32e0a5ad1bf90ded1f0a87f7825dc5`.

# What it was used to decide
Checksum availability in [Simple English Wikipedia dataset](/datasets/wikipedia-simple.md); pin the dated URLs (`/simplewiki/20260901/`) in the build, not `latest/`.
