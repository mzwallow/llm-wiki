# Wayland Protocol Ingestion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ingest Drew DeVault's "The Wayland Protocol" as a new wiki source and update core Wayland documentation.

**Architecture:** Create a detailed summary page for the new source, then surgically update the core `wayland.md` concept page with technical details missing from the Freedesktop source. Update discovery files (`index.md`, `log.md`).

**Tech Stack:** Markdown, Bun (for qmd embedding).

---

### Task 1: Create The Wayland Protocol Summary

**Files:**
- Create: `wiki/the-wayland-protocol.md`

- [ ] **Step 1: Write the summary content**

```markdown
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
```

- [ ] **Step 2: Verify the file exists**

Run: `ls -l wiki/the-wayland-protocol.md`

### Task 2: Update Wayland Concept Page

**Files:**
- Modify: `wiki/wayland.md`

- [ ] **Step 1: Enhance architecture and protocol sections**

```markdown
# Wayland

Wayland is a modern display server protocol and architecture intended to replace the X Window System on Linux and Unix-like operating systems.

## Architecture
Unlike X11, where the X server acts as a middleman for both input and rendering, Wayland simplifies the graphics stack. The **Wayland compositor** is the display server itself.
- **Input:** The kernel sends input events to the compositor, which transforms coordinates and forwards events directly to the target client.
- **Rendering:** Clients render directly into shared memory buffers using libraries like EGL or Vulkan. They then pass a reference (like a dma-buf FD) to the compositor and notify it of updated regions (damage). The compositor composites these buffers and displays them.

### Key Abstractions
Fundamental to the Wayland model are **Proxies** (client-side) and **Resources** (server-side). A proxy on the client represents a resource on the server, and messages are exchanged between them to synchronize state.

## Protocol
The Wayland protocol is an **asynchronous, binary, message-based** protocol running over a UNIX domain socket. 
- **Object-Oriented:** Communication centers around objects that implement specific interfaces defined in XML (like `wl_compositor`, `wl_surface`, `wl_seat`).
- **Atomic Updates:** Changes to surface state are often double-buffered, allowing clients to prepare a complete state change before committing it atomically.

## See Also
- [[the-wayland-protocol]]
- [[wayland-protocol]]
- [[xwayland]]
- [[wayland-book]]
- [[libwayland]]
- [[libwayland-server]]
- [[libwayland-client]]
- [[libwayland-protocol-spec]]
```

### Task 3: Update Discovery and Logs

**Files:**
- Modify: `wiki/index.md`
- Modify: `wiki/log.md`

- [ ] **Step 1: Add to index.md**

Find the Wayland section and add `[[the-wayland-protocol]]`.

- [ ] **Step 2: Add to log.md**

```markdown
## [2026-05-10] ingest | The Wayland Protocol (Drew DeVault)
- Ingested `raw/wayland/wayland-book.md`.
- Created [[the-wayland-protocol]].
- Updated [[wayland]] and [[index.md]].
```

### Task 4: Re-index Wiki

- [ ] **Step 1: Run qmd embed**

Run: `bunx @tobilu/qmd embed`
