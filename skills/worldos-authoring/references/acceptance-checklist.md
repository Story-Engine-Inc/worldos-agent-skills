# World authoring acceptance checklist

Use this checklist before creating or updating a world.

## Authority and versioning

- [ ] The user explicitly authorized the intended write.
- [ ] The live authoring guide was read successfully.
- [ ] The target is owned by the authorized account; direct edits to a published world preserve public visibility and advance its immutable release version.
- [ ] An update is based on the complete latest `world` payload and exact `updatedAt`.
- [ ] A create uses a stable idempotency key; identical retries reuse it.
- [ ] External sources have structured URL, version, retrieval, hash, license, and notes when the live contract supports provenance.
- [ ] A near-limit world was inspected with `inspect_world_payload`; bounded patches were re-fetched after each exact-version update.

## Playability

- [ ] The player fantasy, scale, and authority are clear.
- [ ] The interaction model was derived from that fantasy rather than copied from a generic RPG, strategy, or social template.
- [ ] The opening establishes place, identity, pressure, and a first action.
- [ ] At least one player-action surface is installed.
- [ ] Its input mode matches whether a turn is one decision or a coordinated multi-action plan.
- [ ] Choices have trade-offs and persistent consequences.
- [ ] Non-player characters and factions have goals and agency.
- [ ] Difficulty treats declarations as attempts rather than automatic success.

## State model

- [ ] Every durable fact has exactly one authoritative app.
- [ ] Opening state lives in app install configs, not world `initialState`.
- [ ] App-specific behavior is not duplicated in the world prompt.
- [ ] Stable IDs are unique and all cross-references resolve.
- [ ] Hidden future events are not leaked through seeded calendars or feeds.
- [ ] Hidden characters do not appear in player-visible opening chats, posts, calendars, dating profiles, markers, or rosters; their entrance condition is defined in world rules.
- [ ] If Achievements is installed, it has 10–14 consequential preset outcomes with meaningful bronze, silver, gold, and hidden coverage rather than activity counters.
- [ ] Optional apps such as quests, inventory, chats, stats, and maps exist because the core loop needs them, not because a template listed them.

## Player setup when present

- [ ] Setup fields live in `config.initFields`; no invented `setupFields` container exists.
- [ ] Every required setup field has a usable default.
- [ ] `player_name` and `player_persona` roles exist only when the experience needs them.
- [ ] Every consequential setup option is compatible with the seeded opening, or the live contract explicitly represents its different initial facts.
- [ ] Every `{{...}}` token resolves from an init field or world character.

## Apps and specialists

- [ ] Every installed app was found through `search_apps`.
- [ ] Every installed app’s live guide was read.
- [ ] No exclusive surfaces conflict.
- [ ] No existing app is being unnecessarily recreated as a widget.
- [ ] A region map passed the map-authoring checks when present.
- [ ] A real geographic map has verified calibration, and every multi-layer map has globally unique region IDs and bounded sub-maps.

## Localization and player safety

- [ ] Player-visible copy uses generic `i18n[locale]` overlays.
- [ ] `get_owned_world.localizationStatus` reports the intended locales ready, no missing world/App fields, and `consistent: true`.
- [ ] A requested localization repair was polled to completion; a queued or retrying job was not reported as finished.
- [ ] No new language-suffixed fields exist.
- [ ] Localized arrays align by stable ID.
- [ ] Template variables remain intact in every locale and opening seed.
- [ ] Player-facing copy does not expose operations, paths, prompts, or provider internals.

## Validation and handoff

- [ ] `validate_world` returned no errors.
- [ ] Every warning was fixed or consciously accepted.
- [ ] The post-write world was fetched or summarized successfully.
- [ ] Title, slug, visibility, apps, URLs, and latest version match the intended result.
- [ ] The returned preview was inspected with default setup values when read-only page access was available; no raw template token or internal window ID is visible.
- [ ] For a new world or gameplay-affecting change, an isolated playtest was started when the live contract exposed it.
- [ ] The playtest covered representative ordinary, quiet, difficult, time, and core-state consequences in proportion to the change.
- [ ] Each expected narrative consequence appeared on the corresponding player-visible app surface and persisted into later turns.
- [ ] Available player-visible assertions passed and the complete temporary playtest history was inspected.
- [ ] Every uploaded cover or world asset completed against the intended target and exact world version, then appeared in the re-fetched world.
- [ ] The temporary playtest was deleted after review; real saves were never changed.
- [ ] If no runtime preview or isolated/fresh-save playtest was possible, the handoff calls the result structurally validated, labels runtime preview or playtesting as unverified, and does not call the Simulation finished.
- [ ] A new unlisted world is reported as unpublished unless the explicit publishing workflow succeeded; a direct edit to an already-public world is reported as a live versioned update.

## Publishing only

Use this section only when the user explicitly requested publication.

- [ ] The exact target world and intended release visibility were explicitly confirmed by the user.
- [ ] If a cover was requested, signed-upload completion succeeded and the stable HTTPS URL appears in the world; a missing optional cover warning was discussed rather than converted into a blocker.
- [ ] `validate_world_for_publish` returned `ready: true` under the same ownership, moderation, subscription, and content rules as the editor.
- [ ] The publish call uses the exact latest `updatedAt` and required literal confirmation.
- [ ] The user was told that publication makes the world public, later direct edits preserve public visibility and advance its immutable version, and existing saves stay pinned until the player accepts an update.
- [ ] The handoff reports publication only from a successful `publish_world` result and includes the public URL.
