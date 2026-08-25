# Widget quality checklist

## Product fit

- [ ] Existing apps were searched first.
- [ ] The widget owns a distinct durable concept.
- [ ] The widget is reusable across multiple worlds.
- [ ] World-specific flavor remains in installation config.
- [ ] The slug is generic, stable, and non-colliding.

## SDK semantics

- [ ] Initial rendering reads `WS.state`.
- [ ] Updates are handled through `WS.onUpdate`.
- [ ] Turn-consuming decisions use `WS.sendAction` or `WS.act` according to whether an atomic capability transaction is needed.
- [ ] Passive engagement uses `WS.engage` when appropriate.
- [ ] Optional official capabilities are checked with `WS.capabilities.has` before use.
- [ ] A multi-system guaranteed change uses one `WS.act` transaction rather than separate actions.
- [ ] Another widget's state is read or called through `WS.apps`; it is not copied or directly mutated.
- [ ] `defaultConfig.integration` accurately declares used dependencies, callable commands, and state-sharing intent.
- [ ] Player actions contain semantic intent, not internal state paths.
- [ ] The widget never speaks for the player without a player gesture.

## Sandbox and security

- [ ] No dependency on browser storage or cookies.
- [ ] No arbitrary remote scripts or hidden network calls.
- [ ] No navigation, popup, download, or frame-escape behavior.
- [ ] Untrusted strings are rendered as text rather than unsafe HTML.
- [ ] No token, credential, secret URL, raw prompt, or provider detail is embedded.

## Interaction quality

- [ ] Inputs are at least 16px on mobile.
- [ ] The interface works at narrow widths.
- [ ] No `scrollIntoView`, `autofocus`, or focus-on-mount is used.
- [ ] Keyboard focus is visible and controls have accessible labels.
- [ ] Loading, empty, invalid, and missing-image states are handled.
- [ ] Images retain their aspect ratio.
- [ ] The interface uses concise player-facing language.

## Interface localization

- [ ] `langs` contains every locale required by the live schema (`en`, `es`, and `zh` currently).
- [ ] The HTML reads `WS.locale` and selects a complete per-locale UI dictionary.
- [ ] Titles, controls, placeholders, options, states, notifications, accessibility text, and visible fallbacks all use the dictionary.
- [ ] Each locale is written naturally rather than copying another locale's text.
- [ ] Content from `WS.state` is rendered as supplied instead of being translated in the widget.
- [ ] Localizable object arrays in `defaultConfig` use stable IDs.
- [ ] `validate_app_draft` reports no `unlocalized_ui_copy` or `i18n_lint_unavailable` error.

## Configuration quality

- [ ] `defaultConfig` is minimal and renderable.
- [ ] `configGuide` explains the installation shape succinctly.
- [ ] Localizable data uses stable IDs and can accept `i18n[locale]` overlays.
- [ ] The reusable prompt is short, generic, and aligned with actual behavior.

## MCP lifecycle

- [ ] `validate_app_draft` has no errors.
- [ ] Every warning was assessed.
- [ ] Creates use an idempotency key.
- [ ] Updates use the exact fetched version.
- [ ] The post-write app was fetched and verified.
- [ ] The handoff says a successful create published the widget to the App Market immediately.
