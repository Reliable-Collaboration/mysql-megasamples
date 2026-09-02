---
type: Source
title: Google Cloud blog announcing the Open Knowledge Format
description: Google Cloud Data Cloud team post of 2026-06-12 introducing OKF, its motivation, file layout, and reference implementations.
resource: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
tags:
- okf
- announcement
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:05:32Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:05:32Z"
sources:
- resource: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing
  title: How the Open Knowledge Format can improve data sharing
  accessed: "2026-09-02"
  version: published 2026-06-12
---

# What was read
The announcement post, accessed 2026-09-02.

# Relevant excerpt
> "The answer to this problem isn't another knowledge service. You need a format, a way to represent knowledge that anyone can produce, without an SDK, [and] anyone can consume, without an integration."

> "OKF v0.1 represents knowledge as a directory of markdown files with YAML frontmatter, with a small set of agreed-upon conventions... Just markdown... Just files... Just YAML frontmatter."

Reference implementations named: an enrichment agent, a static HTML visualizer, and three sample bundles (GA4 e-commerce, Stack Overflow, Bitcoin) at https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf.

# What it was used to decide
Background for [the conventions](/runbooks/knowledge-bundle-conventions.md). The visualizer in the knowledge-catalog repository is a candidate for the CI validation step described in PLAN.md section 10 (see [validator question](/questions/okf-validator-availability.md)).
