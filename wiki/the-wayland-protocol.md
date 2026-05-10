# The Wayland Protocol (Drew DeVault)

**Source:** [The Wayland Protocol](https://wayland-book.com/print.html)
**Added:** 2026-05-10

## Overview
A comprehensive guide to Wayland by Drew DeVault, focusing on the mental model, design rationale, and the wire protocol. It provides a more developer-centric view compared to the official documentation.

## Key Concepts

### High-Level Design
- **Compositor:** Manages input and output; dispatches events to clients.
- **Client:** Renders windows and handles its own application logic.

### Wire Protocol Basics
- **Asynchronous & Binary:** Communication over Unix domain sockets.
- **Message-Based:** Messages are the fundamental unit of communication.
- **Object IDs:** Every object has a unique ID used in the wire protocol.

### Key Abstractions
- **Registry:** A special global object used to discover other globals.
- **Globals:** Interfaces advertised by the server (e.g., `wl_compositor`).
- **Proxies (Client-side):** Objects on the client that represent server-side resources.
- **Resources (Server-side):** Objects on the server that represent client-side proxies.

### Protocol Patterns
- **Atomicity:** Mechanisms for grouping state changes to avoid partial updates.
- **Versioning:** How interfaces evolve over time while maintaining compatibility.

### Key Interfaces
- **XDG Shell:** Standardizes application window management (top-levels, popups).
- **Seats:** Abstraction for a group of input devices (keyboard, pointer, touch).
- **Buffers & Surfaces:** Mechanisms for getting pixels onto the screen (SHM, dmabuf).

## See Also
- [[wayland]]
- [[wayland-protocol]]
- [[wayland-book]]
- [[libwayland]]
