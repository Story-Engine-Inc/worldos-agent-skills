# Persistent state ownership

Use one authoritative app for each durable fact. Search the live app catalog and read each app guide before using any example slug below; examples describe responsibilities, not a guaranteed current schema.

| Durable concept | Typical responsibility | Rule |
| --- | --- | --- |
| Current narrative situation | Story | Record what has happened and the immediate scene, not every numeric fact. |
| Long-term objectives | Quests | Use staged prerequisites and visible progress rather than prompt-only promises. |
| Global pressure or resources | World stats | Keep the list small and consequential. |
| Per-character relationships or conditions | Character stats | Model facts about each character; avoid an all-pairs relationship matrix. |
| Objects, evidence, rosters, files | Inventory/list | Each list needs a clear purpose and stable item IDs. |
| Communication | Chats or one compatible chat surface | Seed only communication paths that truly exist in the world. |
| Public discourse | Social, forum, or a compatible feed | Posts and comments must reference real authors. |
| Time and pacing | Time | Advance travel, training, recovery, and deadlines credibly. |
| Known appointments and deadlines | Calendar | Do not reveal hidden future events as calendar entries. |
| Player objectives and consequences requiring decisions | Decisions or quests | Do not duplicate the same decision in multiple panels. |
| Geography and territorial control | Region map | Ownership belongs to factions; per-region facts belong with the map. |
| Hex movement and terrain | Tile map | Follow the live remix restriction and app guide. |
| Custom domain data | Existing reusable widget, otherwise a private UGC widget | Create a widget only when no existing app expresses the state. |

## Prompt ownership

- World `systemPrompt`: scenario-wide causality, player authority, pacing, difficulty, autonomous actors, and win/loss rules.
- App installation `prompt`: world-specific behavior limited to that app.
- App opening config: concrete initial data.
- App’s reusable prompt/guide: generic behavior shared across worlds; do not rewrite it for one Simulation.

Do not copy a data contract into the world prompt. Repetition consumes context and can conflict with the live app contract.

## Detect duplicate ownership

Before validation, list every durable noun in the design brief: money, health, trust, evidence, territory, time, objective, inventory, rank, and so on. Assign each noun to one app. If two apps own the same noun, choose one and make the other a read-only presentation only if the platform explicitly supports that relationship.

## Opening-state rule

All opening state belongs in app installation configs. Do not create a world-level `initialState`. Existing saves are snapshots of their own state and are not rewritten when a draft changes.
