# Wiki Log

## [2026-05-02] ingest | Zig Build System
- Ingested `raw/zig/build-system.md`.
- Created [[zig-build-system]].
- Updated [[zig-language]] and [[index.md]].

## [2026-05-02] lint | Comprehensive cross-reference audit
- Completed exhaustive cross-linking of OpenWrt, Wayland, and Svelte clusters.
- Verified that all pages in `wiki/` are registered in `index.md`.
- Fixed missing `See Also` links in `openwrt-raspberry-pi.md`, `libwayland.md`, `xwayland.md`, and all `libwayland-*` pages.
- Verified Zig cluster integrity after 0.16.0 ingestion.

## [2026-05-02] ingest | Tailscale on OpenWrt
- Ingested `raw/openwrt/tailscale.md`.
- Created [[openwrt-tailscale]].
- Updated [[openwrt]] and [[index.md]].

## [2026-05-01] ingest | Zig 0.16.0 Release Notes
- Ingested `raw/zig/0.16.0-release-notes.md`.
- Created [[zig-0.16.0-release-notes]].
- Updated [[zig-language]] with 0.16.0 highlights.
- Updated [[index.md]].

## [2026-04-25] ingest | Wayland Book
Ingested `raw/wayland/book.md`. Created summary page `wayland-book.md` and concept pages for `wayland`, `wayland-protocol`, and `xwayland`. Updated `index.md`.

## [2026-04-25] ingest | Zig 0.16.0 Documentation
Ingested `raw/zig/0.16.0-doc.md`. Created summary page `zig-0.16.0-doc.md` and concept page `zig-language.md`. Updated `index.md`. Ran `qmd embed`.

## [2026-04-25] ingest | libwayland sources
Ingested `raw/wayland/libwayland-server.md`, `raw/wayland/libwayland-client.md`, and `raw/wayland/libwayland-protocol.md`. Created summary pages for each, and a concept page `libwayland.md`. Updated `index.md`. Ran `qmd embed`.

## [2026-04-25] lint | Wiki Health Check
Checked for orphan pages and missing cross-references. Added missing `See Also` links to `wayland-book.md`, `wayland-protocol.md`, and `wayland.md` to connect the newly ingested libwayland pages and fix orphan relationships. Ran `qmd embed`.

## [2026-04-27] ingest | Bits UI LLM Documentation
Ingested `raw/svelte/bits-ui-llms.md`. Created summary page `bits-ui-llms.md` and concept pages for `bits-ui` and `svelte-component-patterns`. Updated `index.md`. Ran `qmd embed`.

## [2026-04-28] lint | Wiki integrity check and link fixes
Checked for contradictions, missing cross-references, and data gaps across all pages. Fixed: `wl_compositor` contradiction in `libwayland-protocol-spec.md`. Added cross-references to Wayland cluster (`xwayland`, `wayland`, `wayland-book`, `wayland-protocol`, `libwayland-client`, `libwayland-server`, `libwayland-protocol-spec`). Added cross-references to Svelte cluster (`bits-ui`, `bits-ui-llms`). Filled gaps in `svelte.md`: added `$host`, `$props.id()`, `$effect.root`, `$effect.pre`, `{@debug}`, `<svelte:options>`, lifecycle hooks, imperative API.

## [2026-04-28] ingest | Svelte Full Documentation
Ingested `raw/svelte/llms.md` (~36K lines). Created summary page `svelte-llms.md` and concept pages for `svelte` (framework/runes/reactivity) and `sveltekit` (routing/loading/forms/hooks/adapters). Updated `index.md` and cross-references on `svelte-component-patterns.md`.

## [2026-04-28] lint | Verification pass after external lint tool usage
Verified cross-references and content consistency after bulk Svelte ingestion.

## [2026-04-30] ingest | OpenWrt Wireless
- Created [[openwrt-wireless]] from `raw/openwrt/wifi.md`.
- Updated [[openwrt]] and [[index.md]].

## [2026-04-30] ingest | OpenWrt SQM
- Created [[openwrt-sqm]] from `raw/openwrt/sqm.md`.
- Updated [[openwrt]] and [[index.md]].

## [2026-04-29] ingest | OpenWrt Raspberry Pi
Ingested `raw/openwrt/rasppi.md`. Created summary page `openwrt-raspberry-pi.md` and updated `index.md` with `openwrt` and `raspberry-pi` concepts.
