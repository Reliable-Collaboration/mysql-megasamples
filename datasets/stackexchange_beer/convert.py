#!/usr/bin/env python3
"""beer.stackexchange.com (archive.org 2024-04-02 snapshot) -> MySQL.

Each XML file is a flat list of `<row Attr="..."/>` elements, streamed with lxml's iterparse so the
memory cost does not grow with the file. The column list per table comes from Stack Exchange's own
schema documentation, not from the data: an attribute is optional, so inferring the schema from one
site's dump would give a narrower table than the format allows. The converter checks the other way
round instead -- any attribute in the data that the schema does not list stops the build.

Record: knowledge/datasets/stackexchange.md
"""
import os, sys

from lxml import etree
import py7zr

DATABASE = "stackexchange_beer"
CONTEXT = "/context/stackexchange_beer"
ARCHIVE = "beer.stackexchange.com.7z"

# table -> (xml file, [(attribute, MySQL type)]) in schema-documentation order
TABLES = {
    "posts": ("Posts.xml", [
        ("Id", "INT NOT NULL"), ("PostTypeId", "TINYINT NOT NULL"), ("AcceptedAnswerId", "INT"),
        ("ParentId", "INT"), ("CreationDate", "DATETIME(3) NOT NULL"), ("Score", "INT NOT NULL"),
        ("ViewCount", "INT"), ("Body", "MEDIUMTEXT"), ("OwnerUserId", "INT"),
        ("OwnerDisplayName", "VARCHAR(255)"), ("LastEditorUserId", "INT"),
        ("LastEditorDisplayName", "VARCHAR(255)"), ("LastEditDate", "DATETIME(3)"),
        ("LastActivityDate", "DATETIME(3)"), ("Title", "VARCHAR(512)"), ("Tags", "VARCHAR(1024)"),
        ("AnswerCount", "INT"), ("CommentCount", "INT"), ("FavoriteCount", "INT"),
        ("ClosedDate", "DATETIME(3)"), ("CommunityOwnedDate", "DATETIME(3)"),
        ("ContentLicense", "VARCHAR(16)")]),
    "users": ("Users.xml", [
        ("Id", "INT NOT NULL"), ("Reputation", "INT NOT NULL"),
        ("CreationDate", "DATETIME(3) NOT NULL"), ("DisplayName", "VARCHAR(255)"),
        ("LastAccessDate", "DATETIME(3)"), ("WebsiteUrl", "VARCHAR(512)"),
        ("Location", "VARCHAR(512)"), ("AboutMe", "TEXT"), ("Views", "INT"), ("UpVotes", "INT"),
        ("DownVotes", "INT"), ("ProfileImageUrl", "VARCHAR(512)"), ("EmailHash", "VARCHAR(64)"),
        ("AccountId", "INT")]),
    "comments": ("Comments.xml", [
        ("Id", "INT NOT NULL"), ("PostId", "INT NOT NULL"), ("Score", "INT"), ("Text", "TEXT"),
        ("CreationDate", "DATETIME(3) NOT NULL"), ("UserDisplayName", "VARCHAR(255)"),
        ("UserId", "INT"), ("ContentLicense", "VARCHAR(16)")]),
    "badges": ("Badges.xml", [
        ("Id", "INT NOT NULL"), ("UserId", "INT NOT NULL"), ("Name", "VARCHAR(128)"),
        ("Date", "DATETIME(3) NOT NULL"), ("Class", "TINYINT"), ("TagBased", "TINYINT(1)")]),
    "votes": ("Votes.xml", [
        ("Id", "INT NOT NULL"), ("PostId", "INT NOT NULL"), ("VoteTypeId", "TINYINT NOT NULL"),
        ("UserId", "INT"), ("CreationDate", "DATE NOT NULL"), ("BountyAmount", "INT")]),
    "tags": ("Tags.xml", [
        ("Id", "INT NOT NULL"), ("TagName", "VARCHAR(255)"), ("Count", "INT"),
        ("ExcerptPostId", "INT"), ("WikiPostId", "INT"), ("IsModeratorOnly", "TINYINT(1)"),
        ("IsRequired", "TINYINT(1)")]),
    "postlinks": ("PostLinks.xml", [
        ("Id", "INT NOT NULL"), ("CreationDate", "DATETIME(3) NOT NULL"), ("PostId", "INT NOT NULL"),
        ("RelatedPostId", "INT NOT NULL"), ("LinkTypeId", "TINYINT")]),
    "posthistory": ("PostHistory.xml", [
        ("Id", "INT NOT NULL"), ("PostHistoryTypeId", "TINYINT NOT NULL"),
        ("PostId", "INT NOT NULL"), ("RevisionGUID", "CHAR(36)"),
        ("CreationDate", "DATETIME(3) NOT NULL"), ("UserId", "INT"),
        ("UserDisplayName", "VARCHAR(255)"), ("Comment", "TEXT"), ("Text", "MEDIUMTEXT"),
        ("ContentLicense", "VARCHAR(16)")]),
}
# the enumerations from the schema answer, which the dump encodes only as integers
LOOKUPS = {
    "posttypes": [(1, "Question"), (2, "Answer"), (3, "Orphaned tag wiki"), (4, "Tag wiki excerpt"),
                  (5, "Tag wiki"), (6, "Moderator nomination"), (7, "Wiki placeholder"),
                  (8, "Privilege wiki"), (9, "Article"), (10, "Help article"),
                  (12, "Collection"), (13, "ModeratorQuestionnaireResponse"), (14, "Announcement"),
                  (15, "CollectiveDiscussion"), (17, "CollectiveCollection")],
    "votetypes": [(1, "AcceptedByOriginator"), (2, "UpMod"), (3, "DownMod"), (4, "Offensive"),
                  (5, "Favorite"), (6, "Close"), (7, "Reopen"), (8, "BountyStart"),
                  (9, "BountyClose"), (10, "Deletion"), (11, "Undeletion"), (12, "Spam"),
                  (15, "ModeratorReview"), (16, "ApproveEditSuggestion")],
    "linktypes": [(1, "Linked"), (3, "Duplicate")],
}
BOOLEANS = {"TagBased", "IsModeratorOnly", "IsRequired"}


def tsv(value):
    if value is None:
        return "\\N"
    return (value.replace("\\", "\\\\").replace("\t", "\\t")
            .replace("\n", "\\n").replace("\r", "\\r"))


def write_table(source, dest, columns, table):
    names = [c for c, _ in columns]
    known, rows = set(names), 0
    with open(dest, "w", encoding="utf-8", newline="") as out:
        for _, el in etree.iterparse(source, tag="row"):
            unknown = set(el.attrib) - known
            if unknown:
                sys.exit(f"{table}: attribute(s) {sorted(unknown)} are not in the documented schema")
            values = []
            for name in names:
                v = el.get(name)
                if v is not None and name in BOOLEANS:
                    v = "1" if v.lower() == "true" else "0"
                values.append(tsv(v))
            out.write("\t".join(values) + "\n")
            rows += 1
            el.clear()
            while el.getprevious() is not None:
                del el.getparent()[0]
    return rows


def main():
    downloads, dest = sys.argv[1], sys.argv[2]
    context = os.path.dirname(os.path.abspath(dest))
    with py7zr.SevenZipFile(os.path.join(downloads, ARCHIVE)) as archive:
        archive.extractall(path=context)

    ddl, loads, counts = [], [], {}
    for table, (xml, columns) in TABLES.items():
        source = os.path.join(context, xml)
        counts[table] = write_table(source, os.path.join(context, f"{table}.tsv"), columns, table)
        os.remove(source)
        body = ",\n".join(f"  `{c.lower()}` {t}" for c, t in columns)
        ddl.append(f"CREATE TABLE `{table}` (\n{body},\n  PRIMARY KEY (`id`)\n);")
        names = ", ".join(f"`{c.lower()}`" for c, _ in columns)
        loads.append(f"LOAD DATA LOCAL INFILE '{CONTEXT}/{table}.tsv' INTO TABLE `{table}`\n"
                     f"  CHARACTER SET utf8mb4 ({names});")

    for name, values in LOOKUPS.items():
        ddl.append(f"CREATE TABLE `{name}` (\n  `id` TINYINT NOT NULL,\n"
                   f"  `name` VARCHAR(40) NOT NULL,\n  PRIMARY KEY (`id`)\n);")
        rows = ", ".join(f"({i}, '{n}')" for i, n in values)
        loads.append(f"INSERT INTO `{name}` (`id`, `name`) VALUES {rows};")

    out = [f"""-- beer.stackexchange.com, archive.org snapshot 2024-04-02, prepared by
-- datasets/{DATABASE}/convert.py. Content is CC BY-SA 4.0; attribution travels with the data in
-- each row's content_license column. See datasets/{DATABASE}/LICENSE.
SET NAMES utf8mb4;
SET SESSION foreign_key_checks = 0;
DROP DATABASE IF EXISTS `{DATABASE}`;
CREATE DATABASE `{DATABASE}` DEFAULT CHARACTER SET utf8mb4;
USE `{DATABASE}`;
"""]
    out += ddl
    out.append(f"\n-- {'-' * 60}\n-- data\n")
    out += loads
    out.append(f"""
-- {'-' * 60}
-- indexes and views

CREATE INDEX `ix_posts_owner` ON `posts` (`owneruserid`);
CREATE INDEX `ix_posts_parent` ON `posts` (`parentid`);
CREATE INDEX `ix_posts_type` ON `posts` (`posttypeid`);
CREATE INDEX `ix_posts_creation` ON `posts` (`creationdate`);
CREATE FULLTEXT INDEX `ft_posts_body` ON `posts` (`title`, `body`);
CREATE INDEX `ix_comments_post` ON `comments` (`postid`);
CREATE INDEX `ix_comments_user` ON `comments` (`userid`);
CREATE INDEX `ix_badges_user` ON `badges` (`userid`);
CREATE INDEX `ix_votes_post` ON `votes` (`postid`);
CREATE INDEX `ix_posthistory_post` ON `posthistory` (`postid`);
CREATE INDEX `ix_users_reputation` ON `users` (`reputation`);

CREATE SQL SECURITY INVOKER VIEW `v_questions` AS
SELECT p.`id`, p.`title`, p.`tags`, p.`score`, p.`viewcount`, p.`answercount`,
       p.`creationdate`, u.`displayname` AS `owner`
FROM `posts` p LEFT JOIN `users` u ON u.`id` = p.`owneruserid`
WHERE p.`posttypeid` = 1;

CREATE SQL SECURITY INVOKER VIEW `v_answers` AS
SELECT a.`id`, a.`parentid` AS `question_id`, q.`title` AS `question_title`, a.`score`,
       a.`creationdate`, u.`displayname` AS `owner`,
       q.`acceptedanswerid` = a.`id` AS `is_accepted`
FROM `posts` a JOIN `posts` q ON q.`id` = a.`parentid`
LEFT JOIN `users` u ON u.`id` = a.`owneruserid`
WHERE a.`posttypeid` = 2;

SET SESSION foreign_key_checks = 1;
""")
    open(dest, "w", encoding="utf-8").write("\n".join(out))
    print(f"  . {len(TABLES)} tables, {sum(counts.values()):,} rows: "
          + ", ".join(f"{t} {n:,}" for t, n in counts.items()))
    print(f"  . {len(LOOKUPS)} lookup tables generated from the schema documentation")


if __name__ == "__main__":
    main()
