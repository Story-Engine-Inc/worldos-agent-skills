---
name: worldos-widget-authoring
description: Design, validate, create, inspect, or update a private reusable WorldOS UGC widget through the WorldOS MCP. Use when a Simulation needs an interactive interface or persistent domain structure that no existing WorldOS app can represent, or when an owned unpublished widget draft needs revision.
---

# WorldOS Widget Authoring

Create a reusable private UGC widget only when existing WorldOS apps cannot express the required interaction or state. Built-in apps, shared apps, published apps, and platform code are outside this workflow.

## Confirm that a widget is necessary

1. Call `get_authoring_guide`.
2. Call `search_apps` with several focused queries for the required capability.
3. Call `get_app_guide` for plausible existing apps.
4. Prefer an existing app with world-specific install config.
5. Create a widget only when a clear capability gap remains.

Do not create a second source of truth for data already owned by stats, inventory, quests, chat, social, time, calendar, map, or another installed app.

Read [references/widget-quality.md](references/widget-quality.md) before validation.

## Separate reusable behavior from world content

A widget is a reusable, domain-neutral interface. Put reusable structure and behavior in the app draft:

- neutral name and slug;
- concise store description and tagline;
- single-file HTML, CSS, and JavaScript;
- reusable prompt describing the widget’s meaning and supported interactions;
- generic `defaultConfig`;
- a short `configGuide` explaining how a world author should seed it.

Put world-specific labels, people, organizations, starting records, and local rules in the world’s app installation config. Avoid slugs tied to one story when the same interface could serve many worlds.

## Use the WorldOS widget SDK

Use the host-provided SDK rather than inventing storage or a transport layer:

- `WS.state` for the widget’s current persistent namespace;
- `WS.onUpdate(callback)` to render new host state;
- `WS.sendAction(payload)` for a deliberate player action that should consume a Simulation turn and receive an AI response;
- `WS.engage({ kind, id, label, on })` for lightweight reversible engagement such as liking, following, voting, bookmarking, or reposting when no turn should be consumed immediately.

Use `sendAction` only for choices worth a turn. Use `engage` for passive micro-interactions. Keep payloads semantic and player-facing; do not expose raw state paths or operation grammar.

## Respect the sandbox

Treat the widget as a sandboxed opaque-origin iframe:

- do not rely on `localStorage`, `sessionStorage`, cookies, or browser persistence;
- do not rely on arbitrary network fetches or external scripts;
- keep transient interface state in ordinary JavaScript variables;
- persist meaningful state only through the WorldOS SDK and Simulation turn flow;
- avoid navigation, popups, downloads, and attempts to escape the frame;
- use self-contained HTML, CSS, and JavaScript wherever possible.

Never use `scrollIntoView`, `autofocus`, or focus-on-mount. Scroll a specific internal container by setting its own `scrollTop`. If focus is necessary after a user gesture, use `focus({ preventScroll: true })` when supported.

## Design for mobile and failure

- Make input, textarea, and select text at least 16px on mobile.
- Use responsive layouts without fixed desktop-only widths.
- Give buttons meaningful text or accessible labels.
- Preserve visible keyboard focus.
- Use adequate contrast and do not rely on color alone.
- Render an empty state and recover gracefully from absent optional fields.
- Escape untrusted text and avoid assigning user content through unsafe HTML.
- Keep image containers bounded and preserve image aspect ratio with `object-fit`.
- Provide fallbacks for missing or failed images.

## Build the draft

Choose a lowercase hyphenated slug that does not collide with an existing app. Keep names and public copy understandable to non-technical world creators. Do not mention operations, reducers, modules, raw state, or prompt internals in player-facing copy.

Make `configGuide` short and precise. It should explain the expected installation data shape and identify which fields are localizable, without embedding one world’s data.

Make `defaultConfig` small but renderable. It should demonstrate the generic structure without shipping a fictional world’s full content.

## Validate before writing

Call `validate_app_draft` and repair every error. Review warnings about:

- sandbox violations;
- unsupported SDK usage;
- storage or navigation;
- external resources;
- unsafe HTML;
- mobile behavior;
- oversized content;
- incomplete metadata or configuration guidance.

Do not create or update a widget that fails validation.

## Create or update

### Create

Use `create_app_draft` with a stable idempotency key. Reuse the key only to retry an identical draft. The result is a private UGC draft; do not describe it as built-in, shared, or published.

### Update

1. Use `list_owned_apps` when selection is needed.
2. Call `get_owned_app` and retain the full draft and exact `updatedAt`.
3. Preserve untouched fields while applying the intended change.
4. Re-run `validate_app_draft` on the complete candidate.
5. Call `update_app_draft` with the exact version.
6. Fetch the app again and verify the new version.

On a stale version, refetch, reapply the intended change, revalidate, and submit again. Never overwrite concurrent changes blindly.

## Install into a world

After creating a widget, install it only in a world owned by the authorized account. Put world-specific opening data and local rules in that world’s installation config. Revalidate the complete world draft after adding the widget.

## Handoff

Report the widget name, slug, private status, editor/market URLs, SDK actions, configuration contract, validation warnings, and the worlds or use cases it is intended to support. State that a human must review and publish it in WorldOS.

## Hard boundaries

- Do not create or edit built-in apps.
- Do not edit another creator’s, shared, or published app.
- Do not make the widget public or claim it was published.
- Do not bypass validation or ownership through a database or private endpoint.
- Do not put secrets, access tokens, or private URLs in HTML or config.
