# Wayland Book Summary

**Source:** [Wayland Book](https://wayland.freedesktop.org/docs/book/print.html)
**Added:** 2026-04-25

## Overview
The Wayland Book provides a comprehensive guide to the Wayland architecture and protocol. Wayland is a display server protocol that replaces the traditional X Window System (X11) by eliminating the X server as a middleman. 

## Key Concepts

- **Architecture:** The Wayland compositor acts as the display server. It receives input directly from the kernel (evdev) and passes it to clients. Clients render their own window contents into shared memory buffers (using EGL, Vulkan, etc.) and send a damage request to the compositor, which then composites the screen and schedules a pageflip.
- **Protocol:** An asynchronous, object-oriented, message-based protocol running over UNIX domain sockets. Interfaces (e.g., `wl_compositor`, `wl_surface`, `wl_seat`, `wl_output`) define requests (client to server) and events (server to client). 
- **X11 Support (Xwayland):** To support legacy X11 apps, compositors run Xwayland, which is an X server that acts as a Wayland client. The Wayland compositor also runs an X Window Manager (XWM) to bridge window management, allowing rootless X11 windows to mix seamlessly with native Wayland windows.
- **Content Updates:** Mechanism for applying double-buffered state changes to surfaces and subsurfaces. Subsurfaces can be synchronized (applied atomically with the parent) or desynchronized.
- **Color Management:** Wayland shifts color management responsibility to the compositor. Protocols like `color-management` (for colorimetry, HDR, ICC profiles) and `color-representation` (for YCbCr-RGB conversion) allow clients to tag surfaces with metadata, enabling optimal and power-efficient display output.

## See Also
- [[wayland]]
- [[wayland-protocol]]
- [[xwayland]]