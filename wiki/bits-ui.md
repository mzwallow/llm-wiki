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
