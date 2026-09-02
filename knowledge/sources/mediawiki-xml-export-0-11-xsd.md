---
type: Source
title: MediaWiki XML export schema 0.11 (export-0.11.xsd)
description: The XSD that defines the pages-articles dump structure — page, revision, contributor, text and slot elements.
resource: https://www.mediawiki.org/xml/export-0.11.xsd
tags: [source, mediawiki, xml, schema]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://www.mediawiki.org/xml/export-0.11.xsd
    title: export-0.11.xsd (11,677 bytes)
    accessed: "2026-09-02"
---

# What was read
The full XSD on 2026-09-02.

# Relevant excerpt
* Types: MediaWikiType, SiteInfoType, NamespacesType, PageType, RevisionType, ContributorType, TextType, ContentType, UploadType, LogItemType, DiscussionThreadingInfo, ...
* `PageType`: `title` ("Title in text form. (Using spaces, not underscores; with namespace)"), `ns`, `id`, optional `redirect` (attribute `title`), optional `restrictions`, then zero or more `revision` | `upload`, optional `discussionthreadinginfo`.
* `RevisionType`: `id`, optional `parentid`, `timestamp` (xs:dateTime), `contributor` (username+id, or ip, or `deleted="deleted"`), optional `minor`, optional `comment`, `origin` ("corresponds to slot origin for the main slot"), `model`, `format`, `text` (TextType with `bytes`, `sha1`, `deleted`, `space="preserve"`), zero or more `content` (additional slots), `sha1` ("a combined sha1 of content in all slots").
* Namespace: `http://www.mediawiki.org/xml/export-0.11/`.

# What it was used to decide
Field mapping in [MediaWiki dump parsing](/tools/mediawiki-xml-dump-parsing.md) and the synthesized revision/text tables in [Simple English Wikipedia dataset](/datasets/wikipedia-simple.md).
