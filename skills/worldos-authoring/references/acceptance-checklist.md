# World acceptance checklist

Use this checklist before creating or updating a world.

## Authority and versioning

- [ ] The user explicitly authorized the intended write.
- [ ] The live authoring guide was read successfully.
- [ ] The target is owned by the authorized account and is not blocked.
- [ ] An update is based on the complete latest world and exact `updatedAt`.
- [ ] For a published target, the user authorized the intended live-world change and understands that visibility remains public.
- [ ] A create uses a stable idempotency key; identical retries reuse it.
- [ ] External sources have structured URL, version, retrieval, hash, license, and notes when the live contract supports provenance.
- [ ] A near-limit draft was inspected before writing; bounded patches were re-fetched after each exact-version update.

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

## Localization and player safety

- [ ] Player-visible copy uses generic `i18n[locale]` overlays.
- [ ] No new language-suffixed fields exist.
- [ ] Localized arrays align by stable ID.
- [ ] Template variables remain intact in every locale and opening seed.
- [ ] Player-facing copy does not expose operations, paths, prompts, or provider internals.

## Validation and handoff

- [ ] `validate_world_draft` returned no errors.
- [ ] Every warning was fixed or consciously accepted.
- [ ] The post-write world was fetched or summarized successfully.
- [ ] Title, slug, visibility, apps, URLs, and latest version match the intended result.
- [ ] The returned preview was inspected with default setup values when read-only page access was available; no raw template token or internal window ID is visible.
- [ ] For a new world or gameplay-affecting change, an isolated playtest was started when the live contract exposed it.
- [ ] The playtest covered representative ordinary, quiet, difficult, time, and core-state consequences in proportion to the change.
- [ ] Each expected narrative consequence appeared on the corresponding player-visible app surface and persisted into later turns.
- [ ] Available player-visible assertions passed and the complete temporary playtest history was inspected.
- [ ] Every uploaded cover or world asset completed against the intended target and exact world version, then appeared in the re-fetched draft.
- [ ] The temporary playtest was deleted after review; real saves were never changed.
- [ ] If no runtime preview or isolated/fresh-save playtest was possible, the handoff calls the result a structurally validated draft, labels runtime preview or playtesting as unverified, and does not call the Simulation finished.
- [ ] The handoff reports fetched visibility accurately: an already public world remained public, while an unpublished world still requires human review and explicit publication.

## Publishing only

Use this section only when the user explicitly requested publication.

- [ ] The exact target world and public visibility were explicitly confirmed by the user.
- [ ] A stable HTTPS cover is attached; signed-upload completion succeeded when a cover was uploaded.
- [ ] `validate_world_for_publish` returned `ready: true` with reviewer permission.
- [ ] The publish call uses the exact latest `updatedAt` and required literal confirmation.
- [ ] The user was told that publication makes the world public and that later edits remain live, owner-scoped, validated, and exact-versioned.
- [ ] The handoff reports publication only from a successful `publish_world` result and includes the public URL.
