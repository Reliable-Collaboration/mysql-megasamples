---
type: Open Question
title: What are the sha256 of enron_mail_20150507.tar.gz and the exact file count?
description: CMU publishes no checksum and says only "about 0.5M messages"; two third-party READMEs say 517,401 files.
resource: /questions/enron-tarball-checksum-and-message-count.md
tags:
- question
- enron
- checksum
- row-counts
- text-group
status: deprecated
trust: verified
verified:
- by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://www.cs.cmu.edu/~enron/
  accessed: "2026-09-02"
- resource: https://raw.githubusercontent.com/lintool/Enron2mbox/master/README.md
  accessed: "2026-09-02"
---

# Question
The page lists no md5/sha; `Content-Length` is 443,254,787 and `Last-Modified` 2015-05-07. Is the file stable, and is the count 517,401 (Enron2mbox, enron-emails) or the ~517,431 sometimes cited?

# Cheapest experiment
`curl -O https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz && sha256sum enron_mail_20150507.tar.gz && tar tzf enron_mail_20150507.tar.gz | grep -vc '/$'` — record both in [Enron dataset](/datasets/enron.md) `# Tests and expected values` and pin the sha256 in the build.

# Resolves
Test baseline and checksum pin for [Enron](/datasets/enron.md).

# Answer (2026-09-03)
Downloaded and counted.

* `enron_mail_20150507.tar.gz` is **443,254,787 bytes**, matching the `Content-Length` recorded during
  research, with sha256 **`b3da1b3fe0369ec3140bb4fbce94702c33b7da810ec15d718b3fadf5cd748ca7`**, now
  pinned in `manifest.yaml`. CMU still publishes no checksum of its own.
* The archive holds **517,401 message files** in **150 mailboxes**, confirming the two independent
  third-party counts the record cited, plus 3,500 directory entries.
* Uncompressed message bytes total **1,421,183,736** (1.42 GB), which supports the record's inference
  that the page's "about 1.7Gb" refers to the extracted tree rather than the download, and matches the
  third-party "1.4 GB maildir" report.
* None of the paths listed in `DELETIONS.txt` that were checked (`richey-c/inbox/10.`,
  `skilling-j/1584.`, `gay-r/sent/12.`) is present, so this is the post-removal 2015 version. The
  converter asserts that on every build rather than trusting the filename.
* The tar's member order is **not** alphabetical, which matters for any subset rule that depends on
  ordering: the converter takes the member list in a first pass and selects from it, rather than
  reading until it has enough.
