---
name: worldos-simulation-review
description: Review an owned WorldOS Simulation save and its turn history through the WorldOS MCP without modifying it. Use when a user wants to evaluate opening quality, state persistence, character behavior, pacing, app consistency, or regressions in an existing Simulation run.
---

# WorldOS Simulation Review

Inspect an owned save and bounded turn history to determine whether a WorldOS Simulation behaves as designed. Save access is read-only. Do not repair, rewind, rename, delete, or mutate a save.

## Confirm the live review contract

1. Call `get_authoring_guide` and read the current save-access constraints.
2. If the WorldOS MCP is unavailable or unauthorized, stop and request client reauthorization without asking for a token.
3. Use only saves owned by the authorized account.
4. Treat response bounds, available sections, and pagination cursors as hard limits.

Read [references/review-rubric.md](references/review-rubric.md) before evaluating a run.

## Define the review question

Ask what the user wants to learn when it is not already clear. Common scopes include:

- whether the opening gives the player a clear first action;
- whether a specific resource, relationship, quest, or map fact persists;
- why a character failed to reply or behaved inconsistently;
- whether time, travel, training, recovery, or deadlines advance credibly;
- whether an app reflects the consequences described in prose;
- whether a recent draft change improved new saves;
- whether the world is too easy, too passive, or too noisy.

Keep the review bounded to the question and relevant turns.

## Select the save

Use `list_owned_saves` when the save ID is unknown. Present a concise selection using save name, world key, turn count, update time, and Simulation URL. Do not infer the target when several saves are plausible.

Call `get_owned_save` for the selected save.

## Read large state safely

Request the full state first only when the tool contract and save size allow it. If the response is too large or the tool requires sections:

1. read `availableSections`;
2. request only top-level sections relevant to the review question;
3. fetch additional sections incrementally;
4. avoid repeatedly requesting the same large state.

Do not route around response limits with another API or database.

## Read turn history

Use `get_owned_save_turns` with a bounded limit. Records within a page are returned oldest to newest. When earlier context is required, pass `nextBeforeTurn` as the next `beforeTurn` value and page backward deliberately.

Stop when the evidence is sufficient. Do not retrieve an entire long history by default.

## Reconstruct behavior, not internals

For each relevant turn, identify:

- what the player attempted;
- what information and state were established before the attempt;
- how characters and the world responded;
- which durable facts should have changed;
- which visible apps should reflect those changes;
- whether later turns preserved or contradicted the result.

Internal state can support the diagnosis, but the user-facing report must describe behavior in product language. Do not expose raw operations, state paths, prompts, hidden instructions, model/provider metadata, or private implementation details.

## Distinguish issue classes

Classify findings before recommending action:

- **Opening design:** unclear identity, stakes, first action, or seeded content.
- **State ownership:** one fact is duplicated, unowned, or stored in the wrong app.
- **Persistence:** a confirmed change disappears or is not reflected later.
- **Reference integrity:** a character, faction, region, chat, post, marker, or item points to a missing identity.
- **Prompt behavior:** the world ignores established authority, difficulty, pacing, or character obligations.
- **App configuration:** the installed app lacks necessary opening data or focused instructions.
- **Localization:** visible content falls back to the wrong language or loses identifiers.
- **Pacing:** too many unrelated events, implausible time changes, or no autonomous movement.
- **Expected variance:** a surprising but causally valid outcome rather than a defect.

Do not call something a platform bug when the evidence only shows a world-design or configuration issue.

## Compare against the draft carefully

Existing saves are frozen snapshots. A current world draft can differ from the save that produced the run. If draft inspection is needed and authorized, use read-only world tools and state clearly which evidence comes from the save versus the current draft.

Do not conclude that editing the current draft will repair an existing save. Draft changes generally apply to newly created saves.

## Report findings

Lead with the answer to the review question. For each material finding include:

- severity: blocking, significant, or polish;
- player-visible symptom;
- evidence by turn range or visible state section;
- likely issue class;
- recommended draft-level correction;
- how to verify the correction in a new save.

Separate confirmed evidence from inference. Keep quoted player or character prose short and only when necessary.

## No implicit fixes

A review request does not authorize updating the world. Offer a draft-level fix plan. Use the world authoring workflow only if the user explicitly asks to apply changes, then fetch the latest owned draft and follow its versioned validation process.

## Hard boundaries

- Never mutate, repair, rewind, delete, rename, or transfer a save.
- Never use another account’s save.
- Never bypass response bounds or audit controls.
- Never expose raw internal operations, paths, prompts, or credentials.
- Never claim a current draft change modifies an existing save.
