---
type: Source
title: Meta SE answer 2678 — "Database schema documentation for the public data dump and SEDE" (last edited 2026-03-23)
description: The community-maintained column-by-column schema of the dump XML files, including enumerations and the July 2025 canary-post note.
resource: https://meta.stackexchange.com/questions/2677/database-schema-documentation-for-the-public-data-dump-and-sede/2678#2678
tags:
- source
- stackexchange
- schema
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:25:00Z"
sources:
- resource: https://api.stackexchange.com/2.3/answers/2678?site=meta&filter=withbody
  title: answer body via the Stack Exchange API
  accessed: "2026-09-02"
  version: last edited 2026-03-23T16:06Z; original owner Stu Thompson (community wiki)
---

# What was read
The full answer body on 2026-09-02.

# Relevant excerpt (columns; no SQL types are given — the answer says "Find the exact T-SQL datatype ... in this query: List all Fields in all Tables on SEDE")
* General: "foreign key fields are formatted as links"; "if a column is optional or nullable, when it is NULL, it won't appear as an attribute in data dump / <row ...>".
* **Posts**: Id, PostTypeId (1 Question, 2 Answer, 3 Orphaned tag wiki, 4 Tag wiki excerpt, 5 Tag wiki, 6 Moderator nomination, 7 Wiki placeholder, 8 Privilege wiki, 9 Article, 10 HelpArticle, 12 Collection, 13 ModeratorQuestionnaireResponse, 14 Announcement, 15 CollectiveDiscussion, 17 CollectiveCollection), AcceptedAnswerId (PostTypeId=1), ParentId (PostTypeId=2), CreationDate, DeletionDate (SEDE only, "Column not present on data dump"), Score, ViewCount (nullable), Body ("as rendered HTML, not Markdown"), OwnerUserId ("always -1 for tag wiki entries"), OwnerDisplayName, LastEditorUserId, LastEditorDisplayName, LastEditDate (e.g. 2009-03-05T22:28:34.823), LastActivityDate, Title, Tags, AnswerCount, CommentCount, FavoriteCount, ClosedDate, CommunityOwnedDate, ContentLicense. "starting with the July 2025 data dump, the Posts.xml file will contain 2 artificially generated posts with Id values of 1000000001 & 1000000010. These do not exist in the SEDE database, and can be excluded."
* **Users**: Id, Reputation, CreationDate, DisplayName, LastAccessDate, WebsiteUrl, Location, AboutMe, Views, UpVotes, DownVotes, ProfileImageUrl, EmailHash ("now always NULL"), AccountId ("NULL if the user has hidden this community").
* **Comments**: Id, PostId, Score, Text, CreationDate, UserDisplayName, UserId ("Absent if user has been deleted"), ContentLicense.
* **Badges**: Id, UserId, Name, Date, Class (1 Gold, 2 Silver, 3 Bronze), TagBased.
* **PostHistory**: Id, PostHistoryTypeId (1..66 enumerated; 1-3 initial title/body/tags, 4-6 edits, 7-9 rollbacks, 10-16 close/reopen/delete/undelete/lock/unlock/community-owned, 17 migrated, 18 merged, 19/20 protect, 21 disassociated, 22 unmerged, 24 suggested edit applied, 25 tweeted, 31 moved to chat, 33/34 notices, 35/36 migrated away/here, 37/38 merge source/destination, 50 bumped, 52/53 hot question, 66 Ask Wizard), PostId, RevisionGUID, CreationDate, UserId, UserDisplayName, Comment (CloseReasonId when type 10: old 1,2,3,4,7,10,20; current 101-105), Text ("A raw version of the new value"; JSON of voters for types 10-15,19,20,35), ContentLicense.
* **PostLinks**: Id, CreationDate, PostId, RelatedPostId, LinkTypeId (1 Linked, 3 Duplicate).
* **Tags**: Id, TagName, Count, ExcerptPostId, WikiPostId, IsModeratorOnly, IsRequired.
* **Votes**: Id, PostId, VoteTypeId (-1 InformModerator, 0 UndoMod, 1 AcceptedByOriginator, 2 UpMod, 3 DownMod, 4 Offensive, 5 Favorite, 6 Close, 7 Reopen, 8 BountyStart, 9 BountyClose, 10 Deletion, 11 Undeletion, 12 Spam, 15 ModeratorReview, 16 ApproveEditSuggestion, 17-28 reactions (Teams), 18 Helpful, 19 ThankYou, 20 WellWritten, 21 Follow, 29 Outdated, 30 NotOutdated, 31 PreVote, 32/33 collective discussion, 35-37 privateAiAnswer*), UserId ("present only if VoteTypeId in (5,8); -1 if user is deleted"), CreationDate ("Date only ... time data is purposefully removed to protect user privacy"), BountyAmount (types 8, 9).
* SEDE-only tables (not in the dump): PostsWithDeleted, CloseAsOffTopicReasonTypes, PendingFlags, PostFeedback, PostNotices, PostNoticeTypes, PostTags, ReviewRejectionReasons, ReviewTaskResults, ReviewTasks, SuggestedEdits, SuggestedEditVotes, TagSynonyms, *Types, sede_* views.

# What it was used to decide
Column set and enumerations in [Stack Exchange dataset](/datasets/stackexchange.md); canary handling in [Stack Exchange XML parsing](/tools/stackexchange-xml-parsing.md).
