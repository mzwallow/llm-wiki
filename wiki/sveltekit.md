# SvelteKit

## What It Is

SvelteKit is the official application framework for Svelte. Handles routing, SSR, data loading, form handling, and deployment. Built on Vite. Analogous to Next.js (React) or Nuxt (Vue).

## Routing

File-based router in `src/routes/`. Files prefixed with `+`:

| File | Purpose |
|------|---------|
| `+page.svelte` | Page UI component |
| `+page.js` | Universal load function (server + client) |
| `+page.server.js` | Server-only load, form actions |
| `+layout.svelte` | Shared UI wrapper (nav, footer) |
| `+layout.js` / `+layout.server.js` | Shared data for child routes |
| `+error.svelte` | Error boundary for route subtree |
| `+server.js` | API endpoints (export `GET`, `POST`, etc.) |

- Dynamic segments: `[param]`, rest params `[...slug]`
- Route groups: `(group)` — organizes without affecting URL
- Layouts nest. `+error.svelte` renders at nearest error boundary level.
- Navigation uses standard `<a>` tags (no `<Link>` component).

## Loading Data

**Server loads** (`+page.server.js`): access database, private env, cookies. Output must be devalue-serializable.

**Universal loads** (`+page.js`): run on both server and client. Can return non-serializable values (component constructors, class instances).

Both receive: `params`, `url`, `fetch`, `depends`, `parent`, `setHeaders`. Server-only: `cookies`, `locals`, `clientAddress`, `request`.

- Parallel execution by default (no waterfall between sibling loads)
- Streaming supported (skeleton UI while data resolves)
- Invalidation: `invalidate(url)`, `invalidateAll()`, `depends()` markers

## Form Actions

Export `actions` from `+page.server.js`:

```js
export const actions = {
  default: async ({ request, cookies }) => { /* ... */ },
  create: async ({ request }) => { /* ... */ }
};
```

- `fail(status, data)` returns validation errors
- `redirect()` for post-action navigation
- `use:enhance` from `$app/forms` for progressive enhancement (no full-page reload)
- Works without JavaScript (native form submission fallback)

## Page Options

Exported from any `+page` or `+layout` file. Children override parents:

- **`ssr`** (default `true`) — server render HTML
- **`csr`** (default `true`) — ship JavaScript, hydrate
- **`prerender`** (`true`/`false`/`'auto'`) — static generation at build time
- **`trailingSlash`** — enforce or ignore trailing slashes

## Hooks

Middleware functions in `src/hooks.server.js`, `src/hooks.client.js`, or `src/hooks.js`:

| Hook | Purpose |
|------|---------|
| `handle({ event, resolve })` | Every server request. Populate `event.locals`, modify response. Chain with `sequence()`. |
| `handleFetch({ event, request, fetch })` | Intercept server-side fetch calls. Rewrite URLs, forward cookies. |
| `handleError({ error, event })` | Log unexpected errors. Returns sanitized error for UI. |
| `reroute({ url })` | Map URL to different route before routing. |
| `init()` | Runs once at app startup. Async init (DB connections). |

## Adapters

Deploy targets control how the app is built:

- `adapter-auto` — auto-detects platform (default)
- `adapter-node` — Node.js server, Docker, VPS
- `adapter-static` — fully static site (SSG)
- `adapter-vercel`, `adapter-netlify`, `adapter-cloudflare` — platform-specific

## Project Structure

```
src/
  lib/          # shared code ($lib alias)
    server/     # server-only ($lib/server)
  routes/       # file-based routing
  params/       # param matchers
  app.html      # page template
  hooks.server.js / hooks.client.js
static/         # unprocessed assets
```

## Key Modules

- `$app/environment` — `browser`, `dev`, `building`, `version`
- `$app/forms` — `enhance`, `applyAction`, `deserialize`
- `$app/navigation` — `goto`, `pushState`, `replaceState`, `invalidate`
- `$app/state` — `page` (reactive page state: `url`, `params`, `data`, `form`, `status`)
- `$app/stores` — legacy store-based page state
- `$env/static/private`, `$env/static/public` — build-time env vars
- `$env/dynamic/private`, `$env/dynamic/public` — runtime env vars

## Error Handling

- `error(status, body)` — expected errors (404, 403). Renders `+error.svelte`.
- Unexpected errors — message hidden from users, logged via `handleError`.
- `<svelte:boundary>` for component-level error catching.

## See Also

- [[svelte]]
- [[svelte-llms]]
- [[svelte-component-patterns]]
