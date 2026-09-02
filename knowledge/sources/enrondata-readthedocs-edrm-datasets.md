---
type: Source
title: EnronData.org — EDRM Enron Email Datasets page
description: States that EDRM withdrew its v1 and v2 sets because of remaining PII and now provides only a cleansed v1.
resource: https://enrondata.readthedocs.io/en/latest/data/edrm-enron-email-datasets/
tags: [source, enron, edrm, personal-data]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://enrondata.readthedocs.io/en/latest/data/edrm-enron-email-datasets/
    title: EDRM Enron Email Datasets
    accessed: 2026-09-02
---

# What was read
The page on 2026-09-02 (via WebFetch summary; wording quoted as returned).

# Relevant excerpt
> "EDRM has provided 3 versions of the Enron Email Dataset, of which 1 is currently provided." Only the "EDRM Enron v1 Data Set Cleansed of Private, Health and Financial Information" is currently available; the original v1 and v2 are "no longer available" because they contained "Personally Identifiable Information (PII) that remained in the dataset when the Federal Energy Regulatory Commission (FERC) released the Enron email data set on March 26, 2003."

The live EDRM site (https://www.edrm.net/resources/data-sets/edrm-enron-email-data-set/) returned HTTP 403 / a generic "Other Data Sets" page on 2026-09-02, so this page is the evidence used.

# What it was used to decide
Personal-data section of [Enron public record](/licenses/enron-public-record.md); the "why CMU, not EDRM" argument in [Enron dataset](/datasets/enron.md).
