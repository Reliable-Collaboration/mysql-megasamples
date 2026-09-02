---
type: Decision
title: "Dispositions of the first code review (Claude code-review and GitHub Copilot) on PR #1"
description: "Every finding from the two reviews validated against the original request, classified, and resolved as a class or explicitly declined with the reason; the conventions runbook revision 2 came out of this pass."
resource: /decisions/review-2026-09-02-dispositions.md
tags: [decision, review, process]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T22:33:25Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T22:33:25Z" }
sources:
  - resource: https://github.com/Reliable-Collaboration/mysql-megasamples/pull/1
    title: "PR #1 with the Copilot review (8 comments) and the code-review findings (15 numbered, 38 merged, 6 refuted, about 30 cut)"
    accessed: "2026-09-02"
---

# Question
Which review findings are real defects in the plan or bundle, which are artefacts of a badly worded convention, and which are noise; and for each real one, what is the class of similar defects that should be fixed together?

# Options considered
1. Accept every finding literally — rejected: six Copilot comments and one code-review sub-finding apply revision 1 of the conventions runbook, whose trust clause was self-contradictory; applying it literally would have downgraded 81 records whose quotations were genuinely read, hiding real evidence.
2. Fix only the 15 numbered findings — rejected: the code-review tool caps output at 15 and the bundle has 500+ files, so each finding was treated as a class and swept with scripts.
3. **Validate each finding against the original request, fix the convention where the convention was wrong, then fix every instance of each class** (chosen).

# Evidence
The finding texts are recorded in the PR; the sweeps that sized each class are in this session's log entries. Checker output before the pass: 170 errors under the revised rules; after: 0.

# Outcome

| # | Finding (source) | Verdict | Class and resolution |
|---|---|---|---|
| 1 | Row-digest SUM over CONV string is DOUBLE; float and JSON rules inconsistent (review) | valid, design defect | [checksum method](/decisions/test-checksum-method.md): `CAST(... AS UNSIGNED)`; floats and JSON excluded from the digest and compared per column / as parsed objects; native-SQL baseline exception stated; PLAN §4 and oracle-co updated |
| 2 | Bake decision contradicts itself; wrapper specified three ways; post-exec hook; registry has three writers (review) | valid | [bake decision](/decisions/bake-data-vs-initdb.md), [naming convention](/decisions/database-naming-convention.md), [large-tabular path](/decisions/large-tabular-conversion-path.md), PLAN §2.2–2.3: no initdb scripts at all; one `--init-file` wrapper; `MEGASAMPLES_EXTENDED` removed; `scripts/registry.py` is the single registry writer |
| 3 | Sakila/Employees/DVD Store records still load via initdb (review) | valid, same class as 2 | swept every "init sequence / init directory / at init / via the entrypoint" mention in datasets, decisions and tools; all now load through the build server during `make <dataset>` |
| 4 | AdventureWorks record says extended, plan says core; tier tag vocabulary inconsistent (review) | valid | tier vocabulary defined in conventions and checked; all 34 dataset records re-tagged from [tier assignments](/decisions/tier-assignments.md); AdventureWorks section rewritten |
| 5 | Resolved decisions still marked pending/draft/open; mixed-case table names in test SQL (review) | valid | checker now cross-checks `# Status` with `status`/`trust`/tags/description; four decisions fixed; test SQL in seven dataset records lower-cased per the naming convention; column names with spaces get underscores |
| 6 | Undefined task IDs, make targets, scripts (review) | valid | PLAN §2.4 now lists every target used anywhere (swept by grep); E-02 row and V series added, P-07/O-05 references fixed; `scripts/registry.py`, `canon.sql`, `mirror.sh` added to the layout; `checksum.py` → `canon.py`; `verify.py sizes` named in §4 |
| 7 | Plan and repository-layout record disagree (review) | valid | PLAN §2.1 declared authoritative; the record now mirrors it (`ipv4_first`, scripts, `.gitignore` = committed file, tests files, `dataset.yaml`) |
| 8 | Provenance generator reads a `# Attribution` heading no license record has; Applied-to gaps (review) | valid | License section template made mandatory and checked; 18 records received attribution wording, headings normalized in all 24; Applied-to gaps for Stack Exchange (CC BY-SA 3.0), Wikidata (CC0), TPC-C (Apache-2.0) filled |
| 9 | core-fast rule contradicts its list; §11 DAG inconsistent (review) | valid | explicit `CORE_FAST` list with a 200 MB rule; S-01 depends on P-03; X-03 depends on M-04 |
| 10 | Citi Bike 2.5 M vs 1.1 M; jaffle_shop_v3 unnamed; corrupted question description; two plausible sub-items (review) | valid | figure corrected; `jaffle_shop_gen` added to the naming convention and used everywhere; description restored; Titanic and checksum wording clarified |
| 11–12 | `_mini_yaml` corrupts titles; verdict depends on PyYAML presence; numeric tags (review) | valid | fallback parser deleted, PyYAML required; ISO check accepts parsed datetimes; `tags` must be strings (four records quoted); every `accessed`/`version` scalar quoted by the fixer so implicit typing cannot recur |
| 13 | Quote-fixer breaks block scalars, unterminated frontmatter, list items (review + Copilot ×2) | valid | fixer rewritten: parser-driven decision, full indicator set, unterminated frontmatter reported and left untouched, list-item keys handled, shared frontmatter splitter |
| 14 | Checker enforces far less than claimed (review) | valid | checker rewritten: links in index/log/frontmatter resolved, missing bundle path is an error, log heading and verb rules, sections per type, index content compared, `bundle_status` marker introduced (draft now, stable at R-02); PLAN §10.4 describes exactly what runs |
| 15a | Log verb "Init" not allowed (review) | valid | changed to **Creation**; verb list unified in executor-discipline; checker enforces |
| 15b | 77 source records fold several documents (review) | **convention was wrong** | granularity redefined: one record per source artifact (a document, a repository at a commit, a manual page set), every URL under `sources`; no records split |
| 15c | Missing template sections in 38 sources, 7 decisions (review) | valid | sections generated from frontmatter where mechanical, written by hand for decisions; tools, questions and licenses normalized to the new per-type templates; checker enforces |
| 15d | tpc-ds spec lists an unread PDF; gpl-2-0 hedge unmarked; from-memory claims (review) | valid | unread entry moved to the body; hedge marked **Inferred:**; from-memory claims replaced by links to the verified MySQL records (CHECK, NVARCHAR, partitioning) or an explicit verification task |
| 15e | Trust rule clauses mutually exclusive (review); six records "violate the mixed-trust rule" (Copilot) | **convention was wrong** | trust rule rewritten: `verified` describes the load-bearing claims and may carry **Inferred:**-marked asides; the six Copilot records stay verified because their quotations were read and their inferences are marked; "from memory" outside an Inferred line is now a checker error |
| 15f | verified.at earlier than generated.at in nine records (review, plausible) | valid, minor | conventions say re-stamp `verified` only when claims are re-checked; an **Update** log entry now records the convention-alignment edits |
| cut | Duplicate BSD-3 records, dead imports, hardcoded index prose, CI/Enron efficiency items (review) | partly adopted | BSD generic record kept (build-time packages); dead code removed with the rewrite; root intro moved into a preserved marker block; Enron core subset published as a release asset; native.yaml runs on change instead of weekly; the other cuts declined as cosmetic |
| refuted | S9 CHECKSUM TABLE, §7 sizes, oracle-sh FK claim, agpl resource, draft-with-trust, WWI-DW shared resource (review) | agreed | no change |

# Status
accepted
