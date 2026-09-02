---
type: Source
title: ds3/ds3_Documentation.txt (DS3 documentation, 5/15/15)
description: Full DS3 documentation - what is new in 3, Perl-based data generation (InstallDVDStore.pl), driver usage; states the kit is open source and that Small load data is included.
resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/ds3_Documentation.txt
tags: [dvdstore, ds3, documentation]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/ds3_Documentation.txt
    title: ds3_Documentation.txt (Dave Jaffe, Todd Muirhead; DS2.1 features by Girish Khadke)
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/ds3_faq.txt
    title: ds3_faq.txt
    accessed: "2026-09-02"
---

# What was read
Sections 1-5 of ds3_Documentation.txt (29 KB) and the FAQ, accessed 2026-09-02.

# Relevant excerpt
* "The DVD Store Version 3 (DS3) is a complete open source online e-commerce test application"; "Load data for the small DVD Store database is included in the kit."; "The DVD Store kit is available at github.com/dvdstore".
* What's new in 3: product reviews (write/view, helpfulness rating 1-10, "seven new stored procedures"), premium membership (bronze/silver/gold), new generators for reviews, reviews_helpfulness and membership; InstallDVDStore.pl updated.
* Section 5.1: InstallDVDStore.pl asks for size (integer), MB/GB, database type (mssql/mysql/pgsql/oracle), OS type; generates CSVs under data_files/{cust,orders,reviews,membership,prod} and size-specific build scripts from `_generic_template` files (MySQL: only `mysqlds3_cleanup_generic_template.sql`).
* FAQ: "S/M/L refer to the size of the database (10 MB/ 1 GB/ 100 GB). Things like maximum number of products and customers are tied to the size."

No license text appears in the documentation itself; licensing is in gpl.txt and the source headers.

# What it was used to decide
Generator workflow and size semantics in [Dell DVD Store](/datasets/dell-dvd-store.md).
