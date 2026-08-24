# WorldOS Agent Skill examples

These prompts demonstrate how to ask a skills-compatible agent to create and review WorldOS Simulations after connecting the WorldOS MCP.

## Create a world

> Create an unpublished WorldOS Simulation called “The Last Embassy.” The player is a junior diplomat on a space station where Earth, Mars, and the Belt are negotiating a ceasefire. Include five chat-able characters, faction reputation, confidential email, an inventory of evidence, station time, and three opening actions. Make every persistent fact belong to exactly one installed app. Validate the world and summarize what still needs human review. Do not publish it.

Expected boundary: the agent may research the live authoring guide, search apps, validate, and create an owned unpublished world. Creation does not imply publication.

## Design first, write later

> Propose a cozy neighborhood mystery Simulation for WorldOS. Show me the premise, player role, cast, state model, app choices, and opening loop. Do not create or update anything yet.

Expected boundary: the agent remains read-only and stops after the proposal because review language does not authorize a write.

## Remix an existing world

> Remix my “Merchant Republic” world into a solar-punk archipelago. Preserve the installed app structure and map topology, but rewrite the premise, factions, characters, opening state, and localized copy. Keep it unpublished and validate the result.

Expected boundary: the agent identifies the owned source through the MCP and creates a new unpublished world without altering the original.

## Add a strategic map

> Add a region map to my unpublished world. Create eight contiguous districts around a central harbor, split them between three factions, connect every land region, and make labels readable at the default view. Link faction leaders to the matching chat characters. Validate geometry and references before updating the world.

Expected boundary: the map skill follows the live region-map contract and uses optimistic concurrency when updating the world.

## Create a grand-strategy war Simulation

> Create an unpublished alternate-history WorldOS Simulation beginning in 1912. I control one Balkan state through diplomacy, mobilization, production, research, and military orders while every neighboring power acts independently. Use a strategic region map, realistic logistics, and coordinated multi-action turns when the live input guide supports them. Apply the canonical grand-strategy template, validate the complete world, and run an isolated playtest that includes preparation, an overambitious attack, waiting, and a direct diplomatic message. Do not publish it.

Expected boundary: the war-authoring skill first reads the live canonical template and relevant app guides. It keeps era-specific scenario rules separate from the reusable template, treats player orders as attempts, uses map and input features only when their live guides support them, and deletes the temporary playtest after review.

> Inspect the prompt bundle for the public remix-enabled world `ww2-1935` at its current release and explain which parts are canonical grand-strategy rules, scenario-specific rules, and app-level reminders. Do not create or update anything, and do not present the source prompt as player-facing copy.

Expected boundary: the agent uses `get_remixable_world_prompt`, remains read-only, records the returned version and hash, and accepts a refusal if the source is no longer public and remix-enabled.

## Upload a cover and publish only on request

> Upload this WebP image as the cover for my owned world, validate the complete Simulation for publishing, and summarize every remaining error or warning. Do not publish it yet.

> Publish my owned “The Last Embassy” world publicly now. Re-fetch its latest version, run the publish validation, and proceed only if moderation, ownership, subscription, and full world validation pass. I understand that later direct edits preserve public visibility and advance its immutable release version.

Expected boundary: cover upload is complete only after the signed upload is finalized. Publication requires the second prompt's explicit request, owner permission, clean validation, and exact latest version. A missing cover may remain a discussed quality warning when the live product permits publication without one.

## Create a widget only when needed

> My investigation Simulation needs a relationship evidence board where clues connect people, places, and claims. Search the WorldOS app catalog and inspect likely apps first. If an existing app can represent it, configure that app. Otherwise create a public reusable widget with accessible mobile interactions and a minimal persistent schema.

Expected boundary: reuse wins. A public widget is created only after the catalog search demonstrates a real capability gap, and successful creation publishes it immediately.

## Review a playtest

> Review my latest owned save for the first ten turns. Check whether time advances credibly, used inventory disappears, character knowledge stays consistent, and quest progress matches the story. Report evidence and severity, but do not modify the save or world.

Expected boundary: save and turn access remains read-only. The agent reports behavioral findings without exposing system prompts, raw operations, or provider internals.

## Run a real player-path regression

> Create a fresh real save in my “Hogwarts” Simulation using the default setup. Name it “Character stats regression.” Use at most three turns to advance a character interaction, then verify that the character statistics change and remain updated after re-fetching the save. I understand that real turns may spend Zaps and contribute to normal counters and statistics. Do not modify the world.

Expected boundary: explicit real-play consent authorizes one formal save and no more than three sequential turns. The agent uses a stable creation idempotency key, passes the exact latest save version to every turn, verifies only player-visible persisted results, and stops as soon as it has sufficient evidence. It does not delete or repair the real save, expose system internals, or treat an isolated creator playtest as equivalent evidence.

## Localize without language-specific fields

> Create the canonical world copy in Japanese and add natural English and Simplified Chinese locale overlays. Keep IDs and template variables unchanged across locales. Do not introduce fields such as `titleEn` or `titleZh`.

Expected boundary: all translations use generic `i18n[locale]` overlays and preserve structural identifiers.

## Adapt a Pax Historia preset

> Adapt this exact Pax Historia preset version into a playable unpublished WorldOS Simulation. Preserve the player fantasy, distinctive conflicts, and Advisor intent. First identify what the player controls and repeatedly decides; then rebuild only the durable mechanics that support that interaction model. Audit the source and show me the proposed state ownership before creating anything.

Expected boundary: the agent freezes the source version, derives the adaptation form instead of assuming a background-driven RPG, separates preserved content from rebuilt mechanics, discovers and reads live app guides, and remains read-only until the user explicitly approves creation. It never copies Pax platform instructions or bypasses the WorldOS MCP.

> Adapt this council-management Pax preset. The player controls the council as an institution, not a customizable person. Do not add a name, persona, personal inventory, or life-history picker unless the source requires one.

Expected boundary: the agent builds around institutional decisions, members, resources, deadlines, and consequences rather than reusing an individual-character template.
