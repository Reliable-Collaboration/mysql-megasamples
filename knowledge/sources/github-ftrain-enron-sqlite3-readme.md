---
type: Source
title: ftrain/enron-sqlite3 README — pointers to the surviving MySQL version of the Enron corpus
description: README that describes a SQLite conversion of the 2015 tarball and points to the ahschulz/ah-ruhe MySQL dump as "the right way".
resource: https://github.com/ftrain/enron-sqlite3
tags: [source, enron, relational-versions]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/ftrain/enron-sqlite3/master/README.md
    title: README.md at master
    accessed: "2026-09-02"
---

# What was read
README.md (raw) on 2026-09-02.

# Relevant excerpt
> "SQL is here: http://www.ahschulz.de/enron-email-data/ Which I loaded into MySQL, dumped, and imported using mysql2sqlite"
> "20 spare gigs or thereabouts (the DB is around 5Gb all in when done)" ... "the 3.6 gigs of data you're dumping into SQLite"
> "Download enron_mail_20150507.tar.gz from https://www.cs.cmu.edu/~enron/" — "This will produce a maildir folder"
> quoting MIT Technology Review: the FERC release was "more than 1.6 million e-mails" later culled; the cleaned corpus "remains the largest public domain database of real e-mails in the world"

# What it was used to decide
Size expectation (a full relational load with full-text is several GB → extended tier) and the pointer to the ah-ruhe.de MySQL version in [Enron dataset](/datasets/enron.md).
