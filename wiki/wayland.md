# Wayland

Wayland is a modern display server protocol and architecture intended to replace the X Window System on Linux and Unix-like operating systems.

## Architecture
Unlike X11, where the X server acts as a middleman for both input and rendering, Wayland simplifies the graphics stack. The **Wayland compositor** is the display server itself.
- **Input:** The kernel sends input events to the compositor, which transforms coordinates and forwards events directly to the target client.
- **Rendering:** Clients render directly into shared memory buffers using libraries like EGL or Vulkan. They then pass a reference (like a dma-buf FD) to the compositor and notify it of updated regions (damage). The compositor composites these buffers and displays them.

## Protocol
The Wayland protocol is asynchronous and object-oriented. Communication happens over a UNIX domain socket. Objects implement specific interfaces defined in XML (like `wl_compositor`, `wl_surface`, `wl_seat`).

## See Also
- [[wayland-protocol]]
- [[xwayland]]
- [[wayland-book]]
- [[libwayland]]