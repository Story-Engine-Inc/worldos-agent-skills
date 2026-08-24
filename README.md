# WorldOS Agent Skills

[![Validate skills](https://github.com/Story-Engine-Inc/worldos-agent-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/Story-Engine-Inc/worldos-agent-skills/actions/workflows/validate.yml)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![skills.sh](https://skills.sh/b/Story-Engine-Inc/worldos-agent-skills)](https://skills.sh/Story-Engine-Inc/worldos-agent-skills)

Create living, playable AI worlds with Codex, Claude Code, Cursor, GitHub Copilot, and other skills-compatible agents.

[WorldOS](https://worldos.cc/) is an AI world simulation platform and no-code world builder powered by Civilization 1, a world model for human behavior and social simulation. Each WorldOS world is a persistent, interactive Simulation where characters, conversations, social feeds, maps, economies, time, and other apps evolve together—and where players can act freely, publish their creations, and remix community worlds.

This open-source repository provides portable [Agent Skills](https://agentskills.io/) for designing, mapping, extending, publishing, playing, and reviewing WorldOS Simulations through the public [WorldOS Model Context Protocol (MCP)](https://worldos.cc/docs/mcp). The skills add reliable workflows while the MCP remains the capability and security boundary.

[Explore AI-simulated worlds](https://worldos.cc/worlds) · [Create an AI world](https://worldos.cc/worlds/create) · [Browse the WorldOS App Market](https://worldos.cc/apps) · [Read the WorldOS MCP documentation](https://worldos.cc/docs/mcp)

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

> Create a political intrigue Simulation set in a floating city. Give me three rival factions, five chat-able characters, an opening crisis, and meaningful state that persists between turns. Keep it unpublished for review.

The skill reads the live WorldOS authoring contract, discovers suitable apps, drafts the Simulation, validates it, and uses authorized MCP writes only when the request permits them.

## What you can build

- Original role-playing, strategy, social, historical, educational, and narrative Simulations.
- Alternate-history and grand-strategy Simulations like [Pax Historia](https://worldos.cc/pax-historia), where players lead nations, negotiate, wage war, and reshape history on living maps.
- Remixable worlds with characters, chats, stats, inventory, quests, time, social feeds, calendars, email, maps, and other WorldOS apps.
- Region maps with coherent geometry, factions, territorial ownership, labels, and markers.
- Public reusable widgets when the existing WorldOS app catalog does not fit.
- Controlled real-save regression runs through the normal player, billing, counter, and statistics path.
- Read-only playtest reviews covering pacing, persistence, character behavior, and cross-app consistency.

## Skills

| Skill | Use it for |
| --- | --- |
| [`worldos-authoring`](skills/worldos-authoring/SKILL.md) | Design, validate, create, remix, update, cover, and explicitly publish owned WorldOS Simulations. Start here. |
| [`worldos-war-authoring`](skills/worldos-war-authoring/SKILL.md) | Build polity-scale grand-strategy war Simulations from the live canonical rules, eligible source prompts, strategic maps, and isolated playtests. |
| [`worldos-pax-adaptation`](skills/worldos-pax-adaptation/SKILL.md) | Adapt versioned Pax Historia worlds into playable unpublished WorldOS Simulations with explicit persistent state. |
| [`worldos-map-authoring`](skills/worldos-map-authoring/SKILL.md) | Build, remix, and review region maps or tile maps with coherent geometry, terrain, ownership, labels, and markers. |
| [`worldos-widget-authoring`](skills/worldos-widget-authoring/SKILL.md) | Create and update public reusable WorldOS UGC widgets when no existing app fits. |
| [`worldos-simulation-play`](skills/worldos-simulation-play/SKILL.md) | Create a formal owned save and run bounded real turns through the normal player path. |
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

Install all seven skills for every detected agent:

```bash
npx skills add Story-Engine-Inc/worldos-agent-skills --all
```

The open `skills` CLI supports Codex, Claude Code, Cursor, GitHub Copilot, Gemini CLI, OpenCode, and many other agents. Installing a skill does not configure the WorldOS MCP; complete both steps before authoring.

## Example prompts

- “Create a bilingual cyberpunk detective world with chats, email, inventory, time, and a case board. Validate it, but do not publish it.”
- “Remix my existing world into a Renaissance banking rivalry while preserving its installed app structure.”
- “Add a regional map with six connected districts, two factions, readable labels, and ownership that matches the characters.”
- “Search the app catalog first. If nothing supports a relationship evidence board, create a public reusable widget.”
- “Create a fresh real save in my Hogwarts Simulation and use at most three turns to verify that character statistics update and persist. I understand this may spend Zaps and affect normal statistics.”
- “Review my latest save and tell me whether time, inventory, relationships, and quest progress remain consistent. Do not change anything.”
- “Upload this image as my world's cover, validate it for publishing, and show me any remaining issues. Do not publish yet.”
- “Adapt this exact Pax Historia preset version into an unpublished WorldOS Simulation. Preserve the player fantasy and Advisor intent, but rebuild prompt-only mechanics as app-owned persistent state.”

See [examples/prompts.md](examples/prompts.md) for more prompts and the expected workflow boundaries.

## Why Skills and MCP work together

The MCP provides authenticated tools, live schemas, ownership checks, validation, and version controls. The skills provide procedural knowledge: how to choose apps, place opening state, structure localization, design maps, avoid duplicate state ownership, and review a world before publishing.

This separation keeps the workflow portable across agents and resilient as the WorldOS authoring API evolves:

- Every authoring workflow begins with the live `get_authoring_guide` response.
- Existing apps are searched and understood before a new widget is considered.
- When an official app satisfies a required capability, it is preferred over a non-official app; non-official apps remain available when no official app fits or the creator explicitly requests one.
- World payloads are validated before any write.
- Creates use idempotency keys; updates fetch the current resource and use its exact version.
- Only resources owned by the authorized account can be edited. Published worlds remain directly editable; each successful edit preserves public visibility and advances to a new immutable release.
- Publishing is never implied. It requires an explicit request, clean publish validation, the latest world version, and the same ownership and product rules as the WorldOS editor.
- Save review is read-only. Real save creation and turns require separate explicit consent and use the normal persistent, metered, counting player path.
- Skills never bypass the MCP through Supabase, SQL, private APIs, or repository internals.

## Repository layout

```text
skills/
  worldos-authoring/
  worldos-war-authoring/
  worldos-pax-adaptation/
  worldos-map-authoring/
  worldos-widget-authoring/
  worldos-simulation-play/
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
