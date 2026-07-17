# Pax Historia adaptation guide

Use this guide after reading the live WorldOS authoring contract. It provides adaptation heuristics, not fixed app schemas.

## Capture an exact public source snapshot

Do not treat rendered browser text as the authoritative source when an exact public version is available. Pax currently exposes the frontend's versioned Firestore document at:

```text
https://firestore.googleapis.com/v1/projects/pax-historia-dev/databases/(default)/documents/simplePresets/<preset-id>/versions/<version-id>
```

This is an undocumented public frontend data layer, not an officially supported Pax developer API. Its availability and schema may change. Fetch only a preset and version already supplied by the user or present in the public preset URL. Do not use credentials, enumerate unknown documents, or work around HTTP 401 or 403 responses.

Prefer the bundled standard-library helper because it verifies the returned document identity, preserves the raw response, computes reproducible hashes, and refuses to overwrite a different snapshot:

```bash
python3 scripts/fetch-pax-version.py <preset-id> <version-id> pax-version-<version-id>.json
```

Decode the Firestore typed values and create a coverage worksheet immediately after fetching:

```bash
python3 scripts/decode-pax-version.py pax-version-<version-id>.json \
  --normalized pax-version-<version-id>.decoded.json \
  --audit pax-version-<version-id>.coverage.json
```

The worksheet records paths, labels, sizes, counts, and hashes without embedding the source prose. Complete every row with one disposition. A preserved or rebuilt row needs one WorldOS state owner and a concrete implementation; an omitted row needs a rationale; a verification row needs a plan or result.

When the current working directory is not this skill directory, invoke the same script by its resolved installed-skill path. A direct one-off request is also possible:

```bash
curl --fail --location --compressed \
  'https://firestore.googleapis.com/v1/projects/pax-historia-dev/databases/(default)/documents/simplePresets/<preset-id>/versions/<version-id>' \
  -o pax-version-<version-id>.json
```

After retrieval:

1. Cross-check the preset and version from the user URL, the Firestore document `name`, and the document's internal version or preset metadata when present. Stop on any mismatch.
2. Preserve the raw response as the source snapshot. Record its byte count and SHA-256. Also record a canonical SHA-256 calculated after parsing JSON and sorting object keys, because equivalent Firestore responses may serialize map keys in a different order.
3. Decode Firestore's typed value wrappers instead of assuming `fields` contains ordinary JSON values.
4. Inventory `rulesText`, `startingTimelineText`, `prompts` including Advisor behavior, `regionData`, `baseMap`, recommended entities, decisions, and version or publication metadata when present. Do not assume every version has every field.
5. Use `https://www.paxhistoria.co/api/presets/search` only for discovery and summary cross-checks. It is not a replacement for the versioned document. Use the public preset page for identity, visible version history, and visual review rather than DOM-based full extraction.
6. If the document is unavailable, denied, malformed, or inconsistent, stop and request a user export or pasted source. Do not silently fall back to an unversioned page.

Before validation or writing, run the coverage and content-budget gate against the candidate draft:

```bash
python3 scripts/check-pax-adaptation.py pax-version-<version-id>.coverage.json \
  --draft worldos-draft.json
```

Repair every coverage error. Distill copy that exceeds the reported budgets instead of moving the same lore between prompts. Warnings about near-limit payloads or duplicated long prompt paragraphs require an explicit review.

A public response establishes technical readability, not reuse rights. Summarize and transform source prose. Check provenance and permission before copying images, flags, geometry, or other protected assets into WorldOS.

## Source audit worksheet

Record:

- exact preset URL, preset identifier, version identifier, title, and source language;
- source snapshot retrieval time, byte count, raw SHA-256, canonical SHA-256, and identity cross-check result;
- player scale: individual, household, organization, faction, or state;
- opening date, place, historical anchor, and known event chain;
- characters, factions, relationships, and Advisor guidance;
- objectives, skills, injuries, locations, items, money, pressure, and other durable facts;
- map geometry, territorial ownership, markers, cover art, flags, and external dependencies;
- contradictions, anachronisms, fan additions, future spoilers, and platform-specific instructions.

For each source element, record whether to preserve, rebuild, omit, or verify it. Do not begin WorldOS writes until this classification and the intended player fantasy are clear.

## Adaptation matrix

Use live app discovery before selecting an implementation. The responsibilities below are conceptual.

| Pax concept | WorldOS responsibility | Adaptation rule |
| --- | --- | --- |
| Scenario prompt | World scenario rules | Keep only setting-wide causality, authority, pacing, difficulty, and autonomous behavior. |
| Long opening lore | Intro and Story opening | Keep immediate context and a live hook; remove encyclopedia detail and future spoilers. |
| Player setup | Optional `config.initFields` | Add only inputs that change or personalize the chosen experience. A fixed protagonist, organization, state, or god-view world may need none. |
| `chatWithAdvisor` | Advisor presets | Preserve explanation and strategic guidance without creating another Advisor system. |
| Objectives and power goals | Quests | Create staged prerequisites and retain progress after failed attempts. |
| Skills, rank, wounds, and pressure | Appropriate Stats responsibility | Make consequential conditions visible and persistent. |
| Possessions and resources | Inventory or one appropriate resource owner | Update gains, use, loss, and damage with the narrative consequence. |
| Currency and transactions | One money owner | Record payments, rewards, debt, and losses without duplicating balances elsewhere. |
| Contacts and diplomacy | Reachable communication surface | Seed only relationships with a credible communication path. |
| Timeline | Time | Advance travel, training, recovery, and waiting credibly. |
| Known deadlines | Calendar | Include only appointments and deadlines the player actually knows. |
| Hidden future events | World pressure | Let them emerge through play; do not seed them as spoilers. |
| Countries and provinces | Region map | Use factions and ownership when territory materially affects play. |
| Villages, clans, and organizations | Characters, markers, or relationships | Do not turn non-sovereign organizations into territorial owners merely to color the map. |
| Difficulty | Rules plus staged state | Use preparation, resistance, uncertainty, cost, and consequences rather than repetitive refusal. |

Reject any adaptation where an important durable mechanic exists only as prose in a prompt.

## Choose the adaptation form

Do not treat every Pax source as a life-path RPG. Identify what the player controls and what kind of decision repeats:

- a fixed protagonist making embodied choices;
- a customizable individual whose identity materially changes play;
- an ensemble shaped by conversations and relationships;
- an investigator connecting people, places, claims, and evidence;
- a household or dynasty managing lineage, obligations, and succession;
- an organization or business allocating people, money, and projects;
- a faction or state directing diplomacy, territory, production, and war;
- a manager or builder optimizing a changing system;
- a god-view or counterfactual player applying interventions and observing consequences.

These are diagnostic examples, not templates. A source may combine forms or require another one. Select apps from the actual recurring decisions and durable consequences. Do not add personal inventory to a state strategy world, a map to a relationship chamber drama, or a background selector to a fixed-protagonist story unless the core loop requires it.

## Core-loop conversion

Replace descriptive world text with a causal loop:

```text
hook → decision → cost or test → persistent payoff → new pressure
```

Answer:

1. What meaningful decision appears on the first turn?
2. What repeats every two or three turns?
3. Which persistent facts prove progress after five turns?
4. Who acts when the player waits?
5. What can fail, and how does failure create a changed situation?

Create several setting-specific situations. For each, define the actor creating pressure, what they want, what the player knows, two or three plausible responses, the cost of each, the durable facts that may change, and the later reaction. Avoid one free reward beside two obviously bad options.

## Active-story pacing

- Keep one active main arc connected to recent player choices.
- After at most two turns of preparation, travel, recovery, shopping, observation, or other quiet activity, bring a credible external hook to the player.
- Resolve an ordinary opportunity in roughly two or three meaningful turns: contact or choice, complication, then payoff or next hook.
- Escalate, transform, or conclude the main arc every few turns rather than endlessly adding unrelated events.
- Make each meaningful turn change at least one durable fact: objective, ability, relationship, item, money, information, injury, status, location, or threat.

Routine logistics should normally be montage. Expand them only when they contain uncertainty, conflict, discovery, or a resource decision.

## Motivating progression

Separate final mastery from partial progress:

- A basic ability may require one or two meaningful actions.
- An advanced ability may require a short sequence of training, access, and field testing.
- A legendary ability may require a long quest, but every few meaningful steps should unlock a teacher, clue, prerequisite, controlled prototype, derivative technique, or real field test.

When an ambitious attempt fails:

1. Do not grant the final result.
2. Apply a credible cost or consequence.
3. Create or advance the staged objective in the same turn.
4. Record any genuine discovery or partial capability visibly.
5. Offer a concrete next route instead of asking the player to repeat the attempt unchanged.

An extraordinary starting trait may accelerate progress, but it does not erase requirements for knowledge, access, bodily tolerance, politics, time, or ethics.

## Playable opening

Include:

- current date and place;
- the person, group, institution, territory, or viewpoint the player controls and its authority;
- one concrete problem already in motion;
- only the context needed for the first choice;
- several distinct suggestions covering a bold main-arc route, a social or investigative route, a measurable progression route, and an optional safer route.

Player setup is optional. Put it only in `config.initFields`, and give every required field a real default. Keep the opening short enough that the player sees the decision rather than an encyclopedia.

When an option claims to change a durable opening fact, make an option-coverage table using only the affected facts. Depending on the source, columns might include location, allegiance, controlled character or faction, resources, relationships, capabilities, known information, objectives, or time period. There is no universal list. Verify each option against every seeded app. If the live contract cannot represent the differences, narrow or split the options rather than faking variety in prose.

## Map adaptation

Apply a mandatory map gate before assembling the draft:

1. Record whether the Pax source contains a map or map-owned facts.
2. Record whether location, movement, ownership, regional state, or regional action changes player decisions in the adapted core loop.
3. If either answer identifies gameplay-relevant geography, invoke the map-authoring workflow and create or remix a validated map.
4. Omit the map only when geography is genuinely decorative or interchangeable, or when the live contract blocks every lawful implementation. Record the reason; do not silently downgrade a geographic Simulation.

An unlicensed Pax image or geometry blocks copying that asset, not map gameplay itself. Prefer an original schematic region map or lawfully sourced geometry when a map is required.

For a region map:

- use stable region, faction, character, and marker IDs;
- ensure ownership and every cross-reference resolve;
- keep sovereign territory in factions and owners;
- represent non-territorial organizations as characters, relationships, or markers;
- focus the initial view on the playable area;
- keep overview labels sparse and readable;
- enable east-west wrapping only for a genuinely global map;
- maintain one stable player marker and move it after credible travel;
- use lawful geometry and stable public assets with attribution when required.

Treat Pax geometry and imagery as reference material unless reuse is lawful and passes live WorldOS validation. Follow the live contract for region-map creation and tile-map remix restrictions.

## Adaptation acceptance checklist

### Source and intent

- [ ] The exact Pax source and version are recorded.
- [ ] Preserve, rebuild, omit, and verify decisions are explicit.
- [ ] The generated coverage worksheet has no undecided row and passes the bundled checker against the candidate draft.
- [ ] Prompt, opening, and total payload budgets pass without hiding source prose in another injected field.
- [ ] The player fantasy, authority, opening decision, and core loop are clear.
- [ ] The adaptation form comes from the source rather than a default RPG or strategy template.
- [ ] The user explicitly authorized any intended write.

### Apps and state

- [ ] The live authoring guide was read.
- [ ] Every selected app was found through search and its live guide was read.
- [ ] Every durable fact has exactly one authoritative owner.
- [ ] Opening state lives in app installation configs, not world `initialState`.
- [ ] Advisor intent is preserved without a parallel system.
- [ ] At least one player-action surface exists.

### Playability

- [ ] Player setup exists only when useful; required fields use `config.initFields` and have usable defaults.
- [ ] Every consequential setup option is consistent with all seeded app state, or the option set was narrowed.
- [ ] The opening contains a live hook and distinct actions.
- [ ] Quiet play triggers grounded external pressure within two turns.
- [ ] Ordinary arcs resolve or transform within a few meaningful turns.
- [ ] Difficult goals expose staged and motivating partial progress.
- [ ] Hidden future events are not leaked through Calendar or seeded feeds.

### Integrity and localization

- [ ] Every `{{...}}` token resolves from `config.initFields` or a real character variable.
- [ ] Stable IDs and template variables survive every locale.
- [ ] Generic `i18n[locale]` overlays replace language-suffixed fields.
- [ ] Character, chat, post, faction, region, owner, and marker references resolve.
- [ ] The source-map/core-loop gate was recorded; every gameplay-relevant geographic adaptation invoked the map-authoring workflow.
- [ ] A required map was not omitted merely because Pax artwork or geometry could not be copied.
- [ ] Map geometry, ownership, assets, and attribution pass the relevant checks.
- [ ] A bounded regional map does not repeat horizontally.

### Validation and handoff

- [ ] The complete draft passes validation with every warning assessed.
- [ ] The exact source URL, version, retrieval time, hashes, and rights notes are stored in live structured provenance when supported.
- [ ] Near-limit payloads were inspected before writing; large world or map sections used exact-version bounded patches when supported.
- [ ] A create uses a stable source-versioned idempotency key.
- [ ] An update uses the latest complete draft and exact version.
- [ ] The post-write draft is re-fetched or summarized successfully.
- [ ] The returned preview was inspected when read-only page access was available; raw templates and internal window IDs are not visible.
- [ ] When exposed by the live contract, the isolated playtest completed at least five successful turn calls: ordinary action, quiet action, second quiet action with external pressure, ambitious failure/cost, and a persistence-confirming follow-up.
- [ ] Applicable relationship and map checks used their real chat and map interaction surfaces, with additional turns when necessary.
- [ ] Available player-visible assertions passed and the complete temporary turn history was inspected before deletion.
- [ ] Expected consequences changed the correct player-visible surfaces and remained consistent in later turns.
- [ ] The temporary playtest session was deleted after review.
- [ ] Without a preview or isolated/fresh-save playtest, the handoff calls the result a structurally validated draft with runtime preview or playtesting still unverified, rather than finished.
- [ ] Any real-save review remains owner-scoped and read-only.
- [ ] The handoff identifies remaining asset, copy, preview, and publishing review.
