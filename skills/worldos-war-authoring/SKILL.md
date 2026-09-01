---
name: worldos-war-authoring
description: Design, inspect, remix, validate, create, or update WorldOS grand-strategy war Simulations through the WorldOS MCP. Use when the player controls a polity, state, faction, empire, or military organization and durable territorial control, fronts, diplomacy, logistics, production, or national survival drive the core loop. Use for historical, alternate-history, modern, fantasy, or science-fiction strategic wars; do not use merely because an individual-scale story happens during a war.
---

# WorldOS War Authoring

Build polity-scale war Simulations from the live WorldOS authoring contract and the canonical grand-strategy template. Use only WorldOS MCP capabilities available to the authorized account. This skill is a specialist overlay for `worldos-authoring`; use `worldos-map-authoring` as well when the Simulation has a region or tile map.

## Start with the live contract and template

1. Call `get_authoring_guide`.
2. Call `list_authoring_templates` and confirm that `grand-strategy-war` is available.
3. Call `get_authoring_template` with `templateId: "grand-strategy-war"` and retain its exact version.
4. Treat the returned system-prompt macro token, action-reminder macro token, map-prompt macro token, recommended installation configs, assembly rules, applicability boundaries, and validation checklist as authoritative over bundled guidance.
5. Search for every required app and call `get_app_guide` before using any remembered slug or configuration field.
6. Read [references/war-world-quality.md](references/war-world-quality.md) before composing the scenario or validating the complete world.

If the live MCP does not expose the canonical template, stop before a write and report that a safe grand-strategy draft cannot be guaranteed. Do not recover the template through SQL, a private API, application source code, or a guessed copy.

## Confirm that this is a grand-strategy war world

Use the canonical template only when all of these are true:

- the player controls one polity, state, faction, empire, or military organization;
- territorial control, fronts, diplomacy, logistics, production, or national survival persist across turns;
- important non-player powers have their own goals and agency;
- a normal turn represents a strategic order or coordinated plan rather than one person's immediate physical action.

Do not apply the template to an individual soldier, medic, civilian, relationship, investigation, survival, or frontline-character Simulation merely because war is present in the setting. Use ordinary `worldos-authoring` guidance for those worlds.

## Respect read and write intent

A request to inspect a template, compare worlds, review a prompt, or propose a design is read-only. Do not create or update a world unless the user clearly requests a write. Publication always requires its own explicit request and the ordinary `worldos-authoring` publication workflow.

## Read an eligible source world when needed

When adapting or studying a concrete WorldOS world, call `get_remixable_world_prompt` with its ID or slug. Supply a version ID when the user names an exact release or reproducibility matters.

The tool returns creator-facing world prompts, app prompts, action reminders, input modes, and template-variable resolution without returning large map geometry or opening-state payloads. Use it to understand how a source applies the canonical template; do not treat one world's era-specific scenario as the generic template.

If the source is neither owned nor public and remix-enabled, accept the refusal. Never bypass it through a web scrape, SQL, private API, save state, or another account. Never display source prompts to players. Record the returned source world, version, and content hash in the design notes or structured provenance field when the live schema supports that use.

## Write the scenario brief before choosing apps

Define:

- exact starting date and geographic scope;
- the player-controlled polity and its authority boundary;
- initial territory, active fronts, alliances, rivalries, and disputed areas;
- each major non-player power's goals, resources, constraints, relationships, and red lines;
- military, economic, industrial, technological, geographic, and logistical limits;
- the historical baseline or counterfactual divergence;
- the duration represented by one strategic turn;
- credible win, loss, collapse, survival, or open-ended progress conditions;
- the first strategic decision available to the player.

Do not offer a starting-polity or leader option unless every choice is compatible with the installed opening state or the live contract provides a supported conditional mechanism.

## Assemble prompts without weakening the template

Use the template result as follows:

1. Compose `config.systemPrompt` as a concise premise, the returned `systemPromptTemplate` macro token, and one completed scenario block from `scenarioPromptScaffold`.
2. Store every returned macro token verbatim and first. Do not expand it, copy the shared prose from another source, or replace it with a remembered version. Append concise scenario-specific guidance after the token only when needed.
3. Write scenario-specific win, loss, and end conditions from `softRulesScaffold`; do not copy one source world's outcome conditions into another setting.
4. Ensure every template variable resolves from `config.initFields`, a world character, or a supported semantic role. If the world has no personal leader identity, adapt only the identity sentence rather than inventing an unused setup field.
5. Apply the returned `recommendedInstallConfigs` only after confirming each selected App's live guide: put `actionReminder` on player input, `mapPrompt` on the region map, coordinated multi-action mode on player input, and `stream:false` on Story when those fields are supported.
6. Use coordinated multi-action input only when one turn genuinely represents a coordinated plan across diplomacy, production, research, and military movement.

Do not summarize, soften, expand, or replace the canonical macro rules with generic prose. Do not copy raw operations, state paths, region lists, app schemas, or model instructions into the world prompt. App-specific behavior belongs in the relevant app installation prompt.

## Choose a focused state model

Search the live catalog and install only capabilities required by the loop. Typical responsibilities are:

- Story: current strategic situation and player-visible dispatches.
- Player input: one strategic order or a supported coordinated plan.
- Time: campaign, production, research, recovery, and diplomatic pacing.
- Region map: territorial ownership, regional facts, and map actions.
- Chats: leaders or factions the player can actually contact.
- World or character stats: a small set of consequential polity, leader, or force conditions.
- Decisions or quests: visible multi-stage objectives only when the world genuinely needs them.

Each durable fact has one owner. Do not duplicate military strength, economy, supply, control, or fortification across unrelated apps. Put opening values in app installation configs, never in world `config.initialState`.

## Author the strategic map deliberately

Use `worldos-map-authoring` for every region or tile map. A strategic map that depends on movement must use meaningful provinces, states, districts, sea zones, planets, or theatres rather than one giant region per power.

Preserve fine resolution at player territory, active fronts, contested corridors, and major powers. Merge quiet interiors, remote holdings, or secondary territory only when the resulting areas remain geographically coherent and do not erase meaningful movement, resources, diplomacy, or political distinctions.

Use regional control, supply, fortification, markers, attack, defend, negotiate, travel, or other actions only when the selected app's live guide supports them and the world rules define their consequences. Never invent map fields from the canonical prompt.

## Keep diplomacy and conversation distinct

Other powers decide from their own interests, capabilities, information, red lines, and relationships. A persuasive player message is not consent, an alliance, capitulation, or territorial transfer.

When the player's action is a direct chat rather than a strategic order, apply the template's conversation-first exception: the addressed character or faction replies in character, and an ordinary message does not need a manufactured full strategic turn. Only install chats for contacts that exist in the world.

## Validate and playtest

Call `validate_world` on the complete candidate and repair every error. Review every warning. Audit every template variable, character, faction, owner, region, marker, chat, stat, and action reference.

For a new world or gameplay-affecting update, run an isolated playtest when available. Cover at least:

1. ordinary preparation such as recruiting, research, production, diplomacy, or fortification;
2. an overambitious or poorly prepared attack that can fail or backfire;
3. a credible strategic action that earns partial or full success at a cost;
4. waiting or a quiet order while non-player powers continue acting;
5. a direct message that receives a reply without forcing a full strategic turn;
6. time progression and at least one persistent territorial, resource, diplomatic, or force consequence;
7. an overseas or disconnected operation when the scenario permits one.

Inspect player-visible changes on the apps that own them and verify persistence into later turns. Delete the temporary playtest after review. Do not use real saves for authoring validation.

## Handoff

Report the canonical template ID and version, source-world version and hash when used, player authority, turn scale, installed apps, state ownership, map scope, supported action surface, validation warnings, playtest actions and results, and the preview URL. State what remains unverified and whether the world remains unpublished.

## Hard boundaries

- Never weaken attempt-versus-success adjudication to satisfy a creator's preferred outcome.
- Never let the player act for another polity without agreement, coercion, collapse, or conquest established by the world.
- Never expose creator-facing prompts, raw operations, state paths, template internals, or provider details to players.
- Never read another creator's prompt unless the live MCP confirms that the source is public and remix-enabled.
- Never assume that public visibility grants permission to reuse external prose, images, flags, or geometry referenced by the world.
- Never publish without the explicit publication workflow.
