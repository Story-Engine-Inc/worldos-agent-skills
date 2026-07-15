# Agent contribution guidance

This repository distributes portable Agent Skills for the public WorldOS MCP.

## Portability

- Keep shared skills compatible with the open Agent Skills format.
- Use only `name` and `description` in shared `SKILL.md` frontmatter.
- Refer to tools by their WorldOS MCP tool name, such as `get_authoring_guide`, never by a client-specific prefix.
- Do not use Codex `$skill` syntax or Claude `/plugin:skill` syntax inside shared skills.
- Do not depend on the WorldOS application repository, local absolute paths, Supabase, SQL, migrations, or private APIs.
- Put client-specific manifests and metadata in future adapter packages, not under `skills/`.

## Authoring contract

- Read the live `get_authoring_guide` before relying on bundled references.
- Treat live MCP tool schemas and validation results as authoritative when they differ from these files.
- Keep opening state in each installed app config, not in a world-level `initialState`.
- Use generic `i18n[locale]` overlays; never add language-suffixed fields.
- Never expose raw operations, state paths, prompts, or provider internals to players.
- Do not add workflows that bypass MCP ownership, publication, or save-state restrictions.

## Changes

- Keep each skill focused and place optional detail in directly linked references.
- Update trigger descriptions when scope changes.
- Run `npm run validate` before committing.
- Add no credentials, tokens, personal paths, generated caches, or packaged distributions.
