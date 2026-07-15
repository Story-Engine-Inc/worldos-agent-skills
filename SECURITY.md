# Security policy

## Supported versions

The latest commit on the default branch and the latest tagged release receive security fixes. Older revisions may contain stale workflow guidance and are not supported.

## Reporting a vulnerability

Do not disclose credential exposure, authorization bypasses, malicious skill behavior, or MCP security issues in a public issue.

Use [GitHub private vulnerability reporting](https://github.com/Story-Engine-Inc/worldos-agent-skills/security/advisories/new). If private reporting is unavailable, contact the maintainers through the [Story Engine organization profile](https://github.com/Story-Engine-Inc) before sharing technical details publicly.

Include the affected skill and revision, a sanitized reproduction, expected impact, and any suggested mitigation. The maintainers will acknowledge a report as soon as practical, investigate it privately, and coordinate disclosure after a fix is available.

## Scope

This repository contains instructional Agent Skills. The WorldOS MCP server is responsible for authentication, authorization, ownership enforcement, schema validation, concurrency controls, and write restrictions.

Never include access tokens, OAuth credentials, Supabase credentials, private API endpoints, or production data in a report attachment or reproduction committed to a fork.

Vulnerabilities in the WorldOS service or MCP server may be transferred to the appropriate private WorldOS security channel. General usage questions and feature requests belong in public repository issues once the repository is public.
