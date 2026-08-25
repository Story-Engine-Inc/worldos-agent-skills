# Widget SDK v2 collaboration

Read the live `get_authoring_guide` and tool schema first. This reference applies when a widget needs player-visible world data, an installed official capability, an atomic cross-capability action, or another installed UGC widget.

## Choose the interaction primitive

- `WS.sendAction(payload, ownStateMutation?)`: one deliberate Simulation turn. The optional mutation can change only the calling widget's namespace and only for a fact guaranteed by the player's click.
- `WS.act({ payload, transaction?, idempotencyKey? })`: one deliberate Simulation turn with an optional atomic transaction. Every transaction step commits or every step rolls back.
- `WS.apps.call(slug, command, payload)`: one deliberate Simulation turn invoking a command declared by another installed widget.
- `WS.engage({ kind, id, label, on })`: a reversible passive interaction that spends no turn and is handed to the AI with the player's next real action.

An `act` or `apps.call` promise acknowledges host acceptance, not turn completion. Observe `WS.world.subscribe` or the relevant app subscription for completed state.

## Read player-visible state

Use `WS.context.get()` for SDK, world, app, locale, turn, and player-character identity. Use `WS.world.getSnapshot()` and `WS.world.subscribe(callback)` for the player-visible world projection.

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

## Declare collaboration

Put the manifest in `defaultConfig.integration`:

```json
{
  "data": {},
  "integration": {
    "provides": [
      { "name": "reserve", "description": "Reserve one available item" }
    ],
    "requires": ["wallet", "inventory", "item-catalog"],
    "exposeState": true
  }
}
```

- `provides`: up to 32 unique public commands. Names start with a lowercase letter and contain only lowercase letters, digits, `.`, `_`, or `-`.
- `requires`: up to 32 unique official capability names or lowercase installed-widget slugs. Do not require the widget itself.
- `exposeState`: defaults to `true`; set it to `false` only for a namespace other widgets must not read.

The manifest describes compatibility, not install-time permission grants. The host still checks installed capabilities, target installation, declared commands, payload shape and size, atomicity, idempotency, and replay behavior.

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

Transactions support at most 20 steps and 32 KiB. A negative resulting wallet balance, unavailable capability, missing update/remove target, unsafe path, malformed step, or duplicate idempotency key with incompatible content rejects the whole transaction.
