---
type: License
title: Apache License 2.0
description: Permissive license of dbt-labs/jaffle-shop-classic (seed data + dbt project) and the jafgen generator; requires license copy, change notices and retained attribution notices.
resource: https://www.apache.org/licenses/LICENSE-2.0
tags: [license, apache-2-0, permissive]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/dbt-labs/jaffle-shop-classic/main/LICENSE
    title: jaffle-shop-classic LICENSE (full Apache-2.0 text)
    accessed: "2026-09-02"
  - resource: https://pypi.org/pypi/jafgen/json
    title: jafgen license metadata (full Apache-2.0 text)
    accessed: "2026-09-02"
  - resource: https://api.github.com/repos/dbt-labs/jaffle-shop-generator
    title: GitHub license detection Apache-2.0
    accessed: "2026-09-02"
---

# Where the text lives
Verbatim text: `LICENSE` in dbt-labs/jaffle-shop-classic and dbt-labs/jaffle-shop-generator (11,357 bytes each, "Apache License Version 2.0, January 2004 http://www.apache.org/licenses/"). Canonical URL https://www.apache.org/licenses/LICENSE-2.0 (not opened in this session; the repository copies were read - [source](/sources/github-dbt-labs-jaffle-shop-classic-license.md)).

# Key clause (Section 4, verbatim)
"(a) You must give any other recipients of the Work or Derivative Works a copy of this License; and (b) You must cause any modified files to carry prominent notices stating that You changed the files; and (c) You must retain, in the Source form of any Derivative Works that You distribute, all copyright, patent, trademark, and attribution notices from the Source form of the Work ...; and (d) If the Work includes a "NOTICE" text file as part of its distribution, then any Derivative Works that You distribute must include a readable copy of the attribution notices contained within such NOTICE file".

# Obligations
Ship a copy of the license with the converted Jaffle Shop database; state that the CSVs were converted (change notice); neither repository has a NOTICE file or a filled-in copyright line (the appendix still reads "Copyright {yyyy} {name of copyright owner}") - attribute to "dbt Labs, Inc." as the repository owner (**Inferred** attribution string; no explicit author line exists).

# Attribution
Ship the Apache-2.0 text as `LICENSE` next to the seeds, keep any upstream `NOTICE` content, and state changes made. Wording used: "Jaffle Shop seed data and dbt project © dbt Labs, Inc., licensed under the Apache License, Version 2.0 (http://www.apache.org/licenses/LICENSE-2.0); converted to MySQL by this project." The same notice covers the `sysbench-tpcc` scripts executed at TPC-C load time.

# Applied to
* [Jaffle Shop](/datasets/jaffle-shop.md) - classic seeds and project (dbt-labs/jaffle-shop-classic); jafgen generator (tool). The newer dbt-labs/jaffle-shop repository has no license file ([question](/questions/jaffle-shop-new-repo-license.md)).
* [TPC-C](/datasets/tpc-c.md) - the `Percona-Lab/sysbench-tpcc` Lua scripts executed at load time.
