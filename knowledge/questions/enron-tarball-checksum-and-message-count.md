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
status: draft
trust: open
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
