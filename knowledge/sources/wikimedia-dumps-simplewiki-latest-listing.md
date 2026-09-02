---
type: Source
title: dumps.wikimedia.org/simplewiki/latest/ directory listing (snapshot 20260901)
description: Exact file names, sizes and dates of the current Simple English Wikipedia dump, including every published .sql.gz table.
resource: https://dumps.wikimedia.org/simplewiki/latest/
tags: [source, wikipedia, size-evidence]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
stale_after: 2026-10-05
sources:
  - resource: https://dumps.wikimedia.org/simplewiki/latest/
    title: latest/ listing (symlinks to 20260901)
    accessed: 2026-09-02
  - resource: https://dumps.wikimedia.org/simplewiki/
    title: "simplewiki/ dated directories (monthly: 20260101 ... 20260901, latest/ dated 02-Sep-2026 01:53)"
    accessed: 2026-09-02
  - resource: https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-pages-articles.xml.bz2
    title: HEAD request — Content-Length 356186307, Last-Modified Tue, 01 Sep 2026 20:27:10 GMT
    accessed: 2026-09-02
---

# What was read
The directory listing (curl) on 2026-09-02; the `latest/` directory mirrors the 20260901 run (monthly full runs on the 1st; the dated `simplewiki/` index shows one directory per month in 2026).

# Relevant excerpt (bytes, 01-Sep-2026 unless noted)
XML: `pages-articles.xml.bz2` **356,186,307**; `pages-meta-current.xml.bz2` 483,314,097; `pages-meta-history.xml.bz2` 4,327,256,004 (02-Sep); `pages-meta-history.xml.7z` 1,655,125,198; `stub-articles.xml.gz` 64,051,767; `stub-meta-current.xml.gz` 106,973,125; `stub-meta-history.xml.gz` 902,130,820; `pages-logging.xml.gz` 141,263,357.
SQL (`simplewiki-latest-<table>.sql.gz`): page 33,064,269; categorylinks 28,305,762; pagelinks 82,424,067; linktarget 37,519,370; redirect 1,463,928; category 1,199,048; page_props 10,703,331; page_restrictions 31,585; protected_titles 25,008; templatelinks 44,014,629; imagelinks 5,500,169; image 4,916; externallinks 55,707,558; langlinks 122,267,466; iwlinks 3,598,049; change_tag 56,368,073; change_tag_def 3,070; geo_tags 1,202,882; site_stats 862; sites 24,012; user_groups 3,790; user_former_groups 3,121; babel 7,451; wbc_entity_usage 9,941,196.
Other: `md5sums.txt` 2,858; `sha1sums.txt` 3,162; `all-titles-in-ns0.gz` 2,450,403; `all-titles.gz` 5,906,605; `siteinfo-namespaces.json.gz` 5,225.
**Not published as SQL:** `revision`, `text`, `slots`, `content`, `actor`, `comment`, `user` — page text and revision metadata exist only in the XML files.

# What it was used to decide
Source artifact, table selection and size estimates in [Simple English Wikipedia dataset](/datasets/wikipedia-simple.md).
