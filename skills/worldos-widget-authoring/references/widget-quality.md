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
- [ ] Turn-consuming decisions use `WS.sendAction`.
- [ ] Passive engagement uses `WS.engage` when appropriate.
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
- [ ] The handoff says the widget remains private and unpublished.
