---
name: worldos-widget-authoring
description: Design, validate, create, inspect, or update a public reusable WorldOS UGC widget through the WorldOS MCP. Use when a Simulation needs an interactive interface or persistent domain structure that no existing WorldOS app can represent, or when an owned widget needs revision.
---

# WorldOS Widget Authoring

Create a reusable public UGC widget only when existing WorldOS apps cannot express the required interaction or state. A successful create publishes the widget to the App Market immediately. Built-in apps, official apps, widgets owned by another creator, and platform code are outside this workflow.

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

- `WS.context.get()` for runtime, world, app, locale, turn, and player-character identity;
- `WS.state` for the widget’s current persistent namespace;
- `WS.onUpdate(callback)` to render new host state;
- `WS.sendAction(payload)` for a deliberate player action that should consume a Simulation turn and receive an AI response;
- `WS.engage({ kind, id, label, on })` for lightweight reversible engagement such as liking, following, voting, bookmarking, or reposting when no turn should be consumed immediately.

Use `sendAction` only for choices worth a turn. Use `engage` for passive micro-interactions. Keep payloads semantic and player-facing; do not expose raw state paths or operation grammar.

When the widget needs player-visible world data, an installed official capability, an atomic multi-system action, or collaboration with another UGC widget, read [references/widget-sdk-v2.md](references/widget-sdk-v2.md). In particular:

- call `infer_app_data_requirements` with the creator's plain-language brief, implement only its returned `WS.data.get` calls, and declare exactly those ids in `defaultConfig.integration.reads`; never ask a non-technical creator to choose ids or state paths;
- load normalized world data in one `refresh()` and register one `WS.data.subscribe(() => void refresh())` subscription;
- inspect availability with `WS.capabilities.has(name)` before using an optional official capability;
- use `WS.act()` for a turn-worthy action whose capability transaction must commit or roll back as one unit;
- use `WS.apps.list/get/subscribe/call` to discover and collaborate with installed UGC widgets while keeping the provider as the sole owner of its data;
- declare the state schema, action payloads, public commands, dependencies, fixtures, and state sharing in `defaultConfig.integration`.

## Localize the complete interface

Every create or update candidate must implement all UI locales required by the live draft schema. Currently that means setting `langs` to exactly `en`, `es`, and `zh` and writing every visible interface string in one per-locale dictionary selected through `WS.locale`:

```js
const DICTS = {
  en: { title: "Bounty Board", accept: "Accept", empty: "No bounties yet." },
  es: { title: "Tablón de Encargos", accept: "Aceptar", empty: "Aún no hay encargos." },
  zh: { title: "悬赏板", accept: "接受", empty: "暂无悬赏。" },
};
const L = DICTS[WS.locale] || DICTS.en;
```

Route headings, app and logo titles, `<title>`, buttons, labels, empty states, placeholders, select options, alerts, toasts, tooltips, `aria-label` and `alt` text, and visible fallback strings through that dictionary. Translate each locale naturally; do not copy one language into the other blocks. Real-world brand names may remain unchanged, but ordinary or fictional names should be localized naturally.

Render content from `WS.state` as authored because the Simulation already supplies it in the player's language. Write display text in `defaultConfig` once, in one natural source language, and give every object in a localizable array a stable `id`; the platform generates complete default-seed overlays before the public App is saved.

`validate_app_draft` performs a model-backed visible-copy inspection in addition to structural checks. Treat `i18n_lint_unavailable` as a retryable validation failure, not permission to write. Repair every `unlocalized_ui_copy` result before create or update. App Market name, tagline, and description translations are generated and persisted automatically by the MCP write; do not invent a separate store-copy overlay in the draft.

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

Every new or updated widget carries a versioned, typed App Contract:

```json
{
  "data": {},
  "integration": {
    "contractVersion": 1,
    "stateSchema": {
      "type": "object",
      "properties": { "items": { "type": "array", "items": { "type": "object" } } },
      "required": ["items"],
      "additionalProperties": false
    },
    "reads": ["world.quests", "world.time"],
    "actions": [{ "name": "buy", "inputSchema": { "type": "object" } }],
    "provides": [{ "name": "reserve", "description": "Reserve one available item", "inputSchema": { "type": "object" } }],
    "requires": ["wallet", "inventory", "item-catalog"],
    "exposeState": true,
    "tests": [{ "name": "default state", "kind": "state", "value": { "items": [] }, "expect": "valid" }]
  }
}
```

`stateSchema` defines the complete durable namespace. `reads` is the minimal set returned by `infer_app_data_requirements`, so Studio and world validation can verify the connection without world-specific wiring rules. `actions[].inputSchema` validates full `WS.act`/`WS.sendAction` payloads, including their `type` or `action` discriminator. `provides[].inputSchema` validates public command payloads. `requires` lists explicit official capability or installed-widget dependencies needed beyond those read declarations, `tests` provides deterministic valid/invalid fixtures, and `exposeState: false` hides this widget’s namespace from other widgets. These fields describe compatibility rather than install-time permissions. Never list the widget’s own slug in `requires`.

Use only the restricted schema dialect described in [references/widget-sdk-v2.md](references/widget-sdk-v2.md). When `stateSchema` is absent, validation infers a strict version-1 schema from `defaultConfig.data`; write an explicit schema whenever fields are optional or need enums or bounds.

Set `langs` to every locale required by the live schema and ensure the HTML actually implements each declared dictionary. A declaration without matching UI copy is invalid.

## Validate before writing

When the widget displays world data, call `infer_app_data_requirements` before writing the final HTML. Then call `run_app_contract_tests`; preserve its normalized `integration` result, repair every failed state/action fixture, and require every `readTests` entry to use `mode: "normalized"` and pass. Finally call `validate_app_draft` and repair every error. Review warnings about:

- sandbox violations;
- unsupported SDK usage;
- malformed, duplicate, self-referential, or undeclared integration dependencies;
- undeclared world reads or world data that the intended target does not provide;
- storage or navigation;
- external resources;
- unsafe HTML;
- mobile behavior;
- oversized content;
- incomplete metadata or configuration guidance.

Also repair every multilingual error, including missing locale dictionaries, visible strings outside the dictionary, or an unavailable localization inspection. Do not downgrade an MCP-authored widget to a single-language draft.

Do not create or update a widget that fails validation.

## Create or update

### Create

Use `create_app_draft` with a stable idempotency key. Reuse the key only to retry an identical draft. A successful result is an owned public UGC widget available in the App Market; do not describe it as built-in or official.

### Update

1. Use `list_owned_apps` when selection is needed.
2. Call `get_owned_app` and retain the full draft and exact `updatedAt`.
3. Preserve untouched fields while applying the intended change.
4. If the displayed world data changes, call `infer_app_data_requirements` again and replace the read set and SDK calls together.
5. If the fetched legacy draft declares fewer than the required locales, add the missing dictionaries and replace `langs` with the complete current set.
6. Re-run `run_app_contract_tests` and `validate_app_draft` on the complete candidate.
7. Call `update_app_draft` with the exact version.
8. Fetch the app again and verify the new version, locale declarations, and persisted contract.

On a stale version, refetch, reapply the intended change, revalidate, and submit again. Never overwrite concurrent changes blindly. Updating an owned public widget changes the shared App for every world that uses it, so confirm that the requested change is intended for all installations before writing.

## Install into a world

After creating a widget, install it only in a world owned by the authorized account. Put world-specific opening data in `apps[].config.initialData`, not `config.data`; it must validate after being merged over the App defaults. Put local rules in that world’s installation config. Revalidate the complete world after adding the widget so missing dependencies and invalid seed state are caught before persistence.

## Handoff

Report the widget name, slug, public status, editor/market URLs, SDK actions, integration manifest, configuration contract, validation warnings, and the worlds or use cases it is intended to support. State that successful creation already published it to the WorldOS App Market.

## Hard boundaries

- Do not create or edit built-in apps.
- Do not edit another creator’s or an official app.
- Do not imply that public visibility grants ownership; update only an App returned by the owner-scoped tools.
- Do not bypass validation or ownership through a database or private endpoint.
- Do not put secrets, access tokens, or private URLs in HTML or config.
