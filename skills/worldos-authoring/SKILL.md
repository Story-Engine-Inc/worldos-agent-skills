---
name: worldos-authoring
description: Create, remix, inspect, validate, directly update, or explicitly publish an owned WorldOS Simulation through the WorldOS MCP. Use when a user wants to design a new world, select and configure WorldOS apps, author characters and opening state, remix an existing world, edit an owned unpublished or published world, upload its cover, or publish it after review without using a code repository or database access.
---

# WorldOS Authoring

Build a playable WorldOS Simulation through the public WorldOS MCP. Use only MCP capabilities exposed to the authorized account. Do not use Supabase, SQL, private APIs, platform source code, or repository-specific scripts as a fallback.

## Start with the live contract

1. Call `get_authoring_guide` before designing or editing a world.
2. Treat the live guide and current tool schemas as the transport contract. Validation errors are write blockers; warnings describe quality or compatibility concerns and may be consciously accepted when the runtime supports the world.
3. If the WorldOS MCP is unavailable or unauthorized, stop and explain how to connect or reauthorize it. Never request an access token in chat.

Read the supporting material that matches the task:

- For gameplay and content design, read [references/world-design.md](references/world-design.md).
- For deciding which app owns each persistent fact, read [references/state-ownership.md](references/state-ownership.md).
- For locale overlays and template variables, read [references/i18n-and-templates.md](references/i18n-and-templates.md).
- Before any write, read [references/acceptance-checklist.md](references/acceptance-checklist.md).

When the player controls a polity or faction and durable territorial war drives the core loop, use the `worldos-war-authoring` specialist workflow and its live canonical template. Do not infer that workflow merely from a war-themed setting.

## Respect write intent

Read-only requests such as “review,” “audit,” “explain,” or “show me a proposal” do not authorize creation or updates. Stop after research, a candidate world payload, or validation.

Call a write tool only when the user clearly asks to create, import, remix, modify, upload to, or publish a WorldOS resource. Publishing is never implied by creation or editing. Call `publish_world` only when the user explicitly asks to make an unpublished identified world public in the current conversation. An edit to an already-public world is applied directly, remains public, and advances its release version.

## Choose the authoring branch

### New world

Compose the world payload manually when fidelity and deliberate mechanics matter. Use `start_world_generation` only when the user accepts an AI-generated starting point, then poll `get_world_generation` until completion or failure. Treat generated output as editable candidate data, not an approved result.

### Update an owned world

1. Use `list_owned_worlds` if the user has not supplied an unambiguous world ID.
2. Call `get_owned_world` and retain its complete `world` payload and exact `updatedAt`.
3. Inspect the returned read-only `localizationStatus`. It audits actual world and installed-App overlay coverage; do not infer readiness from `config.localization` alone. If the user asked to repair missing translations, call `request_world_localization` with the exact `updatedAt`, then poll `get_owned_world` until the job completes or needs attention.
4. Modify only the intended fields while preserving every untouched world field and app installation config.
5. Call `validate_world` on the complete candidate world.
6. Call `patch_world` for bounded world-copy or app-install changes when the live contract exposes it; otherwise call `update_world` with the complete candidate. Pass the exact `updatedAt` as `expectedUpdatedAt` either way.
7. Fetch the world again and verify the new version.

`update_world` replaces the accepted world copy and complete app-installation list atomically. `patch_world` merges a bounded section but still validates and saves the complete result atomically. A published world remains public and receives a new immutable release version. Do not attempt to change fields the selected schema does not accept, such as a base remix relationship.

If the version is stale, fetch the latest world, reapply the intended change, revalidate, and submit with the new version. Never overwrite concurrent changes blindly.

If a write reports concurrent changes from another editor session, do not retry around the guard or discard that work. Ask the user to resolve the editor session, then fetch, reapply, and validate the intended MCP change against the resulting world.

### Update a world's default layout

Default desktop and mobile window layouts are live presentation metadata, not versioned Simulation content. Change them only when the user explicitly asks to arrange or update the world's default layout.

1. Call `get_world_layout` for the owned world and retain its exact layout `updatedAt`.
2. Preserve the other platform's defaults when changing only desktop or mobile layout.
3. Call `update_world_layout` with the exact `updatedAt` and only `windows`, `windowsRef`, or `mobileLayout` fields accepted by the live schema.
4. Fetch the layout again and verify the intended values.

Do not put `windows`, `windowsRef`, or `mobileLayout` in `create_world`, `update_world`, or `patch_world`. Layout updates take effect without `publish_world` and do not authorize publication. Player-saved personal layouts continue to override the world default. On a layout-version conflict, fetch the latest layout, reapply the requested arrangement, and retry instead of overwriting concurrent work.

### Upload a world cover

1. Fetch the owned world and retain its exact `updatedAt`.
2. Call `create_world_cover_upload` with the actual JPEG, PNG, WebP, GIF, MP4, or WebM content type and file size when known.
3. Upload the raw file with HTTP `PUT` to the returned signed upload URL before it expires. Do not send the file bytes through an MCP JSON argument.
4. Call `complete_world_cover_upload` with the returned path and the exact current world version.
5. Fetch the world again and verify `config.coverImage` and the new `updatedAt`.

The completion tool validates and moderates the file, then directly attaches its public URL to the owned world. JPEG, PNG, and WebP inputs normalize to WebP; GIF and video inputs remain in their original supported format. A failed completion must not be described as uploaded or attached. Fetch a fresh version before retrying after a conflict.

### Upload other world assets

When exposed by the live contract, use the target-bound world-asset upload for character avatars, faction flags, map backgrounds, and installed-app backgrounds. Fetch the exact world version, create an upload for the intended target, upload the raw image to the signed URL, and complete with the same target and version. Re-fetch and verify the destination field. Never reuse a staged path for another target or describe an uncompleted upload as attached.

### Publish an owned world

Publishing is a separate, high-impact step available to an authorized creator for a world they own.

1. Confirm that the user explicitly asked to publish this exact world. Creating, finishing, reviewing, or sharing a preview does not imply publishing.
2. Fetch the latest owned world and retain its exact `updatedAt`.
3. Confirm the intended release visibility and remix setting. A stable HTTPS cover improves discovery but is not required when validation reports it only as a warning.
4. Call `validate_world_for_publish`. Repair every error and discuss material warnings with the user.
5. Explain that publication makes the world public; later direct edits preserve public visibility and advance its immutable release while existing Simulation saves remain pinned until their player accepts an update.
6. Call `publish_world` with the exact version and the literal confirmation required by the live schema.
7. Report success only from the tool result and return its public world URL.

If ownership, moderation, subscription, or another shared product rule blocks publication, stop with the validation result. Do not bypass the refusal through the website, database, or another account. Unpublishing is outside this workflow.

### Remix

Use `remixOf` only when the source permits remixing or the authorized creator owns it. A remix may change prose, apps, characters, region maps, or tile maps within the ordinary live schemas; preserve source fields only when the user intends to keep them. Do not claim a remix is ready until `validate_world` has no blocking errors.

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
4. When an official app satisfies a required capability, prefer it over a non-official app. Use a non-official app when no official app fits or the user explicitly requests it; do not install an irrelevant official app merely because it is official.
5. Select the smallest set that expresses the core loop and persistent state.
6. Include at least one clear player-action surface.

Match the action surface to the turn structure. Keep single-action input when one decision should resolve the turn. For strategy, operations, or management worlds where one turn represents a coordinated plan, prefer a player-input configuration that can queue several editable actions and execute them together. Use only modes documented by the selected app's live guide; do not invent configuration fields from memory.

Prefer existing apps. World-specific flavor belongs in each app installation config, including display copy, focused app instructions, and opening data. Do not create a widget merely to reproduce an existing app.

If a required reusable interface does not exist, use the `worldos-widget-authoring` workflow if it is available. If the world needs a region map, use the `worldos-map-authoring` workflow before final validation. If it is a polity-scale grand-strategy war world, use `worldos-war-authoring` before composing prompts or selecting the action surface.

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

Record external source identity, exact URL and version, retrieval time, hashes, license, and concise notes in the live structured provenance field when one exists. Public readability does not establish permission to copy source prose or assets.

## Characters and player setup

- Give every character a stable, unique ID.
- Keep the cast small enough for each character to have a distinct role, motivation, leverage, and relationship to the player.
- Ensure every character reference in chats, posts, factions, markers, stats, and prompts resolves to a real character.
- Use `hidden:true` only for a spoiler character the AI should introduce later. State the entrance condition in world-level scenario rules, and keep that character out of player-visible opening chats, posts, calendars, dating profiles, markers, and other rosters. Private character-stat opening data may still establish their initial condition.
- Player setup is optional. A fixed protagonist, state, organization, or god-view Simulation may need no name or persona field at all.
- Put setup fields only in `config.initFields`; never invent `setupFields` or another container. Use `{key:"player_name", role:"name"}` and `{key:"player_persona", role:"persona"}` only when those concepts are genuinely part of the experience.
- Use character template variables for references to customizable characters, including references inside every app’s opening data.
- Provide useful defaults and clickable options for required setup fields so a player can start immediately.
- If a setup option claims to change affiliation, location, era, equipment, condition, authority, or another durable opening fact, verify that every option is compatible with the shared opening state or can be represented through a conditional mechanism documented by the live contract. Otherwise narrow the options or split the experience; do not offer cosmetic choices that contradict seeded state.
- Put Advisor presets in `config.advisorPresets` for explanation and strategic guidance, never to take actions on the player’s behalf.

When Achievements supports the intended loop, author a fixed roster of 10–14 consequential outcomes: roughly half attainable bronze milestones, 4–5 difficult silver goals, 2–3 exceptional gold outcomes, and 2–3 genuinely hidden discoveries. Reward choices, victories, completed relationship or objective routes, mutually exclusive paths, and endings. Do not reward mere turn counts, message counts, opening an App, or an automatic first-turn event. Leave Achievements uninstalled rather than shipping an empty roster.

## Localize as structured data

Use generic `i18n[locale]` overlays. Never invent fields such as `titleZh`, `nameEn`, or `labelEs`.

The canonical language is not necessarily English. Treat each locale, including `en`, as eligible for an overlay. Preserve stable IDs so array elements can be matched across locales. Write native product copy for each locale rather than mirroring sentence structure mechanically.

`get_owned_world.localizationStatus` is the readiness authority for authoring. It reports actual missing world fields and App fields per locale, the persisted `availableLocales`, and whether the two agree. When translations are incomplete or inconsistent, use `request_world_localization`; it queues a complete en/es/zh repair without publishing the world or changing its visibility. Re-fetch until every requested locale is ready and the status is consistent. Do not claim success merely because a localization job was queued.

## Validate, repair, then write

Call `validate_world` on the complete candidate world. Repair every error. Review every warning and either fix it or record why it is acceptable; do not silently ignore warnings.

For a new world, call `create_world` only after validation and write authorization. Pass the canonical content locale accepted by the live schema. Creation returns an owned unpublished world immediately; it does not create a separate draft resource and it does not publish. Use the returned `updatedAt` for any subsequent exact-version edit.

For a large candidate, call `inspect_world_payload` before strict validation. Use bounded exact-version world patches and validated map batches instead of repeatedly resending a near-limit payload. Re-fetch after each successful batch.

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

For a create, generate a stable idempotency key of 8–200 characters. Reuse the same key only when retrying the exact same intent and identical world payload. Change the revision when content changes materially.

After a create, call `get_world_summary`. After an update, call `get_owned_world`. Verify title, slug, visibility, installed apps, URLs, and the latest version. A structurally valid world is not a completed playtest.

For a new world or a change that affects opening state, prompts, apps, maps, pacing, or progression, use the live isolated-playtest tools when available:

1. Call `start_world_playtest` with default or deliberately chosen setup values and inspect the player-visible opening.
2. Call `playtest_world_turn` with the exact session version for a bounded sequence of natural-language actions. Attach player-visible assertions when the live schema supports them and check detailed changes rather than surface names alone.
3. Use `get_world_playtest` to recover the latest version after a lost response or version conflict. Use the temporary history tool, when available, to review all completed changes and assertion results.
4. If the world changes, discard the stale session and start again; playtests are bound to the world version they began from.
5. Call `delete_world_playtest` after review. Do not leave temporary sessions merely to preserve evidence.

Test proportionately. A new gameplay world normally needs an ordinary action, quiet or waiting behavior, a difficult or failed attempt, time progression, and one core resource, relationship, objective, or map consequence. A copy-only metadata edit does not require replaying the full loop. Temporary playtests never authorize changes to real saves.

## Deliver the result

Report:

- title, slug, and world ID;
- current visibility and whether it remains unpublished, was explicitly published, or was directly updated while public;
- editor and preview URLs;
- installed apps and which persistent facts each owns;
- the opening action available to the player;
- validation warnings that remain relevant;
- whether an explicitly requested live default-layout change was applied and verified;
- isolated playtest actions run, player-visible surfaces changed, any unresolved defects, and checks that remain unverified;
- assets or copy that need human review;
- any unsupported request that was intentionally left undone.

Never say an unpublished world was published unless `publish_world` succeeded in this conversation. For a previously public world, report that the direct edit preserved public visibility and advanced its version; for a new world, state that it remains unpublished and requires review.

## Hard boundaries

- Do not edit resources owned by another account or blocked resources. Direct writes to an owned public world must use the exact-versioned MCP tools so the outgoing immutable release is preserved.
- Do not delete, transfer, unpublish, or publish without the explicit owner workflow above.
- Do not mutate, repair, rewind, rename, or delete real saves. Use only live isolated-playtest tools for temporary authoring sessions.
- Do not create built-in apps or modify official apps or Apps owned by another creator. Owned public widgets may be updated, with the understanding that the change affects every installation.
- Do not expose raw operations, state paths, prompts, model/provider details, or other system internals to players.
- Do not bypass an MCP refusal through another data source or private endpoint.
