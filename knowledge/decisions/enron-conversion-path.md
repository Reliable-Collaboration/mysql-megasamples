---
type: Decision
title: Enron — parse the CMU maildir with Python's email stdlib into a three-table schema
description: Choose a purpose-written parser over reusing third-party SQL dumps for the Enron corpus.
resource: /decisions/enron-conversion-path.md
tags: [decision, enron, conversion-path, text-group]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://www.cs.cmu.edu/~enron/
    accessed: 2026-09-02
  - resource: https://www.ah-ruhe.de/enron-email-data/
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/ftrain/enron-sqlite3/master/README.md
    accessed: 2026-09-02
---

# Question
How do we get the Enron corpus into MySQL reproducibly, with a defensible provenance chain?

# Options considered
1. **Own parser over the CMU 2015 tarball** (Python `email` stdlib → TSV → `LOAD DATA`), schema `mailbox / message / recipient`.
2. Reuse the repaired Shetty/Adibi MySQL dump from ah-ruhe.de — older 2004-era corpus content, no license statement, MySQL 4 origin repaired by a third party, does not reflect the 2009-2015 privacy removals.
3. Reuse a GitHub converter (enron-sqlite3, Enron2mbox, spark-mail) — different targets (SQLite/mbox/Avro); would still need a MySQL stage.
4. EDRM/ZL v2 with attachments — 79 GB, withdrawn upstream for PII.

# Evidence
[CMU page](/sources/cmu-enron-email-dataset-page.md) (single authoritative artifact, removal policy); [ah-ruhe.de](/sources/ah-ruhe-enron-email-data.md) (ISI dump offline, repaired copy unlicensed); [enron-sqlite3](/sources/github-ftrain-enron-sqlite3-readme.md) and [Enron2mbox](/sources/github-lintool-enron2mbox-readme.md) (the parse is a few hundred lines, half an hour of runtime); [tool record](/tools/text-enron-maildir-parsing.md).

# Outcome
Option 1. Deterministic file order, keep every file as a row (folder placement is data), FULLTEXT on subject/body, personal-data README per [Enron public record](/licenses/enron-public-record.md). Dataset record: [Enron](/datasets/enron.md).

# Status
accepted
