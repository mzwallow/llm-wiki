# Svelte LLM Documentation Summary

**Source:** `raw/svelte/llms.md` — Full developer documentation for Svelte 5 and SvelteKit, fetched from `https://svelte.dev/llms-full.txt`. ~36K lines.

## Structure

The source contains three major sections:
1. **Svelte 5** — language, runes, components, template syntax, compiler API
2. **SvelteKit** — routing, loading, forms, hooks, adapters, configuration
3. **Svelte CLI & AI** — `sv` CLI, MCP tools, code writer rules

## Svelte 5 Highlights

### Runes

Runes are compiler keywords (prefixed `$`) that control reactivity:

| Rune | Purpose |
|------|---------|
| `$state` | Reactive state. Objects/arrays become deep proxies. Use `$state.raw` for non-mutable state, `$state.snapshot` for static copies, `$state.eager` for immediate UI updates. |
| `$derived` | Computed values from reactive state. Side-effect free. Use `$derived.by` for complex functions. Writable since 5.25 (optimistic UI). Push-pull model: dependents notified immediately, deriveds re-evaluate on read. |
| `$effect` | Side-effect runner. Runs after mount, re-runs on dependency change. Return teardown function. Never update state inside. Use `$effect.pre` for pre-DOM, `$effect.root` for non-tracked scopes. |
| `$props` | Component inputs. Destructuring, renaming, rest spread. Fallbacks not reactive. `$props.id()` for unique instance IDs. |
| `$bindable` | Marks a prop as two-way bindable. Parent uses `bind:value`. Supports fallback. |
| `$inspect` | Dev-only reactive `console.log`. `.with(callback)` for custom handler. `.trace()` for dependency tracing. |
| `$host` | Access host element in custom element components. |

### Component Model

- `.svelte` files: `<script>`, `<script module>`, `<style>`, markup (all optional)
- `.svelte.js` / `.svelte.ts` files can use runes (shared reactive logic)
- Components are functions in Svelte 5; use `mount()` / `unmount()` instead of `new`
- Props via `$props()` destructuring (replaces `export let`)

### Template Syntax

- `{#if}`, `{#each}`, `{#key}`, `{#await}` blocks
- `{#snippet}` replaces slots; rendered via `{@render}`
- `{@html}` for raw HTML (XSS risk)
- `{@attach}` (5.29+) replaces `use:` actions
- `{@const}` for block-scoped constants
- `{@debug}` for dev breakpoint

### Bindings & Directives

- `bind:` — two-way data flow (inputs, media, dimensions, `bind:this`, components)
- `transition:` / `in:` / `out:` — enter/leave animations
- `animate:` — reorder animations in keyed `{#each}`
- `style:` — inline style shorthand, CSS custom properties
- `class` / `class:` — dynamic class application (prefer attribute form since 5.16)

### Special Elements

- `<svelte:boundary>` — error handling, async loading states (5.3+)
- `<svelte:window>`, `<svelte:document>`, `<svelte:body>` — global event listeners
- `<svelte:head>` — inject into `<head>`
- `<svelte:element>` — dynamic element via `this={tag}`
- `<svelte:options>` — per-component compiler options

### Styling

- Scoped by default (hash-based class). Global via `:global(...)`.
- CSS custom properties pass to child components: `<Child --color="red" />`
- `style:--var={value}` bridges JS state to CSS custom properties

### Stores & Context

- Stores (`svelte/store`): `writable`, `readable`, `derived`, `readonly`. Prefer classes with `$state` fields in Svelte 5.
- Context: `setContext`/`getContext` or type-safe `createContext` (5.40+). Scoped to component subtree. Prevents SSR global state leaks.

### Lifecycle

- `onMount` — after DOM mount (no SSR). Return cleanup function.
- `onDestroy` — before unmount (runs on server too).
- `tick()` — resolves after pending state changes applied.

## SvelteKit Highlights

### Routing

File-based router in `src/routes/`. Files prefixed with `+`:
- `+page.svelte` — page component
- `+page.js` — universal load function
- `+page.server.js` — server load, form actions
- `+layout.svelte` / `+layout.js` / `+layout.server.js` — shared UI and data
- `+error.svelte` — error boundary
- `+server.js` — API endpoints (HTTP verb exports)

Dynamic params: `[param]`, rest `[...param]`, matchers in `src/params/`. Layout groups via `(group)`.

### Loading Data

- Server loads (`+page.server.js`): database, private env. Output must be devalue-serializable.
- Universal loads (`+page.js`): run server + client. Any values.
- Parallel by default. Streaming supported.
- Invalidation: `invalidate(url)`, `invalidateAll()`, `depends()`, param changes.

### Form Actions

- Export `actions` from `+page.server.js`. Default or named.
- `fail(status, data)` for validation errors.
- `use:enhance` from `$app/forms` for progressive enhancement.

### Page Options

- `ssr`, `csr`, `prerender`, `trailingSlash` — exported from load files.
- Children override parents.

### Hooks

- `handle({ event, resolve })` — middleware for every request
- `handleFetch` — intercept server-side fetch
- `handleError` — unexpected error logging
- `reroute` — URL remapping before routing
- Chain with `sequence()` from `@sveltejs/kit/hooks`

### Adapters

Deploy targets: `adapter-auto` (default), `adapter-node`, `adapter-static`, `adapter-vercel`, `adapter-netlify`, `adapter-cloudflare`.

## Best Practices

- `$derived` over `$effect` for computed state
- `$state.raw` for large non-mutated data
- Context over shared module state
- Keyed `{#each}` with unique keys
- Snippets over slots
- Event handlers (`onclick`) over `$effect` for user interactions
- `{@attach}` over `use:` actions

## See Also

- [[svelte]]
- [[sveltekit]]
- [[svelte-component-patterns]]
- [[bits-ui]]
