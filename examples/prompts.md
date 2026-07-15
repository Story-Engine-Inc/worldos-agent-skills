# WorldOS Agent Skill examples

These prompts demonstrate how to ask a skills-compatible agent to create and review WorldOS Simulations after connecting the WorldOS MCP.

## Create a world

> Create an unpublished WorldOS Simulation called “The Last Embassy.” The player is a junior diplomat on a space station where Earth, Mars, and the Belt are negotiating a ceasefire. Include five chat-able characters, faction reputation, confidential email, an inventory of evidence, station time, and three opening actions. Make every persistent fact belong to exactly one installed app. Validate the draft and summarize what still needs human review. Do not publish it.

Expected boundary: the agent may research the live authoring guide, search apps, validate, and create an owned draft. Publication stays manual.

## Design first, write later

> Propose a cozy neighborhood mystery Simulation for WorldOS. Show me the premise, player role, cast, state model, app choices, and opening loop. Do not create or update anything yet.

Expected boundary: the agent remains read-only and stops after the proposal because review language does not authorize a write.

## Remix an existing draft

> Remix my “Merchant Republic” draft into a solar-punk archipelago. Preserve the installed app structure and map topology, but rewrite the premise, factions, characters, opening state, and localized copy. Keep it unpublished and validate the result.

Expected boundary: the agent identifies the owned source through the MCP and creates a new draft without altering the original.

## Add a strategic map

> Add a region map to my unpublished draft. Create eight contiguous districts around a central harbor, split them between three factions, connect every land region, and make labels readable at the default view. Link faction leaders to the matching chat characters. Validate geometry and references before updating the world.

Expected boundary: the map skill follows the live region-map contract and uses optimistic concurrency when updating the draft.

## Create a widget only when needed

> My investigation Simulation needs a relationship evidence board where clues connect people, places, and claims. Search the WorldOS app catalog and inspect likely apps first. If an existing app can represent it, configure that app. Otherwise create a private reusable widget with accessible mobile interactions and a minimal persistent schema.

Expected boundary: reuse wins. A private widget is created only after the catalog search demonstrates a real capability gap.

## Review a playtest

> Review my latest owned save for the first ten turns. Check whether time advances credibly, used inventory disappears, character knowledge stays consistent, and quest progress matches the story. Report evidence and severity, but do not modify the save or world.

Expected boundary: save and turn access remains read-only. The agent reports behavioral findings without exposing system prompts, raw operations, or provider internals.

## Localize without language-specific fields

> Create the canonical world copy in Japanese and add natural English and Simplified Chinese locale overlays. Keep IDs and template variables unchanged across locales. Do not introduce fields such as `titleEn` or `titleZh`.

Expected boundary: all translations use generic `i18n[locale]` overlays and preserve structural identifiers.
