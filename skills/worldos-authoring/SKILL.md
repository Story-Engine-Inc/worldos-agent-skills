---
name: worldos-authoring
description: Create, remix, inspect, validate, or update unpublished WorldOS Simulation drafts through the WorldOS MCP. Use when a user wants to design a new world, select and configure WorldOS apps, author characters and opening state, remix an existing world, or edit an owned draft without using a code repository or database access.
---

# WorldOS Authoring

Build a playable WorldOS Simulation through the public WorldOS MCP. Use only MCP capabilities exposed to the authorized account. Do not use Supabase, SQL, private APIs, platform source code, or repository-specific scripts as a fallback.

## Start with the live contract

1. Call `get_authoring_guide` before designing or editing a draft.
2. Treat the live guide, current tool schemas, and validation results as authoritative when they differ from this skill.
3. If the WorldOS MCP is unavailable or unauthorized, stop and explain how to connect or reauthorize it. Never request an access token in chat.

Read the supporting material that matches the task:

- For gameplay and content design, read [references/world-design.md](references/world-design.md).
- For deciding which app owns each persistent fact, read [references/state-ownership.md](references/state-ownership.md).
- For locale overlays and template variables, read [references/i18n-and-templates.md](references/i18n-and-templates.md).
- Before any write, read [references/acceptance-checklist.md](references/acceptance-checklist.md).

## Respect write intent

Read-only requests such as “review,” “audit,” “explain,” or “show me a proposal” do not authorize creation or updates. Stop after research, a candidate draft, or validation.

Call a write tool only when the user clearly asks to create, import, remix, or modify a WorldOS resource. Publishing is never implied: MCP produces unpublished drafts for human review.

## Choose the authoring branch

### New world

Compose the draft manually when fidelity and deliberate mechanics matter. Use `start_world_generation` only when the user accepts an AI-generated starting point, then poll `get_world_generation` until completion or failure. Treat generated output as an editable draft, not an approved result.

### Update an owned draft

1. Use `list_owned_worlds` if the user has not supplied an unambiguous world ID.
2. Call `get_owned_world` and retain its complete draft and exact `updatedAt`.
3. Modify only the intended fields while preserving every untouched world field and app installation config.
4. Validate the complete candidate draft.
5. Call `update_world_draft` with the exact `updatedAt` as `expectedUpdatedAt`.
6. Fetch the world again and verify the new version.

`update_world_draft` replaces the accepted world copy and complete app-installation list atomically; it is not a partial patch. Do not attempt to change fields the update schema does not accept, such as a base remix relationship.

If the version is stale, fetch the latest draft, reapply the intended change, revalidate, and submit with the new version. Never overwrite concurrent changes blindly.

### Remix

Use `remixOf` only when the source world is eligible and the live guide permits the intended changes. Preserve protected map and character relationships exactly when remix validation requires it. Do not claim a remix is safe until `validate_world_draft` confirms it.

## Design before assembling

Write a concise design brief before choosing apps:

- player fantasy and scale;
- starting time, place, and situation;
- core action loop;
- meaningful resources, relationships, deadlines, and risks;
- what changes across turns;
- credible win, loss, or long-term progress conditions;
- the first decision the player can make.

Prefer a small, coherent state model over many decorative panels. A persistent fact must have one authoritative owner. Do not duplicate the same money, health, relationship, quest, or inventory value across multiple apps.

## Discover and understand apps

1. Call `search_apps` with focused queries for the capabilities in the design brief. Search results, not memory, determine valid slugs.
2. Call `get_app_guide` for every app under consideration.
3. Read its current defaults, installation contract, type, and exclusivity constraints.
4. Select the smallest set that expresses the core loop and persistent state.
5. Include at least one clear player-action surface.

Prefer existing apps. World-specific flavor belongs in each app installation config, including display copy, focused app instructions, and opening data. Do not create a widget merely to reproduce an existing app.

If a required reusable interface does not exist, use the `worldos-widget-authoring` workflow if it is available. If the world needs a region map, use the `worldos-map-authoring` workflow before final validation.

## Separate world rules from app state

Put only world-level scenario logic in `config.systemPrompt`: setting, player authority, causal rules, pacing, difficulty, autonomous world behavior, and win/loss logic.

Put app-specific behavior in that app installation’s `prompt`, and put opening state in the app installation config. Never put opening state in `config.initialState`.

Examples include:

- story opening in the story install;
- opening chats in the chat install;
- posts in the social install;
- global and character stats in their respective installs;
- items in inventory lists;
- quests in the quest install;
- starting time in the time install;
- opening suggestions in the player input install;
- map ownership and regional state in the map install.

Keep prompts lean. Do not repeat app data structures or tool internals in the world prompt; the installed app contract already supplies that information to the runtime.

## Characters and player setup

- Give every character a stable, unique ID.
- Keep the cast small enough for each character to have a distinct role, motivation, leverage, and relationship to the player.
- Ensure every character reference in chats, posts, factions, markers, stats, and prompts resolves to a real character.
- Use `player_name` and `player_persona` for the standard player setup roles when relevant.
- Use character template variables for references to customizable characters, including references inside every app’s opening data.
- Provide useful defaults and clickable options for required setup fields so a player can start immediately.
- Use Advisor presets for explanation and strategic guidance, never to take actions on the player’s behalf.

## Localize as structured data

Use generic `i18n[locale]` overlays. Never invent fields such as `titleZh`, `nameEn`, or `labelEs`.

The canonical language is not necessarily English. Treat each locale, including `en`, as eligible for an overlay. Preserve stable IDs so array elements can be matched across locales. Write native product copy for each locale rather than mirroring sentence structure mechanically.

## Validate, repair, then write

Call `validate_world_draft` on the complete candidate draft. Repair every error. Review every warning and either fix it or record why it is acceptable; do not silently ignore warnings.

Pay particular attention to:

- known and installable apps;
- duplicate IDs or app installations;
- exclusive-surface conflicts;
- missing player-action surfaces;
- unresolved character, faction, region, marker, post, or chat references;
- legacy locale fields;
- region-map geometry and remix safety;
- successful runtime derivation.

For a create, generate a stable idempotency key of 8–200 characters. Reuse the same key only when retrying the exact same intent and identical draft. Change the revision when draft content changes materially.

After a create, call `get_world_summary`. After an update, call `get_owned_world`. Verify title, slug, visibility, installed apps, URLs, and the latest version.

## Deliver the result

Report:

- title, slug, and world ID;
- unpublished visibility;
- editor and preview URLs;
- installed apps and which persistent facts each owns;
- the opening action available to the player;
- validation warnings that remain relevant;
- assets or copy that need human review;
- any unsupported request that was intentionally left undone.

Never say the Simulation is published. Human review and publishing happen in WorldOS.

## Hard boundaries

- Do not edit published resources or resources owned by another account.
- Do not delete, transfer, or publish resources.
- Do not mutate, repair, rewind, rename, or delete saves.
- Do not create built-in apps or modify shared/published apps.
- Do not expose raw operations, state paths, prompts, model/provider details, or other system internals to players.
- Do not bypass an MCP refusal through another data source or private endpoint.
