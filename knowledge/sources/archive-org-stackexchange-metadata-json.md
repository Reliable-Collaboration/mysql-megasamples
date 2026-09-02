---
type: Source
title: archive.org metadata API — stackexchange item file list with sizes, md5 and mtimes
description: Machine-readable listing used for exact byte sizes, md5 checksums and the last-upload date of the public Stack Exchange dumps.
resource: https://archive.org/metadata/stackexchange
tags: [source, stackexchange, checksums, size-evidence]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
stale_after: 2027-03-01
sources:
  - resource: https://archive.org/metadata/stackexchange
    title: metadata JSON (116,026 bytes)
    accessed: 2026-09-02
---

# What was read
The full metadata JSON on 2026-09-02.

# Relevant excerpt
* `subject`: "Stack Exchange Data Dump - 2024-04-02"; `creator`: "Stack Exchange, Inc."; `uploader`: team+datadump@stackexchange.com; `addeddate` 2014-01-21; `item_last_updated` 2025-06-24 (metadata only); **newest .7z mtime 2024-04-07 19:38:56 UTC** — no file has been added since.
* 386 files; sum of `.7z` sizes 99,092,341,190 bytes.
* Exact per-file values (name, bytes, mtime UTC, md5):
  * `dba.stackexchange.com.7z` 319,345,462 · 2024-04-06 22:23:48 · `d0f417b3c3c9210ed32623a071651411`
  * `datascience.stackexchange.com.7z` 89,531,447 · 2024-04-07 06:47:39 · `e9362d731c9180ea384236dabbe0b939`
  * `devops.stackexchange.com.7z` 16,771,120 · `c67ec48509355e43d7ee83001e88118b`
  * `ai.stackexchange.com.7z` 37,062,342 · `2fb5e5b6321826f4d61dc45b6d931608`
  * `coffee.stackexchange.com.7z` 5,095,298 · `458d102b0d9083a5c0d53031f4b03af7`
  * `beer.stackexchange.com.7z` 4,317,770 · `5da8bd0067af280aeb53ebfd6b5e650d`
  * `cooking.stackexchange.com.7z` 87,555,311 · `f6ffe54c3783c8faebc33b30f8ff61d1`
  * `codereview.stackexchange.com.7z` 508,596,604; `softwareengineering.stackexchange.com.7z` 363,040,159; `serverfault.com.7z` 859,606,467; `superuser.com.7z` 1,294,499,667; `mathoverflow.net.7z` 510,436,127
  * `stackoverflow.com-Posts.7z` 23,026,928,274; `stackoverflow.com-PostHistory.7z` 37,747,369,973; `stackoverflow.com-Comments.7z` 6,997,473,057; `stackoverflow.com-Votes.7z` 2,202,885,100; `stackoverflow.com-Users.7z` 990,180,949
  * `readme.txt` 5,856 (2024-04-01); `license.txt` 1,738 (2024-04-01)
  * smallest archives are meta sites around 100 KB (e.g. `solana.meta.stackexchange.com.7z` 100,282).

# What it was used to decide
Sizes, checksums and site choice in [Stack Exchange dataset](/datasets/stackexchange.md).
