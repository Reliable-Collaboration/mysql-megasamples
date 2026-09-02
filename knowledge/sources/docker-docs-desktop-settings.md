---
type: Source
title: "Docker Docs: Change your Docker Desktop settings"
description: "Docker Engine settings tab edits a daemon.json at $HOME/.docker/daemon.json; Windows network tab caveats."
resource: https://docs.docker.com/desktop/settings-and-maintenance/settings/
tags: [docker, docker-desktop]
status: stable
trust: verified
generated: { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
verified:
  - { by: "claude-code/claude-fable-5-1", at: "2026-09-02T20:37:05Z" }
sources:
  - resource: https://docs.docker.com/desktop/settings-and-maintenance/settings/
    title: "Docker Docs: Change your Docker Desktop settings"
    accessed: 2026-09-02
---

# What was read
https://docs.docker.com/desktop/settings-and-maintenance/settings/, accessed 2026-09-02.

# Relevant excerpt
> "Configure the Docker daemon using a JSON configuration file. The file is located at $HOME/.docker/daemon.json."
* The page did not (in the fetched text) describe an IPv6 networking-mode switch; only Mac networking options and "On Windows, the Network tab is not available in Windows container mode."

# What it was used to decide
[IPv6 runbook](/runbooks/ipv6-and-privileges.md): confirms the Docker Desktop daemon.json location pattern seen in the [environment survey](/sources/build-machine-environment-2026-09-02.md); any IPv6 toggle in the Desktop GUI is **Inferred** and must be located by the user.
