---
name: worldos-authoring
description: Create, remix, inspect, validate, update, or explicitly publish an owned WorldOS Simulation through the WorldOS MCP. Use when a user wants to design a new world, select and configure WorldOS apps, author characters and opening state, remix an existing world, edit an owned draft, upload its cover, or publish it after review without using a code repository or database access.
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

Call a write tool only when the user clearly asks to create, import, remix, modify, upload to, or publish a WorldOS resource. Publishing is never implied by creation or editing. Call `publish_world` only when the user explicitly asks to publish the identified world in the current conversation and accepts that published worlds can no longer be edited through MCP.

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

### Upload a world cover

1. Fetch the owned draft and retain its exact `updatedAt`.
2. Call `create_world_cover_upload` with the actual JPEG, PNG, or WebP content type and file size when known.
3. Upload the raw file with HTTP `PUT` to the returned signed upload URL before it expires. Do not send the file bytes through an MCP JSON argument.
4. Call `complete_world_cover_upload` with the returned path and the exact current world version.
5. Fetch the world again and verify `config.coverImage` and the new `updatedAt`.

The completion tool validates the file, normalizes it to WebP, moderates it, and attaches the public URL. A failed completion must not be described as uploaded or attached. Fetch a fresh version before retrying after a conflict.

### Publish an owned world

Publishing is a separate, high-impact step. It requires an MCP account with reviewer permission.

1. Confirm that the user explicitly asked to publish this exact world. Creating, finishing, reviewing, or sharing a preview does not imply publishing.
2. Fetch the latest owned world and retain its exact `updatedAt`.
3. Ensure it has a stable HTTPS cover. Use the cover-upload workflow when necessary.
4. Call `validate_world_for_publish`. Repair every error and discuss material warnings with the user.
5. Remind the user that publication makes the world public and ends MCP editing for it.
6. Call `publish_world` with the exact version and the literal confirmation required by the live schema.
7. Report success only from the tool result and return its public world URL.

If reviewer permission is missing, stop with the validation result. Do not bypass the refusal through the website, database, or another account. Unpublishing is outside this workflow.

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

Do not begin from a fixed RPG template. Derive the interaction model from the requested fantasy: a fixed protagonist, a customizable individual, an ensemble relationship drama, an investigation, a household or dynasty, an organization or business, a faction or state, a management builder, or a god-view counterfactual may all need different apps and turn structures. Player setup, quests, inventory, character chats, stats, and maps are optional; include each only when it supports the chosen loop.

Prefer a small, coherent state model over many decorative panels. A persistent fact must have one authoritative owner. Do not duplicate the same money, health, relationship, quest, or inventory value across multiple apps.

## Discover and understand apps

1. Call `search_apps` with focused queries for the capabilities in the design brief. Search results, not memory, determine valid slugs.
2. Call `get_app_guide` for every app under consideration.
3. Read its current defaults, installation contract, type, and exclusivity constraints.
4. Select the smallest set that expresses the core loop and persistent state.
5. Include at least one clear player-action surface.

Match the action surface to the turn structure. Keep single-action input when one decision should resolve the turn. For strategy, operations, or management worlds where one turn represents a coordinated plan, prefer a player-input configuration that can queue several editable actions and execute them together. Use only modes documented by the selected app's live guide; do not invent configuration fields from memory.

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
- Player setup is optional. A fixed protagonist, state, organization, or god-view Simulation may need no name or persona field at all.
- Put setup fields only in `config.initFields`; never invent `setupFields` or another container. Use `{key:"player_name", role:"name"}` and `{key:"player_persona", role:"persona"}` only when those concepts are genuinely part of the experience.
- Use character template variables for references to customizable characters, including references inside every app’s opening data.
- Provide useful defaults and clickable options for required setup fields so a player can start immediately.
- If a setup option claims to change affiliation, location, era, equipment, condition, authority, or another durable opening fact, verify that every option is compatible with the shared opening state or can be represented through a conditional mechanism documented by the live contract. Otherwise narrow the options or split the experience; do not offer cosmetic choices that contradict seeded state.
- Put Advisor presets in `config.advisorPresets` for explanation and strategic guidance, never to take actions on the player’s behalf.

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
- an action-input mode that matches the world's single-decision or coordinated-plan loop;
- unresolved character, faction, region, marker, post, or chat references;
- legacy locale fields;
- region-map geometry and remix safety;
- successful runtime derivation.

Before writing, audit every `{{...}}` token against `config.initFields` and the world character IDs. After writing, use any available read-only browser or page-inspection capability to open the returned preview with default setup values. Check that no raw template token or internal window identifier such as `inv:` or `app:` is visible. If preview inspection is unavailable, state that runtime rendering remains unverified instead of calling the Simulation finished.

For a create, generate a stable idempotency key of 8–200 characters. Reuse the same key only when retrying the exact same intent and identical draft. Change the revision when draft content changes materially.

After a create, call `get_world_summary`. After an update, call `get_owned_world`. Verify title, slug, visibility, installed apps, URLs, and the latest version. A structurally valid draft is not a completed playtest.

## Deliver the result

Report:

- title, slug, and world ID;
- current visibility and whether it remains a draft or was explicitly published;
- editor and preview URLs;
- installed apps and which persistent facts each owns;
- the opening action available to the player;
- validation warnings that remain relevant;
- assets or copy that need human review;
- any unsupported request that was intentionally left undone.

Never say the Simulation is published unless `publish_world` succeeded in this conversation. Otherwise state that it remains unpublished and requires review.

## Hard boundaries

- Do not edit published resources or resources owned by another account.
- Do not delete, transfer, unpublish, or publish without the explicit reviewer workflow above.
- Do not mutate, repair, rewind, rename, or delete saves.
- Do not create built-in apps or modify shared/published apps.
- Do not expose raw operations, state paths, prompts, model/provider details, or other system internals to players.
- Do not bypass an MCP refusal through another data source or private endpoint.
