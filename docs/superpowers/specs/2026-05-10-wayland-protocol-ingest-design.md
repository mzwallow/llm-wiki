# Design Spec: Ingest "The Wayland Protocol" by Drew DeVault

## Overview
Ingest `raw/wayland/wayland-book.md` into the wiki as a new source summary and update related concept pages.

## Proposed Changes

### 1. New Wiki Page: `wiki/the-wayland-protocol.md`
- **Title:** The Wayland Protocol (Drew DeVault)
- **Content:**
    - High-level design summary (Compositor vs Client).
    - Wire protocol details (asynchronous, binary, message-based).
    - Key abstractions (Globals, Registry, Proxies vs Resources).
    - Protocol patterns (Atomicity, Versioning).
    - Interface summaries (XDG Shell, Input/Seats, Buffers/SHM).

### 2. Update `wiki/wayland.md`
- Incorporate details on the wire protocol (binary format over Unix socket).
- Add mention of "Proxies" (client-side) and "Resources" (server-side) as fundamental abstractions.
- Expand on the "asynchronous" nature of the protocol.

### 3. Update `wiki/index.md`
- Register `the-wayland-protocol` under a new "Books" or "Sources" section.

### 4. Update `wiki/log.md`
- Record the ingestion.

## Success Criteria
- `the-wayland-protocol.md` exists and summarizes the new source.
- `wayland.md` has deeper technical detail from the new source.
- All links are valid.
- Search index is updated.
