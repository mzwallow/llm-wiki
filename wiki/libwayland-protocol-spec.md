# Wayland Protocol Specification

**Source:** [Protocol Specification](https://wayland.freedesktop.org/docs/html/apa.html)
**Added:** 2026-04-25

## Overview
This document defines the core interfaces and messages (requests and events) that make up the Wayland protocol, generated directly from the protocol XML files.

## Key Interfaces
- **`wl_display`**: The core global object. Provides the `sync` request for asynchronous roundtrips and the `get_registry` request to discover other globals. Emits `error` and `delete_id` events.
- **`wl_registry`**: The global registry object. Emits `global` and `global_remove` events to announce the presence or removal of global objects (like inputs and outputs). Clients use the `bind` request to connect to these globals.
- **`wl_callback`**: An object used to notify clients when a specific request is done, typically used with `wl_display.sync`.
- **`wl_compositor`**: The singleton global responsible for combining the contents of multiple surfaces into one displayable output. Provides the `create_surface` request.

## See Also
- [[wayland]]
- [[wayland-protocol]]
- [[libwayland]]