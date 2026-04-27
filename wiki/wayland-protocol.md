# Wayland Protocol

The Wayland protocol defines how clients and the compositor communicate.

## Characteristics
- **Asynchronous & Object-Oriented:** Requests (client-to-server) and events (server-to-client) are invoked on objects.
- **Message-based:** Messages contain a header (object ID, size, opcode) and typed arguments (integers, strings, object IDs, file descriptors).
- **XML Definition:** The core protocol is defined in `wayland.xml`. This XML is used to generate C headers and language bindings.
- **Versioning:** Interfaces are versioned. A global interface's version dictates the version of its child objects.

## Key Interfaces
- `wl_compositor`: The core global object used to create surfaces.
- `wl_surface`: Represents a rectangular grid of pixels (a window or part of one).
- `wl_seat`: Represents a group of input devices (keyboard, pointer, touch).
- `wl_output`: Represents a physical monitor/display.

## See Also
- [[wayland]]
- [[wayland-book]]
- [[libwayland-protocol-spec]]
- [[libwayland]]
- [[xwayland]]