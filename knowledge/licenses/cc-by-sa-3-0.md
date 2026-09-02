---
type: License
title: Creative Commons Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)
description: Copyleft data/content license used by the Employees (test_db) and Lahman Baseball databases; requires attribution and same-license redistribution of adaptations.
resource: https://creativecommons.org/licenses/by-sa/3.0/legalcode
tags: [license, cc-by-sa-3-0, share-alike, attribution]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://creativecommons.org/licenses/by-sa/3.0/legalcode
    title: Attribution-ShareAlike 3.0 Unported - Legal Code
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/datacharmer/test_db/master/README.md
    title: test_db README LICENSE section
    accessed: 2026-09-02
  - resource: https://sabr.app.box.com/public/static/qtgh1olzcaauz5x234wqx8huixizff8l.txt
    title: SABR Lahman readme 2025, section 0.1
    accessed: 2026-09-02
---

# Where the text lives
Full legal code: https://creativecommons.org/licenses/by-sa/3.0/legalcode (title line "Attribution-ShareAlike 3.0 Unported"). Human-readable deed: https://creativecommons.org/licenses/by-sa/3.0/.

# Key clauses (verbatim, Section 4 "Restrictions")
* 4(a): "You may Distribute or Publicly Perform the Work only under the terms of this License. You must include a copy of, or the Uniform Resource Identifier (URI) for, this License with every copy of the Work You Distribute or Publicly Perform."
* 4(b): "You may Distribute or Publicly Perform an Adaptation only under: (i) the terms of this License; (ii) a later version of this License with the same License Elements as this License; (iii) a Creative Commons jurisdiction license ..." (share-alike).
* 4(c): "If You Distribute, or Publicly Perform the Work or any Adaptations or Collections, You must ... keep intact all copyright notices for the Work and provide, reasonable to the medium or means You are utilizing: (i) the name of the Original Author ..." (attribution; also the title, the URI the licensor specifies, and for Adaptations a credit identifying the use).

# Obligations for this project
* Ship the license URI and the upstream notice alongside each converted database (README section per dataset, and a `LICENSE-*.txt` in the repo).
* A MySQL conversion of the data is an Adaptation: it must be offered under CC BY-SA 3.0 (or later BY-SA) - it cannot be relicensed; the project's own repository license must carve these datasets out.
* Keep the "fabricated data" disclaimer for Employees and SABR's copyright line for Lahman intact.

# Applied to
* [Employees (test_db)](/datasets/employees.md) - notice: "This work is licensed under the Creative Commons Attribution-Share Alike 3.0 Unported License." Attribution: original data by Fusheng Wang and Carlo Zaniolo (Siemens Corporate Research); schema by Giuseppe Maxia; conversion by Patrick Crews; "Copyright (C) 2007,2008, MySQL AB".
* [Lahman Baseball Database](/datasets/lahman.md) - notice: "This database is copyright 1996-2025 by SABR, via generious donation from Sean Lahman. This work is licensed under a Creative Commons Attribution-ShareAlike 3.0 Unported License."
