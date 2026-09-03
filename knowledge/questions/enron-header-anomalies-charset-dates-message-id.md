---
type: Open Question
title: Enron header anomalies — charset of non-ASCII bodies, Date offsets/bogus years, Message-ID uniqueness
description: The parsing plan assumes cp1252 fallbacks, `-0700 (PDT)` dates with a few bogus years, and one Message-ID per file; none is verified from an authoritative source.
resource: /questions/enron-header-anomalies-charset-dates-message-id.md
tags:
- question
- enron
- charset
- dates
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
- resource: https://raw.githubusercontent.com/angel-hernandez91/enron-emails/master/README.md
  accessed: "2026-09-02"
---

# Question
(1) How many files fail strict UTF-8/ASCII decoding and what charset are they? (2) What is the distribution of `Date` offsets and out-of-range years? (3) Is `Message-ID` unique across the 517k files (so it can be a UNIQUE key)?

# Cheapest experiment
After extraction: `python3 - <<'PY'` walking `maildir/`, counting `UnicodeDecodeError` under `utf-8`, collecting `email.utils.parsedate_to_datetime` failures and years outside 1998-2002, and `collections.Counter` of `Message-ID` values with count > 1. Runs in minutes; record results in [Enron dataset](/datasets/enron.md) `# Type-mapping hazards` and decide on `UNIQUE(message_id)`.

# Resolves
Column constraints and decode strategy in [Enron maildir parsing](/tools/text-enron-maildir-parsing.md).

# Answer (2026-09-03)
Measured by parsing **all 517,401 messages** of the CMU 2015-05-07 corpus with `email` under
`policy=compat32` — not a sample. The corpus is far cleaner than the question assumed:

| measure | result |
|---|---|
| messages parsed | 517,401 |
| bodies needing the cp1252 fallback | **0** |
| missing `Date` | **0** |
| `Date` present but unparseable | **0** |
| missing `Message-ID` | **0** |
| distinct `Message-ID` | **517,401** |
| `Message-ID` values that repeat | **0** |
| messages with any `email` header defect | 30 |

Declared charsets are `us-ascii` (479,286), `ansi_x3.4-1968` (38,086, an ASCII alias) and none at
all (29). Every body decodes under its declared charset, so the cp1252 fallback the converter carries
never fires on this corpus; it is kept because it costs nothing and the column that records it
(`charset_fallback`) is what makes that visible rather than assumed.

**Consequence for the schema**: the plan said "no `UNIQUE(message_id)` until uniqueness is measured".
It has been measured across the whole corpus, so `message` now declares it.
