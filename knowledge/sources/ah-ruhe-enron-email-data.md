---
type: Source
title: ah-ruhe.de "Enron Data" — repaired Shetty/Adibi MySQL dump
description: The page (formerly ahschulz.de) that redistributes a repaired copy of the ISI Shetty and Adibi MySQL 4 dump of the Enron corpus with employeelist, message, recipientinfo and referenceinfo tables.
resource: https://www.ah-ruhe.de/enron-email-data/
tags: [source, enron, relational-versions]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://www.ah-ruhe.de/enron-email-data/
    title: Enron Data (redirect target of http://www.ahschulz.de/enron-email-data/)
    accessed: 2026-09-02
---

# What was read
The page (HTTP 200, 6,346 bytes after redirect from ahschulz.de) on 2026-09-02.

# Relevant excerpt
> "When Enron collapsed in 2001, about 500.000 internal emails were made public. Jitesh Shetty and Jafar Adibi cleaned the data and put it in a MySQL database. The dump is no longer online, but was created under MySQL 4 anyway and cannot be imported in MySQL 5 without changes in the dump-file."
> "I "repaired" the dump, found another list with the positions of the former employees and updated the old one. ... The data can be downloaded as a single sql-file and as a RData-file."
> Tables: `employeelist` (Email_id, folder, ...), `message` (mid, message_id, ...), `recipientinfo` (mid, ...), `referenceinfo` (mid, ...).

No license is stated on the page. The page confirms the ISI dump is offline.

# What it was used to decide
"Known relational versions" paragraph in [Enron dataset](/datasets/enron.md) — we do not reuse this dump (older 2004 corpus version, unknown license, MySQL 4 origin) but mirror its table naming ideas (message / recipientinfo).
