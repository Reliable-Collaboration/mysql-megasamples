---
type: Source
title: Meta SE 402153 — "Latest Data Dump has invalid XML and invalid characters" (2024-08-14)
description: Report that the first profile-page dumps (2024-Q2) contained invalid XML character references such as &#x1E; and &#x00;, with a community stream-cleaning workaround.
resource: https://meta.stackexchange.com/questions/402153/latest-data-dump-has-invalid-xml-and-invalid-characters
tags: [source, stackexchange, xml, data-quality]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://api.stackexchange.com/2.3/questions/402153?site=meta&filter=withbody
    title: question body and top answer (rene) via API
    accessed: "2026-09-02"
---

# What was read
Question body and top answer on 2026-09-02.

# Relevant excerpt
> "it seems like a non-compliant XML serializer was used. There are numerous escape sequences that are simply invalid XML such as &#x1E or even &#x00 ... These issues break most XML parsers. Further ... there is even an escape sequence for a character that is not valid UTF-8"
> Answer: "I've crafted a CleaningStreamReader (C#) that replaces any illegal character sequence with the space sequence so that at least the XmlReader can process the whole file." (replaces `&#x00;`-`&#x1F;` with `&#x20;`).

# What it was used to decide
Defensive byte filter in [Stack Exchange XML parsing](/tools/stackexchange-xml-parsing.md).
