# libwayland

`libwayland` is the open-source C reference implementation of the Wayland protocol. It is split into two libraries:

1. **`libwayland-server`**: Used by compositors to implement the server side of the Wayland IPC. Manages client connections, resources, and globals.
2. **`libwayland-client`**: Used by applications and toolkits to connect to a Wayland compositor. Manages proxies, event queues, and the display connection.

Both libraries handle the low-level details of marshalling/unmarshalling messages over UNIX domain sockets based on the XML protocol specifications.

## Documentation
- [[libwayland-server]]: Server API documentation.
- [[libwayland-client]]: Client API documentation.
- [[libwayland-protocol-spec]]: Core protocol interface specifications.

## See Also
- [[wayland]]
- [[wayland-protocol]]