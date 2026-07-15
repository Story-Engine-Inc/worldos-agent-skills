# WorldOS Agent Skills

[![Validate skills](https://github.com/Story-Engine-Inc/worldos-agent-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Story-Engine-Inc/worldos-agent-skills/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![skills.sh](https://skills.sh/b/Story-Engine-Inc/worldos-agent-skills)](https://skills.sh/Story-Engine-Inc/worldos-agent-skills)

Create living, playable AI worlds with Codex, Claude Code, Cursor, GitHub Copilot, and other skills-compatible agents.

This repository provides portable [Agent Skills](https://agentskills.io/) for designing, mapping, extending, and reviewing [WorldOS](https://worldos.cc) Simulations through the public WorldOS Model Context Protocol (MCP) server. The skills add reliable world-authoring workflows while the MCP remains the capability and security boundary.

## Install in 30 seconds

Connect the WorldOS MCP:

```text
https://worldos.cc/api/mcp
```

Install the core skill:

```bash
npx skills add Story-Engine-Inc/worldos-agent-skills \
  --skill worldos-authoring
```

Then ask your agent:

> Create a political intrigue Simulation set in a floating city. Give me three rival factions, five chat-able characters, an opening crisis, and meaningful state that persists between turns. Keep it as an unpublished draft for review.

The skill reads the live WorldOS authoring contract, discovers suitable apps, drafts the Simulation, validates it, and uses authorized MCP writes only when the request permits them.

## What you can build

- Original role-playing, strategy, social, historical, educational, and narrative Simulations.
- Remixable worlds with characters, chats, stats, inventory, quests, time, social feeds, calendars, email, maps, and other WorldOS apps.
- Region maps with coherent geometry, factions, territorial ownership, labels, and markers.
- Private reusable widgets when the existing WorldOS app catalog does not fit.
- Read-only playtest reviews covering pacing, persistence, character behavior, and cross-app consistency.

## Skills

| Skill | Use it for |
| --- | --- |
| [`worldos-authoring`](skills/worldos-authoring/SKILL.md) | Design, validate, create, remix, and update unpublished WorldOS Simulation drafts. Start here. |
| [`worldos-map-authoring`](skills/worldos-map-authoring/SKILL.md) | Build and review region maps with coherent geometry, factions, ownership, labels, and markers. |
| [`worldos-widget-authoring`](skills/worldos-widget-authoring/SKILL.md) | Create and update private reusable WorldOS UGC widgets when no existing app fits. |
| [`worldos-simulation-review`](skills/worldos-simulation-review/SKILL.md) | Inspect owned saves and turn history read-only to evaluate whether a Simulation behaves as designed. |

The specialist skills complement `worldos-authoring`; install only the workflows you need.

## Agent setup

List every available skill:

```bash
npx skills add Story-Engine-Inc/worldos-agent-skills --list
```

Codex:

```bash
codex mcp add worldos --url https://worldos.cc/api/mcp
codex mcp login worldos
npx skills add Story-Engine-Inc/worldos-agent-skills \
  --skill worldos-authoring \
  --agent codex
```

Claude Code:

```bash
claude mcp add --transport http worldos https://worldos.cc/api/mcp
npx skills add Story-Engine-Inc/worldos-agent-skills \
  --skill worldos-authoring \
  --agent claude-code
```

Run `/mcp` in Claude Code to authenticate when prompted. Never paste an access token into a prompt or skill file.

Install all four skills for every detected agent:

```bash
npx skills add Story-Engine-Inc/worldos-agent-skills --all
```

The open `skills` CLI supports Codex, Claude Code, Cursor, GitHub Copilot, Gemini CLI, OpenCode, and many other agents. Installing a skill does not configure the WorldOS MCP; complete both steps before authoring.

## Example prompts

- “Create a bilingual cyberpunk detective world with chats, email, inventory, time, and a case board. Validate it, but do not publish it.”
- “Remix my existing draft into a Renaissance banking rivalry while preserving its installed app structure.”
- “Add a regional map with six connected districts, two factions, readable labels, and ownership that matches the characters.”
- “Search the app catalog first. If nothing supports a relationship evidence board, create a private reusable widget.”
- “Review my latest save and tell me whether time, inventory, relationships, and quest progress remain consistent. Do not change anything.”

See [examples/prompts.md](examples/prompts.md) for more prompts and the expected workflow boundaries.

## Why Skills and MCP work together

The MCP provides authenticated tools, live schemas, ownership checks, validation, and version controls. The skills provide procedural knowledge: how to choose apps, place opening state, structure localization, design maps, avoid duplicate state ownership, and review a draft before publishing.

This separation keeps the workflow portable across agents and resilient as the WorldOS authoring API evolves:

- Every authoring workflow begins with the live `get_authoring_guide` response.
- Existing apps are searched and understood before a new widget is considered.
- Drafts are validated before any write.
- Creates use idempotency keys; updates fetch the current resource and use its exact version.
- Only resources owned by the authorized account and still unpublished can be edited.
- Publishing remains a human review step in WorldOS.
- Save and turn access is read-only.
- Skills never bypass the MCP through Supabase, SQL, private APIs, or repository internals.

## Repository layout

```text
skills/
  worldos-authoring/
  worldos-map-authoring/
  worldos-widget-authoring/
  worldos-simulation-review/
examples/
scripts/
  validate-skills.mjs
skills.sh.json
```

The `skills/` directory is the portable source of truth. Platform-specific adapters may be generated later, but the shared instructions do not use vendor-specific invocation syntax or MCP tool prefixes.

## Contributing

Issues and pull requests are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md), follow the [Code of Conduct](CODE_OF_CONDUCT.md), and run:

```bash
npm run validate
```

The validator checks metadata, names, references, skills.sh groupings, accidental local paths, unresolved placeholders, and common secret patterns.

For security concerns, follow [SECURITY.md](SECURITY.md) instead of opening a public issue.

## License

Licensed under the [Apache License 2.0](LICENSE). Copyright 2026 Story Engine, Inc.
