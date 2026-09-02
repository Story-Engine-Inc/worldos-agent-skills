# Widget SDK v2 collaboration

Read the live `get_authoring_guide` and tool schema first. This reference applies when a widget needs player-visible world data, an installed official capability, an atomic cross-capability action, or another installed UGC widget.

## Choose the interaction primitive

- `WS.sendAction(payload, ownStateMutation?)`: one deliberate Simulation turn. The optional mutation can change only the calling widget's namespace and only for a fact guaranteed by the player's click.
- `WS.act({ payload, transaction?, idempotencyKey? })`: one deliberate Simulation turn with an optional atomic transaction. Every transaction step commits or every step rolls back.
- `WS.apps.call(slug, command, payload)`: one deliberate Simulation turn invoking a command declared by another installed widget.
- `WS.engage({ kind, id, label, on })`: a reversible passive interaction that spends no turn and is handed to the AI with the player's next real action.

An `act` or `apps.call` promise acknowledges host acceptance, not turn completion. Observe `WS.data.subscribe`, `WS.world.subscribe`, or the relevant app subscription for completed state.

## Read player-visible state

Use `WS.context.get()` for SDK, world, app, locale, turn, and player-character identity. For a new read-only widget, call `infer_app_data_requirements` with the creator's plain-language brief. It returns the smallest source set plus exact `WS.data.get` calls, normalized DTO shapes, and preview fixtures. Do not ask the creator to choose source ids or raw state paths.

Load the returned sources in one asynchronous `refresh()` and register exactly one `WS.data.subscribe(() => void refresh())`. Render loading, empty, and error states, escape world/player text, and declare exactly the returned ids in `defaultConfig.integration.reads`.

```js
async function refresh() {
  const quests = await WS.data.get("world.quests");
  render(quests.items);
}
WS.data.subscribe(() => void refresh());
void refresh();
```

The normalized read catalog is:

| Source id | Read API | DTO |
| --- | --- | --- |
| `world.story` | `await WS.data.get("world.story")` | `{ items: [{ id, text, turn, time? }] }` |
| `world.time` | `await WS.data.get("world.time")` | `{ value }` |
| `world.stats` | `await WS.data.get("world.stats")` | `{ items: [{ id, label, value, min?, max? }] }` |
| `world.quests` | `await WS.data.get("world.quests")` | `{ items: [{ id, title, description?, status, kind, reward? }] }` |
| `world.characters` | `await WS.data.get("world.characters")` | `{ items: [{ id, name, avatar?, role?, intro? }] }` |
| `world.characterStats` | `await WS.data.get("world.characterStats")` | `{ characters: [{ id, name, stats }] }` |
| `world.map` | `await WS.data.get("world.map")` | `{ regions, markers }` |
| `world.chats` | `await WS.data.get("world.chats")` | `{ conversations }` |
| `world.social` | `await WS.data.get("world.social")` | `{ items }` |
| `player.inventory` | `await WS.data.get("player.inventory")` | `{ lists: [{ id, label, items }] }` |
| `player.equipment` | `await WS.data.get("player.equipment")` | `{ items, attributes, proficiencies, xp? }` |
| `player.wallet` | `await WS.data.get("player.wallet")` | `{ balance }` |

`WS.world.getSnapshot()` and the capability-specific read helpers below remain available for existing published widgets, but new read-only widgets should not parse those raw or legacy shapes.

Check `WS.capabilities.has(name)` before using an optional official capability:

- `WS.wallet.getBalance()`
- `WS.inventory.list(listId)`
- `WS.equipment.get()`
- `WS.stats.get()`
- `WS.characterStats.get(characterId)`
- `WS.characters.list()`
- `WS.time.get()`
- `WS.chats.list()`
- `WS.social.get()`
- `WS.map.get()`

The projection excludes private prompts, model and billing settings, raw operation and replay data, hidden characters, and widget namespaces that opted out of sharing.

`reads` is compatibility metadata, not a permission request. It lets world validation reject an installation when the target world lacks the corresponding data App. Do not add `WS.apps` collaboration, copied state, or write transactions merely to read world data.

## Declare collaboration

Put the manifest in `defaultConfig.integration`:

```json
{
  "data": {},
  "integration": {
    "contractVersion": 1,
    "stateSchema": {
      "type": "object",
      "properties": {
        "items": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": { "id": { "type": "string" }, "reserved": { "type": "boolean" } },
            "required": ["id", "reserved"],
            "additionalProperties": false
          }
        }
      },
      "required": ["items"],
      "additionalProperties": false
    },
    "reads": ["world.quests", "world.time"],
    "actions": [{
      "name": "buy",
      "inputSchema": {
        "type": "object",
        "properties": { "type": { "type": "string", "enum": ["buy"] }, "itemId": { "type": "string" } },
        "required": ["type", "itemId"],
        "additionalProperties": false
      }
    }],
    "provides": [
      {
        "name": "reserve",
        "description": "Reserve one available item",
        "inputSchema": {
          "type": "object",
          "properties": { "itemId": { "type": "string" } },
          "required": ["itemId"],
          "additionalProperties": false
        }
      }
    ],
    "requires": ["wallet", "inventory", "item-catalog"],
    "exposeState": true,
    "tests": [
      { "name": "default state", "kind": "state", "value": { "items": [] }, "expect": "valid" },
      { "name": "buy requires an id", "kind": "action", "subject": "buy", "value": { "type": "buy" }, "expect": "invalid" }
    ]
  }
}
```

- `contractVersion`: use `1` for the current machine-readable contract.
- `stateSchema`: the complete durable namespace under `WS.state`. World installation merges `apps[].config.initialData` over `defaultConfig.data` and validates the result.
- `reads`: unique stable ids for player-visible world or player sources consumed by the widget. World validation checks their backing capability directly; a read-only widget does not need a separate world linkage rule.
- `actions`: up to 32 unique turn-worthy action names. Each `inputSchema` validates the full payload, including its `type` or `action` discriminator.
- `provides`: up to 32 unique public commands. Names start with a lowercase letter and contain only lowercase letters, digits, `.`, `_`, or `-`.
- `provides[].inputSchema`: validates the complete `WS.apps.call` payload before a turn is accepted.
- `requires`: up to 32 unique official capability names or lowercase installed-widget slugs. Do not require the widget itself.
- `exposeState`: defaults to `true`; set it to `false` only for a namespace other widgets must not read.
- `tests`: up to 32 deterministic `state`, `action`, or `command` fixtures with `expect: "valid" | "invalid"`. Non-state tests name their declaration in `subject`.

The restricted schema dialect supports `type`, `description`, `properties`, `required`, `items`, scalar `enum`, `additionalProperties`, `minItems`, `maxItems`, `minLength`, `maxLength`, `minimum`, `maximum`, and `default`. It intentionally rejects `$ref`, patterns, executable formats, alternatives, and remote schemas. If `stateSchema` is omitted, authoring validation infers a strict version-1 schema from `defaultConfig.data`; use an explicit contract for optional fields, bounds and enums.

Call `run_app_contract_tests` before `validate_app_draft`, then preserve the normalized integration returned by the contract runner. Its `readTests` reports the SDK call, DTO and fixture for every declared source; new code must pass in `normalized` mode. Installation validation catches missing dependencies and invalid `initialData`. At runtime, invalid action/command payloads are rejected before the turn, transactions roll back atomically, and AI or widget writes that would leave the calling namespace outside `stateSchema` are dropped.

The manifest describes compatibility, not install-time permission grants. A widget still receives only the player-visible projection. The host checks declared read availability, installed capabilities, target installation, declared commands, payload shape and size, contracted state, atomicity, idempotency, and replay behavior.

Discover collaborators with `WS.apps.list()`, inspect one with `WS.apps.get(slug)`, and subscribe with `WS.apps.subscribe(slug, callback)`. A consumer may read an exposed provider namespace but never mutate it directly. Use `WS.apps.call` for provider-owned behavior and keep the provider as the single source of truth.

## Build an atomic action

Supported transaction steps are:

- calling widget: `set`, `update`, `inc`, `push`, `remove`;
- wallet: `adjust`;
- inventory: `add`, `update`, `remove`;
- equipment: `grant`, `revoke`, `equip`, `unequip`, `discard`, `setStat`, `incrementStat`;
- world stats and character stats: `set`, `increment`;
- time: `set`.

Example:

```js
await WS.act({
  payload: { type: "buy", itemId: item.id },
  transaction: [
    { capability: "wallet", operation: "adjust", amount: -item.price, description: item.name },
    { capability: "app", verb: "inc", path: `stock.${item.id}`, value: -1 },
    { capability: "inventory", operation: "add", listId: "bag", item }
  ]
});
```

Transactions support at most 20 steps and 32 KiB. A negative resulting wallet balance, unavailable capability, missing update/remove target, unsafe path, malformed step, invalid resulting App state, or duplicate idempotency key with incompatible content rejects the whole transaction.
