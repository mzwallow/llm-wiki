# libwayland-server API

**Source:** [Server API](https://wayland.freedesktop.org/docs/html/apc.html)
**Added:** 2026-04-25

## Overview
This document details the C API for `libwayland-server`, the reference implementation of the server side of the Wayland protocol. Its main responsibility is to handle Inter-process communication (IPC), marshalling, and message synchronization.

## Key Concepts
- **`wl_client`**: Represents an open socket connection to a specific client.
- **`wl_resource`**: Represents a client-created protocol object on the server side.
- **`wl_global`**: Represents a global object created by the server, available for clients to bind.
- **`wl_argument`**: A union type representing all possible argument types in the Wayland protocol wire format.
- **`wl_array`**: A dynamic array implementation used internally for handling variable-sized allocations.

## See Also
- [[libwayland]]
- [[wayland-protocol]]