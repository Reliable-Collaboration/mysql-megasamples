---
type: Source
title: Enron Email Dataset page (William W. Cohen, CMU)
description: The canonical distribution page for the CMU Enron corpus; states provenance, cleaning, redactions, the May 7, 2015 tarball and the absence of any license.
resource: https://www.cs.cmu.edu/~enron/
tags: [source, enron]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
sources:
  - resource: https://www.cs.cmu.edu/~enron/
    title: Enron Email Dataset
    accessed: 2026-09-02
    version: page links enron_mail_20150507.tar.gz (May 7, 2015 version)
---

# What was read
https://www.cs.cmu.edu/~enron/ on 2026-09-02 (full HTML). Also a `HEAD` on https://www.cs.cmu.edu/~enron/enron_mail_20150507.tar.gz: `HTTP/1.1 200`, `Content-Length: 443254787` (443.3 MB = 422.7 MiB), `Last-Modified: Thu, 07 May 2015 20:35:29 GMT`.

# Relevant excerpt
> "This dataset was collected and prepared by the CALO Project (A Cognitive Assistant that Learns and Organizes). It contains data from about 150 users, mostly senior management of Enron, organized into folders. The corpus contains a total of about 0.5M messages."
> "This data was originally made public, and posted to the web, by the Federal Energy Regulatory Commission during its investigation."
> "The dataset here does not include attachments, and some messages have been deleted "as part of a redaction effort due to requests from affected employees". Invalid email addresses were converted to something of the form user@enron.com whenever possible (i.e., recipient is specified in some parse-able format like "Doe, John" or "Mary K. Smith") and to no_address@enron.com when no recipient was specified."
> "Prior versions of the dataset are no longer being distributed. If you are using the March 2, 2004 Version; the August 21, 2009 Version; or the April 2, 2011 Version of this dataset for your work, you are requested to replace it with the newer version"
> "May 7, 2015 Version of dataset (about 1.7Gb, tarred and gzipped)."
> "Jitesh Shetty has put up a database of link-analysis results." (links http://www.isi.edu/~adibi/Enron/Enron.htm) — "A version of the dataset with all attachments is available" (links http://edrm.net/resources/data-sets/enron-data-set-files)

No md5/sha checksum is published; no license or terms text appears anywhere on the page. The "about 1.7Gb" conflicts with the observed 443 MB Content-Length; **Inferred:** 1.7 GB is the extracted size (a third-party README says the extracted `maildir` is 1.4 GB).

# What it was used to decide
[Enron dataset](/datasets/enron.md), [Enron public-record license record](/licenses/enron-public-record.md).
