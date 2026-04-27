# Svelte Component Patterns

## Overview
The Bits UI documentation highlights several Svelte patterns for building composable, accessible components. These patterns are useful beyond Bits UI because they describe how consumers customize rendered elements, state, styling, and mounted content.

## Patterns
- **Child snippets:** Let consumers replace or customize rendered markup while preserving component behavior and props.
- **Refs:** Expose underlying DOM elements to consumers when direct element access is needed.
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
