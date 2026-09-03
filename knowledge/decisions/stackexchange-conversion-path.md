---
type: Decision
title: Stack Exchange — build from the archive.org 2024-04-02 snapshot with an own streaming XML loader
description: Choose the last click-through-free public dump and a purpose-written MySQL loader over the profile-page dumps and the Postgres converter.
resource: /decisions/stackexchange-conversion-path.md
tags:
- decision
- stackexchange
- conversion-path
- licensing-finding
- text-group
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://archive.org/metadata/stackexchange
  accessed: "2026-09-02"
- resource: https://meta.stackexchange.com/questions/401324/announcing-a-change-to-the-data-dump-process
  accessed: "2026-09-02"
- resource: https://stackoverflow.com/help/data-dumps
  accessed: "2026-09-02"
- resource: https://github.com/Networks-Learning/stackexchange-dump-to-postgres
  accessed: "2026-09-02"
---

# Question
Which Stack Exchange dump may a public MySQL image redistribute without anyone accepting the 2024 "Data dump access" agreement, and how is it loaded?

# Options considered
1. **archive.org item `stackexchange`, snapshot 2024-04-02** — CC BY-SA only, md5 per file, no login. Data frozen at April 2024.
2. Profile-page quarterly dump (latest 2026-Q2) — requires login and the checkbox "for projects that do not include training a large language model ... should I distribute this file for the purpose of LLM training, Stack Overflow reserves the right to decline ... future downloads"; contains watermark posts since July 2025; checksums only on Meta.
3. Stack Exchange API — rate-limited, no bulk bodies for PostHistory/Votes; not a dump.
Loader: (a) own Python `iterparse` → `LOAD DATA`; (b) adapt Networks-Learning/stackexchange-dump-to-postgres (MIT, Postgres-specific, skips Body by default).

# Evidence
[Terms record with the finding](/licenses/stackexchange-data-dump-terms.md); [announcement](/sources/meta-stackexchange-401324-data-dump-process-change.md); [help page](/sources/stackoverflow-help-data-dumps.md); [item metadata](/sources/archive-org-stackexchange-metadata-json.md); [watermark thread](/sources/meta-stackexchange-412018-fabricated-posts.md); [converter](/sources/github-networks-learning-stackexchange-dump-to-postgres.md); [tool record](/tools/stackexchange-xml-parsing.md).

# Outcome
Option 1 with loader (a). Sites: `dba` (extended) and `beer` or `coffee` (core). The README names the snapshot date and states that the project does not use the profile-page channel. Revisit if Stack Overflow resumes public, click-through-free publication. Dataset record: [Stack Exchange](/datasets/stackexchange.md).

# Status
accepted
