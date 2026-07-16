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

## Large strategic map budget

Do not carry every source province into a global or continent-scale Simulation. Thousands of regions and highly detailed paths make the draft harder to inspect and can consume runtime context without adding meaningful choices. Aim for the smallest map that preserves the player's actual fronts, routes, supply decisions, and political distinctions.

Vary resolution by strategic importance:

- keep player territory, active fronts, contested corridors, and major powers relatively fine;
- merge secondary powers, quiet interiors, remote territory, and large colonial holdings more aggressively;
- keep an original region only when its separate identity changes movement, ownership, resources, diplomacy, or another player decision.

When lawful source geometry is available, merge adjacent regions that share an initial owner and strategic role. Prefer real administrative groupings first. Split an oversized grouping into geographically coherent pieces, for example along its long axis, instead of creating arbitrary scattered clusters. For historical empires, a coherent territorial area may cross modern country boundaries when the historical owner and gameplay role are the same.

Use a topology-aware dissolve so shared interior borders disappear while the exterior boundary remains recognizable. Apply only light simplification after merging. Simplifying each polygon independently can create cracks, overlaps, and visibly mismatched borders.

Name merged areas with a stable cascade:

1. retain the source name for a single region;
2. use a real shared administrative or geographic name for an intact group;
3. add a geographic qualifier or anchor region when a known group is split;
4. fall back to a directional label plus the polity or territory name;
5. make every resulting label and ID unique.

After merging, regenerate anchors and bounds, then recheck owners, labels, markers, regional state, actions, and every cross-reference. Compare region count and path detail before and after the merge, and inspect the preview at both overview and local-front zoom levels. A lower count is useful only if the map still supports the intended decisions.

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
