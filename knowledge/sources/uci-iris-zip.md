---
type: Source
title: UCI iris.zip (iris.data, bezdekIris.data, iris.names) - inspection
description: The 3,738-byte UCI archive; iris.data carries the two historical errors, bezdekIris.data is the corrected file (differs exactly at rows 35 and 38); iris.names documents the discrepancy.
resource: https://archive.ics.uci.edu/static/public/53/iris.zip
tags:
- iris
- uci
- artifact
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
- resource: https://archive.ics.uci.edu/static/public/53/iris.zip
  title: iris.zip (3,738 bytes; md5 7a07b2b4163b650dc451aca467d4fb58)
  accessed: "2026-09-02"
---

# What was read
The zip fetched and extracted with python `zipfile`; files diffed; accessed 2026-09-02.

# Relevant excerpt (measurements)
* Entries: `Index` 105 B, `iris.data` 4,551 B (md5 `42615765a885ddf54427f12c34a0a070`), `bezdekIris.data` 4,551 B (md5 `7352471c39afdf2dad640df6dd867b72`), `iris.names` 2,998 B.
* iris.data: 150 data lines + one trailing empty line (151 `wc -l`), no header, format `5.1,3.5,1.4,0.2,Iris-setosa`; class labels `Iris-setosa`, `Iris-versicolor`, `Iris-virginica`. Line 35 = `4.9,3.1,1.5,0.1,Iris-setosa`, line 38 = `4.9,3.1,1.5,0.1,Iris-setosa` (the erroneous values).
* bezdekIris.data: identical except line 35 = `4.9,3.1,1.5,0.2,Iris-setosa` and line 38 = `4.9,3.6,1.4,0.1,Iris-setosa` (`diff` shows only 35c35 and 38c38) - i.e. the corrected data.
* iris.names: "Creator: R.A. Fisher; Donor: Michael Marshall (MARSHALL%PLU@io.arc.nasa.gov); Date: July, 1988"; "This data differs from the data presented in Fishers article ... The 35th sample should be: 4.9,3.1,1.5,0.2,"Iris-setosa" where the error is in the fourth feature. The 38th sample: 4.9,3.6,1.4,0.1,"Iris-setosa" where the errors are in the second and third features."

# What it was used to decide
Which file to load (bezdekIris.data / corrected) and the tests in [Iris](/datasets/iris.md).
