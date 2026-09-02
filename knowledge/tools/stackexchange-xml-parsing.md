---
type: Tool
title: Stack Exchange data dump XML parsing (streaming iterparse; own MySQL loader)
description: How the per-site 7z archives of `<row .../>` XML files are read and loaded into MySQL, and what existing converters teach us.
resource: https://github.com/Networks-Learning/stackexchange-dump-to-postgres
tags: [tool, stackexchange, xml, python, mysql-load, text-group]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://github.com/Networks-Learning/stackexchange-dump-to-postgres
    title: stackexchange-dump-to-postgres README and GitHub API repo metadata
    accessed: 2026-09-02
    version: master, pushed 2026-04-21, MIT, 92 stars
  - resource: https://archive.org/download/stackexchange/readme.txt
    title: readme.txt in the archive.org dump item
    accessed: 2026-09-02
  - resource: https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede/2678#2678
    title: Database schema documentation for the public data dump and SEDE (answer 2678, last edited 2026-03-23)
    accessed: 2026-09-02
    version: read via api.stackexchange.com /answers/2678?filter=withbody
  - resource: https://meta.stackexchange.com/questions/402153/latest-data-dump-has-invalid-xml-and-invalid-characters
    title: Latest Data Dump has invalid XML and invalid characters (2024-08-14)
    accessed: 2026-09-02
  - resource: https://meta.stackexchange.com/questions/402501/data-dumps-updates-and-bug-fixes
    title: Data Dumps - updates and bug fixes (2024-08-29)
    accessed: 2026-09-02
---

# Input shape (verified)
* archive.org item description: "Each site is formatted as a separate archive consisting of XML files zipped via 7-zip using bzip2 compression. Each site archive includes Posts, Users, Votes, Comments, Badges, Tags, PostHistory, and PostLinks." (Stack Overflow itself is split into `stackoverflow.com-Posts.7z` etc.)
* Each XML file is a single root element (e.g. `<posts>`) containing one `<row .../>` element per record with **attributes only**; per the schema answer: "if a column is optional or nullable, when it is NULL, it won't appear as an attribute in data dump / <row ...>". Dates are ISO `2009-03-05T22:28:34.823` (millisecond precision, no zone; SEDE is UTC). `Body` is rendered HTML; `PostHistory.Text` is raw Markdown; `Tags` is `<tag1><tag2>` (XML-escaped as `&lt;tag1&gt;`).
* Encoding UTF-8. Entities: standard XML escapes plus numeric `&#x...;` references.

# Parsing approach (chosen)
* Python `xml.etree.ElementTree.iterparse(fh, events=("end",))`, keep only `elem.tag == "row"`, read `elem.attrib`, then `elem.clear()`; `lxml.etree.iterparse` is a drop-in speed-up (2-3x, **Inferred**). Extract with `7z x` or stream with `py7zr`; the 7z uses bzip2 so extraction is CPU-bound.
* Load via `LOAD DATA LOCAL INFILE` from TSV written per table (bodies contain newlines/tabs → escape) or batched INSERTs. Disable secondary indexes and FULLTEXT during load; add afterwards.
* Column-to-type mapping comes from the schema answer (see [dataset record](/datasets/stackexchange.md)); attributes missing on a row → SQL NULL.

# Known hazards (verified in Meta posts)
* **Invalid XML in the 2024-Q2 (July 2024) dumps**: "numerous escape sequences that are simply invalid XML such as &#x1E or even &#x00" and an escape for a non-Unicode code point (Meta 402153). Staff response (Meta 402501, 2024-08-29): "Reverted to C# for producing XML to avoid illegal characters SQL Server misses" and the Q2 files were regenerated. The archive.org 2024-04-02 dump predates this bug; still wrap the reader in a byte-level filter that replaces `&#x0;`..`&#x1F;` (except tab/LF/CR) with a space, as the community `CleaningStreamReader` does.
* Since 2024-Q2 regenerated dumps: GUIDs lower-cased, `ViewCount` omitted on answers, `license.txt` and `sede-and-data-dump-schema.md` inside each .7z, `stackoverflow.com.7z` contains XML directly. `Sites.xml` is no longer present (Meta 404002, not opened; title only from tag listing).
* **Canary rows** from the July 2025 dump onward: Posts.xml carries two fabricated posts with `Id` 1000000001 and 1000000010 (schema answer; Meta 412018) — delete `WHERE Id >= 1000000000` if a post-2025 dump is ever used.

# Existing converter (reviewed, not reused)
`Networks-Learning/stackexchange-dump-to-postgres` (MIT, Python, `lxml` + `psycopg2-binary`, README says it loads "Badges, Posts, Tags, Users, Votes, PostLinks, PostHistory, and Comments" and that "The Body field in Posts table is NOT populated by default" without `--with-post-body`; `ViewCount` empty strings → NULL). It targets PostgreSQL and its column list predates `ContentLicense`; we write our own MySQL loader (~200 lines) and keep its table/column naming for familiarity.
