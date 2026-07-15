# WorldOS Agent Skills

Portable Agent Skills for creating, editing, mapping, and reviewing WorldOS Simulations through the WorldOS MCP.

The skills are written against the open Agent Skills format and are designed for Codex, Claude Code, Cursor, GitHub Copilot, and other skills-compatible agents. The WorldOS MCP remains the capability and security boundary; these skills provide reliable authoring workflows on top of it.

## Skills

| Skill | Purpose |
| --- | --- |
| `worldos-authoring` | Design, validate, create, remix, and update unpublished WorldOS Simulation drafts. |
| `worldos-map-authoring` | Build and review region maps with coherent geometry, factions, ownership, labels, and markers. |
| `worldos-widget-authoring` | Create and update private reusable WorldOS UGC widgets when no existing app fits. |
| `worldos-simulation-review` | Inspect owned saves and turn history read-only to evaluate whether a Simulation behaves as designed. |

Start with `worldos-authoring`. The other skills are conditional specialists.

## Install skills

List the available skills:

```bash
npx skills add Story-Engine-Inc/worldos-agent-skills --list
```

Install the core skill for Codex:

```bash
npx skills add Story-Engine-Inc/worldos-agent-skills \
  --skill worldos-authoring \
  --agent codex
```

Install the core skill for Claude Code:

```bash
npx skills add Story-Engine-Inc/worldos-agent-skills \
  --skill worldos-authoring \
  --agent claude-code
```

Install every skill interactively:

```bash
npx skills add Story-Engine-Inc/worldos-agent-skills
```

## Connect the WorldOS MCP

Installing a skill does not configure external tools. Connect the WorldOS MCP separately and complete OAuth in the client. Never paste an access token into a prompt or skill file.

Endpoint:

```text
https://worldos.cc/api/mcp
```

Codex:

```bash
codex mcp add worldos --url https://worldos.cc/api/mcp
codex mcp login worldos
```

Claude Code:

```bash
claude mcp add --transport http worldos https://worldos.cc/api/mcp
```

Then run `/mcp` in Claude Code to authenticate when prompted.

## How the skills behave

- Every authoring workflow begins with the live WorldOS MCP `get_authoring_guide` response.
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
scripts/
  validate-skills.mjs
skills.sh.json
```

The `skills/` directory is the portable source of truth. Platform-specific plugin packages may be generated from it later, but the core instructions do not use vendor-specific invocation syntax or tool-name prefixes.

## Validate changes

```bash
npm run validate
```

The validator checks skill metadata, names, references, skills.sh groupings, accidental local paths, unresolved placeholders, and common secret patterns.

## Security

WorldOS authorization, ownership checks, validation, version conflicts, and publishing restrictions are enforced by the MCP server. Skills are workflow guidance, not a security boundary.

Review a skill before installing it. Report security concerns according to [SECURITY.md](SECURITY.md).

## skills.sh

[![skills.sh](https://skills.sh/b/Story-Engine-Inc/worldos-agent-skills)](https://skills.sh/Story-Engine-Inc/worldos-agent-skills)

Once the public repository is installed through the `skills` CLI with telemetry enabled, skills.sh can index it automatically.
