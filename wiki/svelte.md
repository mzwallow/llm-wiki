# Svelte

## What It Is

Svelte is a component-based UI framework that compiles declarative HTML/CSS/JS into optimized JavaScript at build time. Unlike React/Vue, it does not use a virtual DOM — updates are surgical, targeting exact DOM nodes.

## Reactivity Model (Svelte 5)

Runes are compiler keywords controlling reactivity:

- **`$state`** — reactive state. Deeply proxies objects/arrays for granular updates. `$state.raw` skips proxying (perf for large data). `$state.snapshot` creates static copy. `$state.eager` forces immediate UI update.
- **`$derived`** — computed value from reactive deps. Pure expression only. `$derived.by` for multi-statement logic. Writable since 5.25 for optimistic UI. Push-pull: dependents notified immediately, deriveds lazily re-evaluated on read.
- **`$effect`** — side-effect runner. Auto-tracks synchronous reads. Runs post-mount, re-runs on dep change. Return function for teardown. `$effect.pre` runs before DOM update. `$effect.root` creates non-tracked scope for effects outside component init. **Never use to sync state** — use `$derived` instead.
- **`$props`** — component inputs via destructuring. Fallbacks, renaming, rest spread. `$props.id()` for unique instance IDs (5.20+).
- **`$bindable`** — marks prop for two-way binding.
- **`$inspect`** — dev-only reactive logging. `.trace()` shows which dep caused re-run.
- **`$host`** — access host element in custom element components.

State is pass-by-value. To retain reactivity across function boundaries, pass state via proxy properties or getter/setter objects — not destructured primitives.

## Component Model

- `.svelte` files: `<script>`, `<script module>` (shared across instances), `<style>` (scoped), markup
- `.svelte.js/.ts` files can use runes for shared reactive logic
- Cannot export reassigned `$state` from `.svelte.js` modules — wrap in object or use getter functions
- Classes can use `$state` in fields; compiler generates get/set on prototype

## Template Syntax

| Syntax | Purpose |
|--------|---------|
| `{#if}/{:else if}/{:else}` | Conditional rendering |
| `{#each items as item (key)}` | List rendering. Keyed preferred. |
| `{#key expression}` | Re-render block on value change |
| `{#await promise}` | Async rendering |
| `{#snippet name(args)}` | Reusable template blocks (replaces slots) |
| `{@render snippet(args)}` | Render a snippet |
| `{@html expr}` | Raw HTML injection (no sanitization) |
| `{@attach fn}` | Element-level effect (replaces `use:`) |
| `{@const val = expr}` | Block-scoped constant |
| `{@debug vars}` | Dev breakpoint (comma-separated variable names) |

## Bindings

- `bind:value`, `bind:checked`, `bind:group` — form elements
- `bind:this` — DOM/component reference
- `bind:` on components requires `$bindable` prop
- Function bindings: `bind:value={[get, set]}` for validation (5.9+)

## Special Elements

- `<svelte:boundary>` — error/async boundary with `pending`, `failed`, `onerror`
- `<svelte:window>`, `<svelte:document>`, `<svelte:body>` — global listeners with auto-cleanup
- `<svelte:head>` — inject into document head
- `<svelte:element this={tag}>` — dynamic element
- `<svelte:options>` — per-component compiler options (runes, namespace, customElement, css)

## Styling

- Scoped by default (hash class). `:global(...)` to escape.
- CSS custom properties pass to children: `<Child --prop="val" />`
- `style:--var={expr}` sets CSS custom properties from JS

## Lifecycle Hooks

- `onMount(callback)` — runs after DOM mount (no SSR). Return function for cleanup.
- `onDestroy(callback)` — runs before unmount (also runs on server).
- `tick()` — resolves after pending state changes applied.

## Imperative API

- `mount(Component, { target, props })` — create and mount component. Async.
- `unmount(component)` — destroy mounted component.
- `render(Component, { props })` — SSR, returns `{ body, head }`.
- `hydrate(Component, { target, props })` — hydrate SSR HTML.

`svelte/store`: `writable`, `readable`, `derived`, `readonly`. Svelte 5 best practice: prefer classes with `$state` fields over stores.

## Context API

- `setContext(key, value)` / `getContext(key)` — scoped to component subtree
- `createContext<T>()` (5.40+) — type-safe alternative returning `[get, set]`
- Prefer over shared module state (prevents SSR leaks)

## Key Principles

1. `$derived` for computed state, never `$effect`
2. `$state.raw` for large non-mutated data
3. Event handlers for user interaction, `$effect` only for external sync
4. Keyed `{#each}` with unique keys
5. Snippets over slots, `onclick` over `on:click`
6. Context over global module state

## See Also

- [[sveltekit]]
- [[svelte-llms]]
- [[svelte-component-patterns]]
- [[bits-ui]]
