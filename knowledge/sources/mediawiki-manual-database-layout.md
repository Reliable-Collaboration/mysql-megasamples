---
type: Source
title: MediaWiki Manual:Database layout
description: Overview of the core tables (page, revision, text, actor, user) and the link tables, and where the schema source lives.
resource: https://www.mediawiki.org/wiki/Manual:Database_layout
tags: [source, mediawiki, schema]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://www.mediawiki.org/wiki/Manual:Database_layout
    title: Manual:Database layout (diagram for 1.41.0)
    accessed: 2026-09-02
---

# What was read
The manual page on 2026-09-02.

# Relevant excerpt
* Core tables: page, revision, text, actor, user. Link tables: pagelinks, categorylinks, templatelinks, imagelinks, externallinks, langlinks, iwlinks, redirect, linktarget.
* "The SQL code that creates the MySQL/MariaDB core tables for any MediaWiki version is in the sql/tables.json source file." (before 1.35: maintenance/tables.sql); as of 1.44 schema files moved to a top-level `sql` directory with generated MySQL/SQLite/PostgreSQL variants.

# What it was used to decide
Which tables to model in [Simple English Wikipedia dataset](/datasets/wikipedia-simple.md).
