---
type: Decision
title: "Dispositions of the first code review (Claude code-review and GitHub Copilot) on PR #1"
description: Every finding from the first two reviews (and the second Copilot pass) validated against the original request, classified, and resolved as a class or explicitly declined with the reason; the conventions runbook revision 2 came out of this pass.
resource: /decisions/review-2026-09-02-dispositions.md
tags:
- decision
- review
- process
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T22:33:25Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T22:33:25Z"
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

# Outcome, second review (same day, commit c86315b)

| # | Finding (source) | Verdict | Class and resolution |
|---|---|---|---|
| 1 | No network-reachable root account on the baked datadir (review) | valid, design defect | the skipped `docker_setup_db` also loads time-zone tables: builder now creates `root@'%'` (default `root`, overridable) and loads tz data; unsupported `MYSQL_*` env vars documented; S8 tests root over TCP and `CONVERT_TZ` ([bake decision](/decisions/bake-data-vs-initdb.md), [accounts](/decisions/database-naming-convention.md), PLAN §1/§2.2/§4) |
| 2 | ci.yaml builds 12 datasets but S8 expects every core database; CORE_FAST rule contradicts its list (review) | valid | `make image DATASETS=` builds a subset image; S8 asserts the databases named in the built image's registry; CORE_FAST is an explicit curated list (16 datasets) with the exclusion reasons stated |
| 3 | SUM over zero rows is NULL (review) | valid | `COALESCE(...,0)` in the fingerprint ([checksum method](/decisions/test-checksum-method.md)) |
| 4 | SHOW WARNINGS after importTable is vacuous; loader rule contradicted by three sections (review) | valid | one project-wide loader rule in PLAN §2.2 (server-side strict `LOAD DATA`; `importTable` only ≥ 5 M rows with the S4 digest as guard and a verify-first on its summary line); §3.24/3.25/3.26, [large-tabular decision](/decisions/large-tabular-conversion-path.md) and the Shell record aligned |
| 5, 11, 12 | checker crashes on list values; from-memory gate rejects `# Inferred` sections and ignores frontmatter; headings scanned inside code fences; literal Status match; no deprecated path (review) | valid | checker rewritten: type-checked frontmatter, code-stripped heading scan, Inferred section/paragraph aware hedge gate including title/description, Status normalized with accepted/pending/superseded-by/deprecated rules, `verified` shape, BOM/CRLF tolerance, `-` bullets, titled links |
| 6 | line-based fixer has no YAML context (review) | valid, whole approach replaced | `okf_fix_quotes.py` is now a YAML-aware canonicalizer (parse → normalize types → dump, key order kept); the bundle was canonicalized once (block style) and `--check` guards it; the conventions describe the canonical form |
| 7 | index links checked before child indexes are written; shallow subdirectory detection (review) | valid | indexes are all written first, then validated; directory detection and counts are recursive |
| 8 | PLAN §10 still states revision-1 conventions (review) | valid | §10.1 and §10.3 rewritten to revision 2; executor-discipline sources rule aligned |
| 9 | mixed-case identifiers in eight more records (review) | valid, class incomplete last time | all eight records and PLAN §3.2 lower-cased; the earlier sweep only matched `FROM/JOIN` patterns |
| 10 | Employees smoke test names a non-existent view; salary dump sizes (review) | valid | `v_full_departments` named; exact byte sizes |
| 13 | three license Applied-to sections omit linking records (review) | valid | checker now enforces coverage for every Dataset and Tool record that links a license (source records and questions merely cite licenses and are exempt by design); seven gaps filled |
| 14 | extended.yaml scope exceeds `make extended` (review) | valid | workflow defined as `make extended` (release-asset datasets) plus explicit `gen-*` runs; Citi Bike/Divvy excluded from CI; [orchestration](/decisions/build-orchestration.md) names the target |
| 15 | gen_provenance inputs inconsistent; record keys do not match database names (review) | valid | inputs specified once in PLAN §8.2 via `dataset.yaml` (which names the knowledge records and license ids per database), measurements optional; registry columns widened to JSON arrays |
| cut | Sakila definer wording, IPv6 runbook fetch design, §5 clustered-key rule, jaffle tier wording, exit-code doc, BOM/CRLF, `-` bullets, titled links (review) | adopted | fixed alongside the classes above; the remaining cuts (CI double trigger, caching, single-RUN bake layer, tier lists in four places) declined as cosmetic or already documented redundancy |
| C1 | Oracle NUMBER→DECIMAL "always fits"; truncated vs rounded (Copilot) | valid | mapping restricted to `0 ≤ s ≤ p ≤ 38, s ≤ 30` with the converter asserting no negative/oversized scales; rounding wording aligned with the source |
| C2 | PR description says 525 concepts (Copilot) | valid | updated to 526 |
| C3 | BSD record contradicts a verified source record (Copilot) | valid | cites the OSI source record; sqlparse removed |
| C4 | objects.sql function count (Copilot) | valid | five |
| C5 | `okf` package conclusion unsupported (Copilot) | valid | reworded to what the metadata shows (no documented interface; not inspected) |
| C6 | stale sqlparse dependency (Copilot) | valid | sqlparse recorded as evaluated and rejected; converters own their `GO`/`DELIMITER` splitting |

# Outcome, third review (same day, commit 21c9829)

The review coordinator was cut off by a rate limit after dispatching its verifiers, so this round is not a
complete 15-finding set: six verifiers and one finder angle returned, the rest did not. Everything that came
back was validated here (each tooling claim reproduced locally before it was fixed) and is listed below; the
unreturned candidates are unknown and a further review pass is worth running.

| # | Finding | Verdict | Class and resolution |
|---|---|---|---|
| 1 | `okf_fix_quotes.py` re-serialised PyYAML's *parsed* value, so it silently rewrote the author's token: `version: 1.10` → `"1.1"`, `title: yes` → `"True"`, `id: 010` → `"8"`, `stale_after: 12:30` → `"750"`, `100.00` → `"100.0"` | valid, data-loss defect | rewritten: it now composes the frontmatter, finds the plain scalars whose resolved type is not a string, and splices quotes into the raw text at the composer's marks, so the token is preserved verbatim and comments, key order and block scalars are untouched. All five probes now round-trip exactly |
| 2 | The same tool turned an empty `tags:` into the string `None`, and `[a, null]` into a `None` tag | valid | null-tagged and empty scalars are never touched |
| 3 | Its CLI dropped every `--flag`, so `--chekc` (or any typo) silently rewrote 526 records and exited 0; a missing bundle directory reported success | valid | argparse; unknown flags exit 2, a missing or empty bundle exits 2, `--check` is the only read-only mode and is now unmissable |
| 4 | `strip_code` paired an opening fence with any later line starting with the same characters, so a four-backtick block exposed `# X` inside it as a section | valid | replaced with a fence state machine following CommonMark closing rules (same character, at least as long); an unclosed fence swallows the rest of the file |
| 5 | Mixed-case identifiers remained in PLAN §3 count lists, `chinook.md`'s literal `SELECT MIN(InvoiceDate) FROM Invoice` and one WWI line | valid, and the earlier sweep's blind spot | the runnable SQL is lower-cased; the count lists keep the upstream names on purpose (they are the CSV filenames on disk) and each affected subsection now says so and points at `name_map.yaml`, which removes the contradiction without breaking traceability |
| 6 | No reserved-word rule anywhere, and `lahman.md` asserted "`Rank` ... fine" although `RANK` became reserved in MySQL 8.0.2 | valid | rule added to the [naming convention](/decisions/database-naming-convention.md) (backtick reserved identifiers everywhere, mark them in `name_map.yaml`, known instances `teams.rank`, `teamshalf.rank`, `sales_salesterritory.group`, digit-leading `2b`/`3b`); the Lahman statement corrected |
| 7 | The entrypoint wrapper writes a root-owned `mktemp` file but mysqld runs as uid 999 via `gosu`, and passwords were not escaped | valid | the wrapper creates the file with `install -m 0400 -o mysql -g mysql`, single-quotes each password with `\` and `'` doubled, and removes it on a trap |
| 8 | `mysqlsh -u root` without `--no-password` prompts, which cannot succeed in a non-interactive build | valid | `--no-password` added to the builder's load loop |
| 9 | The planned Enron view used `GROUP_CONCAT`, which truncates at 1024 bytes — the same reason it was rejected for checksums — on exactly the broadcast mails the record calls out | valid | the view uses `JSON_ARRAYAGG` |
| 10 | `docker/init/10-registry.sql` is generated into a git-tracked path, absent from the tree and `.gitignore` | valid (the CI-failure mechanism claimed alongside it was wrong) | listed in the tree and ignored |
| 11 | `# Applied to` was checked for omissions but never for stale entries | valid | the checker now compares both directions, with an asymmetric rule: any mention counts against omission, only a bullet's subject link counts as an assertion, and negative or aside bullets are exempt. Five genuine one-way references were found and the missing back-links added (`internet-archive-mirroring`→AGPL, `python-conversion-stack`→BSD, `iris`→BSD, `wikidata`→CC BY-SA 4.0, `tpc-h`→MIT) |
| 12 | The license-coverage check re-scanned every Dataset and Tool body once per License (1,488 pairs, ~63 ms) | valid, efficiency | each record's resolved link targets are cached once during its own check; behaviour verified identical |
| 13 | `dir_has_md` counted a directory holding only a stale `index.md` | valid | only non-reserved files count |
| 14 | `lahman.md` listed a 404 probe under `sources` although nothing was read from it | valid | entry removed (a properly documented source record already covers the probe); the conventions now say when a failed probe *is* a legitimate source |
| 15 | CORE_FAST excluded `dvdstore` "until its release asset exists", but its CSVs are committed | valid | rationale corrected to conversion time |
| 16 | `ipv4_first` is a hand-set flag with no fallback | plausible; every current instance is correctly flagged | `fetch.py` now retries once with `-4` after a connect timeout regardless of the flag, so a newly hanging host needs no manifest edit |
| 17 | "accepted (pending X)" in five decisions is an unhandled status | **refuted** | the count was wrong (5, not 16) and the pattern is the documented convention: the Decision records the choice, a linked Open Question tracks the outstanding measurement. No change |
| 18 | Lahman's release asset would not exist when CI must be green | **refuted** | M-04 publishes it and the DAG puts M-04 before E-01 before R-01. No change |

# Status
accepted
