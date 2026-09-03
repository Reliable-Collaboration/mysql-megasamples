---
type: Source
title: hbiostat.org/data/repo/titanic3.csv (inspection)
description: 1,309 passenger rows, 14 columns, 116,752 bytes, pure ASCII, LF; header and sample rows; checksums.
resource: https://hbiostat.org/data/repo/titanic3.csv
tags:
- titanic
- csv
- measurement
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://hbiostat.org/data/repo/titanic3.csv
  title: titanic3.csv (md5 01b027be0a49ab8538efbd60a8c43288; sha256 db6df9666818c69a753cd85d743e01502c8518b00579b6aada0d4fc5a66ccb9d)
  accessed: "2026-09-02"
- resource: https://hbiostat.org/data/repo/titanic5.html
  title: titanic5 notes (David Beltran del Rio, March 2016) and titanic5.csv HEAD (199,639 bytes)
  accessed: "2026-09-02"
---

# What was read
titanic3.csv fetched and measured; titanic5.html read; titanic5.csv HEAD; accessed 2026-09-02.

# Relevant excerpt (measurements)
* Content-Length 116,752; 1,310 lines = header + 1,309 rows; `file`: "CSV ASCII text"; 0 non-ASCII lines; 0 CR bytes.
* Header: `"pclass","survived","name","sex","age","sibsp","parch","ticket","fare","cabin","embarked","boat","body","home.dest"`.
* Rows: `1,1,"Allen, Miss. Elisabeth Walton","female",29,0,0,"24160",211.3375,"B5","S","2",,"St Louis, MO"` and `1,1,"Allison, Master. Hudson Trevor","male",0.92,1,2,"113781",151.5500,"C22 C26","S","11",,"Montreal, PQ / Chesterville, ON"` - strings double-quoted, empty fields for missing values, fractional ages, fares with 4 decimals, multi-cabin strings.
* titanic5 (2016): "strip all the passenger and crew data from the Encyclopedia Titanica ... match to your earlier titanic3 dataset ... the new set has less missing ages - 51 missing (vs 263) out of 1309"; distributed as xlsx with tabs Titanic5_all, Titanic5_passenger, Titanic5_metadata, Titanic3_wID; csv 199,639 bytes with "older" variable names.

# What it was used to decide
Row count, columns and encoding statement in [Titanic](/datasets/titanic.md).
