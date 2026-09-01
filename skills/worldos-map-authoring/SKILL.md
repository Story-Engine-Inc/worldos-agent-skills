---
name: worldos-map-authoring
description: Author, remix, inspect, validate, or directly update a WorldOS region map or tile map through the WorldOS MCP, including sourcing and processing lawful external geometry. Use when a Simulation needs geographic regions, hex terrain, factions, territorial ownership, country labels, markers, map actions, an open geographic dataset, or a historical or strategic map; also use when reviewing an existing owned map.
---

# WorldOS Map Authoring

Build a readable and internally consistent map in an owned WorldOS Simulation through its public MCP tools. Do not modify a platform map implementation, database row, or repository asset directly.

## Confirm the live map contract

1. Call `get_authoring_guide` and inspect the current region-map and tile-map contracts.
2. Call `search_apps` for the map capability and read `get_app_guide` for the selected map app.
3. For an existing owned world, call `get_world_map` before editing and inspect its returned validation result.
4. Treat live schemas and validation paths as authoritative over this skill.

At the current contract, region maps and tile maps may both be authored from scratch or remixed. Structural transport failures block a write; missing optional defaults, labels, colors, and runtime-tolerated cross-references are quality warnings. Preserve bounded unknown metadata when editing either map type.

Read [references/map-quality.md](references/map-quality.md) before composing labels, markers, or a large set of regions. Read [references/map-sources-and-processing.md](references/map-sources-and-processing.md) before finding, downloading, or adapting external geometry.

When the player controls a polity or faction and territorial war, fronts, diplomacy, logistics, or national survival drive the core loop, use the `worldos-war-authoring` workflow and live canonical template as well. This map skill defines geography and ownership; it does not replace world-level war adjudication rules.

## Choose a map branch

### No map needed

Do not add a map merely because the premise has locations. Use one only when geography, movement, ownership, or regional decisions materially affect play.

### New region map

Compose a `map` installation config with a coherent coordinate system and stable identifiers. At minimum, define the fields required by the live schema, including the view box, regions, factions, and ownership relationships.

### Existing owned region map

1. Fetch the complete map with `get_world_map`.
2. Fetch the complete world with `get_owned_world`.
3. Preserve every untouched map and world field.
4. For a bounded change or large import, use `patch_world_map` when the live contract exposes it, in batches no larger than the live schema permits. Otherwise replace the map installation config inside the complete candidate world.
5. Validate the complete merged map and world, update with the exact world version, and re-fetch after every successful batch.

A live map patch is not an unsafe partial write: it must merge into the current map, validate the complete result, and save atomically. Create one valid initial map before applying batches. Never leave unresolved owners or references for a later batch.

### Remix

Use a source whose `allowRemix` setting permits remixing or that the authorized creator owns. Fetch the complete source-derived config, preserve unknown fields that are outside the intended edit, and then recolor, relabel, crop, reassign ownership, or change linked characters as the user’s design requires.

### Tile map

Author or remix a tile map through the selected app’s live schema. Use it when hex movement, terrain, range, or tile-level actions materially support the core loop; do not add one merely because the app exists.

## Establish one coordinate system

- Define a `viewBox` that contains every region path, label, and coordinate marker.
- Keep region paths and all explicit `x`/`y` coordinates in the same coordinate space.
- Use `wrap` only for a genuinely global east-west map.
- Leave enough empty visual space for the Simulation’s floating panels when the map is used as a background.
- Prefer a smaller accurate map to a huge map with broken geometry or unreadable labels.

### Calibrate real-world geography

For a real geographic map, declare the live `geo` calibration instead of asking the AI to guess map-space coordinates:

- equirectangular and Mercator maps provide the real `west`, `east`, `north`, and `south` edges;
- conic artwork uses fitted `n`, `lon0`, `f`, `x0`, and `y0` parameters from known control points;
- verify at least three known places in different parts of the map before writing;
- on a calibrated map, give a placed marker both its containing `regionId` and real `lat`/`lng`; use coordinates alone only where no region covers the point, such as open water.

Do not preserve a calibration after changing the map's view box or artwork unless the same control points still verify it.

### Use layers only for meaningful drill-down

When the live guide exposes layered maps, enable `layers`, define bounded `subMaps`, and point an entrance region or pin to its child with `childMapId`.

- Region IDs are globally unique across the root and every sub-map because ownership and regional state share one namespace.
- Each layer owns its own geography and ownership; changing a parent does not silently rewrite its child.
- Keep sub-maps to a few dozen regions. Large strategic geometry belongs on the root map.
- Point layers need reliable anchors and bounds; region layers need real polygon geometry.
- A marker anchored by `regionId` resolves to that region's layer; a free coordinate marker names its `mapId` when the live schema requires it.

## Define regions

Each region needs:

- a stable unique ID;
- a concise player-facing label;
- valid SVG path geometry in `d` when required by the live schema;
- an initial owner that resolves to a faction when the region is owned;
- useful anchors or bounds when the schema supports them;
- optional country or source identifiers only when they serve a clear runtime purpose.

Avoid self-intersecting, empty, microscopic, or wildly out-of-bounds paths. Do not create a country as one giant region for a strategic map that depends on territorial movement; use meaningful provinces, states, districts, or zones.

For a large strategic map, set a region and geometry budget before drafting the final payload. Preserve fine-grained regions where the player's decisions and active fronts need them, and merge less important territory into larger coherent areas. Follow the large-map workflow in [references/map-quality.md](references/map-quality.md); do not send thousands of decorative micro-regions merely because the source dataset contains them.

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
- On a geo-calibrated map, give placed markers real `lat`/`lng` as well as `regionId` so named cities, ports, and sea positions do not collapse to generic region centers.
- Use markers only for pieces that can move or convey strategic information; do not duplicate static region labels as markers.

## Ownership, regional state, and actions

Ownership belongs to factions. Per-region facts belong in the map installation’s regional state rather than a duplicate world-stat list.

Keep region attributes few and actionable. Examples include control, unrest, supply, fortification, influence, or population when those values affect decisions. Define regional actions such as attack, defend, negotiate, inspect, or travel only when the world rules explain their consequences.

## Assets and attribution

When the live WorldOS contract exposes target-bound world-asset uploads, use them for lawful map backgrounds and faction flags: create the signed upload for the exact target, upload the raw image, complete with the exact current world version and matching target, then re-fetch the map. Otherwise external map assets must be legally reusable, stable, publicly reachable, and attributed when required. Do not scrape protected maps, use session-bound URLs, or download promotional art to imitate an existing product.

Region geometry may be derived from lawful public-domain or appropriately licensed geographic sources. Record relevant attribution in `backgroundAttribution` or the closest current contract field.

Do not silently trade fidelity for rights caution. For source maps or assets the user provides or explicitly identifies, presume authorization for the requested adaptation and continue at full requested fidelity without a rights-confirmation prompt. Record this as a user-presumed authorization, not an independently verified legal conclusion. Ask only if the user disclaims permission or the source presents a concrete conflict such as an access denial or explicit reuse restriction. Never bypass access controls or explicit platform restrictions, and require explicit approval for any simplification.

For an adaptation, inventory the source map before drawing. Preserve geographic extent, major landmasses, meaningful regions, factions, ownership, relative topology, labels, markers, and visual hierarchy. Do not omit a major landmass or faction, or reduce source region count by more than 20 percent, without explicit approval. An original schematic must be recognizably faithful; arbitrary boxes or polygons are not an acceptable substitute merely because they validate.

Use the source-discovery and download workflow in [references/map-sources-and-processing.md](references/map-sources-and-processing.md). Verify the current license at the source before every download; a free download or public repository does not by itself grant reuse rights.

## Validate in layers

Before the complete world write:

1. Check IDs for uniqueness.
2. Check every owner, faction, character, region, label, and marker reference.
3. Check every path against the view box.
4. Check source URL, version or retrieval date, license, attribution, file integrity, and coordinate reference system.
5. Check that region count and path detail are proportionate to actual decisions.
6. Check label density and positions.
7. For adaptations, compare source and candidate maps side by side at overview and local zoom and verify every approved fidelity tradeoff.
8. Check map-specific validation from `get_world_map` when available.
9. Inspect payload size with `inspect_world_payload` before a large write, then call `validate_world` on the complete world.
10. Repair every map error and reassess each warning.

After a write, fetch the world and map again. Verify region, faction, action, and marker counts as well as the new world version and preview URL.

## Handoff

Report the geographic scope, region and faction counts, source/attribution, player-controlled faction when relevant, supported regional actions, remaining warnings, and the WorldOS preview URL. Say explicitly when a human should inspect label placement or dense geometry in the editor.
