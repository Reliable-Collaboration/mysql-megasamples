---
type: Tool
title: Enron maildir parsing with the Python `email` standard library
description: Build-time parser for the CMU Enron maildir tree — one RFC 822 file per message, no attachments — into messages/recipients/mailbox tables.
resource: https://docs.python.org/3/library/email.html
tags: [tool, enron, python, email, mysql-load, text-group]
status: stable
trust: inferred
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://www.cs.cmu.edu/~enron/
    title: Enron Email Dataset page
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/lintool/Enron2mbox/master/README.md
    title: Enron2mbox README (maildir layout, 517,401 files)
    accessed: 2026-09-02
  - resource: https://raw.githubusercontent.com/angel-hernandez91/enron-emails/master/README.md
    title: enron-emails README (517,401 emails; "encoded in ASCII")
    accessed: 2026-09-02
---

# Verified input shape
* Tarball extracts to `maildir/<custodian>/<folder>/<n>.` — each file is one message in RFC 822 form ("distributed in maildir format, which means that each message is stored in a separate file" — Enron2mbox README). Two independent third-party counts give **517,401** files (Enron2mbox `count_messages.sh`; enron-emails "Total Emails: 517,401"); 150 custodian directories (CMU page: "about 150 users").
* Note the Enron tree is *not* a real Maildir (no `cur/`/`new/`); Enron2mbox restructures it to use Python's `mailbox.Maildir`. We do not need that: walk the tree and parse each file with `email.parser.BytesParser(policy=email.policy.compat32).parse(fh)`.

# Approach (Inferred, to be verified on the first 1,000 files)
* Deterministic order: `sorted(os.walk)` by path; the row `id` is the 1-based position in that order so re-runs produce identical tables. Store the relative path (`allen-p/inbox/1.`) as the natural key; `mailbox` = first path component; `folder` = the remaining directory path.
* Headers of interest: `Message-ID`, `Date`, `From`, `To`, `Cc`, `Bcc`, `Subject`, `Mime-Version`, `Content-Type`, `Content-Transfer-Encoding`, `X-From`, `X-To`, `X-cc`, `X-bcc`, `X-Folder`, `X-Origin`, `X-FileName` (**Inferred** from the corpus' known header set; verify).
* Recipients: split `To/Cc/Bcc` on commas after unfolding; `email.utils.getaddresses` handles quoted display names. Expect thousands of recipients on some messages and the CMU placeholders `no_address@enron.com` / `user@enron.com` (CMU page).
* Dates: `email.utils.parsedate_to_datetime`; the corpus uses offsets like `-0700 (PDT)` (**Inferred**); store UTC `DATETIME` plus the raw header string; reject/flag years outside 1979-2002 (**Inferred:** a few messages carry bogus 1979/1980 dates).
* Charset: files are mostly 7-bit ASCII (enron-emails README: "the emails where encoded in ASCII"); **Inferred:** some bodies contain Latin-1 / Windows-1252 bytes and quoted-printable `=20` sequences; decode with `charset` from `Content-Type` if declared, else try UTF-8 then fall back to `cp1252` with `errors="replace"` and record `charset_fallback = 1`. Body stored as utf8mb4 `MEDIUMTEXT`.
* Malformed headers: `email` returns `defects`; store `header_defects` count.
* Duplicates: the same message often appears in several folders (`all_documents`, `inbox`, `sent`, `sent_items`, `_sent_mail`); keep every file as a row (the folder placement is data) and expose a `sha1(body)` column so consumers can deduplicate.
