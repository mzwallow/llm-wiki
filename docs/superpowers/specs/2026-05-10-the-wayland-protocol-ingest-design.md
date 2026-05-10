# Design: Ingest The Wayland Protocol (Drew DeVault)

**Date:** 2026-05-10
**Topic:** Ingesting Drew DeVault's "The Wayland Protocol" into the LLM Wiki.

## Overview
Ingest the summary of Drew DeVault's book "The Wayland Protocol" from `raw/wayland/wayland-book.md` into the `wiki/` directory. This source provides a developer-centric mental model of Wayland, complementing the official Wayland Book already in the wiki.

## Architecture & Components

### 1. Summary Page (`wiki/the-wayland-protocol.md`)
- Create a new summary page based on the provided content.
- Ensure cross-references to `wayland`, `wayland-protocol`, `wayland-book` (official), and `libwayland`.

### 2. Catalog Update (`index.md`)
- Register the new source in the `Sources` section.

### 3. Chronological Log (`log.md`)
- Record the ingestion activity.

### 4. Search Index Update
- Use `qmd` tools to re-embed the wiki content.

## Data Flow
1. **Source:** `raw/wayland/wayland-book.md` (read for context, though content is provided).
2. **Output:** `wiki/the-wayland-protocol.md`.
3. **Side Effects:** Updates to `index.md`, `log.md`, and the QMD search index.

## Success Criteria
- `wiki/the-wayland-protocol.md` exists and contains the summary.
- `index.md` links to the new page.
- `log.md` has an entry for 2026-05-10.
- `bunx @tobilu/qmd embed` runs successfully.
