#!/usr/bin/env python3
"""Simple English Wikipedia (dump run 20260901) -> MySQL, as a deterministic article sample.

The sample is the rule the record states: the **5,000 lowest page_id non-redirect articles in
namespace 0**, their text, and the link rows among them. Nothing is chosen by hand, so the same dump
always produces the same database.

The seven `.sql.gz` files are MariaDB `mysqldump` output that MySQL 9.7 accepts unchanged -- every
construct was tried on the target server before this was written -- so their `CREATE TABLE` is used
verbatim and only the rows are filtered. `revision` and `text` are synthesized from the XML, which is
the only place the wikitext exists.

Record: knowledge/datasets/wikipedia-simple.md
"""
import bz2, os, sys

from lxml import etree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sqldump  # noqa: E402

DATABASE = "wikipedia_simple"
PREFIX = "simplewiki-20260901-"
SAMPLE = 5000
MW = "{http://www.mediawiki.org/xml/export-0.11/}"


def tsv(value):
    if value is None:
        return "\\N"
    return (str(value).replace("\\", "\\\\").replace("\t", "\\t")
            .replace("\n", "\\n").replace("\r", "\\r"))


def read_articles(path, context, sample=SAMPLE):
    """The sample, written straight out as revision and text rows; returns the page ids kept."""
    kept, previous, out_of_order = [], 0, 0
    revision = open(os.path.join(context, "revision.tsv"), "w", encoding="utf-8", newline="")
    text = open(os.path.join(context, "text.tsv"), "w", encoding="utf-8", newline="")
    with bz2.open(path, "rb") as fh:
        for _, page in etree.iterparse(fh, tag=f"{MW}page"):
            ns = page.findtext(f"{MW}ns")
            page_id = int(page.findtext(f"{MW}id"))
            redirect = page.find(f"{MW}redirect") is not None
            if page_id < previous:
                out_of_order += 1
            previous = page_id
            if ns == "0" and not redirect and (sample is None or len(kept) < sample):
                rev = page.find(f"{MW}revision")
                body = rev.findtext(f"{MW}text") or ""
                kept.append(page_id)
                revision.write("\t".join(tsv(v) for v in [
                    int(rev.findtext(f"{MW}id")), page_id,
                    rev.findtext(f"{MW}parentid"),
                    (rev.findtext(f"{MW}timestamp") or "").replace("T", " ").rstrip("Z"),
                    1 if rev.find(f"{MW}minor") is not None else 0,
                    len(body.encode("utf-8")), rev.findtext(f"{MW}sha1"),
                    rev.findtext(f"{MW}contributor/{MW}id"),
                    rev.findtext(f"{MW}contributor/{MW}username")
                    or rev.findtext(f"{MW}contributor/{MW}ip"),
                    rev.findtext(f"{MW}comment"), rev.findtext(f"{MW}model"),
                ]) + "\n")
                text.write(f"{tsv(int(rev.findtext(f'{MW}id')))}\t{tsv(body)}\n")
            page.clear()
            while page.getprevious() is not None:
                del page.getparent()[0]
            if sample is not None and len(kept) >= sample:
                break                      # the dump is in ascending page_id order (checked above)
    revision.close(); text.close()
    return kept, out_of_order


def filter_dump(downloads, context, name, table, key_index, keep, extra=None):
    """Copy one dumped table's CREATE plus the rows whose key column is in `keep`."""
    path = os.path.join(downloads, f"{PREFIX}{name}.sql.gz")
    create = sqldump.create_table(path)
    written, collected = 0, set()
    # the dumps' varbinary columns hold bytes that are not valid UTF-8, read with surrogateescape;
    # writing them back the same way reproduces the upstream bytes exactly, which is what a
    # CHARSET=binary column expects
    with open(os.path.join(context, f"{table}.sql"), "w", encoding="utf-8",
              errors="surrogateescape") as out:
        out.write(create + "\n")
        batch = []
        for _, row in sqldump.rows(path):
            if key_index is not None:
                try:
                    key = int(sqldump.fields(row)[key_index])
                except ValueError:
                    continue
                if key not in keep:
                    continue
                if extra is not None:
                    collected.add(int(sqldump.fields(row)[extra]))
            batch.append(row)
            written += 1
            if len(batch) >= 500:
                out.write(f"INSERT INTO `{table}` VALUES " + ",".join(batch) + ";\n")
                batch = []
        if batch:
            out.write(f"INSERT INTO `{table}` VALUES " + ",".join(batch) + ";\n")
    return written, collected


def main():
    downloads, dest = sys.argv[1], sys.argv[2]
    full = "--full" in sys.argv[3:]
    database = "wikipedia_simple_full" if full else DATABASE
    context = os.path.dirname(os.path.abspath(dest))
    inside = f"/context/{os.path.basename(context)}"

    ids, out_of_order = read_articles(
        os.path.join(downloads, f"{PREFIX}pages-articles.xml.bz2"), context,
        sample=None if full else SAMPLE)
    if out_of_order:
        sys.exit(f"the XML is not in ascending page_id order ({out_of_order} steps back); "
                 "the sample rule assumes it is")
    keep = set(ids)

    counts = {}
    counts["page"], _ = filter_dump(downloads, context, "page", "page", 0, keep)
    # In the current MediaWiki schema categorylinks no longer carries the category name in `cl_to`:
    # it points at `linktarget` through `cl_target_id`, so both link tables feed the same lookup.
    counts["categorylinks"], category_targets = filter_dump(
        downloads, context, "categorylinks", "categorylinks", 0, keep, extra=6)
    counts["pagelinks"], page_targets = filter_dump(downloads, context, "pagelinks", "pagelinks",
                                                    0, keep, extra=2)
    counts["linktarget"], _ = filter_dump(downloads, context, "linktarget", "linktarget",
                                          0, page_targets | category_targets)
    counts["redirect"], _ = filter_dump(downloads, context, "redirect", "redirect", 0, keep)
    counts["category"], _ = filter_dump(downloads, context, "category", "category", None, keep)
    counts["site_stats"], _ = filter_dump(downloads, context, "site_stats", "site_stats", None, keep)

    parts = [f"""-- Simple English Wikipedia, dump run 20260901, prepared by
-- datasets/{database}/convert.py as the record's deterministic sample: {'every article' if full else f'the {SAMPLE:,} lowest'}
-- page_id non-redirect articles in namespace 0, their text, and the link rows among them.
--
-- Text is CC BY-SA 4.0 and GFDL 1.3 (Wikimedia Terms of Use section 7). Attribution is by hyperlink
-- to the article and its history: https://simple.wikipedia.org/wiki/<page_title> and ?action=history
-- Images are not included. See datasets/{database}/LICENSE.
--
-- The MediaWiki tables are the upstream dump's own CREATE TABLE, unaltered: MySQL 9.7 accepts the
-- MariaDB output as it stands, including CHARSET=binary, varbinary titles, integer display widths
-- and ROW_FORMAT=COMPRESSED. Titles are therefore binary; the v_* views convert them to utf8mb4.
SET NAMES utf8mb4;
SET SESSION foreign_key_checks = 0;
DROP DATABASE IF EXISTS `{database}`;
CREATE DATABASE `{database}` DEFAULT CHARACTER SET utf8mb4;
USE `{database}`;
"""]
    # read straight into the output rather than substituting placeholders: "page" is a prefix of
    # "pagelinks", so a naive replace would splice the page dump into the pagelinks one
    for table in ("page", "categorylinks", "pagelinks", "linktarget", "redirect", "category",
                  "site_stats"):
        path = os.path.join(context, f"{table}.sql")
        with open(path, encoding="utf-8", errors="surrogateescape") as fh:
            parts.append(fh.read())
        os.remove(path)

    parts.append(f"""
-- {'-' * 60}
-- revision and text, synthesized from the XML (the dump's own revision table is not published)

CREATE TABLE `revision` (
  `rev_id` INT UNSIGNED NOT NULL,
  `rev_page` INT UNSIGNED NOT NULL,
  `rev_parent_id` INT UNSIGNED,
  `rev_timestamp` DATETIME NOT NULL,
  `rev_minor_edit` TINYINT UNSIGNED NOT NULL DEFAULT 0,
  `rev_len` INT UNSIGNED,
  `rev_sha1` VARBINARY(32),
  `rev_user_id` INT UNSIGNED,
  `rev_user_text` VARBINARY(255),
  `rev_comment` TEXT,
  `rev_content_model` VARBINARY(32),
  PRIMARY KEY (`rev_id`),
  KEY `rev_page` (`rev_page`),
  KEY `rev_timestamp` (`rev_timestamp`)
);

CREATE TABLE `text` (
  `old_id` INT UNSIGNED NOT NULL,
  `old_text` MEDIUMTEXT,
  PRIMARY KEY (`old_id`),
  FULLTEXT KEY `ft_old_text` (`old_text`)
);

LOAD DATA LOCAL INFILE '{inside}/revision.tsv' INTO TABLE `revision`
  CHARACTER SET utf8mb4 (`rev_id`, `rev_page`, `rev_parent_id`, `rev_timestamp`, `rev_minor_edit`,
  `rev_len`, `rev_sha1`, `rev_user_id`, `rev_user_text`, `rev_comment`, `rev_content_model`);
LOAD DATA LOCAL INFILE '{inside}/text.tsv' INTO TABLE `text`
  CHARACTER SET utf8mb4 (`old_id`, `old_text`);

-- {'-' * 60}
-- utf8mb4 views over the binary MediaWiki columns

CREATE SQL SECURITY INVOKER VIEW `v_page` AS
SELECT `page_id`, `page_namespace`,
       CONVERT(`page_title` USING utf8mb4) AS `page_title`,
       `page_is_redirect`, `page_len`, `page_latest`,
       CONVERT(`page_touched` USING utf8mb4) AS `page_touched`
FROM `page`;

CREATE SQL SECURITY INVOKER VIEW `v_article` AS
SELECT p.`page_id`, CONVERT(p.`page_title` USING utf8mb4) AS `title`, p.`page_len`,
       r.`rev_timestamp`, CONVERT(r.`rev_user_text` USING utf8mb4) AS `last_editor`,
       t.`old_text` AS `wikitext`
FROM `page` p
JOIN `revision` r ON r.`rev_page` = p.`page_id`
JOIN `text` t ON t.`old_id` = r.`rev_id`;

CREATE SQL SECURITY INVOKER VIEW `v_category_member` AS
SELECT c.`cl_from` AS `page_id`, CONVERT(p.`page_title` USING utf8mb4) AS `page_title`,
       CONVERT(lt.`lt_title` USING utf8mb4) AS `category`
FROM `categorylinks` c
JOIN `page` p ON p.`page_id` = c.`cl_from`
JOIN `linktarget` lt ON lt.`lt_id` = c.`cl_target_id`;

CREATE SQL SECURITY INVOKER VIEW `v_pagelink` AS
SELECT pl.`pl_from` AS `from_page_id`,
       CONVERT(f.`page_title` USING utf8mb4) AS `from_title`,
       lt.`lt_namespace` AS `to_namespace`,
       CONVERT(lt.`lt_title` USING utf8mb4) AS `to_title`
FROM `pagelinks` pl
JOIN `page` f ON f.`page_id` = pl.`pl_from`
JOIN `linktarget` lt ON lt.`lt_id` = pl.`pl_target_id`;

SET SESSION foreign_key_checks = 1;
""")
    open(dest, "w", encoding="utf-8", errors="surrogateescape").write("\n".join(parts))

    print(f"  . sample: {len(ids):,} articles, page_id {min(ids)}..{max(ids)}")
    print("  . filtered rows: " + ", ".join(f"{t} {n:,}" for t, n in counts.items()))


if __name__ == "__main__":
    main()
