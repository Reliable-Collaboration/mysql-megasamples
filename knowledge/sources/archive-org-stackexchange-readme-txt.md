---
type: Source
title: readme.txt in the archive.org Stack Exchange dump (2024-04-01)
description: The dump's own column list per XML file, including the PostHistoryTypeId enumeration and example values.
resource: https://archive.org/download/stackexchange/readme.txt
tags: [source, stackexchange, schema]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://archive.org/download/stackexchange/readme.txt
    title: readme.txt (5,856 bytes, UTF-8 with BOM)
    accessed: 2026-09-02
---

# What was read
The whole file on 2026-09-02 (starts with a UTF-8 BOM).

# Relevant excerpt
"Format: 7zipped"; files and columns:
* Badges.xml: Id, UserId, Name, Date, Class (1 Gold, 2 Silver, 3 Bronze), TagBased
* Comments.xml: Id, PostId, Score, Text, CreationDate, UserDisplayName ("populated if a user has been removed"), UserId
* PostHistory.xml: Id, PostHistoryTypeId (1..38 enumerated), PostId, RevisionGUID, CreationDate, UserId, UserDisplayName, Comment, Text
* PostLinks.xml: Id, CreationDate, PostId, RelatedPostId, LinkTypeId (1 Linked, 3 Duplicate)
* Posts.xml: Id, PostTypeId, ParentId, AcceptedAnswerId, CreationDate, DeletionDate, Score, ViewCount, Body, OwnerUserId, OwnerDisplayName, LastEditorUserId, LastEditorDisplayName, LastEditDate, LastActivityDate, CommunityOwnedDate, ClosedDate, Title, Tags, AnswerCount, CommentCount, FavoriteCount
* Tags.xml: Id, TagName, Count, ExcerptPostId, WikiPostId
* Users.xml: Id, Reputation, CreationDate, DisplayName, EmailHash, ProfileImageUrl, LastAccessDate, WebsiteUrl, Location, Age, AboutMe, Views, UpVotes, DownVotes, AccountId
Example date: "2008-09-15T08:55:03.923". (Votes.xml is not described in this readme; the schema answer covers it.)

# What it was used to decide
Column lists in [Stack Exchange dataset](/datasets/stackexchange.md), cross-checked with the Meta schema answer.
