# Ingest The Wayland Protocol Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ingest Drew DeVault's "The Wayland Protocol" summary into the wiki, update indexes, and refresh search.

**Architecture:** Standard ingestion workflow as per `GEMINI.md`.

**Tech Stack:** Markdown, QMD CLI.

---

### Task 1: Create Summary Page

**Files:**
- Create: `wiki/the-wayland-protocol.md`

- [ ] **Step 1: Write the summary content**

Write the following to `wiki/the-wayland-protocol.md`:

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
Expected: File exists with correct permissions.

---

### Task 2: Update Index and Log

**Files:**
- Modify: `index.md`
- Modify: `log.md`

- [ ] **Step 1: Add to index.md**

Add `[[the-wayland-protocol]]: Drew DeVault's guide to the Wayland protocol.` to the `Sources` section of `index.md`.

- [ ] **Step 2: Add to log.md**

Add the following entry to `log.md`:

```markdown
## [2026-05-10] ingest | The Wayland Protocol (Drew DeVault)
- Ingested `raw/wayland/wayland-book.md`.
- Created [[the-wayland-protocol]].
- Updated [[index.md]].
```

- [ ] **Step 3: Verify updates**

Run: `grep "the-wayland-protocol" index.md log.md`
Expected: Both files contain the reference.

---

### Task 3: Refresh Search Index

- [ ] **Step 1: Run embedding command**

Run: `bunx @tobilu/qmd embed`
Expected: Command completes successfully, updating the local search index.

- [ ] **Step 2: Verify search (Optional but recommended)**

Run: `bunx @tobilu/qmd search "Drew DeVault"`
Expected: `wiki/the-wayland-protocol.md` appears in search results.
