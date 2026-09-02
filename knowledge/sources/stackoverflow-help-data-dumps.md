---
type: Source
title: Stack Overflow Help Center — "What is the data dump?"
description: The current official description of the quarterly per-site dump behind the account "Data dump access" page and the LLM-training checkbox.
resource: https://stackoverflow.com/help/data-dumps
tags: [source, stackexchange, click-through]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://stackoverflow.com/help/data-dumps
    title: What is the data dump? How often is an updated version posted?
    accessed: 2026-09-02
---

# What was read
The help article (HTTP 200 via curl with a browser user agent; WebFetch is blocked on this host) on 2026-09-02.

# Relevant excerpt
> "Content from each Stack Exchange site is made available quarterly in the form of a "data dump" file that can be accessed by a user via their account settings page."
> "To obtain the most recent file for a site, choose the "Settings" tab at the top of your profile page, then choose "Data dump access" under the "Access" heading on the left. The date of the most recent data dump and the size of the file are noted there. Check the box affirming that you do not intend to use the file for LLM training, and then use the "Download data" button to begin downloading the file."
> "Answers on this community-curated question on Meta Stack Exchange provide details on the structure of the data dump file, including a diagram of the schema."

Login is implicit (account settings page). No mention of archive.org.

# What it was used to decide
[Stack Exchange data dump terms](/licenses/stackexchange-data-dump-terms.md); [Stack Exchange dataset](/datasets/stackexchange.md).
