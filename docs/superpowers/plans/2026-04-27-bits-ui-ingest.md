# Bits UI Source Ingest Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ingest `raw/svelte/bits-ui-llms.md` into the wiki as one source summary plus two concept pages.

**Architecture:** Follow the existing wiki pattern: concise markdown pages under `wiki/`, backlinks through `See Also`, catalog entries in `wiki/index.md`, and an append-only entry in `wiki/log.md`. Keep the first pass balanced: summarize source-wide knowledge and reusable concepts, not every component.

**Tech Stack:** Markdown wiki files, Obsidian-style `[[links]]`, `bunx @tobilu/qmd embed` for index refresh.

---

## File Map

- Create: `wiki/bits-ui-llms.md` source summary for `raw/svelte/bits-ui-llms.md`.
- Create: `wiki/bits-ui.md` concept page for Bits UI.
- Create: `wiki/svelte-component-patterns.md` concept page for reusable Svelte/Bits UI authoring patterns.
- Modify: `wiki/index.md` to add one source and two concepts.
- Modify: `wiki/log.md` to append the ingest entry.

## Task 1: Create Source Summary Page

**Files:**
- Create: `wiki/bits-ui-llms.md`
- Read: `raw/svelte/bits-ui-llms.md`

- [ ] **Step 1: Inspect the source headers for coverage**

Run:
```bash
rg '^# |^## ' raw/svelte/bits-ui-llms.md
```

Expected: output includes introduction, child snippets, dates and times, getting started, refs, state management, styling, transitions, and component documentation sections such as accordion.

- [ ] **Step 2: Create `wiki/bits-ui-llms.md`**

Write this file:
```markdown
# Bits UI LLM Documentation

**Source:** [Bits UI LLM Documentation](../raw/svelte/bits-ui-llms.md)
**Added:** 2026-04-27

## Overview
This source is the LLM-friendly documentation bundle for Bits UI, a headless component library for Svelte. It combines introductory material, installation guidance, authoring patterns, styling guidance, accessibility-focused primitives, and reference material for many component families.

## Major Areas Covered
- **Core Bits UI model:** Headless components that provide behavior, accessibility, state attributes, and composition hooks while leaving visual styling to the application.
- **Svelte integration patterns:** Child snippets, refs, two-way binding, function binding, transitions, and reusable component composition patterns.
- **Styling:** Bring-your-own-styles workflows using CSS frameworks, data attributes, global classes, scoped styles, style props, CSS variables, and animation hooks.
- **State and accessibility:** Controlled and uncontrolled state patterns, keyboard interactions, ARIA behavior, focus management, and production-ready accessibility defaults.
- **Date and time utilities:** `CalendarDate`, `CalendarDateTime`, `ZonedDateTime`, ranges, placeholders, formatting, parsing, and date value updates.
- **Component documentation:** Reference sections for interactive UI primitives such as accordion and many other Bits UI components.

## Practical Takeaways
- Bits UI is useful when an application needs accessible component behavior without adopting a fixed design system.
- Styling is primarily driven by data attributes, CSS variables, classes, and framework-specific utility classes.
- Child snippets and refs are central extension points for replacing rendered elements or integrating custom markup.
- Floating, mounted, or transition-managed components often need specific wrapper structure so transitions and positioning work correctly.
- Many components expose state through data attributes, making behavior and visual state easy to connect in CSS.

## See Also
- [[bits-ui]]
- [[svelte-component-patterns]]
```

- [ ] **Step 3: Verify page format**

Run:
```bash
test -f wiki/bits-ui-llms.md && rg '\[\[bits-ui\]\]|\[\[svelte-component-patterns\]\]' wiki/bits-ui-llms.md
```

Expected: command succeeds and prints both `See Also` links.

## Task 2: Create Bits UI Concept Page

**Files:**
- Create: `wiki/bits-ui.md`
- Read: `raw/svelte/bits-ui-llms.md`

- [ ] **Step 1: Review introduction and getting started source sections**

Run:
```bash
rg -n '^# Introduction Documentation|^## Why Bits UI\?|^# Getting Started Documentation|^## Adding Styles|^# Styling Documentation' raw/svelte/bits-ui-llms.md
```

Expected: output points to the sections used for product overview, installation, and styling model.

- [ ] **Step 2: Create `wiki/bits-ui.md`**

Write this file:
```markdown
# Bits UI

## Overview
Bits UI is a headless component library for Svelte. It provides accessible behavior, state management, keyboard interaction, and composable primitives while leaving markup customization and styling decisions to the application.

## Design Model
- **Headless primitives:** Components provide behavior and accessibility instead of fixed visuals.
- **Bring your own styles:** Styling can use TailwindCSS, UnoCSS, custom CSS, scoped styles, data attributes, and CSS variables.
- **Composable APIs:** Child snippets, refs, and prop forwarding let applications customize rendered elements without discarding built-in behavior.
- **Accessibility defaults:** Components are designed around ARIA behavior, focus management, keyboard interaction, and production UI expectations.

## When It Fits
Bits UI fits Svelte applications that need robust interactive components but already have their own visual design system. It is less useful when a project wants a fully styled component kit out of the box.

## See Also
- [[bits-ui-llms]]
- [[svelte-component-patterns]]
```

- [ ] **Step 3: Verify page format**

Run:
```bash
test -f wiki/bits-ui.md && rg '\[\[bits-ui-llms\]\]|\[\[svelte-component-patterns\]\]' wiki/bits-ui.md
```

Expected: command succeeds and prints both `See Also` links.

## Task 3: Create Svelte Component Patterns Concept Page

**Files:**
- Create: `wiki/svelte-component-patterns.md`
- Read: `raw/svelte/bits-ui-llms.md`

- [ ] **Step 1: Review source pattern sections**

Run:
```bash
rg -n '^# Child Snippet Documentation|^# Ref Documentation|^# State Management Documentation|^# Styling Documentation|^# Transitions Documentation' raw/svelte/bits-ui-llms.md
```

Expected: output points to the sections used for reusable Svelte component patterns.

- [ ] **Step 2: Create `wiki/svelte-component-patterns.md`**

Write this file:
```markdown
# Svelte Component Patterns

## Overview
The Bits UI documentation highlights several Svelte patterns for building composable, accessible components. These patterns are useful beyond Bits UI because they describe how consumers customize rendered elements, state, styling, and mounted content.

## Patterns
- **Child snippets:** Let consumers replace or customize rendered markup while preserving component behavior and props.
- **Refs:** Expose DOM elements or component internals to consumers when direct element access is needed.
- **Two-way binding:** Supports controlled state flows where parent components own and react to state changes.
- **Function binding:** Allows custom getter/setter logic around state updates when plain binding is not enough.
- **Data attributes:** Expose component state to CSS, such as open, closed, selected, disabled, or highlighted states.
- **Transitions and force mounting:** Keep elements mounted when animation libraries or Svelte transitions need stable DOM nodes.
- **Floating content wrappers:** Some positioned content needs specific wrapper structure so measurement, positioning, and transitions can cooperate.

## Practical Notes
- Prefer child snippets when customization needs to change element structure.
- Prefer data attributes for styling state instead of duplicating component state in application CSS logic.
- Use forced mounting when exit transitions need an element to remain in the DOM long enough to animate.
- Keep wrapper requirements from floating components intact; removing them can break positioning or transition behavior.

## See Also
- [[bits-ui]]
- [[bits-ui-llms]]
```

- [ ] **Step 3: Verify page format**

Run:
```bash
test -f wiki/svelte-component-patterns.md && rg '\[\[bits-ui\]\]|\[\[bits-ui-llms\]\]' wiki/svelte-component-patterns.md
```

Expected: command succeeds and prints both `See Also` links.

## Task 4: Update Index and Log

**Files:**
- Modify: `wiki/index.md`
- Modify: `wiki/log.md`

- [ ] **Step 1: Update `wiki/index.md`**

Add one source entry under `## Sources` and two concept entries under `## Concepts`:
```markdown
- [[bits-ui-llms]]: Summary of the Bits UI LLM-friendly documentation.
```

```markdown
- [[bits-ui]]: Overview of the Bits UI headless component library for Svelte.
- [[svelte-component-patterns]]: Reusable Svelte component patterns from the Bits UI documentation.
```

- [ ] **Step 2: Update `wiki/log.md`**

Append this entry after the current last entry:
```markdown

## [2026-04-27] ingest | Bits UI LLM Documentation
Ingested `raw/svelte/bits-ui-llms.md`. Created summary page `bits-ui-llms.md` and concept pages for `bits-ui` and `svelte-component-patterns`. Updated `index.md`. Ran `qmd embed`.
```

- [ ] **Step 3: Verify links exist in index and log**

Run:
```bash
rg '\[\[bits-ui-llms\]\]|\[\[bits-ui\]\]|\[\[svelte-component-patterns\]\]' wiki/index.md && rg 'raw/svelte/bits-ui-llms.md|Bits UI LLM Documentation' wiki/log.md
```

Expected: command succeeds and prints the new index and log lines.

## Task 5: Refresh Search Index and Final Verification

**Files:**
- No markdown edits expected unless verification finds a mistake in files created by earlier tasks.

- [ ] **Step 1: Run markdown link verification**

Run:
```bash
for page in wiki/bits-ui-llms.md wiki/bits-ui.md wiki/svelte-component-patterns.md; do test -f "$page" || exit 1; done
```

Expected: command exits successfully with no output.

- [ ] **Step 2: Refresh QMD index**

Run:
```bash
bunx @tobilu/qmd embed
```

Expected: command completes successfully. If `bunx` or network access is unavailable, record the exact error in the final response.

- [ ] **Step 3: Check working tree diff**

Run:
```bash
git diff -- docs/superpowers/specs/2026-04-27-bits-ui-ingest-design.md docs/superpowers/plans/2026-04-27-bits-ui-ingest.md wiki/bits-ui-llms.md wiki/bits-ui.md wiki/svelte-component-patterns.md wiki/index.md wiki/log.md
```

Expected: diff only contains the spec path correction, this plan, three new wiki pages, and index/log updates for Bits UI ingest.

- [ ] **Step 4: Commit only if user explicitly asks**

No commit by default. If the user asks for a commit, run the repository commit protocol and include only relevant files.

## Self-Review

- Spec coverage: source summary, Bits UI concept, Svelte patterns concept, index update, log update, and embed refresh are each covered by tasks.
- Placeholder scan: no `TBD`, `TODO`, or unspecified implementation steps remain.
- Consistency check: all paths use `raw/svelte/bits-ui-llms.md`, `wiki/bits-ui-llms.md`, `wiki/bits-ui.md`, and `wiki/svelte-component-patterns.md`.
