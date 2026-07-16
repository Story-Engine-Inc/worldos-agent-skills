---
name: worldos-pax-adaptation
description: Adapt a versioned Pax Historia preset, world link, export, prompt, map, timeline, or character set into an unpublished WorldOS Simulation draft through the WorldOS MCP. Use when a user asks to import, port, recreate, or convert a Pax world while preserving its premise and Advisor intent and rebuilding prompt-only mechanics as app-owned persistent state.
---

# WorldOS Pax Adaptation

Turn a Pax Historia source into a playable WorldOS Simulation rather than a textual copy. Preserve the player fantasy and distinctive conflicts, then rebuild mechanics around WorldOS apps, explicit state ownership, active pacing, and reviewable unpublished drafts.

Use only public WorldOS MCP capabilities for WorldOS reads and writes. Do not fall back to Supabase, SQL, private APIs, platform source code, or repository-specific scripts.

## Start with the live contract

1. Call `get_authoring_guide` before designing or editing a draft.
2. Treat the live guide, current tool schemas, and validation results as authoritative.
3. Stop and request client reauthorization if the MCP is unavailable or unauthorized. Never request an access token in chat.
4. Read [references/pax-adaptation.md](references/pax-adaptation.md) before composing the state model or opening.

Read-only requests such as “review,” “audit,” “explain,” or “show me a proposal” do not authorize a write. Create or update a draft only when the user clearly asks to import, adapt, create, or modify it. Publishing always remains a human step in WorldOS.

## Freeze and audit the source

Record the exact Pax URL, preset identifier, version identifier, title, and source language. Treat an unversioned latest page as unstable. If the source cannot be read through the agent's available read-only browsing, ask the user for an export or pasted content instead of guessing.

Classify source material before choosing apps:

- **Preserve:** premise, player role, time and place, distinctive conflicts, useful characters, and meaningful choices.
- **Rebuild:** prompt-only mechanics, long openings, objectives, Advisor behavior, timeline events, player setup, and maps.
- **Omit:** Pax branding, provider instructions, tool syntax, duplicated lore, hidden spoilers, and unsupported assets.
- **Verify:** factual claims, chronology, geography, rights, provenance, and contradictory additions.

Give the user a concise preflight summary of what will be preserved, rebuilt, omitted, and left for manual review.
Summarize and transform source prose; do not reproduce long Pax prompts or other source text verbatim.

## Define the adaptation brief

Before assembling a draft, state:

- the player's identity and authority scale;
- the immediate opening pressure and first meaningful decision;
- the repeating two-to-three-turn core loop;
- the visible progress expected after about five turns;
- the characters or institutions that move the main arc when the player waits;
- the durable resources, relationships, objectives, risks, time facts, and geography.

Do not preserve a passive encyclopedia opening. Convert routine travel, preparation, eating, shopping, resting, and waiting into montage unless one of those activities contains a consequential choice.

## Assign one owner to every durable fact

Use `search_apps` for each required capability and call `get_app_guide` for every app under consideration. Search results and live guides, not remembered slugs or schemas, determine the installation plan.

Assign each persistent fact to exactly one authoritative app. Typical responsibilities include Story for the current situation, Quests for staged objectives, Stats for abilities and conditions, Inventory for possessions, Wallet for money, Chats for reachable contacts, Time for elapsed time, Calendar for known appointments, and Map for geography and territorial control. Treat these as responsibilities, not guaranteed app names.

Keep world-level causality, player authority, pacing, difficulty, autonomous actors, and win or loss logic in `config.systemPrompt`. Keep app-specific behavior in the relevant app installation prompt. Put all opening state in app installation configs, never in world `config.initialState`.

Preserve Pax `chatWithAdvisor` intent through WorldOS Advisor presets. Advisor explains the world and helps the player reason; it does not act for the player and does not require a parallel chat system.

Prefer the smallest coherent set of existing apps. Include at least one clear player-action surface. Consider a private reusable widget only after catalog search proves that no existing app can represent a required reusable interface.

## Rebuild the experience for play

Create an active opening with place, identity, pressure, stakes, and several distinct player-voiced actions. Give every required setup field a useful default and clickable options so the Simulation can start immediately. Use standard player and character template variables consistently in world copy and every app seed.

Maintain one active main arc tied to recent choices. After no more than two quiet turns, introduce a causally grounded message, visitor, summons, discovery, attack, deadline, or other external pressure. Escalate, transform, or resolve an ordinary opportunity within a few meaningful turns.

Treat extraordinary declarations as attempts, not facts. For difficult long-term goals, create staged prerequisites and visible partial progress. Failure may block final mastery, but it should change the situation, advance or clarify the objective, and give a concrete next route rather than demand the same action again.

## Choose the map branch deliberately

- Use no map when geography does not materially affect decisions.
- Use a new region map only when lawful geometry, coherent ownership, and stable references can pass validation.
- Use remix when the live contract protects a source map or requires remixing, including current tile-map restrictions.
- Treat Pax geometry and imagery as reference material unless reuse is lawful and technically stable.
- Use east-west wrapping only for a genuinely global map; disable it for bounded regional maps to avoid repeated horizontal worlds.

For any region map, use the `worldos-map-authoring` workflow when available. Keep territorial owners as factions; represent villages, clans, organizations, and points of interest as characters or markers when they are not sovereign territory. The WorldOS MCP cannot upload assets, so report any cover, avatar, or background that still needs a stable lawful replacement.

## Localize without changing identity

Use generic `i18n[locale]` overlays and stable IDs. Never create language-suffixed fields. The canonical language may be any language, and English is not a privileged read path. Keep template variables, IDs, enum values, URLs, and numeric data unchanged across locales. Write native product copy rather than literal translations.

## Validate and write safely

Call `validate_world_draft` on the complete candidate draft. Repair every error and assess every warning. Confirm app availability, action surfaces, exclusive-surface compatibility, runtime derivation, reference integrity, locale structure, map safety, and one authoritative owner for every durable fact.

For a new draft, use a stable idempotency key tied to the Pax source version and adaptation revision. Reuse it only for an identical retry. After creation, call `get_world_summary` and verify the unpublished result.

For an update, call `get_owned_world`, preserve the complete latest draft, change only intended fields, validate the full candidate, and call `update_world_draft` with the exact current `updatedAt`. Re-fetch after success. On a version conflict, fetch, reapply, and revalidate instead of overwriting concurrent work.

Do not edit a published resource or one owned by another account. Do not delete, transfer, or publish resources. Do not mutate, repair, rewind, rename, or delete saves.

## Review the adaptation

After creation or update, ask the user to start a fresh Simulation when a playtest is needed; the MCP does not create or mutate saves. Once an owned save exists, review it only through read-only save and turn tools, preferably with the `worldos-simulation-review` workflow when available.

Test the opening, an ordinary arc, a failed ambitious attempt, time progression, one resource change, one relationship interaction, and one map move when applicable. Verify that five turns create visible progress and that the world introduces credible pressure after quiet play.

Report the exact Pax source version, preserve/rebuild/omit decisions, installed apps and state ownership, map and asset choices, validation results, editor and preview URLs, playtest scope, and remaining human review. Never claim the Simulation is published.
