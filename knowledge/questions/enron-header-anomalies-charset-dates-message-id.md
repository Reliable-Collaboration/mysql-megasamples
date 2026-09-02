---
type: Open Question
title: Enron header anomalies — charset of non-ASCII bodies, Date offsets/bogus years, Message-ID uniqueness
description: The parsing plan assumes cp1252 fallbacks, `-0700 (PDT)` dates with a few bogus years, and one Message-ID per file; none is verified from an authoritative source.
resource: /questions/enron-header-anomalies-charset-dates-message-id.md
tags: [question, enron, charset, dates, text-group]
status: draft
trust: open
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/angel-hernandez91/enron-emails/master/README.md
    accessed: 2026-09-02
---

# Question
(1) How many files fail strict UTF-8/ASCII decoding and what charset are they? (2) What is the distribution of `Date` offsets and out-of-range years? (3) Is `Message-ID` unique across the 517k files (so it can be a UNIQUE key)?

# Cheapest experiment
After extraction: `python3 - <<'PY'` walking `maildir/`, counting `UnicodeDecodeError` under `utf-8`, collecting `email.utils.parsedate_to_datetime` failures and years outside 1998-2002, and `collections.Counter` of `Message-ID` values with count > 1. Runs in minutes; record results in [Enron dataset](/datasets/enron.md) `# Type-mapping hazards` and decide on `UNIQUE(message_id)`.

# Resolves
Column constraints and decode strategy in [Enron maildir parsing](/tools/text-enron-maildir-parsing.md).
