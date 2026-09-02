---
type: License
title: "GNU AGPL v3 (internetarchive Python library / ia CLI)"
description: "Strong copyleft licence of the maintainer-side upload tool; never shipped in the image and never linked by project code, so no obligation attaches to the repository or the image."
resource: https://www.gnu.org/licenses/agpl-3.0.html
tags: [license, copyleft, agpl]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:51:18Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:51:18Z" }
sources:
  - resource: https://archive.org/developers/internetarchive/
    title: "internetarchive library documentation (states AGPL-3 licensing)"
    accessed: 2026-09-02
---

# Text location
The developer portal states the `internetarchive` library is distributed under AGPL-3 ([record](/sources/archive-org-developers-internetarchive.md)); the licence text lives at https://www.gnu.org/licenses/agpl-3.0.html (not opened this session).

# Obligations and how the project avoids them
AGPL applies to redistribution and network use of the library itself. The project only invokes the `ia` command line from a maintainer's machine (`scripts/mirror.sh`); it does not import the library into repository code and does not ship it in the image.

# Applied to
* `ia` CLI in [archive.org mirroring](/tools/internet-archive-mirroring.md).
