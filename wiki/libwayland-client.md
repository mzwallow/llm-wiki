# libwayland-client API

**Source:** [Client API](https://wayland.freedesktop.org/docs/html/apb.html)
**Added:** 2026-04-25

## Overview
This document details the C API for `libwayland-client`, the reference implementation used by applications to communicate with a Wayland server.

## Key Concepts
- **`wl_display`**: The core object representing the client's connection to the compositor. Handles reading and writing data to the UNIX domain socket.
- **`wl_event_queue`**: Holds events received from the server until they are dispatched. Multi-threading is supported by using multiple event queues.
- **`wl_proxy`**: The client-side representation of a protocol object. It holds the object ID, client data pointer, and a pointer to the `wl_interface`.
- **Marshalling & Dispatching**: 
  - Requests are sent using `wl_proxy_marshal()`.
  - Events are handled by calling a dispatcher callback stored in the `wl_proxy`.

## See Also
- [[wayland]]
- [[wayland-protocol]]
- [[wayland-book]]
- [[xwayland]]
- [[libwayland]]
- [[libwayland-server]]
- [[libwayland-protocol-spec]]