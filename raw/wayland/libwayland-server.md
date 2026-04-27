---
title: "Appendix C. Server API"
source: "https://wayland.freedesktop.org/docs/html/apc.html"
author:
published:
created: 2026-04-25
description:
tags:
  - "clippings"
---

## Introduction

The open-source reference implementation of Wayland protocol is split in two C libraries, [libwayland-client](https://wayland.freedesktop.org/docs/html/apb.html "Appendix B. Client API") and libwayland-server. Their main responsibility is to handle the Inter-process communication (*IPC*) with each other, therefore guaranteeing the protocol objects marshaling and messages synchronization.

The server library is designed to work much like libwayland-client, although it is considerably complicated due to the server needing to support multiple versions of the protocol. It is best to learn libwayland-client first.

Each open socket to a client is represented by a [wl\_client](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__client "wl_client"). The equivalent of the [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") that libwayland-client uses to represent an object is [wl\_resource](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__resource "wl_resource") for client-created objects, and [wl\_global](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__global "wl_global") for objects created by the server.

Often a server is also a client for another Wayland server, and thus must link with both libwayland-client and libwayland-server. This produces some type name conflicts (such as the [client wl\_display](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display "wl_display - Represents a connection to the compositor and acts as a proxy to the wl_display singleton object.") and [server wl\_display](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__display "wl_display"), but the duplicate-but-not-the-same types are opaque, and accessed only inside the correct library where it came from. Naturally that means that the program writer needs to always know if a pointer to a wl\_display is for the server or client side and use the corresponding functions.

## wl\_argument - Protocol message argument data types.

This union represents all of the argument types in the Wayland protocol wire format. The protocol implementation uses [wl\_argument](https://wayland.freedesktop.org/docs/html/apc.html#Server-unionwl__argument "wl_argument - Protocol message argument data types.") within its marshalling machinery for dispatching messages between a client and a compositor.

See also: [wl\_message](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__message "wl_message - Protocol message signature.") See also: [wl\_interface](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__interface "wl_interface - Protocol object interface.") See also: Wire Format

i - int

```
int32_t wl_argument::i
```

u - uint

```
uint32_t wl_argument::u
```

f - fixed

```
wl_fixed_t wl_argument::f
```

s - string

```
const char* wl_argument::s
```

o - object

```
struct wl_object* wl_argument::o
```

n - new\_id

```
uint32_t wl_argument::n
```

a - array

```
struct wl_array* wl_argument::a
```

h - fd

```
int32_t wl_argument::h
```

## wl\_array - Dynamic array.

A [wl\_array](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__array "wl_array - Dynamic array.") is a dynamic array that can only grow until released. It is intended for relatively small allocations whose size is variable or not known in advance. While construction of a [wl\_array](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__array "wl_array - Dynamic array.") does not require all elements to be of the same size, [wl\_array\_for\_each()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__array_1ab050f7375dcae916506142763080ed80) does require all elements to have the same type and size.

size - Array size.

```
size_t wl_array::size
```

alloc - Allocated space.

```
size_t wl_array::alloc
```

data - Array data.

```
void* wl_array::data
```

wl\_array\_init - Initializes the array.

```
void wl_array_init(struct wl_array *array)
```

wl\_array\_release - Releases the array data.

```
void wl_array_release(struct wl_array *array)
```

*Note: Leaves the array in an invalid state.*

array

Array whose data is to be released

wl\_array\_add - Increases the size of the array by size bytes.

```
void * wl_array_add(struct wl_array *array, size_t size)
```

array

Array whose size is to be increased

size

Number of bytes to increase the size of the array by

Returns:

A pointer to the beginning of the newly appended space, or NULL when resizing fails.

wl\_array\_copy - Copies the contents of source to array.

```
int wl_array_copy(struct wl_array *array, struct wl_array *source)
```

array

Destination array to copy to

source

Source array to copy from

Returns:

0 on success, or -1 on failure

wl\_array\_for\_each - Iterates over an array.

This macro expresses a for-each iterator for [wl\_array](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__array "wl_array - Dynamic array."). It assigns each element in the array to pos, which can then be referenced in a trailing code block. pos must be a pointer to the array element type, and all array elements must be of the same type and size.

pos

Cursor that each array element will be assigned to

array

Array to iterate over

See also: wl\_list\_for\_each()

## wl\_client

wl\_client\_flush - Flush pending events to the client.

```
void wl_client_flush(struct wl_client *client)
```

Events sent to clients are queued in a buffer and written to the socket later - typically when the compositor has handled all requests and goes back to block in the event loop. This function flushes all queued up events for a client immediately.

wl\_client\_get\_display - Get the display object for the given client.

```
struct wl_display * wl_client_get_display(struct wl_client *client)
```

Returns:

The display object the client is associated with.

wl\_client\_get\_credentials - Return Unix credentials for the client.

```
void wl_client_get_credentials(const struct wl_client *client, pid_t *pid, uid_t *uid, gid_t *gid)
```

client

The display object

pid

Returns the process ID

uid

Returns the user ID

gid

Returns the group ID

This function returns the process ID, the user ID and the group ID for the given client. The credentials come from getsockopt() with SO\_PEERCRED, on the client socket fd. All the pointers can be NULL, if the caller is not interested in a particular ID.

Note, process IDs are subject to race conditions and are not a reliable way to identify a client.

Be aware that for clients that a compositor forks and execs and then connects using socketpair(), this function will return the credentials for the compositor. The credentials for the socketpair are set at creation time in the compositor.

wl\_client\_get\_fd - Get the file descriptor for the client.

```
int wl_client_get_fd(struct wl_client *client)
```

client

The display object

Returns:

The file descriptor to use for the connection

This function returns the file descriptor for the given client.

Be sure to use the file descriptor from the client for inspection only. If the caller does anything to the file descriptor that changes its state, it will likely cause problems.

See also [wl\_client\_get\_credentials()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__client_1a8c09e56c834002cb8b0ee00f808d85e9). It is recommended that you evaluate whether [wl\_client\_get\_credentials()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__client_1a8c09e56c834002cb8b0ee00f808d85e9) can be applied to your use case instead of this function.

If you would like to distinguish just between the client and the compositor itself from the client's request, it can be done by getting the client credentials and by checking the PID of the client and the compositor's PID. Regarding the case in which the socketpair() is being used, you need to be careful. Please note the documentation for [wl\_client\_get\_credentials()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__client_1a8c09e56c834002cb8b0ee00f808d85e9).

This function can be used for a compositor to validate a request from a client if there are additional information provided from the client's file descriptor. For instance, suppose you can get the security contexts from the client's file descriptor. The compositor can validate the client's request with the contexts and make a decision whether it permits or deny it.

wl\_client\_get\_object - Look up an object in the client name space.

```
struct wl_resource * wl_client_get_object(struct wl_client *client, uint32_t id)
```

client

The client object

id

The object id

Returns:

The object or NULL if there is not object for the given ID

This looks up an object in the client object name space by its object ID.

wl\_client\_post\_implementation\_error - Report an internal server error.

```
void wl_client_post_implementation_error(struct wl_client *client, char const *msg,...)
```

client

The client object

msg

A printf-style format string

...

Format string arguments

Report an unspecified internal implementation error and disconnect the client.

wl\_client\_add\_destroy\_listener - Add a listener to be called at the beginning of wl\_client destruction.

```
void wl_client_add_destroy_listener(struct wl_client *client, struct wl_listener *listener)
```

The listener provided will be called when [wl\_client](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__client "wl_client") destroy has begun, before any of that client's resources have been destroyed.

There is no requirement to remove the link of the [wl\_listener](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__listener "wl_listener - A single listener for Wayland signals.") when the signal is emitted.

wl\_client\_add\_destroy\_late\_listener - Add a listener to be called at the end of wl\_client destruction.

```
void wl_client_add_destroy_late_listener(struct wl_client *client, struct wl_listener *listener)
```

The listener provided will be called when [wl\_client](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__client "wl_client") destroy is nearly complete, after all of that client's resources have been destroyed.

There is no requirement to remove the link of the [wl\_listener](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__listener "wl_listener - A single listener for Wayland signals.") when the signal is emitted.

Since: 1.22.0

wl\_client\_get\_link - Get the link by which a client is inserted in the client list.

```
struct wl_list * wl_client_get_link(struct wl_client *client)
```

See also: [wl\_client\_for\_each()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1af1e9ad8dd32ea89265936930cd173ec5) See also: [wl\_display\_get\_client\_list()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1a99b9c187d88633fa5ba86d1424f06d7f) See also: [wl\_client\_from\_link()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__client_1aec831218471327f37b4e1f11b571545d)

wl\_client\_from\_link - Get a wl\_client by its link.

```
struct wl_client * wl_client_from_link(struct wl_list *link)
```

link

The link of a [wl\_client](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__client "wl_client")

See also: [wl\_client\_for\_each()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1af1e9ad8dd32ea89265936930cd173ec5) See also: [wl\_display\_get\_client\_list()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1a99b9c187d88633fa5ba86d1424f06d7f) See also: [wl\_client\_get\_link()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__client_1ade7bddc335d60cb95f9d1bd4fb60d25b)

wl\_client\_add\_resource\_created\_listener - Add a listener for the client's resource creation signal.

```
void wl_client_add_resource_created_listener(struct wl_client *client, struct wl_listener *listener)
```

client

The client object

listener

The listener to be added

When a new resource is created for this client the listener will be notified, carrying the new resource as the data argument.

wl\_client\_for\_each\_resource - Iterate over all the resources of a client.

```
void wl_client_for_each_resource(struct wl_client *client, wl_client_for_each_resource_iterator_func_t iterator, void *user_data)
```

client

The client object

iterator

The iterator function

user\_data

The user data pointer

The function pointed by iterator will be called for each resource owned by the client. The user\_data will be passed as the second argument of the iterator function. If the iterator function returns WL\_ITERATOR\_CONTINUE the iteration will continue, if it returns WL\_ITERATOR\_STOP it will stop.

Creating and destroying resources while iterating is safe, but new resources may or may not be picked up by the iterator.

See also: [wl\_iterator\_result](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-util_8h_1adb093d005a4b7e04111b7e385349cf23)

wl\_client\_set\_max\_buffer\_size - Adjust the maximum size of the client connection buffers.

```
void wl_client_set_max_buffer_size(struct wl_client *client, size_t max_buffer_size)
```

client

The client object

max\_buffer\_size

The maximum size of the connection buffers

The actual size of the connection buffers is a power of two, the requested max\_buffer\_size is therefore rounded up to the nearest power of two value.

Lowering the maximum size may not take effect immediately if the current content of the buffer does not fit within the new size limit.

The minimum buffer size is 4096. The default buffers size can be set using [wl\_display\_set\_default\_max\_buffer\_size()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1a98fcb80ac00cfeba2f4a12fba28e012e).

See also: [wl\_display\_set\_default\_max\_buffer\_size()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1a98fcb80ac00cfeba2f4a12fba28e012e) Since: 1.22.90

## wl\_display

wl\_client\_create - Create a client for the given file descriptor.

```
struct wl_client * wl_client_create(struct wl_display *display, int fd)
```

display

The display object

fd

The file descriptor for the socket to the client

Returns:

The new client object or NULL on failure.

Given a file descriptor corresponding to one end of a socket, this function will create a [wl\_client](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__client "wl_client") struct and add the new client to the compositors client list. At that point, the client is initialized and ready to run, as if the client had connected to the servers listening socket. When the client eventually sends requests to the compositor, the [wl\_client](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__client "wl_client") argument to the request handler will be the [wl\_client](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__client "wl_client") returned from this function.

The other end of the socket can be passed to wl\_display\_connect\_to\_fd() on the client side or used with the WAYLAND\_SOCKET environment variable on the client side.

Listeners added with [wl\_display\_add\_client\_created\_listener()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server_8c_1a8c1cdf513c91fa498c4d9259eae3ed71) will be notified by this function after the client is fully constructed.

On failure this function sets errno accordingly and returns NULL.

On success, the new client object takes the ownership of the file descriptor. On failure, the ownership of the socket endpoint file descriptor is unchanged, it is the responsibility of the caller to perform cleanup, e.g. call close().

wl\_display\_create - Create Wayland display object.

```
struct wl_display * wl_display_create(void)
```

Returns:

The Wayland display object. Null if failed to create

This creates the [wl\_display](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__display "wl_display") object.

wl\_display\_destroy - Destroy Wayland display object.

```
void wl_display_destroy(struct wl_display *display)
```

display

The Wayland display object which should be destroyed.

This function emits the [wl\_display](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__display "wl_display") destroy signal, releases all the sockets added to this display, free's all the globals associated with this display, free's memory of additional shared memory formats and destroy the display object.

See also: [wl\_display\_add\_destroy\_listener](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server_8c_1a9ea24547f07538f2a326c42c7793b937)

wl\_display\_set\_global\_filter - Set a filter function for global objects.

```
void wl_display_set_global_filter(struct wl_display *display, wl_display_global_filter_func_t filter, void *data)
```

display

The Wayland display object.

filter

The global filter function.

data

User data to be associated with the global filter.

Set a filter for the [wl\_display](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__display "wl_display") to advertise or hide global objects to clients. The set filter will be used during [wl\_global](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__global "wl_global") advertisement to determine whether a global object should be advertised to a given client, and during [wl\_global](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__global "wl_global") binding to determine whether a given client should be allowed to bind to a global.

Clients that try to bind to a global that was filtered out will have an error raised.

Setting the filter NULL will result in all globals being advertised to all clients. The default is no filter.

The filter should be installed before any client connects and should always take the same decision given a client and a global. Not doing so will result in inconsistent filtering and broken wl\_registry event sequences.

wl\_display\_get\_serial - Get the current serial number.

```
uint32_t wl_display_get_serial(const struct wl_display *display)
```

This function returns the most recent serial number, but does not increment it.

wl\_display\_next\_serial - Get the next serial number.

```
uint32_t wl_display_next_serial(struct wl_display *display)
```

This function increments the display serial number and returns the new value.

wl\_display\_destroy\_clients - Destroy all clients connected to the display.

```
void wl_display_destroy_clients(struct wl_display *display)
```

This function should be called right before [wl\_display\_destroy()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__display_1acd9ad2e1ca3ffb0ba0f1b77ae616f8ee) to ensure all client resources are closed properly. Destroying a client from within [wl\_display\_destroy\_clients()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__display_1ab50365739904f91579a66f4b054a3ecb) is safe, but creating one will leak resources and raise a warning.

wl\_display\_set\_default\_max\_buffer\_size - Sets the default maximum size for connection buffers of new clients.

```
void wl_display_set_default_max_buffer_size(struct wl_display *display, size_t max_buffer_size)
```

display

The display object

max\_buffer\_size

The default maximum size of the connection buffers

This function sets the default size of the internal connection buffers for new clients. It doesn't change the buffer size for existing [wl\_client](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__client "wl_client").

The connection buffer size of an existing [wl\_client](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__client "wl_client") can be adjusted using [wl\_client\_set\_max\_buffer\_size()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1a72bcbf2d850958f1f27c95d0fbbdc0ed).

The actual size of the connection buffers is a power of two, the requested max\_buffer\_size is therefore rounded up to the nearest power of two value.

The minimum buffer size is 4096.

See also: [wl\_client\_set\_max\_buffer\_size](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1a72bcbf2d850958f1f27c95d0fbbdc0ed) Since: 1.22.90

wl\_display\_add\_socket\_auto - Automatically pick a Wayland display socket for the clients to connect to.

```
const char * wl_display_add_socket_auto(struct wl_display *display)
```

display

Wayland display to which the socket should be added.

Returns:

The socket name if success. NULL if failed.

This adds a Unix socket to Wayland display which can be used by clients to connect to Wayland display. The name of the socket is chosen automatically as the first available name in the sequence "wayland-0", "wayland-1", "wayland-2",..., "wayland-32".

The string returned by this function is owned by the library and should not be freed.

See also: [wl\_display\_add\_socket](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__display_1a9fdf7264f0a3a28a75c141db252067b8)

wl\_display\_add\_socket\_fd - Add a socket with an existing fd to Wayland display for the clients to connect.

```
int wl_display_add_socket_fd(struct wl_display *display, int sock_fd)
```

display

Wayland display to which the socket should be added.

sock\_fd

The existing socket file descriptor to be used

Returns:

0 if success. -1 if failed.

The existing socket fd must already be created, opened, and locked. The fd must be properly set to CLOEXEC and bound to a socket file with both bind() and listen() already called.

On success, the socket fd ownership is transferred to libwayland: libwayland will close the socket when the display is destroyed.

wl\_display\_add\_socket - Add a socket to Wayland display for the clients to connect.

```
int wl_display_add_socket(struct wl_display *display, const char *name)
```

display

Wayland display to which the socket should be added.

name

Name of the Unix socket.

Returns:

0 if success. -1 if failed.

This adds a Unix socket to Wayland display which can be used by clients to connect to Wayland display.

If NULL is passed as name, then it would look for WAYLAND\_DISPLAY env variable for the socket name. If WAYLAND\_DISPLAY is not set, then default wayland-0 is used.

If the socket name is a relative path, the Unix socket will be created in the directory pointed to by environment variable XDG\_RUNTIME\_DIR. If XDG\_RUNTIME\_DIR is invalid or not set, then this function fails and returns -1.

If the socket name is an absolute path, then it is used as-is for the the Unix socket.

The length of the computed socket path must not exceed the maximum length of a Unix socket path. The function also fails if the user does not have write permission in the directory or if the path is already in use.

wl\_display\_add\_protocol\_logger - Adds a new protocol logger.

```
struct wl_protocol_logger * wl_display_add_protocol_logger(struct wl_display *display, wl_protocol_logger_func_t func, void *user_data)
```

When a new protocol message arrives or is sent from the server all the protocol logger functions will be called, carrying the user\_data pointer, the type of the message (request or event) and the actual message. The lifetime of the messages passed to the logger function ends when they return so the messages cannot be stored and accessed later.

errno is set on error.

display

The display object

func

The function to call to log a new protocol message

user\_data

The user data pointer to pass to func

Returns:

The protocol logger object on success, NULL on failure.

See also: [wl\_protocol\_logger\_destroy](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1ac5bfbf098cbecb788190bc12e3becad7)

wl\_display\_add\_shm\_format - Add support for a wl\_shm pixel format.

```
uint32_t * wl_display_add_shm_format(struct wl_display *display, uint32_t format)
```

display

The display object

format

The wl\_shm pixel format to advertise

Returns:

A pointer to the wl\_shm format that was added to the list or NULL if adding it to the list failed.

Add the specified wl\_shm format to the list of formats the wl\_shm object advertises when a client binds to it. Adding a format to the list means that clients will know that the compositor supports this format and may use it for creating wl\_shm buffers. The compositor must be able to handle the pixel format when a client requests it.

The compositor by default supports WL\_SHM\_FORMAT\_ARGB8888 and WL\_SHM\_FORMAT\_XRGB8888.

wl\_display\_get\_client\_list - Get the list of currently connected clients.

```
struct wl_list * wl_display_get_client_list(struct wl_display *display)
```

This function returns a pointer to the list of clients currently connected to the display. You can iterate on the list by using the wl\_client\_for\_each macro. The returned value is valid for the lifetime of the display. You must not modify the returned list, but only access it.

See also: [wl\_client\_for\_each()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1af1e9ad8dd32ea89265936930cd173ec5) See also: [wl\_client\_get\_link()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1ade7bddc335d60cb95f9d1bd4fb60d25b) See also: [wl\_client\_from\_link()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1aec831218471327f37b4e1f11b571545d)

## wl\_event\_loop - An event loop context.

Usually you create an event loop context, add sources to it, and call [wl\_event\_loop\_dispatch()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__loop_1ad33162f8fbbae46873e1ba15fe9e3c9d) in a loop to process events.

See also: [wl\_event\_source](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source "wl_event_source - An abstract event source.")

wl\_event\_loop\_create - Create a new event loop context.

```
WL_EXPORT struct wl_event_loop * wl_event_loop_create(void)
```

Returns:

A new event loop context object.

This creates a new event loop context. Initially this context is empty. Event sources need to be explicitly added to it.

Normally the event loop is run by calling [wl\_event\_loop\_dispatch()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__loop_1ad33162f8fbbae46873e1ba15fe9e3c9d) in a loop until the program terminates. Alternatively, an event loop can be embedded in another event loop by its file descriptor, see [wl\_event\_loop\_get\_fd()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__loop_1a21aeba21602cb167fc9264323d65697f).

wl\_event\_loop\_destroy - Destroy an event loop context.

```
WL_EXPORT void wl_event_loop_destroy(struct wl_event_loop *loop)
```

loop

The event loop to be destroyed.

This emits the event loop destroy signal, closes the event loop file descriptor, and frees loop.

If the event loop has existing sources, those cannot be safely removed afterwards. Therefore one must call [wl\_event\_source\_remove()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1afe37015d67b81ae82609f2b8aa78cc4f) on all event sources before destroying the event loop context.

wl\_event\_loop\_dispatch\_idle - Dispatch the idle sources.

```
WL_EXPORT void wl_event_loop_dispatch_idle(struct wl_event_loop *loop)
```

loop

The event loop whose idle sources are dispatched.

See also: [wl\_event\_loop\_add\_idle()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1a90d88ae62b26a25f709977c45b300716)

wl\_event\_loop\_dispatch - Wait for events and dispatch them.

```
WL_EXPORT int wl_event_loop_dispatch(struct wl_event_loop *loop, int timeout)
```

loop

The event loop whose sources to wait for.

timeout

The polling timeout in milliseconds.

Returns:

0 for success, -1 for polling (or timer update) error.

All the associated event sources are polled. This function blocks until any event source delivers an event (idle sources excluded), or the timeout expires. A timeout of -1 disables the timeout, causing the function to block indefinitely. A timeout of zero causes the poll to always return immediately.

All idle sources are dispatched before blocking. An idle source is destroyed when it is dispatched. After blocking, all other ready sources are dispatched. Then, idle sources are dispatched again, in case the dispatched events created idle sources. Finally, all sources marked with [wl\_event\_source\_check()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1aa079264c57dd12168c691c000724efcf) are dispatched in a loop until their dispatch functions all return zero.

wl\_event\_loop\_get\_fd - Get the event loop file descriptor.

```
WL_EXPORT int wl_event_loop_get_fd(struct wl_event_loop *loop)
```

loop

The event loop context.

Returns:

The aggregate file descriptor.

This function returns the aggregate file descriptor, that represents all the event sources (idle sources excluded) associated with the given event loop context. When any event source makes an event available, it will be reflected in the aggregate file descriptor.

When the aggregate file descriptor delivers an event, one can call [wl\_event\_loop\_dispatch()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__loop_1ad33162f8fbbae46873e1ba15fe9e3c9d) on the event loop context to dispatch all the available events.

wl\_event\_loop\_add\_destroy\_listener - Register a destroy listener for an event loop context.

```
WL_EXPORT void wl_event_loop_add_destroy_listener(struct wl_event_loop *loop, struct wl_listener *listener)
```

loop

The event loop context whose destruction to listen for.

listener

The listener with the callback to be called.

See also: [wl\_listener](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__listener "wl_listener - A single listener for Wayland signals.")

wl\_event\_loop\_get\_destroy\_listener - Get the listener struct for the specified callback.

```
WL_EXPORT struct wl_listener * wl_event_loop_get_destroy_listener(struct wl_event_loop *loop, wl_notify_func_t notify)
```

loop

The event loop context to inspect.

notify

The destroy callback to find.

Returns:

The [wl\_listener](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__listener "wl_listener - A single listener for Wayland signals.") registered to the event loop context with the given callback pointer.

## wl\_event\_source - An abstract event source.

This is the generic type for fd, timer, signal, and idle sources. Functions that operate on specific source types must not be used with a different type, even if the function signature allows it.

wl\_event\_loop\_fd\_func\_t - File descriptor dispatch function type.

```
typedef int(* wl_event_loop_fd_func_t) (int fd, uint32_t mask, void *data))(int fd, uint32_t mask, void *data)
```

Functions of this type are used as callbacks for file descriptor events.

fd

The file descriptor delivering the event.

mask

Describes the kind of the event as a bitwise-or of: WL\_EVENT\_READABLE, WL\_EVENT\_WRITABLE, WL\_EVENT\_HANGUP, WL\_EVENT\_ERROR.

data

The user data argument of the related [wl\_event\_loop\_add\_fd()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1ab04146fdca0088fe563a11f74a65d9e5) call.

Returns:

If the event source is registered for re-check with [wl\_event\_source\_check()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1aa14e0d1139efd0af332af68d07d829d5): 0 for all done, 1 for needing a re-check. If not registered, the return value is ignored and should be zero.

See also: [wl\_event\_loop\_add\_fd()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1ab04146fdca0088fe563a11f74a65d9e5)

wl\_event\_loop\_timer\_func\_t - Timer dispatch function type.

```
typedef int(* wl_event_loop_timer_func_t) (void *data))(void *data)
```

Functions of this type are used as callbacks for timer expiry.

Returns:

If the event source is registered for re-check with [wl\_event\_source\_check()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1aa14e0d1139efd0af332af68d07d829d5): 0 for all done, 1 for needing a re-check. If not registered, the return value is ignored and should be zero.

See also: [wl\_event\_loop\_add\_timer()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1a875693493d8095f31983bdc345ac918e)

wl\_event\_loop\_signal\_func\_t - Signal dispatch function type.

```
typedef int(* wl_event_loop_signal_func_t) (int signal_number, void *data))(int signal_number, void *data)
```

Functions of this type are used as callbacks for (POSIX) signals.

signal\_number

data

The user data argument of the related [wl\_event\_loop\_add\_signal()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1a5b071f3e653b6d3de0b01bda52976db4) call.

Returns:

If the event source is registered for re-check with [wl\_event\_source\_check()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1aa14e0d1139efd0af332af68d07d829d5): 0 for all done, 1 for needing a re-check. If not registered, the return value is ignored and should be zero.

See also: [wl\_event\_loop\_add\_signal()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1a5b071f3e653b6d3de0b01bda52976db4)

wl\_event\_loop\_idle\_func\_t - Idle task function type.

```
typedef void(* wl_event_loop_idle_func_t) (void *data))(void *data)
```

Functions of this type are used as callbacks before blocking in [wl\_event\_loop\_dispatch()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1aaa3fdd5590365a4a2106c9814ca9b31b).

See also: [wl\_event\_loop\_add\_idle()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1a82a5247edb54b483a24c5cd18dbb8cff) [wl\_event\_loop\_dispatch()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1aaa3fdd5590365a4a2106c9814ca9b31b)

wl\_event\_loop\_add\_fd - Create a file descriptor event source.

```
WL_EXPORT struct wl_event_source * wl_event_loop_add_fd(struct wl_event_loop *loop, int fd, uint32_t mask, wl_event_loop_fd_func_t func, void *data)
```

loop

The event loop that will process the new source.

fd

The file descriptor to watch.

mask

A bitwise-or of which events to watch for: WL\_EVENT\_READABLE, WL\_EVENT\_WRITABLE.

func

The file descriptor dispatch function.

data

User data.

Returns:

A new file descriptor event source.

The given file descriptor is initially watched for the events given in mask. This can be changed as needed with [wl\_event\_source\_fd\_update()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1aac31a13db42f3c0aa5976bec6a0121a8).

If it is possible that program execution causes the file descriptor to be read while leaving the data in a buffer without actually processing it, it may be necessary to register the file descriptor source to be re-checked, see [wl\_event\_source\_check()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1aa14e0d1139efd0af332af68d07d829d5). This will ensure that the dispatch function gets called even if the file descriptor is not readable or writable anymore. This is especially useful with IPC libraries that automatically buffer incoming data, possibly as a side-effect of other operations.

See also: [wl\_event\_loop\_fd\_func\_t](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1a09e702384ed869548c72f3576399c581)

wl\_event\_source\_fd\_update - Update a file descriptor source's event mask.

```
WL_EXPORT int wl_event_source_fd_update(struct wl_event_source *source, uint32_t mask)
```

source

The file descriptor event source to update.

mask

The new mask, a bitwise-or of: WL\_EVENT\_READABLE, WL\_EVENT\_WRITABLE.

Returns:

0 on success, -1 on failure.

This changes which events, readable and/or writable, cause the dispatch callback to be called on.

File descriptors are usually writable to begin with, so they do not need to be polled for writable until a write actually fails. When a write fails, the event mask can be changed to poll for readable and writable, delivering a dispatch callback when it is possible to write more. Once all data has been written, the mask can be changed to poll only for readable to avoid busy-looping on dispatch.

See also: [wl\_event\_loop\_add\_fd()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1ab04146fdca0088fe563a11f74a65d9e5)

wl\_event\_loop\_add\_timer - Create a timer event source.

```
WL_EXPORT struct wl_event_source * wl_event_loop_add_timer(struct wl_event_loop *loop, wl_event_loop_timer_func_t func, void *data)
```

loop

The event loop that will process the new source.

func

The timer dispatch function.

data

User data.

Returns:

A new timer event source.

The timer is initially disarmed. It needs to be armed with a call to [wl\_event\_source\_timer\_update()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1a01bd334ce62ab0918edaaca9bc3f5a6e) before it can trigger a dispatch call.

See also: [wl\_event\_loop\_timer\_func\_t](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1a59bc490bf28b48e0af908ab91649938a)

wl\_event\_source\_timer\_update - Arm or disarm a timer.

```
WL_EXPORT int wl_event_source_timer_update(struct wl_event_source *source, int ms_delay)
```

source

The timer event source to modify.

ms\_delay

The timeout in milliseconds.

Returns:

0 on success, -1 on failure.

If the timeout is zero, the timer is disarmed.

If the timeout is non-zero, the timer is set to expire after the given timeout in milliseconds. When the timer expires, the dispatch function set with [wl\_event\_loop\_add\_timer()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1a875693493d8095f31983bdc345ac918e) is called once from [wl\_event\_loop\_dispatch()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1aaa3fdd5590365a4a2106c9814ca9b31b). If another dispatch is desired after another expiry, [wl\_event\_source\_timer\_update()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1a01bd334ce62ab0918edaaca9bc3f5a6e) needs to be called again.

wl\_event\_loop\_add\_signal - Create a POSIX signal event source.

```
WL_EXPORT struct wl_event_source * wl_event_loop_add_signal(struct wl_event_loop *loop, int signal_number, wl_event_loop_signal_func_t func, void *data)
```

loop

The event loop that will process the new source.

signal\_number

Number of the signal to watch for.

func

The signal dispatch function.

data

User data.

Returns:

A new signal event source.

This function blocks the normal delivery of the given signal in the calling thread, and creates a "watch" for it. Signal delivery no longer happens asynchronously, but by [wl\_event\_loop\_dispatch()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1aaa3fdd5590365a4a2106c9814ca9b31b) calling the dispatch callback function func.

It is the caller's responsibility to ensure that all other threads have also blocked the signal.

See also: [wl\_event\_loop\_signal\_func\_t](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1a431b418976144a8ebe6b19bc24206d20)

wl\_event\_loop\_add\_idle - Create an idle task.

```
WL_EXPORT struct wl_event_source * wl_event_loop_add_idle(struct wl_event_loop *loop, wl_event_loop_idle_func_t func, void *data)
```

loop

The event loop that will process the new task.

func

The idle task dispatch function.

data

User data.

Returns:

A new idle task (an event source).

Idle tasks are dispatched before [wl\_event\_loop\_dispatch()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1aaa3fdd5590365a4a2106c9814ca9b31b) goes to sleep. See [wl\_event\_loop\_dispatch()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1aaa3fdd5590365a4a2106c9814ca9b31b) for more details.

Idle tasks fire once, and are automatically destroyed right after the callback function has been called.

An idle task can be cancelled before the callback has been called by [wl\_event\_source\_remove()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1a5eeaee7ed55cc067fb1d1ecbd810f55e). Calling [wl\_event\_source\_remove()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1a5eeaee7ed55cc067fb1d1ecbd810f55e) after or from within the callback results in undefined behaviour.

See also: [wl\_event\_loop\_idle\_func\_t](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__source_1ae526dfa099f9ba69285e275c82794a9b)

wl\_event\_source\_check - Mark event source to be re-checked.

```
WL_EXPORT void wl_event_source_check(struct wl_event_source *source)
```

source

The event source to be re-checked.

This function permanently marks the event source to be re-checked after the normal dispatch of sources in [wl\_event\_loop\_dispatch()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1aaa3fdd5590365a4a2106c9814ca9b31b). Re-checking will keep iterating over all such event sources until the dispatch function for them all returns zero.

Re-checking is used on sources that may become ready to dispatch as a side-effect of dispatching themselves or other event sources, including idle sources. Re-checking ensures all the incoming events have been fully drained before [wl\_event\_loop\_dispatch()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1aaa3fdd5590365a4a2106c9814ca9b31b) returns.

wl\_event\_source\_remove - Remove an event source from its event loop.

```
WL_EXPORT int wl_event_source_remove(struct wl_event_source *source)
```

source

The event source to be removed.

The event source is removed from the event loop it was created for, and is effectively destroyed. This invalidates source. The dispatch function of the source will no longer be called through this source.

## wl\_global

wl\_global\_get\_name - Get the name of the global.

```
uint32_t wl_global_get_name(const struct wl_global *global, const struct wl_client *client)
```

global

The global object.

client

Client for which to look up the global.

Returns:

The name of the global, or 0 if the global is not visible to the client.

Since: 1.22

wl\_global\_get\_version - Get the version of the given global.

```
uint32_t wl_global_get_version(const struct wl_global *global)
```

Returns:

The version advertised by the global.

Since: 1.21

wl\_global\_get\_display - Get the display object for the given global.

```
struct wl_display * wl_global_get_display(const struct wl_global *global)
```

Returns:

The display object the global is associated with.

Since: 1.20

## wl\_interface - Protocol object interface.

A [wl\_interface](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__interface "wl_interface - Protocol object interface.") describes the API of a protocol object defined in the Wayland protocol specification. The protocol implementation uses a [wl\_interface](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__interface "wl_interface - Protocol object interface.") within its marshalling machinery for encoding client requests.

The name of a [wl\_interface](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__interface "wl_interface - Protocol object interface.") is the name of the corresponding protocol interface, and version represents the version of the interface. The members method\_count and event\_count represent the number of methods (requests) and events in the respective [wl\_message](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__message "wl_message - Protocol message signature.") members.

For example, consider a protocol interface foo, marked as version 1, with two requests and one event.

```
<interface name="foo" version="1">
  <request name="a"></request>
  <request name="b"></request>
  <event name="c"></event>
</interface>
```

Given two [wl\_message](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__message "wl_message - Protocol message signature.") arrays foo\_requests and foo\_events, a [wl\_interface](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__interface "wl_interface - Protocol object interface.") for foo might be:

```
struct wl_interface foo_interface = {
        "foo", 1,
        2, foo_requests,
        1, foo_events
};
```

*Note: The server side of the protocol may define interface implementation types that incorporate the term interface in their name. Take care to not confuse these server-side structs with a [wl\_interface](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__interface "wl_interface - Protocol object interface.") variable whose name also ends in interface. For example, while the server may define a type struct wl\_foo\_interface, the client may define a struct [wl\_interface](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__interface "wl_interface - Protocol object interface.") wl\_foo\_interface.* See also: [wl\_message](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__message "wl_message - Protocol message signature.") See also: wl\_proxy See also: Interfaces See also: Versioning

name - Interface name.

```
const char* wl_interface::name
```

version - Interface version.

```
int wl_interface::version
```

method\_count - Number of methods (requests)

```
int wl_interface::method_count
```

methods - Method (request) signatures.

```
const struct wl_message* wl_interface::methods
```

event\_count - Number of events.

```
int wl_interface::event_count
```

events - Event signatures.

```
const struct wl_message* wl_interface::events
```

## wl\_list - Doubly-linked list.

On its own, an instance of struct [wl\_list](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list "wl_list - Doubly-linked list.") represents the sentinel head of a doubly-linked list, and must be initialized using [wl\_list\_init()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list_1a1d5c9d41e224538b2edf324c7f8b1ac8). When empty, the list head's next and prev members point to the list head itself, otherwise next references the first element in the list, and prev refers to the last element in the list.

Use the struct [wl\_list](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list "wl_list - Doubly-linked list.") type to represent both the list head and the links between elements within the list. Use [wl\_list\_empty()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list_1a5c6aa8f61fa63374f1c77e7e4462a38a) to determine if the list is empty in O(1).

All elements in the list must be of the same type. The element type must have a struct [wl\_list](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list "wl_list - Doubly-linked list.") member, often named link by convention. Prior to insertion, there is no need to initialize an element's link - invoking [wl\_list\_init()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list_1a1d5c9d41e224538b2edf324c7f8b1ac8) on an individual list element's struct [wl\_list](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list "wl_list - Doubly-linked list.") member is unnecessary if the very next operation is [wl\_list\_insert()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list_1aa7eaac0d363c0473bfc3e8172b0dfd98). However, a common idiom is to initialize an element's link prior to removal - ensure safety by invoking [wl\_list\_init()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list_1a1d5c9d41e224538b2edf324c7f8b1ac8) before [wl\_list\_remove()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list_1aa16d739aaa041dde9d34ad4bcb4d4c83).

Consider a list reference struct [wl\_list](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list "wl_list - Doubly-linked list.") foo\_list, an element type as struct element, and an element's link member as struct [wl\_list](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list "wl_list - Doubly-linked list.") link.

The following code initializes a list and adds three elements to it.

```
struct wl_list foo_list;

struct element {
        int foo;
        struct wl_list link;
};
struct element e1, e2, e3;

wl_list_init(&foo_list);
wl_list_insert(&foo_list, &e1.link);   // e1 is the first element
wl_list_insert(&foo_list, &e2.link);   // e2 is now the first element
wl_list_insert(&e2.link, &e3.link); // insert e3 after e2
```

The list now looks like \[e2, e3, e1\].

The [wl\_list](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list "wl_list - Doubly-linked list.") API provides some iterator macros. For example, to iterate a list in ascending order:

```
struct element *e;
wl_list_for_each(e, foo_list, link) {
        do_something_with_element(e);
}
```

See the documentation of each iterator for details. See also: http://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/tree/include/linux/list.h

prev - Previous list element.

```
struct wl_list* wl_list::prev
```

next - Next list element.

```
struct wl_list* wl_list::next
```

wl\_list\_init - Initializes the list.

```
void wl_list_init(struct wl_list *list)
```

wl\_list\_insert - Inserts an element into the list, after the element represented by list.

```
void wl_list_insert(struct wl_list *list, struct wl_list *elm)
```

When list is a reference to the list itself (the head), set the containing struct of elm as the first element in the list.

*Note: If elm is already part of a list, inserting it again will lead to list corruption.*

list

List element after which the new element is inserted

elm

Link of the containing struct to insert into the list

wl\_list\_remove - Removes an element from the list.

```
void wl_list_remove(struct wl_list *elm)
```

*Note: This operation leaves elm in an invalid state.*

elm

Link of the containing struct to remove from the list

wl\_list\_length - Determines the length of the list.

```
int wl_list_length(const struct wl_list *list)
```

*Note: This is an O(n) operation.*

list

List whose length is to be determined

Returns:

Number of elements in the list

wl\_list\_empty - Determines if the list is empty.

```
int wl_list_empty(const struct wl_list *list)
```

list

List whose emptiness is to be determined

Returns:

1 if empty, or 0 if not empty

wl\_list\_insert\_list - Inserts all of the elements of one list into another, after the element represented by list.

```
void wl_list_insert_list(struct wl_list *list, struct wl_list *other)
```

*Note: This leaves other in an invalid state.*

list

List element after which the other list elements will be inserted

other

List of elements to insert

wl\_list\_for\_each - Iterates over a list.

This macro expresses a for-each iterator for [wl\_list](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list "wl_list - Doubly-linked list."). Given a list and [wl\_list](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list "wl_list - Doubly-linked list.") link member name (often named link by convention), this macro assigns each element in the list to pos, which can then be referenced in a trailing code block. For example, given a [wl\_list](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list "wl_list - Doubly-linked list.") of struct message elements:

```
struct message {
        char *contents;
        wl_list link;
};

struct wl_list *message_list;
// Assume message_list now "contains" many messages

struct message *m;
wl_list_for_each(m, message_list, link) {
        do_something_with_message(m);
}
```

pos

Cursor that each list element will be assigned to

head

Head of the list to iterate over

member

Name of the link member within the element struct

wl\_list\_for\_each\_safe - Iterates over a list, safe against removal of the list element.

*Note: Only removal of the current element, pos, is safe. Removing any other element during traversal may lead to a loop malfunction.* See also: [wl\_list\_for\_each()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list_1a449407fe3c8f273e38bc2253093cb6fb)

pos

Cursor that each list element will be assigned to

tmp

Temporary pointer of the same type as pos

head

Head of the list to iterate over

member

Name of the link member within the element struct

wl\_list\_for\_each\_reverse - Iterates backwards over a list.

See also: [wl\_list\_for\_each()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list_1a449407fe3c8f273e38bc2253093cb6fb)

pos

Cursor that each list element will be assigned to

head

Head of the list to iterate over

member

Name of the link member within the element struct

wl\_list\_for\_each\_reverse\_safe - Iterates backwards over a list, safe against removal of the list element.

*Note: Only removal of the current element, pos, is safe. Removing any other element during traversal may lead to a loop malfunction.* See also: [wl\_list\_for\_each()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list_1a449407fe3c8f273e38bc2253093cb6fb)

pos

Cursor that each list element will be assigned to

tmp

Temporary pointer of the same type as pos

head

Head of the list to iterate over

member

Name of the link member within the element struct

## wl\_listener - A single listener for Wayland signals.

[wl\_listener](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__listener "wl_listener - A single listener for Wayland signals.") provides the means to listen for [wl\_signal](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__signal "wl_signal - A source of a type of observable event.") notifications. Many Wayland objects use [wl\_listener](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__listener "wl_listener - A single listener for Wayland signals.") for notification of significant events like object destruction.

Clients should create [wl\_listener](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__listener "wl_listener - A single listener for Wayland signals.") objects manually and can register them as listeners to signals using wl\_signal\_add(), assuming the signal is directly accessible. For opaque structs like [wl\_event\_loop](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__event__loop "wl_event_loop - An event loop context."), adding a listener should be done through provided accessor methods. A listener can only listen to one signal at a time.

```
struct wl_listener your_listener;

your_listener.notify = your_callback_method;

// Direct access
wl_signal_add(&some_object->destroy_signal, &your_listener);

// Accessor access
wl_event_loop *loop = ...;
wl_event_loop_add_destroy_listener(loop, &your_listener);
```

If the listener is part of a larger struct, [wl\_container\_of](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-util_8h_1a09e3b64ee2195e1b80191aa1884d45aa) can be used to retrieve a pointer to it:

```
void your_listener(struct wl_listener *listener, void *data)
{
        struct your_data *data;

        your_data = wl_container_of(listener, data, your_member_name);
}
```

If you need to remove a listener from a signal, use wl\_list\_remove().

```
wl_list_remove(&your_listener.link);
```

See also: [wl\_signal](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__signal "wl_signal - A source of a type of observable event.")

link - Part of wl\_signal::listener\_list.

```
struct wl_list wl_listener::link
```

notify - Callback function pointer.

```
wl_notify_func_t wl_listener::notify
```

## wl\_message - Protocol message signature.

A [wl\_message](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__message "wl_message - Protocol message signature.") describes the signature of an actual protocol message, such as a request or event, that adheres to the Wayland protocol wire format. The protocol implementation uses a [wl\_message](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__message "wl_message - Protocol message signature.") within its demarshal machinery for decoding messages between a compositor and its clients. In a sense, a [wl\_message](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__message "wl_message - Protocol message signature.") is to a protocol message like a class is to an object.

The name of a [wl\_message](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__message "wl_message - Protocol message signature.") is the name of the corresponding protocol message.

The signature is an ordered list of symbols representing the data types of message arguments and, optionally, a protocol version and indicators for nullability. A leading integer in the signature indicates the since version of the protocol message. A? preceding a data type symbol indicates that the following argument type is nullable. While it is a protocol violation to send messages with non-nullable arguments set to NULL, event handlers in clients might still get called with non-nullable object arguments set to NULL. This can happen when the client destroyed the object being used as argument on its side and an event referencing that object was sent before the server knew about its destruction. As this race cannot be prevented, clients should - as a general rule - program their event handlers such that they can handle object arguments declared non-nullable being NULL gracefully.

When no arguments accompany a message, signature is an empty string.

Symbols:

- i: int
- u: uint
- f: fixed
- s: string
- o: object
- n: new\_id
- a: array
- h: fd
- ?: following argument (o or s) is nullable

While demarshaling primitive arguments is straightforward, when demarshaling messages containing object or new\_id arguments, the protocol implementation often must determine the type of the object. The types of a [wl\_message](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__message "wl_message - Protocol message signature.") is an array of [wl\_interface](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__interface "wl_interface - Protocol object interface.") references that correspond to o and n arguments in signature, with NULL placeholders for arguments with non-object types.

Consider the protocol event [wl\_display](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__display "wl_display") delete\_id that has a single uint argument. The [wl\_message](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__message "wl_message - Protocol message signature.") is:

```
{ "delete_id", "u", [NULL] }
```

Here, the message name is "delete\_id", the signature is "u", and the argument types is \[NULL\], indicating that the uint argument has no corresponding [wl\_interface](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__interface "wl_interface - Protocol object interface.") since it is a primitive argument.

In contrast, consider a wl\_foo interface supporting protocol request bar that has existed since version 2, and has two arguments: a uint and an object of type wl\_baz\_interface that may be NULL. Such a [wl\_message](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__message "wl_message - Protocol message signature.") might be:

```
{ "bar", "2u?o", [NULL, &wl_baz_interface] }
```

Here, the message name is "bar", and the signature is "2u?o". Notice how the 2 indicates the protocol version, the u indicates the first argument type is uint, and the?o indicates that the second argument is an object that may be NULL. Lastly, the argument types array indicates that no [wl\_interface](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__interface "wl_interface - Protocol object interface.") corresponds to the first argument, while the type wl\_baz\_interface corresponds to the second argument.

See also: [wl\_argument](https://wayland.freedesktop.org/docs/html/apc.html#Server-unionwl__argument "wl_argument - Protocol message argument data types.") See also: [wl\_interface](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__interface "wl_interface - Protocol object interface.") See also: Wire Format

name - Message name.

```
const char* wl_message::name
```

signature - Message signature.

```
const char* wl_message::signature
```

types - Object argument interfaces.

```
const struct wl_interface** wl_message::types
```

## wl\_object - A protocol object.

A [wl\_object](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__object "wl_object - A protocol object.") is an opaque struct identifying the protocol object underlying a wl\_proxy or [wl\_resource](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__resource "wl_resource").

*Note: Functions accessing a [wl\_object](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__object "wl_object - A protocol object.") are not normally used by client code. Clients should normally use the higher level interface generated by the scanner to interact with compositor objects.*

## wl\_protocol\_logger

wl\_protocol\_logger\_destroy - Destroys a protocol logger.

```
void wl_protocol_logger_destroy(struct wl_protocol_logger *logger)
```

This function destroys a protocol logger and removes it from the display it was added to with wl\_display\_add\_protocol\_logger. The logger object becomes invalid after calling this function.

See also: [wl\_display\_add\_protocol\_logger](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1a6e8daf2d5520070eb3aa24b8d5efd9dd)

## wl\_protocol\_logger\_message

## wl\_resource

wl\_resource\_post\_error\_vargs - Post a protocol error.

```
void wl_resource_post_error_vargs(struct wl_resource *resource, uint32_t code, const char *msg, va_list argp)
```

resource

The resource object

code

The error code

msg

The error message format string

argp

The format string argument list

wl\_resource\_post\_error - Post a protocol error.

```
void wl_resource_post_error(struct wl_resource *resource, uint32_t code, const char *msg,...)
```

resource

The resource object

code

The error code

msg

The error message format string

...

The format string arguments

wl\_resource\_get\_class - Retrieve the interface name (class) of a resource object.

```
const char * wl_resource_get_class(const struct wl_resource *resource)
```

wl\_resource\_get\_interface - Get the interface of a resource object.

```
const struct wl_interface * wl_resource_get_interface(struct wl_resource *resource)
```

Returns:

The interface of the object associated with the resource

Since: 1.24

wl\_resource\_create - Create a new resource object.

```
struct wl_resource * wl_resource_create(struct wl_client *client, const struct wl_interface *interface, int version, uint32_t id)
```

client

The client owner of the new resource.

interface

The interface of the new resource.

version

The version of the new resource.

id

The id of the new resource. If 0, an available id will be used.

Listeners added with wl\_client\_add\_resource\_created\_listener will be notified at the end of this function.

## wl\_resource\_iterator\_context

## wl\_shm\_buffer - A SHM buffer.

[wl\_shm\_buffer](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__shm__buffer "wl_shm_buffer - A SHM buffer.") provides a helper for accessing the contents of a wl\_buffer resource created via the wl\_shm interface.

A [wl\_shm\_buffer](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__shm__buffer "wl_shm_buffer - A SHM buffer.") becomes invalid as soon as its [wl\_resource](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__resource "wl_resource") is destroyed.

wl\_shm\_buffer\_get\_data - Get a pointer to the memory for the SHM buffer.

```
void * wl_shm_buffer_get_data(struct wl_shm_buffer *buffer)
```

Returns a pointer which can be used to read the data contained in the given SHM buffer.

As this buffer is memory-mapped, reading from it may generate SIGBUS signals. This can happen if the client claims that the buffer is larger than it is or if something truncates the underlying file. To prevent this signal from causing the compositor to crash you should call [wl\_shm\_buffer\_begin\_access()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__shm__buffer_1a809cb5d6b33338c62bbca6daa4138667) and [wl\_shm\_buffer\_end\_access()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__shm__buffer_1a030db6056ef08836e9dee21a8087e2c1) around code that reads from the memory.

wl\_shm\_buffer\_ref - Reference a shm\_buffer.

```
struct wl_shm_buffer * wl_shm_buffer_ref(struct wl_shm_buffer *buffer)
```

Returns a pointer to the buffer and increases the refcount.

The compositor must remember to call [wl\_shm\_buffer\_unref()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__shm__buffer_1a1a3b37eb87634d5f7ce6c4771d8e09c7) when it no longer needs the reference to ensure proper destruction of the buffer.

See also: [wl\_shm\_buffer\_unref](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__shm__buffer_1a1a3b37eb87634d5f7ce6c4771d8e09c7)

wl\_shm\_buffer\_unref - Unreference a shm\_buffer.

```
void wl_shm_buffer_unref(struct wl_shm_buffer *buffer)
```

Drops a reference to a buffer object.

This is only necessary if the compositor has explicitly taken a reference with [wl\_shm\_buffer\_ref()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__shm__buffer_1a8081c8f018c9626c363b6cd05c40ee61), otherwise the buffer will be automatically destroyed when appropriate.

See also: [wl\_shm\_buffer\_ref](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__shm__buffer_1a8081c8f018c9626c363b6cd05c40ee61)

wl\_shm\_buffer\_ref\_pool - Get a reference to a shm\_buffer's shm\_pool.

```
struct wl_shm_pool * wl_shm_buffer_ref_pool(struct wl_shm_buffer *buffer)
```

Returns a pointer to a buffer's shm\_pool and increases the shm\_pool refcount.

The compositor must remember to call [wl\_shm\_pool\_unref()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1a2349156a6b7940645a4754e6c1690051) when it no longer needs the reference to ensure proper destruction of the pool.

See also: [wl\_shm\_pool\_unref](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1a2349156a6b7940645a4754e6c1690051)

wl\_shm\_buffer\_begin\_access - Mark that the given SHM buffer is about to be accessed.

```
void wl_shm_buffer_begin_access(struct wl_shm_buffer *buffer)
```

buffer

The SHM buffer

An SHM buffer is a memory-mapped file given by the client. According to POSIX, reading from a memory-mapped region that extends off the end of the file will cause a SIGBUS signal to be generated. Normally this would cause the compositor to terminate. In order to make the compositor robust against clients that change the size of the underlying file or lie about its size, you should protect access to the buffer by calling this function before reading from the memory and call [wl\_shm\_buffer\_end\_access()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__shm__buffer_1a030db6056ef08836e9dee21a8087e2c1) afterwards. This will install a signal handler for SIGBUS which will prevent the compositor from crashing.

After calling this function the signal handler will remain installed for the lifetime of the compositor process. Note that this function will not work properly if the compositor is also installing its own handler for SIGBUS.

If a SIGBUS signal is received for an address within the range of the SHM pool of the given buffer then the client will be sent an error event when [wl\_shm\_buffer\_end\_access()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__shm__buffer_1a030db6056ef08836e9dee21a8087e2c1) is called. If the signal is for an address outside that range then the signal handler will reraise the signal which would will likely cause the compositor to terminate.

It is safe to nest calls to these functions as long as the nested calls are all accessing the same pool. The number of calls to [wl\_shm\_buffer\_end\_access()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__shm__buffer_1a030db6056ef08836e9dee21a8087e2c1) must match the number of calls to [wl\_shm\_buffer\_begin\_access()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__shm__buffer_1a809cb5d6b33338c62bbca6daa4138667). These functions are thread-safe and it is allowed to simultaneously access different buffers or the same buffer from multiple threads.

wl\_shm\_buffer\_end\_access - Ends the access to a buffer started by wl\_shm\_buffer\_begin\_access()

```
void wl_shm_buffer_end_access(struct wl_shm_buffer *buffer)
```

This should be called after [wl\_shm\_buffer\_begin\_access()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__shm__buffer_1a809cb5d6b33338c62bbca6daa4138667) once the buffer is no longer being accessed. If a SIGBUS signal was generated in-between these two calls then the resource for the given buffer will be sent an error.

## wl\_shm\_pool

wl\_shm\_pool\_unref - Unreference a shm\_pool.

```
void wl_shm_pool_unref(struct wl_shm_pool *pool)
```

Drops a reference to a [wl\_shm\_pool](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__shm__pool "wl_shm_pool") object.

This is only necessary if the compositor has explicitly taken a reference with [wl\_shm\_buffer\_ref\_pool()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1abc49a49c3586821d6ec4efe7ea915305), otherwise the pool will be automatically destroyed when appropriate.

See also: [wl\_shm\_buffer\_ref\_pool](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1abc49a49c3586821d6ec4efe7ea915305)

## wl\_shm\_sigbus\_data

## wl\_signal - A source of a type of observable event.

Signals are recognized points where significant events can be observed. Compositors as well as the server can provide signals. Observers are [wl\_listener](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__listener "wl_listener - A single listener for Wayland signals.") 's that are added through [wl\_signal\_add](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__signal_1aa8bcd3b8e250cfe35ed064d5af589096). Signals are emitted using [wl\_signal\_emit](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__signal_1afe73f44f7f1b517c9c0ba90829c93309), which will invoke all listeners until that listener is removed by wl\_list\_remove() (or whenever the signal is destroyed).

See also: [wl\_listener](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__listener "wl_listener - A single listener for Wayland signals.") for more information on using [wl\_signal](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__signal "wl_signal - A source of a type of observable event.")

wl\_signal\_emit\_mutable - Emits this signal, notifying all registered listeners.

```
void wl_signal_emit_mutable(struct wl_signal *signal, void *data)
```

A safer version of [wl\_signal\_emit()](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__signal_1afe73f44f7f1b517c9c0ba90829c93309) which can gracefully handle additions and deletions of any signal listener from within listener notification callbacks.

Listeners deleted during a signal emission and which have not already been notified at the time of deletion are not notified by that emission.

Listeners added (or readded) during signal emission are ignored by that emission.

Note that repurposing a listener without explicitly removing it and readding it is not supported and can lead to unexpected behavior.

signal

The signal object that will emit the signal

data

The data that will be emitted with the signal

Since: 1.20.90

wl\_signal\_init - Initialize a new wl\_signal for use.

```
static void wl_signal_init(struct wl_signal *signal)
```

signal

The signal that will be initialized

wl\_signal\_add - Add the specified listener to this signal.

```
static void wl_signal_add(struct wl_signal *signal, struct wl_listener *listener)
```

signal

The signal that will emit events to the listener

listener

The listener to add

wl\_signal\_get - Gets the listener struct for the specified callback.

```
static struct wl_listener * wl_signal_get(struct wl_signal *signal, wl_notify_func_t notify)
```

signal

The signal that contains the specified listener

notify

The listener that is the target of this search

Returns:

the list item that corresponds to the specified listener, or NULL if none was found

wl\_signal\_emit - Emits this signal, notifying all registered listeners.

```
static void wl_signal_emit(struct wl_signal *signal, void *data)
```

signal

The signal object that will emit the signal

data

The data that will be emitted with the signal

## wl\_socket

## Functions

wl\_client\_for\_each - Iterate over a list of clients.

wl\_display\_global\_filter\_func\_t - A filter function for wl\_global objects.

```
typedef bool(* wl_display_global_filter_func_t) (const struct wl_client *client, const struct wl_global *global, void *data))(const struct wl_client *client, const struct wl_global *global, void *data)
```

client

The client object

global

The global object to show or hide

data

The user data pointer

A filter function enables the server to decide which globals to advertise to each client.

When a [wl\_global](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__global "wl_global") filter is set, the given callback function will be called during [wl\_global](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__global "wl_global") advertisement and binding.

This function should return true if the global object should be made visible to the client or false otherwise.

wl\_client\_for\_each\_resource\_iterator\_func\_t - Callback function type for wl\_client\_for\_each\_resource()

```
typedef enum wl_iterator_result(* wl_client_for_each_resource_iterator_func_t) (struct wl_resource *resource, void *user_data))(struct wl_resource *resource, void *user_data)
```

wl\_protocol\_logger\_func\_t - Callback function type for wl\_display\_add\_protocol\_logger()

```
typedef void(* wl_protocol_logger_func_t) (void *user_data, enum wl_protocol_logger_type direction, const struct wl_protocol_logger_message *message))(void *user_data, enum wl_protocol_logger_type direction, const struct wl_protocol_logger_message *message)
```

wl\_event\_loop\_create

```
struct wl_event_loop * wl_event_loop_create(void)
```

wl\_event\_loop\_destroy

```
void wl_event_loop_destroy(struct wl_event_loop *loop)
```

wl\_event\_loop\_add\_fd

```
struct wl_event_source * wl_event_loop_add_fd(struct wl_event_loop *loop, int fd, uint32_t mask, wl_event_loop_fd_func_t func, void *data)
```

wl\_event\_source\_fd\_update

```
int wl_event_source_fd_update(struct wl_event_source *source, uint32_t mask)
```

wl\_event\_loop\_add\_timer

```
struct wl_event_source * wl_event_loop_add_timer(struct wl_event_loop *loop, wl_event_loop_timer_func_t func, void *data)
```

wl\_event\_loop\_add\_signal

```
struct wl_event_source * wl_event_loop_add_signal(struct wl_event_loop *loop, int signal_number, wl_event_loop_signal_func_t func, void *data)
```

wl\_event\_source\_timer\_update

```
int wl_event_source_timer_update(struct wl_event_source *source, int ms_delay)
```

wl\_event\_source\_remove

```
int wl_event_source_remove(struct wl_event_source *source)
```

wl\_event\_source\_check

```
void wl_event_source_check(struct wl_event_source *source)
```

wl\_event\_loop\_dispatch

```
int wl_event_loop_dispatch(struct wl_event_loop *loop, int timeout)
```

wl\_event\_loop\_dispatch\_idle

```
void wl_event_loop_dispatch_idle(struct wl_event_loop *loop)
```

wl\_event\_loop\_add\_idle

```
struct wl_event_source * wl_event_loop_add_idle(struct wl_event_loop *loop, wl_event_loop_idle_func_t func, void *data)
```

wl\_event\_loop\_get\_fd

```
int wl_event_loop_get_fd(struct wl_event_loop *loop)
```

wl\_event\_loop\_add\_destroy\_listener

```
void wl_event_loop_add_destroy_listener(struct wl_event_loop *loop, struct wl_listener *listener)
```

wl\_event\_loop\_get\_destroy\_listener

```
struct wl_listener * wl_event_loop_get_destroy_listener(struct wl_event_loop *loop, wl_notify_func_t notify)
```

wl\_display\_create

```
struct wl_display * wl_display_create(void)
```

wl\_display\_destroy

```
void wl_display_destroy(struct wl_display *display)
```

wl\_display\_get\_event\_loop

```
struct wl_event_loop * wl_display_get_event_loop(struct wl_display *display)
```

wl\_display\_add\_socket

```
int wl_display_add_socket(struct wl_display *display, const char *name)
```

wl\_display\_add\_socket\_auto

```
const char * wl_display_add_socket_auto(struct wl_display *display)
```

wl\_display\_add\_socket\_fd

```
int wl_display_add_socket_fd(struct wl_display *display, int sock_fd)
```

wl\_display\_terminate

```
void wl_display_terminate(struct wl_display *display)
```

wl\_display\_run

```
void wl_display_run(struct wl_display *display)
```

wl\_display\_flush\_clients

```
void wl_display_flush_clients(struct wl_display *display)
```

wl\_display\_destroy\_clients

```
void wl_display_destroy_clients(struct wl_display *display)
```

wl\_display\_set\_default\_max\_buffer\_size

```
void wl_display_set_default_max_buffer_size(struct wl_display *display, size_t max_buffer_size)
```

wl\_display\_get\_serial

```
uint32_t wl_display_get_serial(const struct wl_display *display)
```

wl\_display\_next\_serial

```
uint32_t wl_display_next_serial(struct wl_display *display)
```

wl\_display\_add\_destroy\_listener

```
void wl_display_add_destroy_listener(struct wl_display *display, struct wl_listener *listener)
```

wl\_display\_add\_client\_created\_listener - Registers a listener for the client connection signal.

```
void wl_display_add_client_created_listener(struct wl_display *display, struct wl_listener *listener)
```

When a new client object is created, listener will be notified, carrying a pointer to the new [wl\_client](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__client "wl_client") object.

[wl\_client\_create](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1aa2436b6a0b56cd65d8f6e33b76cd292c) [wl\_display](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__display "wl_display") [wl\_listener](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__listener "wl_listener - A single listener for Wayland signals.")

display

The display object

listener

Signal handler object

wl\_display\_get\_destroy\_listener

```
struct wl_listener * wl_display_get_destroy_listener(struct wl_display *display, wl_notify_func_t notify)
```

wl\_global\_create

```
struct wl_global * wl_global_create(struct wl_display *display, const struct wl_interface *interface, int version, void *data, wl_global_bind_func_t bind)
```

wl\_global\_remove - Remove the global.

```
void wl_global_remove(struct wl_global *global)
```

global

The Wayland global.

Broadcast a global remove event to all clients without destroying the global. This function can only be called once per global.

[wl\_global\_destroy()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server_8c_1ab466d94d1f204fb5f07c57e5f558ab7a) removes the global and immediately destroys it. On the other end, this function only removes the global, allowing clients that have not yet received the global remove event to continue to bind to it.

This can be used by compositors to mitigate clients being disconnected because a global has been added and removed too quickly. Compositors can call [wl\_global\_remove()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server_8c_1a7f93649ba31c12220ee77982a37aa270), then wait an implementation-defined amount of time, then call [wl\_global\_destroy()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server_8c_1ab466d94d1f204fb5f07c57e5f558ab7a). Note that the destruction of a global is still racy, since clients have no way to acknowledge that they received the remove event.

Since: 1.17.90

wl\_global\_destroy

```
void wl_global_destroy(struct wl_global *global)
```

wl\_display\_set\_global\_filter

```
void wl_display_set_global_filter(struct wl_display *display, wl_display_global_filter_func_t filter, void *data)
```

wl\_global\_get\_interface

```
const struct wl_interface * wl_global_get_interface(const struct wl_global *global)
```

wl\_global\_get\_name

```
uint32_t wl_global_get_name(const struct wl_global *global, const struct wl_client *client)
```

wl\_global\_get\_version

```
uint32_t wl_global_get_version(const struct wl_global *global)
```

wl\_global\_get\_display

```
struct wl_display * wl_global_get_display(const struct wl_global *global)
```

wl\_global\_get\_user\_data

```
void * wl_global_get_user_data(const struct wl_global *global)
```

wl\_global\_set\_user\_data - Set the global's user data.

```
void wl_global_set_user_data(struct wl_global *global, void *data)
```

global

The global object

data

The user data pointer

Since: 1.17.90

wl\_client\_create

```
struct wl_client * wl_client_create(struct wl_display *display, int fd)
```

wl\_display\_get\_client\_list

```
struct wl_list * wl_display_get_client_list(struct wl_display *display)
```

wl\_client\_get\_link

```
struct wl_list * wl_client_get_link(struct wl_client *client)
```

wl\_client\_from\_link

```
struct wl_client * wl_client_from_link(struct wl_list *link)
```

wl\_client\_destroy

```
void wl_client_destroy(struct wl_client *client)
```

wl\_client\_flush

```
void wl_client_flush(struct wl_client *client)
```

wl\_client\_get\_credentials

```
void wl_client_get_credentials(const struct wl_client *client, pid_t *pid, uid_t *uid, gid_t *gid)
```

wl\_client\_get\_fd

```
int wl_client_get_fd(struct wl_client *client)
```

wl\_client\_add\_destroy\_listener

```
void wl_client_add_destroy_listener(struct wl_client *client, struct wl_listener *listener)
```

wl\_client\_get\_destroy\_listener

```
struct wl_listener * wl_client_get_destroy_listener(struct wl_client *client, wl_notify_func_t notify)
```

wl\_client\_add\_destroy\_late\_listener

```
void wl_client_add_destroy_late_listener(struct wl_client *client, struct wl_listener *listener)
```

wl\_client\_get\_destroy\_late\_listener

```
struct wl_listener * wl_client_get_destroy_late_listener(struct wl_client *client, wl_notify_func_t notify)
```

wl\_client\_get\_object

```
struct wl_resource * wl_client_get_object(struct wl_client *client, uint32_t id)
```

wl\_client\_post\_no\_memory

```
void wl_client_post_no_memory(struct wl_client *client)
```

wl\_client\_post\_implementation\_error

```
void wl_client_post_implementation_error(struct wl_client *client, const char *msg,...)
```

wl\_client\_add\_resource\_created\_listener

```
void wl_client_add_resource_created_listener(struct wl_client *client, struct wl_listener *listener)
```

wl\_client\_for\_each\_resource

```
void wl_client_for_each_resource(struct wl_client *client, wl_client_for_each_resource_iterator_func_t iterator, void *user_data)
```

wl\_client\_set\_user\_data

```
void wl_client_set_user_data(struct wl_client *client, void *data, wl_user_data_destroy_func_t dtor)
```

wl\_client\_get\_user\_data

```
void * wl_client_get_user_data(struct wl_client *client)
```

wl\_client\_set\_max\_buffer\_size

```
void wl_client_set_max_buffer_size(struct wl_client *client, size_t max_buffer_size)
```

wl\_signal\_emit\_mutable

```
void wl_signal_emit_mutable(struct wl_signal *signal, void *data)
```

wl\_resource\_post\_event

```
void wl_resource_post_event(struct wl_resource *resource, uint32_t opcode,...)
```

wl\_resource\_post\_event\_array

```
void wl_resource_post_event_array(struct wl_resource *resource, uint32_t opcode, union wl_argument *args)
```

wl\_resource\_queue\_event

```
void wl_resource_queue_event(struct wl_resource *resource, uint32_t opcode,...)
```

wl\_resource\_queue\_event\_array

```
void wl_resource_queue_event_array(struct wl_resource *resource, uint32_t opcode, union wl_argument *args)
```

wl\_resource\_post\_error\_vargs

```
void wl_resource_post_error_vargs(struct wl_resource *resource, uint32_t code, const char *msg, va_list argp)
```

wl\_resource\_post\_error

```
void wl_resource_post_error(struct wl_resource *resource, uint32_t code, const char *msg,...)
```

wl\_resource\_post\_no\_memory

```
void wl_resource_post_no_memory(struct wl_resource *resource)
```

wl\_client\_get\_display

```
struct wl_display * wl_client_get_display(struct wl_client *client)
```

wl\_resource\_create

```
struct wl_resource * wl_resource_create(struct wl_client *client, const struct wl_interface *interface, int version, uint32_t id)
```

wl\_resource\_set\_implementation

```
void wl_resource_set_implementation(struct wl_resource *resource, const void *implementation, void *data, wl_resource_destroy_func_t destroy)
```

wl\_resource\_set\_dispatcher

```
void wl_resource_set_dispatcher(struct wl_resource *resource, wl_dispatcher_func_t dispatcher, const void *implementation, void *data, wl_resource_destroy_func_t destroy)
```

wl\_resource\_destroy

```
void wl_resource_destroy(struct wl_resource *resource)
```

wl\_resource\_get\_id

```
uint32_t wl_resource_get_id(const struct wl_resource *resource)
```

wl\_resource\_get\_link

```
struct wl_list * wl_resource_get_link(struct wl_resource *resource)
```

wl\_resource\_from\_link

```
struct wl_resource * wl_resource_from_link(struct wl_list *resource)
```

wl\_resource\_find\_for\_client

```
struct wl_resource * wl_resource_find_for_client(struct wl_list *list, struct wl_client *client)
```

wl\_resource\_get\_client

```
struct wl_client * wl_resource_get_client(struct wl_resource *resource)
```

wl\_resource\_set\_user\_data

```
void wl_resource_set_user_data(struct wl_resource *resource, void *data)
```

wl\_resource\_get\_user\_data

```
void * wl_resource_get_user_data(struct wl_resource *resource)
```

wl\_resource\_get\_version

```
int wl_resource_get_version(const struct wl_resource *resource)
```

wl\_resource\_set\_destructor

```
void wl_resource_set_destructor(struct wl_resource *resource, wl_resource_destroy_func_t destroy)
```

wl\_resource\_instance\_of

```
int wl_resource_instance_of(struct wl_resource *resource, const struct wl_interface *interface, const void *implementation)
```

wl\_resource\_get\_class

```
const char * wl_resource_get_class(const struct wl_resource *resource)
```

wl\_resource\_get\_interface

```
const struct wl_interface * wl_resource_get_interface(struct wl_resource *resource)
```

wl\_resource\_add\_destroy\_listener

```
void wl_resource_add_destroy_listener(struct wl_resource *resource, struct wl_listener *listener)
```

wl\_resource\_get\_destroy\_listener

```
struct wl_listener * wl_resource_get_destroy_listener(struct wl_resource *resource, wl_notify_func_t notify)
```

wl\_shm\_buffer\_get

```
struct wl_shm_buffer * wl_shm_buffer_get(struct wl_resource *resource)
```

wl\_shm\_buffer\_begin\_access

```
void wl_shm_buffer_begin_access(struct wl_shm_buffer *buffer)
```

wl\_shm\_buffer\_end\_access

```
void wl_shm_buffer_end_access(struct wl_shm_buffer *buffer)
```

wl\_shm\_buffer\_get\_data

```
void * wl_shm_buffer_get_data(struct wl_shm_buffer *buffer)
```

wl\_shm\_buffer\_get\_stride

```
int32_t wl_shm_buffer_get_stride(const struct wl_shm_buffer *buffer)
```

wl\_shm\_buffer\_get\_format

```
uint32_t wl_shm_buffer_get_format(const struct wl_shm_buffer *buffer)
```

wl\_shm\_buffer\_get\_width

```
int32_t wl_shm_buffer_get_width(const struct wl_shm_buffer *buffer)
```

wl\_shm\_buffer\_get\_height

```
int32_t wl_shm_buffer_get_height(const struct wl_shm_buffer *buffer)
```

wl\_shm\_buffer\_ref

```
struct wl_shm_buffer * wl_shm_buffer_ref(struct wl_shm_buffer *buffer)
```

wl\_shm\_buffer\_unref

```
void wl_shm_buffer_unref(struct wl_shm_buffer *buffer)
```

wl\_shm\_buffer\_ref\_pool

```
struct wl_shm_pool * wl_shm_buffer_ref_pool(struct wl_shm_buffer *buffer)
```

wl\_shm\_pool\_unref

```
void wl_shm_pool_unref(struct wl_shm_pool *pool)
```

wl\_display\_init\_shm

```
int wl_display_init_shm(struct wl_display *display)
```

wl\_display\_add\_shm\_format

```
uint32_t * wl_display_add_shm_format(struct wl_display *display, uint32_t format)
```

wl\_shm\_buffer\_create

```
WL_DEPRECATED struct wl_shm_buffer * wl_shm_buffer_create(struct wl_client *client, uint32_t id, int32_t width, int32_t height, int32_t stride, uint32_t format)
```

wl\_log\_set\_handler\_server

```
void wl_log_set_handler_server(wl_log_func_t handler)
```

wl\_display\_add\_protocol\_logger

```
struct wl_protocol_logger * wl_display_add_protocol_logger(struct wl_display *display, wl_protocol_logger_func_t, void *user_data)
```

wl\_protocol\_logger\_destroy

```
void wl_protocol_logger_destroy(struct wl_protocol_logger *logger)
```

wl\_resource\_post\_event\_array

```
void wl_resource_post_event_array(struct wl_resource *resource, uint32_t opcode, union wl_argument *args)
```

wl\_resource\_post\_event

```
void wl_resource_post_event(struct wl_resource *resource, uint32_t opcode,...)
```

wl\_resource\_queue\_event\_array

```
void wl_resource_queue_event_array(struct wl_resource *resource, uint32_t opcode, union wl_argument *args)
```

wl\_resource\_queue\_event

```
void wl_resource_queue_event(struct wl_resource *resource, uint32_t opcode,...)
```

wl\_client\_post\_no\_memory

```
void wl_client_post_no_memory(struct wl_client *client)
```

wl\_resource\_post\_no\_memory

```
void wl_resource_post_no_memory(struct wl_resource *resource)
```

wl\_resource\_destroy

```
void wl_resource_destroy(struct wl_resource *resource)
```

wl\_resource\_get\_id

```
uint32_t wl_resource_get_id(const struct wl_resource *resource)
```

wl\_resource\_get\_link

```
struct wl_list * wl_resource_get_link(struct wl_resource *resource)
```

wl\_resource\_from\_link

```
struct wl_resource * wl_resource_from_link(struct wl_list *link)
```

wl\_resource\_find\_for\_client

```
struct wl_resource * wl_resource_find_for_client(struct wl_list *list, struct wl_client *client)
```

wl\_resource\_get\_client

```
struct wl_client * wl_resource_get_client(struct wl_resource *resource)
```

wl\_resource\_set\_user\_data

```
void wl_resource_set_user_data(struct wl_resource *resource, void *data)
```

wl\_resource\_get\_user\_data

```
void * wl_resource_get_user_data(struct wl_resource *resource)
```

wl\_resource\_get\_version

```
int wl_resource_get_version(const struct wl_resource *resource)
```

wl\_resource\_set\_destructor

```
void wl_resource_set_destructor(struct wl_resource *resource, wl_resource_destroy_func_t destroy)
```

wl\_resource\_instance\_of

```
int wl_resource_instance_of(struct wl_resource *resource, const struct wl_interface *interface, const void *implementation)
```

wl\_resource\_add\_destroy\_listener

```
void wl_resource_add_destroy_listener(struct wl_resource *resource, struct wl_listener *listener)
```

wl\_resource\_get\_destroy\_listener

```
struct wl_listener * wl_resource_get_destroy_listener(struct wl_resource *resource, wl_notify_func_t notify)
```

wl\_client\_get\_destroy\_listener

```
struct wl_listener * wl_client_get_destroy_listener(struct wl_client *client, wl_notify_func_t notify)
```

wl\_client\_get\_destroy\_late\_listener

```
struct wl_listener * wl_client_get_destroy_late_listener(struct wl_client *client, wl_notify_func_t notify)
```

wl\_client\_destroy

```
void wl_client_destroy(struct wl_client *client)
```

wl\_global\_create

```
struct wl_global * wl_global_create(struct wl_display *display, const struct wl_interface *interface, int version, void *data, wl_global_bind_func_t bind)
```

wl\_global\_remove - Remove the global.

```
void wl_global_remove(struct wl_global *global)
```

global

The Wayland global.

Broadcast a global remove event to all clients without destroying the global. This function can only be called once per global.

[wl\_global\_destroy()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server_8c_1ab466d94d1f204fb5f07c57e5f558ab7a) removes the global and immediately destroys it. On the other end, this function only removes the global, allowing clients that have not yet received the global remove event to continue to bind to it.

This can be used by compositors to mitigate clients being disconnected because a global has been added and removed too quickly. Compositors can call [wl\_global\_remove()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server_8c_1a7f93649ba31c12220ee77982a37aa270), then wait an implementation-defined amount of time, then call [wl\_global\_destroy()](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server_8c_1ab466d94d1f204fb5f07c57e5f558ab7a). Note that the destruction of a global is still racy, since clients have no way to acknowledge that they received the remove event.

Since: 1.17.90

wl\_global\_destroy

```
void wl_global_destroy(struct wl_global *global)
```

wl\_global\_get\_interface

```
const struct wl_interface * wl_global_get_interface(const struct wl_global *global)
```

wl\_global\_get\_user\_data

```
void * wl_global_get_user_data(const struct wl_global *global)
```

wl\_global\_set\_user\_data - Set the global's user data.

```
void wl_global_set_user_data(struct wl_global *global, void *data)
```

global

The global object

data

The user data pointer

Since: 1.17.90

wl\_display\_get\_event\_loop

```
struct wl_event_loop * wl_display_get_event_loop(struct wl_display *display)
```

wl\_display\_terminate

```
void wl_display_terminate(struct wl_display *display)
```

wl\_display\_run

```
void wl_display_run(struct wl_display *display)
```

wl\_display\_flush\_clients

```
void wl_display_flush_clients(struct wl_display *display)
```

wl\_display\_add\_destroy\_listener

```
void wl_display_add_destroy_listener(struct wl_display *display, struct wl_listener *listener)
```

wl\_display\_add\_client\_created\_listener - Registers a listener for the client connection signal.

```
void wl_display_add_client_created_listener(struct wl_display *display, struct wl_listener *listener)
```

When a new client object is created, listener will be notified, carrying a pointer to the new [wl\_client](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__client "wl_client") object.

[wl\_client\_create](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1aa2436b6a0b56cd65d8f6e33b76cd292c) [wl\_display](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__display "wl_display") [wl\_listener](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__listener "wl_listener - A single listener for Wayland signals.")

display

The display object

listener

Signal handler object

wl\_display\_get\_destroy\_listener

```
struct wl_listener * wl_display_get_destroy_listener(struct wl_display *display, wl_notify_func_t notify)
```

wl\_resource\_set\_implementation

```
void wl_resource_set_implementation(struct wl_resource *resource, const void *implementation, void *data, wl_resource_destroy_func_t destroy)
```

wl\_resource\_set\_dispatcher

```
void wl_resource_set_dispatcher(struct wl_resource *resource, wl_dispatcher_func_t dispatcher, const void *implementation, void *data, wl_resource_destroy_func_t destroy)
```

wl\_log\_set\_handler\_server

```
void wl_log_set_handler_server(wl_log_func_t handler)
```

wl\_client\_add\_resource

```
WL_DEPRECATED uint32_t wl_client_add_resource(struct wl_client *client, struct wl_resource *resource)
```

wl\_client\_add\_object

```
WL_DEPRECATED struct wl_resource * wl_client_add_object(struct wl_client *client, const struct wl_interface *interface, const void *implementation, uint32_t id, void *data)
```

wl\_client\_new\_object

```
WL_DEPRECATED struct wl_resource * wl_client_new_object(struct wl_client *client, const struct wl_interface *interface, const void *implementation, void *data)
```

wl\_display\_add\_global

```
WL_DEPRECATED struct wl_global * wl_display_add_global(struct wl_display *display, const struct wl_interface *interface, void *data, wl_global_bind_func_t bind)
```

wl\_display\_remove\_global

```
WL_DEPRECATED void wl_display_remove_global(struct wl_display *display, struct wl_global *global)
```

wl\_display\_init\_shm

```
int wl_display_init_shm(struct wl_display *display)
```

wl\_shm\_buffer\_get

```
struct wl_shm_buffer * wl_shm_buffer_get(struct wl_resource *resource)
```

wl\_shm\_buffer\_get\_stride

```
int32_t wl_shm_buffer_get_stride(const struct wl_shm_buffer *buffer)
```

wl\_shm\_buffer\_get\_format

```
uint32_t wl_shm_buffer_get_format(const struct wl_shm_buffer *buffer)
```

wl\_shm\_buffer\_get\_width

```
int32_t wl_shm_buffer_get_width(const struct wl_shm_buffer *buffer)
```

wl\_shm\_buffer\_get\_height

```
int32_t wl_shm_buffer_get_height(const struct wl_shm_buffer *buffer)
```

WL\_EXPORT - Visibility attribute.

WL\_DEPRECATED - Deprecated attribute.

WL\_PRINTF - Printf-style argument attribute.

x

Ordinality of the format string argument

y

Ordinality of the argument to check against the format string

See also: https://gcc.gnu.org/onlinedocs/gcc-3.2.1/gcc/Function-Attributes.html

WL\_MAX\_MESSAGE\_SIZE - The maximum size of a protocol message.

If a message size exceeds this value, the connection will be dropped. Servers will send an invalid\_method error before disconnecting.

wl\_container\_of - Retrieves a pointer to a containing struct, given a member name.

This macro allows "conversion" from a pointer to a member to its containing struct. This is useful if you have a contained item like a [wl\_list](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__list "wl_list - Doubly-linked list."), [wl\_listener](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__listener "wl_listener - A single listener for Wayland signals."), or [wl\_signal](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__signal "wl_signal - A source of a type of observable event."), provided via a callback or other means, and would like to retrieve the struct that contains it.

To demonstrate, the following example retrieves a pointer to example\_container given only its destroy\_listener member:

```
struct example_container {
        struct wl_listener destroy_listener;
        // other members...
};

void example_container_destroy(struct wl_listener *listener, void *data)
{
        struct example_container *ctr;

        ctr = wl_container_of(listener, ctr, destroy_listener);
        // destroy ctr...
}
```

*Note: sample need not be a valid pointer. A null or uninitialised pointer is sufficient.*

ptr

Valid pointer to the contained member

sample

Pointer to a struct whose type contains ptr

member

Named location of ptr within the sample type

Returns:

The container for the specified pointer

wl\_iterator\_result - Return value of an iterator function.

See also: [wl\_client\_for\_each\_resource\_iterator\_func\_t](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1a3dfebf4109ca3ff4d66d28019a2c2602) See also: [wl\_client\_for\_each\_resource](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1a4a0a6bb48f63ed80ab4575fda4c5d01a)

wl\_fixed\_t - Fixed-point number.

```
typedef int32_t wl_fixed_t
```

A [wl\_fixed\_t](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-util_8h_1a546c8b2b06f97d0617000db4fb4feeeb) is a 24.8 signed fixed-point number with a sign bit, 23 bits of integer precision and 8 bits of decimal precision. Consider [wl\_fixed\_t](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-util_8h_1a546c8b2b06f97d0617000db4fb4feeeb) as an opaque struct with methods that facilitate conversion to and from double and int types.

wl\_dispatcher\_func\_t - Dispatcher function type alias.

```
typedef int(* wl_dispatcher_func_t) (const void *user_data, void *target, uint32_t opcode, const struct wl_message *msg, union wl_argument *args))(const void *user_data, void *target, uint32_t opcode, const struct wl_message *msg, union wl_argument *args)
```

A dispatcher is a function that handles the emitting of callbacks in client code. For programs directly using the C library, this is done by using libffi to call function pointers. When binding to languages other than C, dispatchers provide a way to abstract the function calling process to be friendlier to other function calling systems.

A dispatcher takes five arguments: The first is the dispatcher-specific implementation associated with the target object. The second is the object upon which the callback is being invoked (either wl\_proxy or [wl\_resource](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__resource "wl_resource")). The third and fourth arguments are the opcode and the [wl\_message](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__message "wl_message - Protocol message signature.") corresponding to the callback. The final argument is an array of arguments received from the other process via the wire protocol.

user\_data

Dispatcher-specific implementation data

target

Callback invocation target (wl\_proxy or [wl\_resource](https://wayland.freedesktop.org/docs/html/apc.html#Server-structwl__resource "wl_resource"))

opcode

Callback opcode

msg

Callback message signature

args

Array of received arguments

Returns:

0 on success, or -1 on failure

wl\_log\_func\_t - Log function type alias.

```
typedef void(* wl_log_func_t) (const char *fmt, va_list args))(const char *fmt, va_list args)
```

The C implementation of the Wayland protocol abstracts the details of logging. Users may customize the logging behavior, with a function conforming to the [wl\_log\_func\_t](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-util_8h_1a84c4dc362eef1933db82226459636f2d) type, via wl\_log\_set\_handler\_client and wl\_log\_set\_handler\_server.

A [wl\_log\_func\_t](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-util_8h_1a84c4dc362eef1933db82226459636f2d) must conform to the expectations of vprintf, and expects two arguments: a string to write and a corresponding variable argument list. While the string to write may contain format specifiers and use values in the variable argument list, the behavior of any [wl\_log\_func\_t](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-util_8h_1a84c4dc362eef1933db82226459636f2d) depends on the implementation.

*Note: Take care to not confuse this with [wl\_protocol\_logger\_func\_t](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server-core_8h_1a420c37c10e960e6fb0968e2c30628006), which is a specific server-side logger for requests and events.*

fmt

String to write to the log, containing optional format specifiers

args

Variable argument list

See also: wl\_log\_set\_handler\_client See also: [wl\_log\_set\_handler\_server](https://wayland.freedesktop.org/docs/html/apc.html#Server-wayland-server_8c_1a0a0e1384dce2524161299fcd1669d59f)

wl\_fixed\_to\_double - Converts a fixed-point number to a floating-point number.

```
static double wl_fixed_to_double(wl_fixed_t f)
```

Returns:

Floating-point representation of the fixed-point argument

wl\_fixed\_from\_double - Converts a floating-point number to a fixed-point number.

```
static wl_fixed_t wl_fixed_from_double(double d)
```

wl\_fixed\_to\_int - Converts a fixed-point number to an integer.

```
static int wl_fixed_to_int(wl_fixed_t f)
```

wl\_fixed\_from\_int - Converts an integer to a fixed-point number.

```
static wl_fixed_t wl_fixed_from_int(int i)
```
