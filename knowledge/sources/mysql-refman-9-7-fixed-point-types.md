---
type: Source
title: MySQL 9.7 Reference Manual — Fixed-Point Types (Exact Value) DECIMAL, NUMERIC
description: DECIMAL holds at most 65 digits; default precision 10; values beyond the declared scale are converted to that scale.
resource: https://dev.mysql.com/doc/refman/9.7/en/fixed-point-types.html
tags:
- mysql
- decimal
- type-mapping
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://dev.mysql.com/doc/refman/9.7/en/fixed-point-types.html
  title: Fixed-Point Types (Exact Value) - DECIMAL, NUMERIC
  accessed: "2026-09-02"
---

# What was read
The manual page, 2026-09-02.

# Relevant excerpt
> The maximum number of digits for `DECIMAL` is 65 ... The default value of `M` is 10.
Values with more fractional digits than the declared scale are converted (rounded) to that scale.

# What it was used to decide
Oracle `NUMBER(p,s)` maps directly to MySQL `DECIMAL(p,s)` only when `0 ≤ s ≤ p ≤ 38` and `s ≤ 30`; Oracle also allows negative scales (`NUMBER(5,-2)`) and scales larger than the precision (`NUMBER(4,5)`), which MySQL cannot declare and which the converter would have to rewrite (multiply out the negative scale or widen the precision). None of the four sample schemas declare such columns (the converter asserts this). Unconstrained `NUMBER` is mapped data-driven per the Oracle dataset records. Excess fractional digits on load are **rounded**, as quoted above.
