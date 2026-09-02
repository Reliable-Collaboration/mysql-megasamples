---
type: License
title: Stack Exchange data dump terms (2024 "Data dump access" click-through, ToS clause, archive.org license.txt)
description: The contractual layer around the CC BY-SA licensed Stack Exchange dumps since July 2024 — what the click-through says, what it restricts, and why this project sources the last archive.org dump instead.
resource: https://stackoverflow.com/help/data-dumps
tags: [license, stackexchange, click-through, licensing-finding, cc-by-sa]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:25:00Z" }
stale_after: 2027-03-01
sources:
  - resource: https://stackoverflow.com/help/data-dumps
    title: Help Center - What is the data dump?
    accessed: 2026-09-02
  - resource: https://meta.stackexchange.com/questions/401324/announcing-a-change-to-the-data-dump-process
    title: Announcing a change to the data-dump process (2024-07-12, last edited 2024-09-09)
    accessed: 2026-09-02
    version: read via api.stackexchange.com /questions/401324?filter=withbody
  - resource: https://stackoverflow.com/legal/terms-of-service/public
    title: Public Network Terms of Service (Last updated November 13, 2025)
    accessed: 2026-09-02
  - resource: https://archive.org/download/stackexchange/license.txt
    title: license.txt in the archive.org Stack Exchange Data Dump item (2024-04-01)
    accessed: 2026-09-02
  - resource: https://stackoverflow.com/help/licensing
    title: Help Center - Licensing
    accessed: 2026-09-02
  - resource: https://meta.stackexchange.com/questions/402019/creative-commons-license-by-sa-violation-data-dump-must-not-force-users-to-ag
    title: Creative Commons License (BY-SA) Violation claim and top answer (2024-08-08)
    accessed: 2026-09-02
  - resource: https://meta.stackexchange.com/questions/402311/am-i-allowed-to-publicly-reshare-some-json-file-containing-se-data-created-after
    title: Am I allowed to publicly reshare SE data created after the new process? (2024-08-22)
    accessed: 2026-09-02
---

# The three layers

## 1. Content license (unchanged): CC BY-SA, version by post date
Help/licensing (read 2026-09-02): "Content contributed before 2011-04-08 (UTC) is distributed under the terms of CC BY-SA 2.5. Content contributed from 2011-04-08 up to but not including 2018-05-02 (UTC) is distributed under the terms of CC BY-SA 3.0. Content contributed on or after 2018-05-02 (UTC) is distributed under the terms of CC BY-SA 4.0." Each dump row carries `ContentLicense`. See [CC BY-SA 4.0](/licenses/cc-by-sa-4-0.md) and [CC BY-SA 3.0](/licenses/cc-by-sa-3-0.md).

Public Network Terms (Last updated 2025-11-13): "From time to time, Stack Overflow may make available compilations of all the Subscriber Content on the public Network (the "Creative Commons Data Dump"). The Creative Commons Data Dump is licensed under the CC BY-SA license. By downloading the Creative Commons Data Dump, you agree to be bound by the terms of that license."

## 2. Attribution wording (verbatim, archive.org license.txt, which is the 2009 blog post text)
> "If you republish this content, we *require* that you:
> 1. Visually indicate that the content is from the Stack Exchange site it had originated from in some way. It doesn't have to be obnoxious; a discreet text blurb is fine.
> 2. Hyperlink directly to the original question on the source site (e.g., http://stackoverflow.com/questions/12345)
> 3. Show the author names for every question and answer
> 4. Hyperlink each author name directly back to their user profile page on the source site (e.g., http://stackoverflow.com/users/12345/username)
> By "directly", I mean each hyperlink must point directly to our domain in standard HTML visible even with JavaScript disabled, and not use a tinyurl or any other form of obfuscation or redirection. Furthermore, the links must not be nofollowed."

The former https://stackoverflow.com/help/attribution URL returns 404 (checked 2026-09-02); the same four points are in the 2009 blog post https://stackoverflow.blog/2009/06/25/attribution-required/ (read 2026-09-02). Since 2024-Q2 regenerated dumps a `license.txt` is also inside each .7z (Meta 402501).

## 3. The 2024 click-through ("Data dump access" page, login required)
Help Center (read 2026-09-02): "Content from each Stack Exchange site is made available quarterly in the form of a 'data dump' file that can be accessed by a user via their account settings page. ... choose 'Data dump access' under the 'Access' heading ... Check the box affirming that you do not intend to use the file for LLM training, and then use the 'Download data' button".

Final agreement text (announcement, UPDATE July 26, 2024, signed off by product and legal):
> "I understand that this file is being provided to me for my own use and for projects that do not include training a large language model (LLM), and that should I distribute this file for the purpose of LLM training, Stack Overflow reserves the right to decline to allow me access to future downloads of this data dump."

Superseded draft wording (shown in the 2024-07-12 mock-up, withdrawn on 2024-07-26 — quoted so nobody mistakes it for the live terms): "I agree that I will use this file for non-commercial use. I will not use it for any other purpose, and I will not transfer it to others without permission from Stack Overflow. I certify that I am not downloading this file on behalf of my employer, for use in a for-profit enterprise."

Other statements in the announcement: "The CC BY-SA license is unchanged."; "Stack Overflow is no longer uploading the data dump to archive.org."; "We would really rather users do not upload the file to archive.org or similar data pile sites."; "when you breach the agreement that you make when downloading the dumps file, we do have the option to decline to provide you with future versions of the data dumps."

# LICENSING FINDING (flag for the coordinator)
* The live click-through is a personal contract between the downloader and Stack Overflow. Its only operative restriction is on distributing the file "for the purpose of LLM training", with the sanction being loss of future download access. It does not (any more) say "non-commercial" or "will not transfer to others". The top-voted community reading (Meta 402019 answer, score 15) is that "This wording is not a violation of the CC BY-SA license ... CC BY-SA content can be gated" and that the CC license itself is unaffected.
* Nevertheless, a public MySQL image redistributes the content to anyone, including LLM trainers. A maintainer who obtained the file through the profile page could be accused of distributing it "for the purpose of LLM training" and lose access; that is a project-governance risk, not a copyright problem.
* **Decision taken here:** source the dumps from the archive.org item (last snapshot 2024-04-02, files dated 2024-04-06/07), which carries only the CC BY-SA license (`licenseurl` = by-sa/4.0 in item metadata; `license.txt` inside) and no click-through. Nobody on the project needs to accept the profile-page agreement, and the README states that. Trade-off: data is frozen at April 2024. See [Stack Exchange dataset](/datasets/stackexchange.md) and [decision](/decisions/stackexchange-conversion-path.md).
* If the coordinator later wants a newer dump: (a) the July 2025+ dumps contain two fabricated "watermark" posts (Ids 1000000001 and 1000000010) that are not user content and must be deleted before redistribution (Meta 2678 schema note; Meta 412018 with staff confirmation), and (b) the downloading maintainer should be named in the README as having accepted the clause, with the image's purpose stated as a sample database, not an LLM corpus.

# Applied to
* [Stack Exchange data dump](/datasets/stackexchange.md)
