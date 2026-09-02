---
type: Source
title: angel-hernandez91/enron-emails README — independent 517,401 count and ASCII observation
description: Second independent third-party count of the 2015 corpus (517,401) plus the observation that the files are ASCII-encoded.
resource: https://github.com/angel-hernandez91/enron-emails
tags: [source, enron, row-counts, charset]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/angel-hernandez91/enron-emails/master/README.md
    title: README.md at master
    accessed: "2026-09-02"
---

# What was read
README.md (raw), grepped for counts and encoding, on 2026-09-02.

# Relevant excerpt
> "Total Emails: 517,401" (under "Control Totals: Did we actually capture all of the emails in the maildir directory?")
> "Since the emails where encoded in ASCII, the encoding was maintained"
> "Emails from Enron Employees: 83%"

# What it was used to decide
Corroborates the 517,401 count in [Enron dataset](/datasets/enron.md); the charset expectation in [Enron maildir parsing](/tools/text-enron-maildir-parsing.md) (ASCII-dominant, with an inferred Latin-1 minority still to verify).
