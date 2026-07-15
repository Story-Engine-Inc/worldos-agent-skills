# Localization and template variables

## Locale overlays

Use `i18n[locale]` as a generic overlay that mirrors the canonical structure. Do not introduce language-specific field names.

The canonical content can be written in any language. English is not a privileged read path: when an English overlay exists, it must be eligible just like any other locale.

For arrays of localizable objects:

- give every item a stable `id`;
- align overlay entries by `id`, not by translated label;
- preserve identifiers, enum values, URLs, colors, and numeric data;
- localize player-visible names, descriptions, messages, labels, prompts, and suggestions;
- write natural product copy for the locale rather than literal sentence-by-sentence translation.

Treat legacy fields ending in language suffixes as migration debt, never as examples for new content.

## Player variables

Use the standard semantic setup fields when appropriate:

- `player_name` for the player’s name;
- `player_persona` for background, identity, or play style.

Reference their values with the template syntax supported by the current WorldOS contract. Give required fields useful defaults and a few clickable options so the Simulation can start without typing.

## Character variables

Give customizable characters a stable ID and, when supported, a readable variable key. Reference the character through its template variable everywhere the character appears:

- world prompt;
- character descriptions and relationships;
- story opening;
- chat names and messages;
- posts and comments;
- action suggestions;
- widget initial data;
- map factions or markers.

Keep the character’s canonical `name` as the default value. Replace references to that name with the variable, not the name field itself.

## Reference integrity

Localization must not change identifiers. After composing every locale, verify that:

- character IDs remain identical;
- author and sender IDs resolve;
- faction `charId` values resolve;
- region and owner IDs resolve;
- localized arrays retain the same stable item IDs;
- template variables are not translated or partially rewritten.
