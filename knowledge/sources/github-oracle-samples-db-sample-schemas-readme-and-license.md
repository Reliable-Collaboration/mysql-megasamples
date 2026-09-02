---
type: Source
title: oracle-samples/db-sample-schemas README.md (main and v23.3) and LICENSE.txt
description: Which schemas are current versus archived, the install procedure, and the verbatim license text of the repository.
resource: https://github.com/oracle-samples/db-sample-schemas/blob/main/README.md
tags: [oracle, sample-schemas, readme, license]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/oracle-samples/db-sample-schemas/main/README.md
    title: README.md at main (6,420 bytes)
    accessed: "2026-09-02"
    version: commit 6660bad (2025-06-25)
  - resource: https://raw.githubusercontent.com/oracle-samples/db-sample-schemas/v23.3/README.md
    title: README.md at v23.3 (3,784 bytes)
    accessed: "2026-09-02"
    version: tag v23.3
  - resource: https://raw.githubusercontent.com/oracle-samples/db-sample-schemas/v23.3/LICENSE.txt
    title: LICENSE.txt (1,094 bytes; identical content at main)
    accessed: "2026-09-02"
  - resource: https://raw.githubusercontent.com/oracle-samples/db-sample-schemas/v19.2/README.md
    title: README.md at v19.2 (schema list for the pre-restructure layout)
    accessed: "2026-09-02"
---

# What was read
Root README at `main` and at `v23.3`, the root `LICENSE.txt`, and the v19.2 README (via gh api / raw.githubusercontent.com), 2026-09-02.

# Relevant excerpt
LICENSE.txt (verbatim, first lines): 
> Copyright (c) 2023 Oracle and/or its affiliates. All rights reserved.
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, ...

This is the **MIT license**, not UPL. The same MIT text is repeated at the top of every schema README and in the `rem` header of every `.sql` file (with a stray "rem" inside "substantial portions rem of the Software" in the per-schema READMEs).

README at `main`:
> The following schemas are included: `HR`: Human Resources - useful for introducing basic topics. `CO`: Customer Orders - a modern schema useful for demos of e-commerce transactions. It allows the storage of semi-structured data using JSON. `SH`: Sales History - designed to allow for demos with large amounts of data.
>
> The following schemas are no longer updated, but are still available: `OC`: Online Catalog (**archived**) - a collection of object-relational database objects built inside the `OE` schema. `OE`: Order Entry (**archived**) ... `PM`: Product Media (**archived**) ...
>
> Archived schemas are provided for reference for examples in the documentation but are no longer actively maintained.

README at `v23.3` lists `HR`, `CO`, `SH`, `OE (archived)`, `PM (archived)`; installation: download the release zip, `cd` into the schema folder, run `<schema>_install.sql` with SQLcl (`sql <system>@<connect_string>` then `@hr_install.sql`), answer the password/tablespace prompts, review the verification output. "This project is not accepting external contributions at this time."

README at `v19.2` listed HR, OE, PM, IX, SH, BI as "installed with Oracle Database Enterprise Edition" plus a then-new CO, with a `mksample.sql` driver that dropped users HR, OE, PM, IX, SH and BI. IX therefore existed only up to v19.2/v21.1 and was dropped in the v23 restructure.

# What it was used to decide
[MIT license record](/licenses/mit.md) (applies to all four Oracle datasets); the current-vs-archived statement in every Oracle dataset record; [OE/PM/IX scope](/datasets/oracle-oe-pm-ix.md).
