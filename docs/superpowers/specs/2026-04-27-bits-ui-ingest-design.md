# Bits UI Source Ingest Design

## Goal
Ingest `raw/svelte/bits-ui-llms.md` into the wiki as a useful, searchable summary without creating a page for every documented component.

## Source
- Path: `raw/svelte/bits-ui-llms.md`
- Scope: LLM-friendly Bits UI/Svelte component documentation.
- Size: Large source, roughly 24k lines.

## Approach
Use a balanced ingest:
- Create one source summary page: `wiki/bits-ui-llms.md`.
- Create one product/concept page: `wiki/bits-ui.md`.
- Create one reusable patterns page: `wiki/svelte-component-patterns.md`.
- Update `wiki/index.md` with the new source and concepts.
- Append an ingest entry to `wiki/log.md`.
- Run `bunx @tobilu/qmd embed` after edits.

## Page Responsibilities
`wiki/bits-ui-llms.md` summarizes the source document: what Bits UI covers, major documentation areas, component families, styling, state management, accessibility, and Svelte-specific patterns.

`wiki/bits-ui.md` explains Bits UI as a headless Svelte component library: purpose, design model, accessibility focus, styling approach, and relationship to Svelte.

`wiki/svelte-component-patterns.md` captures reusable patterns that are broader than Bits UI: child snippets, refs, two-way binding, function binding, mount/transition behavior, data attributes, and component composition.

## Non-Goals
- No component-by-component wiki page generation in this pass.
- No restructuring existing Wayland or Zig pages.
- No broad style cleanup outside touched wiki pages.

## Success Criteria
- New pages are concise and match existing wiki style.
- `wiki/index.md` links all new pages.
- `wiki/log.md` records the ingest.
- Search index update command completes or failure is reported.
