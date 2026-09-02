---
type: Source
title: lintool/Enron2mbox README — maildir layout and message count
description: Third-party converter README that documents the extracted layout and reports 517,401 message files in enron_mail_20150507.
resource: https://github.com/lintool/Enron2mbox
tags:
- source
- enron
- row-counts
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://raw.githubusercontent.com/lintool/Enron2mbox/master/README.md
  title: README.md at master
  accessed: "2026-09-02"
---

# What was read
README.md (raw) on 2026-09-02.

# Relevant excerpt
> "The Enron Email Dataset is distributed in maildir format, which means that each message is stored in a separate file."
> "Verify the total number of messages in the dataset: `$ ./count_messages.sh | cut -d' ' -f1 | awk '{s+=$1} END {print s}'` → `517401`"
> after conversion "`ls enron | wc` → 3311" mbox files (i.e. 3,311 custodian/folder combinations)
> "the script creates cur/ and new/ directories, which is part of the expected layout" (the raw tree is not a true Maildir)

# What it was used to decide
Message count baseline (517,401, third-party) and folder count in [Enron dataset](/datasets/enron.md); parsing notes in [Enron maildir parsing tool](/tools/text-enron-maildir-parsing.md).
