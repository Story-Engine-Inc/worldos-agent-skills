# Contributing

Thank you for improving WorldOS Agent Skills. Contributions should make world authoring safer, clearer, more portable, or more capable without depending on a specific agent client.

## Before opening a change

- Search existing issues and pull requests.
- Open an issue first for a new skill, a major scope change, or a change to a WorldOS security boundary.
- Use the live WorldOS MCP authoring guide and tool schemas as the current contract.
- Report vulnerabilities through the process in [SECURITY.md](SECURITY.md), not a public issue.

## Skill requirements

- Place each skill at `skills/<skill-name>/SKILL.md`.
- Use only `name` and `description` in shared skill frontmatter.
- Keep names lowercase and hyphenated, with the directory matching the `name` exactly.
- Describe both capability and trigger conditions in `description`.
- Keep `SKILL.md` focused; put optional detail in directly linked `references/` files.
- Refer to WorldOS MCP tools by logical tool name, never by a client-specific prefix.
- Do not depend on local repositories, Supabase, SQL, private APIs, or unpublished implementation details.
- Do not add client-specific invocation syntax to shared skills.
- Never commit credentials, tokens, production data, or personal filesystem paths.

## Development

Use Node.js 24 or later. This repository has no runtime dependencies.

```bash
npm run validate
npx skills add . --list
```

Both commands must succeed before opening a pull request. Also read every changed skill as an agent would: confirm that write intent, ownership, validation, idempotency, version handling, and publication boundaries remain explicit.

## Pull requests

Keep changes focused and explain:

1. the user request or failure mode addressed;
2. why the change belongs in a reusable skill;
3. how portability and security boundaries were preserved;
4. which validation or forward tests were run.

By contributing, you agree that your contributions are licensed under the Apache License 2.0.
