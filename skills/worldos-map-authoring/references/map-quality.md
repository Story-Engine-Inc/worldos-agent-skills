# Map quality guide

## Geographic resolution

Choose regions at the scale where player decisions happen:

- city story: neighborhoods or important sites;
- regional politics: districts or provinces;
- national strategy: provinces or states;
- global strategy: provinces, states, or meaningful theaters rather than one polygon per country.

Do not mix radically different resolutions without a gameplay reason.

## Geometry checks

For each region:

- parse the SVG path successfully;
- calculate or estimate its bounds;
- ensure the bounds intersect the declared view box;
- reject empty or near-zero-area geometry;
- ensure the intended anchor lies inside or very near the region;
- simplify excessive path detail only when borders remain recognizable and adjacent regions still align acceptably.

Large map payloads should prioritize playable geometry over coastline precision.

## Disconnected territory labels

A single faction can own disconnected land clusters. One label at the bounding-box center may fall in water or on another faction.

Use this approach when enough geometry information is available:

1. group owned regions into neighboring clusters using bounds or shared-border proximity;
2. calculate a size-weighted center for each important cluster;
3. snap that center to the nearest owned region anchor;
4. place one label per important cluster;
5. scale the font to the cluster’s visible width, height, and label length;
6. omit labels too small to read while retaining the largest cluster’s label.

This is a quality heuristic, not a schema requirement.

## Visual hierarchy

- Region labels: small and quiet.
- Faction/country labels: larger and fewer.
- Mobile pieces and hazards: markers with clear icons or badges.
- Player territory and current selection: visually distinguishable without making neutral regions illegible.
- Background imagery: subdued enough that borders and labels remain readable.

Use accessible contrast. Avoid relying on red/green differences alone.

## Map-world consistency

Cross-check that:

- a faction’s player-visible name matches its character identity;
- faction colors and avatars remain consistent in map, chat, and stats;
- story and opening messages refer to valid places;
- ownership in the opening narrative matches `initialOwners`;
- moving markers start in valid regions or coordinates;
- regional stats use the same region IDs as geometry;
- actions operate on the intended scope: own, enemy, neutral, vassal, or any.

## Manual preview review

Schema validation cannot establish visual quality. In the WorldOS preview, inspect:

- the whole map at initial zoom;
- labels on narrow, concave, and island regions;
- dense borders;
- map visibility behind default windows;
- marker overlap;
- mobile readability;
- background loading and attribution.
