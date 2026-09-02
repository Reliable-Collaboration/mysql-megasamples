---
type: Source
title: "MySQL 9.7 Reference Manual: Fine-Tuning MySQL Full-Text Search"
description: "innodb_ft_min_token_size default 3, innodb_ft_max_token_size default 84, ft_min_word_len 4 (MyISAM); stopword variables; indexes must be rebuilt after changes."
resource: https://dev.mysql.com/doc/refman/9.7/en/fulltext-fine-tuning.html
tags: [mysql, docs, fulltext]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:33:59Z" }
sources:
  - resource: https://dev.mysql.com/doc/refman/9.7/en/fulltext-fine-tuning.html
    title: "MySQL 9.7 Reference Manual: Fine-Tuning MySQL Full-Text Search"
    accessed: 2026-09-02
    version: "MySQL 9.7 manual, section 14.9.6"
---

# What was read
https://dev.mysql.com/doc/refman/9.7/en/fulltext-fine-tuning.html, accessed 2026-09-02; version: MySQL 9.7 manual, section 14.9.6.

# Relevant excerpt
* InnoDB: `innodb_ft_min_token_size` default 3, `innodb_ft_max_token_size` default 84; MyISAM: `ft_min_word_len` default 4. These do not apply to ngram-parsed indexes (`ngram_token_size`).
* After changing word-length options FULLTEXT indexes must be rebuilt, e.g. `ALTER TABLE t DROP INDEX idx, ADD FULLTEXT INDEX idx (col);` or `SET GLOBAL innodb_optimize_fulltext_only=ON; OPTIMIZE TABLE t;`.
* Stopwords: `innodb_ft_enable_stopword`, `innodb_ft_server_stopword_table`, `innodb_ft_user_stopword_table`, `ft_stopword_file`; the default InnoDB list is in `INFORMATION_SCHEMA.INNODB_FT_DEFAULT_STOPWORD`. MyISAM natural-language searches ignore words present in more than 50% of rows; boolean mode does not.

# What it was used to decide
[MySQL 9.x behaviour notes](/tools/mysql-9x-behaviour-notes.md): smoke tests for FULLTEXT columns search a term of at least 3 characters that is not in `INNODB_FT_DEFAULT_STOPWORD`.
