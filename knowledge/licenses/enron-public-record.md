---
type: License
title: Enron email corpus — public record status and CMU distribution terms
description: The CMU Enron corpus has no license text; it is FERC public-record material redistributed by CMU with a privacy request; this record states exactly what the page says and what is inferred.
resource: https://www.cs.cmu.edu/~enron/
tags: [license, public-record, enron, personal-data, no-license-text]
status: stable
trust: inferred
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://www.cs.cmu.edu/~enron/
    title: Enron Email Dataset (William W. Cohen, CMU)
    accessed: "2026-09-02"
    version: May 7, 2015 version
  - resource: https://www.cs.cmu.edu/~enron/DELETIONS.txt
    title: DELETIONS.txt removal history
    accessed: "2026-09-02"
  - resource: https://enrondata.readthedocs.io/en/latest/data/edrm-enron-email-datasets/
    title: EnronData.org - EDRM Enron Email Datasets
    accessed: "2026-09-02"
---

# Where the text lives
* "This data was originally made public, and posted to the web, by the Federal Energy Regulatory Commission during its investigation."
* "The email dataset was later purchased by Leslie Kaelbling at MIT, and turned out to have a number of integrity problems. A number of folks at SRI, notably Melinda Gervasio, worked hard to correct these problems"
* "The dataset here does not include attachments, and some messages have been deleted "as part of a redaction effort due to requests from affected employees". Invalid email addresses were converted to something of the form user@enron.com whenever possible"
* "I am distributing this dataset as a resource for researchers who are interested in improving current email tools, or understanding how email is currently used. ... In using this dataset, please be sensitive to the privacy of the people involved (and remember that many of these people were certainly not involved in any of the actions which precipitated the investigation.)"
* DELETIONS.txt: "For privacy reasons, my policy has been to remove emails from this collection when requested by the email's authors or recipients." It lists removals on 2009-08-21 (1 file), 2011-04-02 (6 files, gay-r), 2015-05-07 (23 files, richey-c).

**There is no license statement, no copyright notice and no terms-of-use link on the page.** The word "license" does not occur.

# Why redistribution is generally accepted (Inferred)
**Inferred:** FERC released the emails as part of a federal regulatory proceeding (a public record); the CMU page and every downstream distribution (EDRM/ZL, archive.org, Kaggle, dozens of GitHub converters) redistribute it without a license, and the CMU page itself lists such redistributions approvingly ("A version of the dataset with all attachments is available", "several on-line databases that allow you to search the data"). The copyright position of individual authors of the emails has never, to this author's knowledge, been asserted against a redistributor; this is convention, not a verified legal fact. Record it as inferred and do not call the data "public domain" or "CC0" in the README — say "public record released by FERC; redistributed by CMU without a license; no warranty".

# Obligations
* The corpus contains real names, real email addresses, phone numbers and personal correspondence of about 150 named custodians plus thousands of third parties. Say so in the README.
* Honour the CMU removals: build only from the 2015-05-07 tarball (which already excludes the DELETIONS.txt files) and never re-add earlier versions.
* Provide a documented removal path: a `README` section saying that takedown requests received by the project are honoured by deleting the message from the build list, mirroring CMU's policy.
* Exclude attachments — trivially satisfied because the CMU tarball has none. Do not switch to the EDRM/ZL sets: EnronData.org notes that EDRM withdrew its v1 and v2 sets "due to the presence of Personally Identifiable Information (PII) that remained in the dataset".
* Do not add derived personal fields (e.g., inferred job titles beyond what the corpus contains).

# Attribution
No license text exists; the README carries the provenance statement: "Enron Email Dataset (May 7, 2015 version), collected and prepared by the CALO Project (SRI International) and distributed by William W. Cohen, Carnegie Mellon University, https://www.cs.cmu.edu/~enron/. Originally made public by the U.S. Federal Energy Regulatory Commission during its investigation of Enron. This copy excludes the messages CMU removed at the request of affected individuals; requests for further removal are honoured as described in the README."

# Applied to
* [Enron email corpus](/datasets/enron.md)
