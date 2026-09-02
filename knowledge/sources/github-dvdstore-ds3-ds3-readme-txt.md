---
type: Source
title: ds3/ds3_readme.txt (kit overview, sizes table)
description: The DS3 kit readme - directory layout, the three standard sizes (Small 10 MB / Medium 1 GB / Large 100 GB) and the tarball layout from linux.dell.com.
resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/ds3_readme.txt
tags: [dvdstore, ds3, sizes]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/dvdstore/ds3/master/ds3/ds3_readme.txt
    title: ds3_readme.txt (5/14/15)
    accessed: "2026-09-02"
---

# What was read
The file in full, accessed 2026-09-02.

# Relevant excerpt
> DS3 comes in 3 standard sizes: Database Size Customers Orders Products / Small 10 MB 20,000 1,000/month 10,000 / Medium 1 GB 2,000,000 100,000/month 100,000 / Large 100 GB 200,000,000 10,000,000/month 1,000,000. ds3.tar.gz contains data files for the Small version.

"The goal in designing the database component ... was to utilize many advanced database features (transactions, stored procedures, triggers, referential integity) while keeping the database easy to install". Directories: ./ds3/data_files, ./ds3/drivers, ./ds3/mysqlds3, ./ds3/oracleds3, ./ds3/sqlserverds3, ./ds3/pgsqlds3. Authors davejaffe7@gmail.com and tmuirhead@vmware.com.

# What it was used to decide
Size labels and tier reasoning in [Dell DVD Store](/datasets/dell-dvd-store.md).
