---
type: Source
title: "mysql/mysql-shell LICENSE at tag 9.7.1"
description: "MySQL Shell 9.7 Community is GPLv2 with Oracle's additional linking permission (the 'Universal FOSS Exception' style grant for separately licensed software such as OpenSSL); Election of GPLv2."
resource: https://raw.githubusercontent.com/mysql/mysql-shell/9.7.1/LICENSE
tags: [mysql-shell, license, gpl]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:41:13Z" }
sources:
  - resource: https://raw.githubusercontent.com/mysql/mysql-shell/9.7.1/LICENSE
    title: "mysql/mysql-shell LICENSE at tag 9.7.1"
    accessed: 2026-09-02
    version: "tag 9.7.1; \"Last updated: March 2026\""
---

# What was read
https://raw.githubusercontent.com/mysql/mysql-shell/9.7.1/LICENSE, accessed 2026-09-02; version: tag 9.7.1; "Last updated: March 2026".

# Relevant excerpt
> "This release of MySQL Shell, part of MySQL 9.7.0 Community, is brought to you by the MySQL team at Oracle. This software is released under version 2 of the GNU General Public License (GPLv2), as set forth below, with the following additional permissions:"
> "This distribution of MySQL Shell, part of MySQL 9.7.0 Community, is designed to work with certain software (including but not limited to OpenSSL) that is licensed under separate terms, as designated in a particular file or component or in the license documentation. Without limiting your rights under the GPLv2, the authors of MySQL hereby grant you an additional permission to link the program and your derivative works with the separately licensed software that they have either included with the program or referenced in the documentation."
> "Election of GPLv2 ... Oracle elects to use only the General Public License version 2 (GPLv2) at this time"
* Followed by the full GPLv2 text and third-party notices. GitHub reports the repo license as NOASSERTION (custom file).

# What it was used to decide
[MySQL Shell utilities](/tools/mysql-shell-utilities.md); [GPL-2.0 license record](/licenses/gpl-2-0.md): shipping `mysqlsh` inside the image is already the case for the official base image, so the project's image adds no new GPL obligation beyond what the base carries (source availability is Oracle's, unchanged binaries).
