---
type: Source
title: Meta SE 401324 — "Announcing a change to the data-dump process" (2024-07-12, updated to 2024-09-09)
description: The staff announcement that moved dumps behind the profile page, ended archive.org uploads, and set the LLM-training click-through wording.
resource: https://meta.stackexchange.com/questions/401324/announcing-a-change-to-the-data-dump-process
tags:
- source
- stackexchange
- click-through
- licensing-finding
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://api.stackexchange.com/2.3/questions/401324?site=meta&filter=withbody
  title: question body via the Stack Exchange API (HTML pages return 403 to non-browser clients)
  accessed: "2026-09-02"
  version: created 2024-07-12T13:30Z, last edited 2024-09-09T20:24Z, owner Philippe (staff)
---

# What was read
The full question body (original announcement plus the July 26, August 14 and August 29 updates) on 2026-09-02.

# Relevant excerpt
* "this is primarily only a change in location for where the data dump is accessed. Moving forward, we'll be providing the data dump from a section of the site user profile"
* "this is an attempt to put commercial pressure on LLM manufacturers to join us and our existing partners in the "socially responsible AI" usage"
* "You may download the dumps, free of charge, as you always have ... The CC BY-SA license is unchanged."
* Final agreement text (July 26 update): "I understand that this file is being provided to me for my own use and for projects that do not include training a large language model (LLM), and that should I distribute this file for the purpose of LLM training, Stack Overflow reserves the right to decline to allow me access to future downloads of this data dump."
* Withdrawn mock-up text (July 12): "I agree that I will use this file for non-commercial use. I will not use it for any other purpose, and I will not transfer it to others without permission from Stack Overflow. I certify that I am not downloading this file on behalf of my employer, for use in a for-profit enterprise."
* "users will only be provided the data for the specific Stack Exchange site and its Meta site" — one request per site; site and meta are not bundled.
* "Stack Overflow is no longer uploading the data dump to archive.org. ... We would really rather users do not upload the file to archive.org or similar data pile sites."
* "when you breach the agreement that you make when downloading the dumps file, we do have the option to decline to provide you with future versions of the data dumps."
* Full-network dump: "We're scoping and building a process to allow for this, but it will not be in the initial release".

# What it was used to decide
[Stack Exchange data dump terms](/licenses/stackexchange-data-dump-terms.md); [decision to use the archive.org snapshot](/decisions/stackexchange-conversion-path.md).
