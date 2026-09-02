---
type: Runbook
title: Executor discipline
description: Non-negotiable working rules for the agent or engineer executing PLAN.md; privilege handling, knowledge-bundle upkeep, deviation handling, and verification-first.
resource: /runbooks/executor-discipline.md
tags:
- process
- executor
- privileges
- okf
status: stable
trust: verified
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:17:31Z"
verified:
- by: claude-code/claude-fable-5-1
  at: "2026-09-02T20:17:31Z"
sources:
- resource: /runbooks/knowledge-bundle-conventions.md
  title: Knowledge bundle conventions
  accessed: "2026-09-02"
---

# 1. Privileges: stop and ask, never work around
If a problem is properly solved by something needing `sudo` or administrator rights — installing system packages, editing Docker Desktop engine settings or `daemon.json`, IPv6 or DNS changes, `sysctl`/ulimit, adding a user to `docker`, mounting or resizing disks, firewall ports — the executor:
1. Stops the current step.
2. Writes the exact change and command(s) in a message to the user using this template:

```
BLOCKED on a privileged change.
Problem: <one sentence, with the observed error>
Proposed fix (requires sudo/admin): <exact command(s) or GUI path>
Why this and not a workaround: <one sentence>
Resume with: <the make target / command I will re-run after you confirm>
```
3. Resumes only after the user confirms. It does not substitute user-space reinstalls, disabled verification, running as root inside containers to dodge a host issue, or hand-patched binaries.

What does **not** need asking: `uv`-managed Python environments, Docker builds and containers (the user is already in the `docker` group), files under the repository, downloads into `./downloads/`.

# 2. Verification-first
Before any step marked "verify first" in PLAN.md, run the named check and record the result as a **Verification** entry in [log.md](/log.md), updating the record it concerns. Never assume a tag, URL, checksum or row count that the plan flags as unverified.

# 3. Knowledge bundle upkeep (every session)
* Append to `log.md` under today's ISO date: **Creation** for new records, **Update** for changed ones, **Verification** for measurements (with the command), **Deviation** for departures from PLAN.md, **Deprecation** when a decision is superseded.
* When a conversion reveals a fact (actual row count, a type-mapping surprise, the tool version actually used, load time), update the dataset record's `# Tests and expected values` or `# Type-mapping hazards`, bump `generated.at`, add the evidence to `sources`, and add a `verified` entry with `process:<script-name>` if a script produced it.
* Any research (reading a doc, README, issue, license) is recorded at that moment in a `sources/` record — one per source artifact (a document, a repository at a commit, a manual page set), every URL read listed under `sources` — with access date, version/commit and the excerpt that mattered. No citation without a record.
* A deviation from PLAN.md gets: a dated **Deviation** log entry, a new or updated `decisions/` record (question, options, evidence, outcome), and an edit to PLAN.md pointing at that record. The old decision is set `status: deprecated` with `superseded-by`.
* Trust marking: a record becomes `trust: verified` only when the claim was read in an authoritative source or produced by a command whose output is recorded. Estimates stay `inferred`.

# 4. Reproducibility rules
* No hand-edited SQL or CSV in the repository. Every artifact under `datasets/*/build/` is produced by `make <dataset>` from the upstream artifact plus committed code.
* Every download goes through `scripts/fetch.py` reading `manifest.yaml`; the script verifies sha256 and skips verified files.
* Every dataset build ends by running its `tests/` and refusing to publish on failure.

# 5. IPv6 first when networking misbehaves
Follow [IPv6 and privileges](/runbooks/ipv6-and-privileges.md) before retrying anything that hung.
