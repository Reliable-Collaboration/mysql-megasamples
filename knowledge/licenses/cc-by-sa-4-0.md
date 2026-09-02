---
type: License
title: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
description: Share-alike copyleft license for content; applied to Stack Exchange posts contributed on or after 2018-05-02 and to Wikipedia text (dual-licensed with GFDL).
resource: https://creativecommons.org/licenses/by-sa/4.0/legalcode
tags:
- license
- cc-by-sa
- share-alike
- attribution
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://creativecommons.org/licenses/by-sa/4.0/legalcode
  title: CC BY-SA 4.0 legal code
  accessed: "2026-09-02"
- resource: https://stackoverflow.com/help/licensing
  title: Stack Overflow help - Licensing
  accessed: "2026-09-02"
- resource: https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use
  title: Wikimedia Foundation Terms of Use (effective 2023-06-07)
  accessed: "2026-09-02"
---

# Where the text lives
Legal code: https://creativecommons.org/licenses/by-sa/4.0/legalcode (SPDX: `CC-BY-SA-4.0`). Ship the full legal code as `LICENSES/CC-BY-SA-4.0.txt` in the repository; the deed summary is not the license.

# Obligations that bind this project (verbatim, from the legal code read on 2026-09-02)
Section 3(a)(1) — when Sharing the Licensed Material (including in adapted form) you must retain, if supplied by the Licensor:
> "identification of the creator(s) of the Licensed Material and any others designated to receive attribution"; "a copyright notice"; "a notice that refers to this Public License"; "a notice that refers to the disclaimer of warranties"; "a URI or hyperlink to the Licensed Material to the extent reasonably practicable"

plus an indication of modifications made and a statement that the material is licensed under this Public License.

Section 3(b) — ShareAlike: the Adapter's License you apply to your contributions to Adapted Material
> "must be a Creative Commons license with the same License Elements, this version or later, or a BY-SA Compatible License."

Section 1(a) defines Adapted Material as
> "material subject to Copyright and Similar Rights that is derived from or based upon the Licensed Material"

# How this project complies
* A MySQL conversion of CC BY-SA text is at minimum a Share of the Licensed Material and arguably Adapted Material (the compilation/format is changed; the text itself is not). The converted database and its loader scripts for these datasets are therefore released under CC BY-SA 4.0 (not the repository's code license), and the README says so.
* Attribution is carried per row rather than per file: keep the columns that identify authors (Stack Exchange `OwnerUserId`/`OwnerDisplayName`, `ContentLicense`; MediaWiki `revision.rev_actor` / contributor username) and the row identifiers that let a consumer build the hyperlink (`posts.Id` → `https://<site>/q/<Id>`; `page.page_title` → `https://simple.wikipedia.org/wiki/<title>`).
* Indicate modifications: the README states "converted from XML/SQL dumps to MySQL tables; HTML/wikitext bodies unchanged; canary rows removed" (see dataset records).

# Attribution
Ship the CC BY-SA 4.0 legal code, credit per section 3(a)(1) (creator, copyright notice, license link, indication of modifications) and release the adaptation under the same license. Wording used for Wikipedia: "Text from Simple English Wikipedia (https://simple.wikipedia.org/), dump 2026-09-01, licensed CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/) and GFDL; attribution to the article's contributors via each article's page history link; converted to MySQL by this project." For Stack Exchange posts on or after 2018-05-02: "Content from <site>.stackexchange.com, licensed CC BY-SA 4.0; each post retains its Id, OwnerUserId and author display name so it can be linked and attributed as https://<site>.stackexchange.com/q/<Id> and https://<site>.stackexchange.com/users/<OwnerUserId>."

# Applied to
* [Stack Exchange data dump](/datasets/stackexchange.md) — posts created on or after 2018-05-02 UTC (per-row `ContentLicense` column says which version applies to each post).
* [Simple English Wikipedia](/datasets/wikipedia-simple.md) — all article text, dual-licensed with [GFDL 1.3](/licenses/gfdl-1-3.md); attribution methods per Wikimedia Terms of Use §7.
* [Wikidata](/datasets/wikidata.md) — only non-structured text namespaces (talk, project pages); entity data is [CC0](/licenses/cc0-1-0.md).
