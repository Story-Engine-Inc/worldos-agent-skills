---
name: worldos-pax-adaptation
description: Adapt a versioned Pax Historia preset, world link, export, prompt, map, timeline, or character set into an unpublished WorldOS Simulation draft through the WorldOS MCP. Use when a user asks to import, port, recreate, or convert a Pax world while preserving its premise and Advisor intent and rebuilding prompt-only mechanics as app-owned persistent state.
---

# WorldOS Pax Adaptation

Turn a Pax Historia source into a playable WorldOS Simulation rather than a textual copy. Preserve the player fantasy and distinctive conflicts, then rebuild mechanics around WorldOS apps, explicit state ownership, active pacing, and reviewable unpublished drafts.

Use only public WorldOS MCP capabilities for WorldOS reads and writes. Do not fall back to Supabase, SQL, private APIs, platform source code, or WorldOS application-repository scripts. Ordinary read-only source access and the bundled Pax snapshot helper are allowed only for source acquisition.

## Start with the live contract

1. Call `get_authoring_guide` before designing or editing a draft.
2. Treat the live guide, current tool schemas, and validation results as authoritative.
3. Stop and request client reauthorization if the MCP is unavailable or unauthorized. Never request an access token in chat.
4. Read [references/pax-adaptation.md](references/pax-adaptation.md) before composing the state model or opening.

Read-only requests such as “review,” “audit,” “explain,” or “show me a proposal” do not authorize a write. Create or update a draft only when the user clearly asks to import, adapt, create, or modify it. Publishing always remains a human step in WorldOS.

## Freeze and audit the source

Record the exact Pax URL, preset identifier, version identifier, title, and source language. Treat an unversioned latest page as unstable. Follow the version-specific public snapshot workflow in [references/pax-adaptation.md](references/pax-adaptation.md) when the preset is publicly readable: prefer the exact Firestore document used by the Pax frontend over browser DOM extraction, pin the raw response, and record both raw and canonical JSON hashes. Run the bundled decoder to produce ordinary JSON plus a source-coverage worksheet before designing the WorldOS draft. Use Pax search only for discovery or summary cross-checks, not as the complete source.

Treat these public web endpoints as an undocumented frontend data layer, not a supported Pax developer API. Never add credentials, enumerate unrelated documents, or bypass an access denial. Public readability does not grant permission to republish protected prose, images, flags, or geometry. If the exact version cannot be read through ordinary read-only access, ask the user for an export or pasted content instead of guessing.

When the live WorldOS contract exposes structured source provenance, store the Pax source type, exact URL, preset and version identifiers, retrieval time, hashes, license status, and concise notes in that field. Do not hide provenance only in the handoff message.

Classify source material before choosing apps:

- **Preserve:** premise, player role, time and place, distinctive conflicts, useful characters, and meaningful choices.
- **Rebuild:** prompt-only mechanics, long openings, objectives, Advisor behavior, timeline events, player setup, and maps.
- **Omit:** Pax branding, provider instructions, tool syntax, duplicated lore, hidden spoilers, and unsupported assets.
- **Verify:** factual claims, chronology, geography, rights, provenance, and contradictory additions.

Give the user a concise preflight summary of what will be preserved, rebuilt, omitted, and left for manual review.
Summarize and transform source prose; do not reproduce long Pax prompts or other source text verbatim.
Complete every generated coverage row and run the bundled adaptation checker against the candidate draft. Treat missing source decisions, missing state owners, and exceeded prompt budgets as blockers rather than silently dropping source material or moving all prose into `systemPrompt`.

## Define the adaptation brief

First choose the adaptation form from the source instead of assuming a customizable individual RPG. Pax presets may become a fixed-protagonist narrative, relationship ensemble, investigation, household or dynasty, organization or business simulation, faction or state strategy, management world, or open counterfactual sandbox. Preserve what the player controls and repeatedly decides. Do not add a background picker, inventory, quests, character chats, stats, or a map merely because another adaptation used them.

Before assembling a draft, state:

- the player-controlled person, group, institution, territory, or viewpoint and its authority scale;
- the immediate opening pressure and first meaningful decision;
- the repeating two-to-three-turn core loop;
- the visible progress expected after about five turns;
- the characters or institutions that move the main arc when the player waits;
- the durable resources, relationships, objectives, risks, time facts, and geography.

Do not preserve a passive encyclopedia opening. Convert routine travel, preparation, eating, shopping, resting, and waiting into montage unless one of those activities contains a consequential choice.

## Assign one owner to every durable fact

Use `search_apps` for each required capability and call `get_app_guide` for every app under consideration. Search results and live guides, not remembered slugs or schemas, determine the installation plan.

Assign each persistent fact that matters to the chosen loop to exactly one authoritative app. Typical responsibilities include Story for the current situation, Quests for staged objectives, Stats for abilities and conditions, Inventory for possessions, Wallet for money, Chats for reachable contacts, Time for elapsed time, Calendar for known appointments, and Map for geography and territorial control. Treat these as optional responsibilities, not a required bundle or guaranteed app names.

Keep world-level causality, player authority, pacing, difficulty, autonomous actors, and win or loss logic in `config.systemPrompt`. Keep app-specific behavior in the relevant app installation prompt. Put all opening state in app installation configs, never in world `config.initialState`.

Preserve Pax `chatWithAdvisor` intent through `config.advisorPresets`. Advisor explains the world and helps the player reason; it does not act for the player and does not require a parallel chat system.

Prefer the smallest coherent set of existing apps. Include at least one clear player-action surface. Consider a private reusable widget only after catalog search proves that no existing app can represent a required reusable interface.

## Rebuild the experience for play

Create an active opening that establishes the controlled viewpoint, current situation, pressure, stakes, and several distinct actions appropriate to the chosen interaction model. Player setup is optional. When it is needed, put fields in `config.initFields`, give every required field a useful default and clickable options, and use standard player and character template variables consistently in world copy and every app seed. Never invent `setupFields`.

When setup options imply different affiliations, locations, eras, equipment, conditions, authority, or objectives, audit every option against the seeded Story, apps, and characters. If the live contract cannot express those different initial facts, narrow the options, choose one focused opening, or create separate drafts. Do not present a consequential choice that changes only prose while shared state contradicts it.

Maintain one active main arc tied to recent choices. After no more than two quiet turns, introduce a causally grounded message, visitor, summons, discovery, attack, deadline, or other external pressure. Escalate, transform, or resolve an ordinary opportunity within a few meaningful turns.

Treat extraordinary declarations as attempts, not facts. For difficult long-term goals, create staged prerequisites and visible partial progress. Failure may block final mastery, but it should change the situation, advance or clarify the objective, and give a concrete next route rather than demand the same action again.

## Choose the map branch deliberately

- Before choosing a branch, record whether the Pax source includes a map and whether location, travel, territorial ownership, regional state, or map actions affect the core loop.
- If the source includes a gameplay-relevant map or the adapted core loop depends on any of those geographic facts, use the `worldos-map-authoring` workflow and build or remix a validated map. This is a required adaptation branch, not optional polish.
- Use no map only when geography is genuinely decorative or interchangeable. State that conclusion explicitly in the preflight and handoff.
- Use a new region map only when lawful geometry, coherent ownership, and stable references can pass validation.
- Use remix when the live contract protects a source map or requires remixing, including current tile-map restrictions.
- Treat Pax geometry and imagery as reference material unless reuse is lawful and technically stable. Copyright or asset instability may block copying the source art, but does not by itself justify omitting a gameplay-required map: create an original schematic region map or use another lawful source when the live contract permits it.
- Use east-west wrapping only for a genuinely global map; disable it for bounded regional maps to avoid repeated horizontal worlds.

For any region map, use the `worldos-map-authoring` workflow when available. Keep territorial owners as factions; represent villages, clans, organizations, and points of interest as characters or markers when they are not sovereign territory.

When a lawful stable cover file is available and the live guide exposes cover upload, use `create_world_cover_upload`, upload the raw JPEG, PNG, or WebP to the signed URL, call `complete_world_cover_upload` with the exact current world version, and re-fetch the draft to verify `config.coverImage`. Do not claim an asset is attached before completion succeeds. Report avatars or backgrounds that still lack an equivalent supported upload path.

When the live guide exposes a target-bound world-asset upload, use it for lawful character avatars, faction flags, map backgrounds, and installed-app backgrounds. Match the same target during completion, pass the exact current world version, re-fetch after attachment, and record provenance or attribution where the destination schema supports it.

## Localize without changing identity

Use generic `i18n[locale]` overlays and stable IDs. Never create language-suffixed fields. The canonical language may be any language, and English is not a privileged read path. Keep template variables, IDs, enum values, URLs, and numeric data unchanged across locales. Write native product copy rather than literal translations.

## Validate and write safely

Call `validate_world_draft` on the complete candidate draft. Repair every error and assess every warning. Confirm app availability, action surfaces, exclusive-surface compatibility, runtime derivation, reference integrity, locale structure, map safety, and one authoritative owner for every durable fact. Independently audit every `{{...}}` token against `config.initFields` and the character roster; structural validation alone is not a rendered-preview test.

For a near-limit candidate, call the live payload-inspection tool before validation. When the live contract exposes bounded patch tools, use exact-version world patches for large app sections and validated map batches instead of repeatedly resending one multi-megabyte draft. Re-fetch after every batch; never leave an invalid partial map in the owned draft.

For a new draft, use a stable idempotency key tied to the Pax source version and adaptation revision. Reuse it only for an identical retry. After creation, call `get_world_summary` and verify the unpublished result.

For an update, call `get_owned_world`, preserve the complete latest draft, change only intended fields, validate the full candidate, and call `update_world_draft` with the exact current `updatedAt`. Re-fetch after success. On a version conflict, fetch, reapply, and revalidate instead of overwriting concurrent work.

Do not edit a published resource or one owned by another account. Do not delete, transfer, or publish resources. Do not mutate, repair, rewind, rename, or delete saves.

## Review the adaptation

After creation or update, use any available read-only browser or page-inspection capability to open the returned preview with default setup values. Check the opening, visible app names, cover, localization, and any raw `{{...}}`, `inv:`, or `app:` leakage. If preview inspection is unavailable, mark runtime rendering unverified.

When the live contract exposes isolated playtests, call `start_world_playtest` with default setup values and make at least five successful, versioned `playtest_world_turn` calls. The start call and any `get_world_playtest` call do not count as turns. Use this minimum sequence:

1. Take an ordinary core-loop action.
2. Take a quiet, preparatory, or waiting action.
3. Take a second quiet action and verify grounded external pressure arrives.
4. Attempt an ambitious action that should fail or succeed only with a cost.
5. Take a follow-up action that proves prior consequences persisted and changed available play.

Use additional turns, up to the live limit, for a real chat-surface relationship interaction and a real map-surface action when those systems apply; do not replace them with main-input narration. Across the run, verify time progression and at least one core resource or objective change. Verify that consequences appear on player-visible app surfaces and remain consistent in later turns. Use `get_world_playtest` only to recover the current session version or snapshot, not as a substitute for a turn or a history API. Delete the temporary session after review.

When assertions and temporary turn history are available, attach assertions to each turn for the expected player-visible surface or content, then inspect the complete history before deletion. A failed assertion is a repair signal, not permission to reinterpret an unchanged surface as success.

If the draft changes during repair, delete the version-bound session, fetch the new world version, and restart the playtest. If isolated playtest tools are unavailable, ask the user to start a fresh Simulation, then review it only through read-only save and turn tools. Never mutate a real save.

Report the exact Pax source version, chosen adaptation form, preserve/rebuild/omit decisions, installed apps and state ownership, map gate outcome and asset choices, validation results, editor and preview URLs, preview and playtest scope, player-visible surfaces changed, and remaining human review. Call the result a structurally validated draft and explicitly state that runtime preview or playtesting remains unverified until each relevant check has actually passed. Never claim the Simulation is published unless the explicit live publishing workflow succeeded.
