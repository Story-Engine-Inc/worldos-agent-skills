# World draft acceptance checklist

Use this checklist before creating or updating a world.

## Authority and versioning

- [ ] The user explicitly authorized the intended write.
- [ ] The live authoring guide was read successfully.
- [ ] The target is owned by the authorized account and remains unpublished.
- [ ] An update is based on the complete latest draft and exact `updatedAt`.
- [ ] A create uses a stable idempotency key; identical retries reuse it.

## Playability

- [ ] The player fantasy, scale, and authority are clear.
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
- [ ] The handoff says the world is unpublished and requires human review.
