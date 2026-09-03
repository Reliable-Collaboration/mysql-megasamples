---
type: Source
title: An independent export of Oracle OE product_information
description: A third-party copy of the OE sample data, exported from a live Oracle database with the SQL*Plus continuations already resolved; used as ground truth for the continuation rule.
resource: https://github.com/billwallis/sql-problems/blob/main/src/sql-short-reads/schemas/order-entry.sql
tags:
- oracle
- oe
- verification
status: stable
trust: verified
generated:
  by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
verified:
- by: claude-code/claude-opus-5
  at: "2026-09-03T00:00:00Z"
sources:
- resource: https://github.com/billwallis/sql-problems/blob/main/src/sql-short-reads/schemas/order-entry.sql
  title: order-entry.sql (288 product_information rows, single-line literals)
  accessed: "2026-09-03"
- resource: https://github.com/ogobrecht/sample-data-sets-for-oracle/blob/master/order_entry_human_resources/data/oehr_product_information.sql
  title: oehr_product_information.sql (a second copy, consulted first)
  accessed: "2026-09-03"
---

# What was read
Both files' `product_information` rows, compared column by column against this build's reassembly of
`oe_p_pi.sql`, 2026-09-03. Neither is an Oracle publication; both are third-party copies of the
Oracle sample data with the SQL*Plus continuations already resolved, which is exactly what was needed.

# Relevant excerpt
`INSERT INTO product_information(...) VALUES ('1726', 'LCD Monitor 11/PM', 'Liquid Cristal Display 11
inch passive monitor. The virtually-flat, high-resolution screen delivers outstanding image quality
with reduced glare.', ...)` — the whole description on one line, continuations already resolved.

# What it was used to decide
That a SQL*Plus continuation joins with a single space, which is the rule
`datasets/oracle_oe/oeparse.py` implements; and, by comparing all 288 rows, that the reassembly is
correct rather than merely plausible.

# What it shows
The source writes `...The virtually-flat,-\nhigh-resolution screen...`. Both exports read
`virtually-flat, high-resolution` — **one space**, so SQL*Plus replaces the continuation character and
the line break with a space rather than joining with nothing. Joining with nothing would run 264 pairs
of words together in the English descriptions alone (`that` + `a small monitor` → `thata small`).

Against the `sql-problems` copy, 283 of 288 descriptions reassemble byte for byte. All five remaining
differences are that copy's own edits, each checked back against the Oracle source: an en dash for a
hyphen, `×` for `x`, `…` for `...`, a trimmed trailing space that the source really has, and a
newline flattened to a space where the source literal genuinely spans two lines with no continuation.

The `ogobrecht` copy agrees on the decisive case but disagrees with itself elsewhere (it drops the
separator after `upgrade;` while keeping a double space after `for `), so it is recorded here as the
weaker of the two and was not used to settle the rule.

# Caution
These are third-party repositories, not Oracle releases. They are usable as corroboration of a text
that Oracle itself only ships in continuation form, not as an authority on the schema.
