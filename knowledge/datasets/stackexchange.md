---
type: Dataset
title: Stack Exchange data dump (per-site; dba.stackexchange.com primary)
description: CC BY-SA XML dump of a Stack Exchange Q&A site (Posts, Users, Comments, Votes, Badges, Tags, PostLinks, PostHistory) converted to MySQL with FULLTEXT; sourced from the last public archive.org snapshot (2024-04-02) to avoid the 2024 click-through.
resource: https://archive.org/details/stackexchange
tags:
- tier-core
- tier-extended
- dataset
- text-corpus
- qa
- cc-by-sa
- licensing-finding
- text-group
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
stale_after: "2027-03-01"
sources:
- resource: https://archive.org/details/stackexchange
  title: Stack Exchange Data Dump item
  accessed: "2026-09-02"
- resource: https://archive.org/metadata/stackexchange
  title: item metadata (sizes, md5, mtimes)
  accessed: "2026-09-02"
  version: snapshot 2024-04-02, files 2024-04-06/07
- resource: https://archive.org/download/stackexchange/readme.txt
  title: dump readme.txt
  accessed: "2026-09-02"
- resource: https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede/2678#2678
  title: schema documentation answer (edited 2026-03-23)
  accessed: "2026-09-02"
- resource: https://stackoverflow.com/help/data-dumps
  title: Help Center data dumps
  accessed: "2026-09-02"
- resource: https://stackoverflow.com/help/licensing
  title: Help Center licensing
  accessed: "2026-09-02"
- resource: https://meta.stackexchange.com/questions/401324/announcing-a-change-to-the-data-dump-process
  title: 2024 process-change announcement
  accessed: "2026-09-02"
- resource: https://api.stackexchange.com/2.3/info?site=dba
  title: live totals for dba / datascience
  accessed: "2026-09-02"
---

# Identity
Stack Exchange Data Dump, one database per site. Proposed names: **`stackexchange_dba`** (dba.stackexchange.com, extended), **`stackexchange_beer`** (beer.stackexchange.com, core smoke-test — or `stackexchange_coffee`; both < 6 MB compressed). Rule: `stackexchange_` + host with `.stackexchange.com` removed and remaining dots replaced by `_` (`serverfault.com` → `stackexchange_serverfault_com`).

# Source artifact
* **Chosen:** archive.org item `stackexchange` ([details](/sources/archive-org-stackexchange-item.md), [metadata](/sources/archive-org-stackexchange-metadata-json.md)) — snapshot "2024-04-02", last file 2024-04-07, uploader team+datadump@stackexchange.com, item license URL CC BY-SA 4.0, no login or click-through. Per-file:
  * `https://archive.org/download/stackexchange/dba.stackexchange.com.7z` — 319,345,462 bytes, md5 `d0f417b3c3c9210ed32623a071651411`
  * `https://archive.org/download/stackexchange/datascience.stackexchange.com.7z` — 89,531,447 bytes, md5 `e9362d731c9180ea384236dabbe0b939` (alternative mid-size site)
  * `https://archive.org/download/stackexchange/beer.stackexchange.com.7z` — 4,317,770 bytes, md5 `5da8bd0067af280aeb53ebfd6b5e650d`; `coffee.stackexchange.com.7z` 5,095,298, md5 `458d102b0d9083a5c0d53031f4b03af7`
  * plus `readme.txt` and `license.txt`.
* **Current official channel (not used):** since 2024-08-14 dumps are quarterly per-site downloads from the user's profile page ("Data dump access"), login required, with a checkbox "affirming that you do not intend to use the file for LLM training" ([help](/sources/stackoverflow-help-data-dumps.md)); "Stack Overflow is no longer uploading the data dump to archive.org" ([announcement](/sources/meta-stackexchange-401324-data-dump-process-change.md)). Dumps still ship: Q2-2026 files were posted 2026-07-03 ([Meta 419305](/sources/meta-stackexchange-419305-q2-2026-eta.md)). No checksum-in-download; SHA256 lists are posted on Meta ([402501](/sources/meta-stackexchange-402501-data-dump-updates.md)). Full-network dumps are not obtainable ([412203](/sources/meta-stackexchange-412203-full-dump-requests.md)).
* Why the 2024-04 snapshot: it pre-dates the click-through, the July 2024 invalid-XML bug, and the July 2025 watermark rows; it is the newest copy anyone can redistribute without having personally accepted the LLM clause. See the [licensing finding](/licenses/stackexchange-data-dump-terms.md) and [decision](/decisions/stackexchange-conversion-path.md).

# Native format and friendlier forms
7z (bzip2) archive per site containing `Badges.xml, Comments.xml, PostHistory.xml, PostLinks.xml, Posts.xml, Tags.xml, Users.xml, Votes.xml` ([readme](/sources/archive-org-stackexchange-readme-txt.md)). Each file: one root element with `<row .../>` children, attributes only, NULL = attribute absent, dates `YYYY-MM-DDTHH:MM:SS.mmm`, UTF-8. No SQL/CSV form exists; SEDE (data.stackexchange.com) is a live T-SQL mirror, not a download.

# Shape
Columns per the [schema answer](/sources/meta-stackexchange-2678-schema-documentation.md) (no SQL types are published; types below are this project's proposal):
* **posts**: Id INT PK · PostTypeId TINYINT · AcceptedAnswerId INT NULL · ParentId INT NULL · CreationDate DATETIME(3) · Score INT · ViewCount INT NULL · Body MEDIUMTEXT (rendered HTML) · OwnerUserId INT NULL · OwnerDisplayName VARCHAR(255) NULL · LastEditorUserId INT NULL · LastEditorDisplayName VARCHAR(255) NULL · LastEditDate DATETIME(3) NULL · LastActivityDate DATETIME(3) · Title VARCHAR(512) NULL · Tags VARCHAR(1024) NULL (`<tag1><tag2>`) · AnswerCount INT NULL · CommentCount INT NULL · FavoriteCount INT NULL · ClosedDate DATETIME(3) NULL · CommunityOwnedDate DATETIME(3) NULL · ContentLicense VARCHAR(16). (DeletionDate is SEDE-only.)
* **users**: Id INT PK (−1 = Community) · Reputation INT · CreationDate · DisplayName VARCHAR(255) · LastAccessDate · WebsiteUrl VARCHAR(512) · Location VARCHAR(512) · AboutMe TEXT · Views INT · UpVotes INT · DownVotes INT · ProfileImageUrl VARCHAR(512) · EmailHash VARCHAR(64) NULL (always absent now) · AccountId INT NULL.
* **comments**: Id INT PK · PostId INT · Score INT · Text TEXT · CreationDate · UserDisplayName VARCHAR(255) NULL · UserId INT NULL · ContentLicense.
* **badges**: Id INT PK · UserId INT · Name VARCHAR(128) · Date DATETIME(3) · Class TINYINT (1 gold, 2 silver, 3 bronze) · TagBased BOOL.
* **votes**: Id INT PK · PostId INT · VoteTypeId TINYINT · UserId INT NULL (only types 5, 8) · CreationDate DATE (time removed upstream) · BountyAmount INT NULL.
* **tags**: Id INT PK · TagName VARCHAR(255) · Count INT · ExcerptPostId INT NULL · WikiPostId INT NULL · IsModeratorOnly BOOL · IsRequired BOOL.
* **postlinks**: Id INT PK · CreationDate · PostId INT · RelatedPostId INT · LinkTypeId TINYINT (1 linked, 3 duplicate).
* **posthistory**: Id INT PK · PostHistoryTypeId TINYINT · PostId INT · RevisionGUID CHAR(36) · CreationDate · UserId INT NULL · UserDisplayName VARCHAR(255) NULL · Comment TEXT · Text MEDIUMTEXT (raw Markdown; JSON for vote events) · ContentLicense.
* Lookup tables generated from the schema answer's enumerations: `posttypes`, `votetypes`, `posthistorytypes`, `linktypes`, `closereasontypes`.
* Row counts for the 2024-04-02 dba dump are not published; live 2026-09-02 totals are upper bounds: questions 105,698; answers 142,723; users 321,367; comments 472,821; votes 823,419; badges 458,592 ([API](/sources/stackexchange-api-info-dba-datascience.md)). PostHistory is typically the largest table (several rows per post). Baseline = `grep -c "<row " <file>.xml` per file, recorded at first build ([question](/questions/stackexchange-dump-row-counts-2024-04.md)).
* Encoding hazards: utf8mb4 required (DisplayName/Body contain emoji and CJK; some tags are non-ASCII — Meta 416467 title); HTML entities inside attribute values are XML-escaped (`&lt;p&gt;`); newlines inside `Body`. The 2024-Q2 profile dumps had invalid control-character references — not this snapshot, but the reader filters them anyway ([tool](/tools/stackexchange-xml-parsing.md)).

# Conversion path
Own Python streaming loader (`iterparse` → TSV → `LOAD DATA LOCAL INFILE`), modelled on but not reusing Networks-Learning/stackexchange-dump-to-postgres ([source](/sources/github-networks-learning-stackexchange-dump-to-postgres.md)). See [decision](/decisions/stackexchange-conversion-path.md).

# Type-mapping hazards
* Attribute absence → NULL; booleans are the strings `True`/`False`; `Votes.CreationDate` has no time component → `DATE`.
* `Users.Id = -1` (Community) is referenced by posts; do not enforce FKs, or insert a sentinel user first. Posts of deleted users have no `OwnerUserId` (only `OwnerDisplayName`).
* `Tags` attribute on old dumps may omit tags starting with `.` (Meta 406864, title only) — do not derive `posttags` from it as a test oracle.
* `Body` HTML retains `<code>` blocks with entities; FULLTEXT will index HTML tag names — acceptable for a sample; document it.
* If ever built from a ≥ July 2025 dump: `DELETE FROM posts WHERE Id >= 1000000000` (watermark rows, [Meta 412018](/sources/meta-stackexchange-412018-fabricated-posts.md)).

# Programmable objects
None in the dump (SEDE views/procedures are not exported). We add views `v_questions`, `v_answers`, `v_question_with_accepted_answer`; no triggers.

# Indexing
PKs on Id; `posts(ParentId)`, `posts(OwnerUserId)`, `posts(PostTypeId, CreationDate)`, `posts(AcceptedAnswerId)`; `comments(PostId)`; `votes(PostId, VoteTypeId)`; `badges(UserId)`; `posthistory(PostId)`, `posthistory(RevisionGUID)`; `postlinks(PostId)`, `postlinks(RelatedPostId)`; `tags(TagName)` UNIQUE. `FULLTEXT posts(Title, Body)`, `FULLTEXT users(AboutMe)`, `FULLTEXT comments(Text)`.

# Tests and expected values
* md5 of each downloaded `.7z` equals the archive.org value above.
* Per table `COUNT(*)` = `<row` count of the XML file (recorded baseline).
* Every `posts.parentid` points to a `posttypeid=1` row; every `acceptedanswerid` points to a row whose `parentid` is the question; `MAX(id) < 1000000000`.
* `SELECT DISTINCT contentlicense` ⊆ {'CC BY-SA 2.5','CC BY-SA 3.0','CC BY-SA 4.0'}.

# Tier assignment
* `stackexchange_dba`: **extended** — 319 MB 7z; **Inferred:** ~2.2-2.8 GB of XML and 2-3 GB in InnoDB with FULLTEXT (bzip2 on XML ≈ 7-8×).
* `stackexchange_beer` (or coffee): **core** — 4.3 MB 7z; **Inferred:** < 40 MB loaded. `datascience` (89.5 MB) is the fallback if dba is judged too slow to load.

# License and attribution
[CC BY-SA 4.0](/licenses/cc-by-sa-4-0.md) for posts on/after 2018-05-02, [CC BY-SA 3.0](/licenses/cc-by-sa-3-0.md) 2011-04-08..2018-05-01, CC BY-SA 2.5 before ([help/licensing](/sources/stackoverflow-help-licensing.md)); per-row `ContentLicense`. Contractual layer and the finding: [Stack Exchange data dump terms](/licenses/stackexchange-data-dump-terms.md). README wording (from `license.txt`/2009 blog): "Content from dba.stackexchange.com (Stack Exchange Data Dump, snapshot 2024-04-02, https://archive.org/details/stackexchange), licensed under CC BY-SA (2.5/3.0/4.0 per post, see the ContentLicense column). Each row's `Id` links to https://dba.stackexchange.com/q/<Id> (questions) or /a/<Id> (answers) and each author to https://dba.stackexchange.com/users/<OwnerUserId>; reusers must show author names, link posts and profiles directly, indicate changes, and share alike. Converted to MySQL by this project; HTML bodies unchanged." Share-alike: the converted database is distributed under CC BY-SA 4.0.

# Open questions
* [Row counts of the 2024-04-02 dba dump](/questions/stackexchange-dump-row-counts-2024-04.md)
* [Will the archive.org item persist / should the project mirror the two .7z files](/questions/stackexchange-archive-org-item-persistence.md)
