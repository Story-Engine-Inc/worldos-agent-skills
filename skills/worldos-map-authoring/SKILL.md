---
name: worldos-map-authoring
description: Author, inspect, validate, or update a WorldOS region map through the WorldOS MCP. Use when a Simulation needs geographic regions, factions, territorial ownership, country labels, markers, regional actions, or a historical or strategic map; also use when reviewing an existing owned draft map.
---

# WorldOS Map Authoring

Build a readable and internally consistent region map as part of an unpublished WorldOS world draft. Do not modify a platform map implementation, database row, or repository asset directly.

## Confirm the live map contract

1. Call `get_authoring_guide` and obey its current distinction between region maps and tile maps.
2. Call `search_apps` for the map capability and read `get_app_guide` for the selected map app.
3. For an existing owned draft, call `get_world_map` before editing and inspect its returned validation result.
4. Treat live schemas and validation paths as authoritative over this skill.

At the current contract, region maps may be authored from scratch with strict geometry and reference validation, while tile maps require remixing. If the live guide changes, follow it.

Read [references/map-quality.md](references/map-quality.md) before composing labels, markers, or a large set of regions.

## Choose a map branch

### No map needed

Do not add a map merely because the premise has locations. Use one only when geography, movement, ownership, or regional decisions materially affect play.

### New region map

Compose a `map` installation config with a coherent coordinate system and stable identifiers. At minimum, define the fields required by the live schema, including the view box, regions, factions, and ownership relationships.

### Existing owned region map

1. Fetch the complete map with `get_world_map`.
2. Fetch the complete world with `get_owned_world`.
3. Preserve every untouched map and world field.
4. Replace the map installation config inside the complete candidate world draft.
5. Validate the entire world and update it with the exact world version.

There is no separate map write shortcut: map writes go through validated world creation or update.

### Remix

Preserve protected map config and linked characters exactly when remix validation requires it. Do not assume a base map can be recolored, relabeled, cropped, or given different owners until validation confirms those changes are allowed.

### Tile map

Follow the live remix restriction. Do not hand-author a new tile map merely because a runtime app guide describes its configuration.

## Establish one coordinate system

- Define a `viewBox` that contains every region path, label, and coordinate marker.
- Keep region paths and all explicit `x`/`y` coordinates in the same coordinate space.
- Use `wrap` only for a genuinely global east-west map.
- Leave enough empty visual space for the Simulation’s floating panels when the map is used as a background.
- Prefer a smaller accurate map to a huge map with broken geometry or unreadable labels.

## Define regions

Each region needs:

- a stable unique ID;
- a concise player-facing label;
- valid SVG path geometry in `d` when required by the live schema;
- an initial owner that resolves to a faction when the region is owned;
- useful anchors or bounds when the schema supports them;
- optional country or source identifiers only when they serve a clear runtime purpose.

Avoid self-intersecting, empty, microscopic, or wildly out-of-bounds paths. Do not create a country as one giant region for a strategic map that depends on territorial movement; use meaningful provinces, states, districts, or zones.

For a large strategic map, set a region and geometry budget before drafting the final payload. Preserve fine regions where the player's decisions and active fronts need them, and merge less important territory into larger coherent areas. Follow the large-map workflow in [references/map-quality.md](references/map-quality.md); do not send thousands of decorative micro-regions merely because the source dataset contains them.

## Define factions and characters

- Give every faction a stable unique ID, distinct label, readable color, and suitable avatar when available.
- Ensure every value in `initialOwners` resolves to a real faction.
- If a faction has `charId`, that ID must resolve to a real world character.
- Use `factionsAsCharacters` only when factions themselves should be available as conversational actors.
- Keep the player’s authority clear: the player controls their own polity or character, not every faction.
- Give non-player factions goals and the ability to react independently in the world rules.

## Labels and markers

- Place labels on the land or region they describe, not over unrelated territory or empty water.
- Give each disconnected major land cluster its own label when one label would be misleading.
- Use font size and label density proportional to geographic importance.
- Skip tiny labels that cannot be read, but retain at least one useful label for each major faction.
- Give every marker a stable ID and valid faction, character, or region references.
- Use markers only for pieces that can move or convey strategic information; do not duplicate static region labels as markers.

## Ownership, regional state, and actions

Ownership belongs to factions. Per-region facts belong in the map installation’s regional state rather than a duplicate world-stat list.

Keep region attributes few and actionable. Examples include control, unrest, supply, fortification, influence, or population when those values affect decisions. Define regional actions such as attack, defend, negotiate, inspect, or travel only when the world rules explain their consequences.

## Assets and attribution

The WorldOS MCP does not upload assets. External backgrounds and faction images must be legally reusable, stable, publicly reachable, and attributed when required. Do not scrape protected maps, use session-bound URLs, or download promotional art to imitate an existing product.

Region geometry may be derived from lawful public-domain or appropriately licensed geographic sources. Record relevant attribution in `backgroundAttribution` or the closest current contract field.

## Validate in layers

Before the full draft write:

1. Check IDs for uniqueness.
2. Check every owner, faction, character, region, label, and marker reference.
3. Check every path against the view box.
4. Check that region count and path detail are proportionate to actual decisions.
5. Check label density and positions.
6. Check map-specific validation from `get_world_map` when available.
7. Call `validate_world_draft` on the complete world.
8. Repair every map error and reassess each warning.

After a write, fetch the world and map again. Verify region, faction, action, and marker counts as well as the new world version and preview URL.

## Handoff

Report the geographic scope, region and faction counts, source/attribution, player-controlled faction when relevant, supported regional actions, remaining warnings, and the WorldOS preview URL. Say explicitly when a human should inspect label placement or dense geometry in the editor.
