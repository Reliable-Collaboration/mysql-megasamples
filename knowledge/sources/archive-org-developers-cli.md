---
type: Source
title: "Internet Archive Developer Portal: ia command-line interface"
description: "ia upload syntax with --metadata, mediatype defaults to data and cannot be changed, --retries, ia download --glob, ia metadata --modify."
resource: https://archive.org/developers/internetarchive/cli.html
tags: [archive-org, mirroring, cli]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
sources:
  - resource: https://archive.org/developers/internetarchive/cli.html
    title: "Internet Archive Developer Portal: ia command-line interface"
    accessed: "2026-09-02"
---

# What was read
https://archive.org/developers/internetarchive/cli.html, accessed 2026-09-02.

# Relevant excerpt
* `ia upload <identifier> file1 file2 --metadata="mediatype:texts" --metadata="blah:arg"`; "Please note that, unless specified otherwise, items will be uploaded with a data mediatype. This cannot be changed afterwards."
* "You can use the --retries parameter to retry on errors (i.e. if IA-S3 is overloaded)".
* `ia download TripDown1905`, `ia download TripDown1905 --glob="*.mp4"`, `ia metadata TripDown1905`, `ia metadata <identifier> --modify="foo:bar"`, `ia search '...'`.

# What it was used to decide
[Internet Archive mirroring](/tools/internet-archive-mirroring.md): the mirror script is `ia upload mysql-megasamples-<dataset>-<version> <files> --metadata=mediatype:data --retries=10`.
