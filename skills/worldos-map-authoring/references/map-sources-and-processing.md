# Map sources and processing

Use this workflow when a region map needs external geometry. Treat downloaded data as source material, not as a ready WorldOS map.

## Find a lawful source

1. Search the web for the official project, government open-data portal, or maintainer-owned repository. Prefer the primary source over mirrors and repackaged datasets.
2. Open the dataset page and its license or terms before downloading. Confirm that modification, redistribution, and the intended commercial or public use are allowed.
3. Record the source page, exact file URL, dataset version or commit, retrieval date, license identifier, required attribution, and any disputed-boundary or accuracy warning.
4. Reject a source when the license is missing, contradictory, incompatible with the intended use, or limited to viewing. “Free,” “open,” and “available on GitHub” are not licenses.
5. Preserve required notices and share-alike obligations in the project handoff. Ask for human review when compatibility is uncertain.

Useful primary sources include:

- [Natural Earth 1:10m Cultural Vectors](https://www.naturalearthdata.com/downloads/10m-cultural-vectors/): use Admin 1 States and Provinces for modern province/state geometry. Natural Earth currently describes data on its site as public domain, but verify the current terms and dataset version at download time. Its default boundaries follow a stated de facto viewpoint; review disputed areas and available point-of-view variants for the Simulation.
- [aourednik/historical-basemaps](https://github.com/aourednik/historical-basemaps): use its `index.json` to discover available years and `geojson/world_<year>.geojson` for historical country or cultural-region boundaries. The repository currently declares GPL-3.0 and describes the data as work in progress. Verify the current `LICENSE`, commit, historical claims, and source limitations before reuse.

These are starting points, not mandatory dependencies. Use another authoritative source when it better fits the place, period, resolution, or licensing needs.

## Download and inspect

Use the agent's available browser or HTTP client to download from the exact official file URL. Follow redirects, fail on HTTP errors, and save into a temporary working location. If a shell is available, an equivalent safe pattern is `curl --fail --location --output <file> <official-url>`; do not embed credentials or session-bound URLs.

After download:

1. Keep the original archive or file unchanged beside a provenance note, cryptographic checksum, and license copy or link.
2. Check the HTTP content type, file extension, non-zero size, and archive member list before extraction. Reject HTML error pages masquerading as ZIP, JSON, or GeoJSON.
3. Parse the dataset and report feature count, geometry types, property names, bounds, invalid or empty geometries, and duplicate identifiers.
4. Confirm the coordinate reference system. Normalize to WGS 84 longitude/latitude when combining web geographic datasets, then project every layer into one WorldOS coordinate system before emitting SVG paths.
5. Keep source, normalized, and final simplified data separate so provenance and transformations remain reviewable.

Prefer GeoJSON or GeoPackage when available. Shapefiles are acceptable, but retain all sidecar files and inspect their declared encoding and projection. Do not assume coordinates are longitude/latitude merely because their numeric range looks plausible.

## Combine modern provinces with historical ownership

Historical country datasets are usually too coarse to serve directly as strategic regions. Use province/state geometry for playable shapes and historical polygons as an ownership layer:

1. Freeze the intended historical snapshot as an exact date and document how the map treats colonies, protectorates, occupations, and disputed territory. Then load a province-level geometry source and the matching historical boundary file.
2. Normalize both layers to the same WGS 84 coordinate reference system.
3. For each province, calculate a representative interior point or centroid and test which historical polygon contains it.
4. When a point falls in no polygon or several overlapping polygons, compare polygon intersection area and flag ambiguous or disputed cases for review rather than guessing silently. If a historical boundary materially divides a province between owners, split the province along that boundary instead of assigning the whole shape by centroid.
5. Derive the historical owner from the source's documented fields. In `historical-basemaps`, `NAME` is the polity/region label and `SUBJECTO` identifies the exercising colonial power or otherwise repeats the region; also inspect `PARTOF` and `BORDERPRECISION` when relevant.
6. Maintain an explicit override register with a source and rationale for annexations, dependencies, split control, enclaves, concessions, occupations, and disputed territory. Never infer ownership from modern country codes alone.
7. Keep the resulting provinces fine where gameplay needs them, then apply the importance-tiered merge workflow in [map-quality.md](map-quality.md) to quieter territory.

## Convert to WorldOS geometry

Project the normalized polygons into the map's declared `viewBox`, convert them to valid SVG paths, and preserve stable source identifiers separately from player-facing IDs. After merging or simplification, regenerate bounds, anchors, labels, and ownership references.

Before writing the world draft, verify that every path parses, fits the view box, and resolves to one intended region and owner. Record the transformation summary and attribution in the handoff, and put attribution in `backgroundAttribution` or the closest field supported by the live app guide.
