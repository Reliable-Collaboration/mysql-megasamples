---
type: Decision
title: One configuration file names the stack; the chooser writes it and compose.yaml is generated from it
description: megasamples.yaml holds the engines, the datasets per engine and the consoles; an interactive configurator writes it, every command reads it, and compose.yaml is generated so the running stack is exactly what was chosen.
resource: /decisions/stack-configuration.md
tags:
- decision
- configuration
- compose
- console
status: stable
trust: inferred
generated:
  by: claude-code/claude-fable-5-1
  at: "2026-09-09T18:09:52Z"
sources:
- resource: /decisions/browsing-console-stack.md
  title: the console stack and its rules (loopback ports, both accounts, no UI in the image)
  accessed: "2026-09-09"
- resource: /decisions/build-orchestration.md
  title: how a build is orchestrated
  accessed: "2026-09-09"
---

# Question
With more than one engine, and consoles that browse some engines and not others, how does a user
say what to build and run, and how does the stack follow that choice without hand-editing Compose?

# Options considered
1. **One file, `megasamples.yaml`, written by an interactive chooser and read by every command;
   `compose.yaml` generated from it** (chosen).
2. A static `compose.yaml` with a Compose profile per engine and per console — rejected: a console
   configured for an engine that is not running shows dead connections, and the per-console
   environment cannot be made conditional inside a static file.
3. Environment variables and `make` arguments for every choice — rejected: the choice has to be
   repeatable and reviewable, and a matrix of engines against datasets does not fit in a variable.

# Evidence
* [Browsing console stack](/decisions/browsing-console-stack.md): the rules the generated file
  keeps — loopback ports, memory limits, digest-pinned images, both accounts, no UI inside an image.
* [Build orchestration](/decisions/build-orchestration.md): every `make` target is a shim over the
  package, so the configuration is read in one place.

# Outcome
* `megasamples.yaml`: `engines.<name>.datasets` (a selector — core, quick, all, a tier — or a
  list), `consoles`, `ports`, `build`, `downloads`. Without the file the built-in default is
  MySQL with the core tier and the four consoles. `megasamples.example.yaml` documents every key.
* `megasamples configure` is a full-screen chooser (engines; the dataset-by-engine matrix showing
  tier, download size and whether the download is already verified on the machine; consoles) with a
  line-by-line fallback and non-interactive flags. It writes the file; nothing else does.
* `megasamples compose` generates `compose.yaml` (git-ignored) and `megasamples up` runs it
  first: only the engines chosen, only the consoles that can browse one of them, each console
  configured for every engine present, read-only account first. The console registry
  (`megasamples/consoles.py`) is where a console declares which engines it supports.
* `megasamples run` executes the configuration end to end: fetch, build, verify and bake for every
  engine named; the configuration validates itself first (unknown engines, consoles with no engine
  to browse, port clashes, an engine with no datasets).

# Status
accepted
