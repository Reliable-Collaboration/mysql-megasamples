---
type: Source
title: enrondata/enrondata edrm-v2.0.0 README — lineage of the EDRM/ZL Enron set
description: Community README describing the EDRM v2 data set (PST, MIME, EDRM XML; 149 custodians) and where copies were archived.
resource: https://github.com/enrondata/enrondata/blob/master/edrm-v2.0.0/README.md
tags: [source, enron, edrm]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://raw.githubusercontent.com/enrondata/enrondata/master/edrm-v2.0.0/README.md
    title: edrm-v2.0.0/README.md at master
    accessed: "2026-09-02"
---

# What was read
The raw README on 2026-09-02.

# Relevant excerpt
> "The EDRM v2.0 Data Set is based off the FERC Concordance Data Set. It supports multiple formats: PST, MIME, EDRM XML"
> "Custodians: 149 (vs. 148 custodians in CALO)"
> "FERC (Concordance format) to EDRM v2.0 MIME via custom scripts; EDRM v2.0 MIME to EDRM v2.0 PST and EDRM XML via ZL Unified Archive"
> Archives: searchdaimon.com (MIME/EML, PST, EDRM XML); https://archive.org/details/edrm.enron.email.data.set.v2.xml; https://aws.amazon.com/datasets/enron-email-data/

# What it was used to decide
"Known versions" paragraph of [Enron dataset](/datasets/enron.md): EDRM v2 exists with attachments, but we use CMU.
