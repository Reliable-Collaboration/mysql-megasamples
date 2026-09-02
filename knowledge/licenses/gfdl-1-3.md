---
type: License
title: GNU Free Documentation License 1.3 (GFDL 1.3)
description: Second license of the Wikipedia text dual license (CC BY-SA 4.0 + GFDL); reusers may pick either; this project relies on CC BY-SA and ships GFDL text for completeness.
resource: https://www.gnu.org/licenses/fdl-1.3.txt
tags: [license, gfdl, copyleft, documentation]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://www.gnu.org/licenses/fdl-1.3.txt
    title: GNU Free Documentation License, Version 1.3 (plain text, 22,955 bytes)
    accessed: 2026-09-02
  - resource: https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use
    title: Wikimedia Foundation Terms of Use §7
    accessed: 2026-09-02
  - resource: https://dumps.wikimedia.org/legal.html
    title: Wikimedia dumps legal notice
    accessed: 2026-09-02
---

# Where the verbatim text lives
https://www.gnu.org/licenses/fdl-1.3.txt (SPDX: `GFDL-1.3-only` / `GFDL-1.3-or-later`). Header read 2026-09-02:
> "GNU Free Documentation License / Version 1.3, 3 November 2008 / Copyright (C) 2000, 2001, 2002, 2007, 2008 Free Software Foundation, Inc. / Everyone is permitted to copy and distribute verbatim copies of this license document, but changing it is not allowed."

# Relevant terms
* §2 Verbatim copying: "You may copy and distribute the Document in any medium, either commercially or noncommercially, provided that this License, the copyright notices, and the license notice ... are reproduced in all copies" (first sentence, read 2026-09-02).
* §11 Relicensing defines "CC-BY-SA" as "the Creative Commons Attribution-Share Alike 3.0 license ... as well as future copyleft versions of that license published by that same organization" and let MMC sites relicense before 2009-08-01 — this is the mechanism by which Wikipedia became dual-licensed.
* Wikimedia dumps legal notice: "all original textual content is licensed under the GNU Free Documentation License (GFDL) and the Creative Commons Attribution-Share-Alike 4.0 License".

# How this project uses it
Wikipedia text is offered under CC BY-SA 4.0 **and** GFDL; the reuser may choose. This project redistributes under CC BY-SA 4.0 (simpler attribution, no Invariant Sections/history-section mechanics) and includes `LICENSES/GFDL-1.3.txt` so downstream users retain the choice. The Terms of Use say the GFDL option exists only when text has not been imported under CC BY-SA-only terms — the per-page license is not recorded in the dump, so the README must say "CC BY-SA 4.0; some pages may additionally be available under GFDL".

# Applied to
* [Simple English Wikipedia](/datasets/wikipedia-simple.md)
