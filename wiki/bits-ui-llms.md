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
- [[svelte]]
- [[svelte-llms]]
