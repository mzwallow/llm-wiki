---
title: "Appendix B. Client API"
source: "https://wayland.freedesktop.org/docs/html/apb.html#Client-unionwl__argument"
author:
published:
created: 2026-04-25
description:
tags:
  - "clippings"
---

## Introduction

The open-source reference implementation of Wayland protocol is split in two C libraries, libwayland-client and [libwayland-server](https://wayland.freedesktop.org/docs/html/apc.html "Appendix C. Server API"). Their main responsibility is to handle the Inter-process communication (*IPC*) with each other, therefore guaranteeing the protocol objects marshaling and messages synchronization.

A client uses libwayland-client to communicate with one or more wayland servers. A [wl\_display](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display "wl_display - Represents a connection to the compositor and acts as a proxy to the wl_display singleton object.") object is created and manages each open connection to a server. At least one [wl\_event\_queue](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__event__queue "wl_event_queue - A queue for wl_proxy object events.") object is created for each wl\_display, this holds events as they are received from the server until they can be processed. Multi-threading is supported by creating an additional wl\_event\_queue for each additional thread, each object can have its events placed in a particular queue, so potentially a different thread could be made to handle the events for each object created.

Though some convenience functions are provided, libwayland-client is designed to allow the calling code to wait for events, so that different polling mechanisms can be used. A file descriptor is provided, when it becomes ready for reading the calling code can ask libwayland-client to read the available events from it into the wl\_event\_queue objects.

The library only provides low-level access to the wayland objects. Each object created by the client is represented by a [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") object that this library creates. This includes the id that is actually communicated over the socket to the server, a void\* data pointer that is intended to point at a client's representation of the object, and a pointer to a static [wl\_interface](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__interface "wl_interface - Protocol object interface.") object, which is generated from the xml and identifies the object's class and can be used for introspection into the messages and events.

Messages are sent by calling wl\_proxy\_marshal. This will write a message to the socket, by using the message id and the wl\_interface to identify the types of each argument and convert them into stream format. Most software will call type-safe wrappers generated from the xml description of the [Wayland protocols](https://wayland.freedesktop.org/docs/html/apa.html "Appendix A. Wayland Protocol Specification"). For instance the C header file generated from the xml defines the following inline function to transmit the [wl\_surface::attach](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface-request-attach "wl_surface::attach - set the surface contents") message:

```
static inline void
wl_surface_attach(struct wl_surface *wl_surface, struct wl_buffer *buffer, int32_t x, int32_t y)
{
  wl_proxy_marshal((struct wl_proxy *) wl_surface, WL_SURFACE_ATTACH, buffer, x, y);
}
```

Events (messages from the server) are handled by calling a "dispatcher" callback the client stores in the wl\_proxy for each event. A language binding for a string-based interpreter, such as CPython, might have a dispatcher that uses the event name from the wl\_interface to identify the function to call. The default dispatcher uses the message id number to index an array of functions pointers, called a wl\_listener, and the wl\_interface to convert data from the stream into arguments to the function. The C header file generated from the xml defines a per-class structure that forces the function pointers to be of the correct type, for instance the [wl\_surface::enter](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface-event-enter "wl_surface::enter - surface enters an output") event defines this pointer in the wl\_surface\_listener object:

```
struct wl_surface_listener {
  void (*enter)(void *data, struct wl_surface *, struct wl_output *);
  ...
}
```

## wl\_argument - Protocol message argument data types.

This union represents all of the argument types in the Wayland protocol wire format. The protocol implementation uses [wl\_argument](https://wayland.freedesktop.org/docs/html/apb.html#Client-unionwl__argument "wl_argument - Protocol message argument data types.") within its marshalling machinery for dispatching messages between a client and a compositor.

See also: [wl\_message](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__message "wl_message - Protocol message signature.") See also: [wl\_interface](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__interface "wl_interface - Protocol object interface.") See also: Wire Format

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

A [wl\_array](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__array "wl_array - Dynamic array.") is a dynamic array that can only grow until released. It is intended for relatively small allocations whose size is variable or not known in advance. While construction of a [wl\_array](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__array "wl_array - Dynamic array.") does not require all elements to be of the same size, [wl\_array\_for\_each()](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__array_1ab050f7375dcae916506142763080ed80) does require all elements to have the same type and size.

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

This macro expresses a for-each iterator for [wl\_array](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__array "wl_array - Dynamic array."). It assigns each element in the array to pos, which can then be referenced in a trailing code block. pos must be a pointer to the array element type, and all array elements must be of the same type and size.

pos

Cursor that each array element will be assigned to

array

Array to iterate over

See also: wl\_list\_for\_each()

## wl\_display - Represents a connection to the compositor and acts as a proxy to the wl\_display singleton object.

A [wl\_display](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display "wl_display - Represents a connection to the compositor and acts as a proxy to the wl_display singleton object.") object represents a client connection to a Wayland compositor. It is created with either [wl\_display\_connect()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a37233bec2632b424ff447a4a2abe3c5d) or [wl\_display\_connect\_to\_fd()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a1db07edf920a5f9cb7fe76255e670e97). A connection is terminated using [wl\_display\_disconnect()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a2f06c1bc90bf0cd09c8584349f6d8726).

A [wl\_display](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display "wl_display - Represents a connection to the compositor and acts as a proxy to the wl_display singleton object.") is also used as the [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") for the [wl\_display](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display "wl_display - Represents a connection to the compositor and acts as a proxy to the wl_display singleton object.") singleton object on the compositor side.

A [wl\_display](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display "wl_display - Represents a connection to the compositor and acts as a proxy to the wl_display singleton object.") object handles all the data sent from and to the compositor. When a [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") marshals a request, it will write its wire representation to the display's write buffer. The data is sent to the compositor when the client calls [wl\_display\_flush()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1ac97984c0e57dc56ac3d971b3542617af).

Incoming data is handled in two steps: queueing and dispatching. In the queue step, the data coming from the display fd is interpreted and added to a queue. On the dispatch step, the handler for the incoming event set by the client on the corresponding [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") is called.

A [wl\_display](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display "wl_display - Represents a connection to the compositor and acts as a proxy to the wl_display singleton object.") has at least one event queue, called the default queue. Clients can create additional event queues with [wl\_display\_create\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a4e06e02cba530ee05a8a9920a499b036) and assign [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") 's to it. Events occurring in a particular proxy are always queued in its assigned queue. A client can ensure that a certain assumption, such as holding a lock or running from a given thread, is true when a proxy event handler is called by assigning that proxy to an event queue and making sure that this queue is only dispatched when the assumption holds.

The default queue is dispatched by calling [wl\_display\_dispatch()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a8f85e2c5ec7431cbfd584c3e87350c5a). This will dispatch any events queued on the default queue and attempt to read from the display fd if it's empty. Events read are then queued on the appropriate queues according to the proxy assignment.

A user created queue is dispatched with [wl\_display\_dispatch\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a6d49ca71d5f61c10d68ef7ae6cc863b7). This function behaves exactly the same as [wl\_display\_dispatch()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a8f85e2c5ec7431cbfd584c3e87350c5a) but it dispatches given queue instead of the default queue.

A real world example of event queue usage is Mesa's implementation of eglSwapBuffers() for the Wayland platform. This function might need to block until a frame callback is received, but dispatching the default queue could cause an event handler on the client to start drawing again. This problem is solved using another event queue, so that only the events handled by the EGL code are dispatched during the block.

This creates a problem where a thread dispatches a non-default queue, reading all the data from the display fd. If the application would call poll(2) after that it would block, even though there might be events queued on the default queue. Those events should be dispatched with [wl\_display\_dispatch\_pending()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a11e68d9f863ce375daf7a008223d2d34) or [wl\_display\_dispatch\_queue\_pending()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a532d3e1b436e5cc9e9f12daafc84f1b3) before flushing and blocking.

wl\_display\_create\_queue - Create a new event queue for this display.

```
WL_EXPORT struct wl_event_queue * wl_display_create_queue(struct wl_display *display)
```

Returns:

A new event queue associated with this display or NULL on failure.

wl\_display\_create\_queue\_with\_name - Create a new event queue for this display and give it a name.

```
WL_EXPORT struct wl_event_queue * wl_display_create_queue_with_name(struct wl_display *display, const char *name)
```

display

The display context object

name

A human readable queue name

Returns:

A new event queue associated with this display or NULL on failure.

wl\_display\_connect\_to\_fd - Connect to Wayland display on an already open fd.

```
WL_EXPORT struct wl_display * wl_display_connect_to_fd(int fd)
```

fd

The fd to use for the connection

Returns:

A [wl\_display](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display "wl_display - Represents a connection to the compositor and acts as a proxy to the wl_display singleton object.") object or NULL on failure

The [wl\_display](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display "wl_display - Represents a connection to the compositor and acts as a proxy to the wl_display singleton object.") takes ownership of the fd and will close it when the display is destroyed. The fd will also be closed in case of failure.

wl\_display\_connect - Connect to a Wayland display.

```
WL_EXPORT struct wl_display * wl_display_connect(const char *name)
```

name

Name of the Wayland display to connect to

Returns:

A [wl\_display](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display "wl_display - Represents a connection to the compositor and acts as a proxy to the wl_display singleton object.") object or NULL on failure

Connect to the Wayland display named name. If name is NULL, its value will be replaced with the WAYLAND\_DISPLAY environment variable if it is set, otherwise display "wayland-0" will be used.

If WAYLAND\_SOCKET is set, it's interpreted as a file descriptor number referring to an already opened socket. In this case, the socket is used as-is and name is ignored.

If name is a relative path, then the socket is opened relative to the XDG\_RUNTIME\_DIR directory.

If name is an absolute path, then that path is used as-is for the location of the socket at which the Wayland server is listening; no qualification inside XDG\_RUNTIME\_DIR is attempted.

If name is NULL and the WAYLAND\_DISPLAY environment variable is set to an absolute pathname, then that pathname is used as-is for the socket in the same manner as if name held an absolute path. Support for absolute paths in name and WAYLAND\_DISPLAY is present since Wayland version 1.15.

wl\_display\_disconnect - Close a connection to a Wayland display.

```
WL_EXPORT void wl_display_disconnect(struct wl_display *display)
```

Close the connection to display. The [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") and [wl\_event\_queue](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__event__queue "wl_event_queue - A queue for wl_proxy object events.") objects need to be manually destroyed by the caller before disconnecting.

wl\_display\_get\_fd - Get a display context's file descriptor.

```
WL_EXPORT int wl_display_get_fd(struct wl_display *display)
```

Return the file descriptor associated with a display so it can be integrated into the client's main loop.

wl\_display\_roundtrip\_queue - Block until all pending request are processed by the server.

```
WL_EXPORT int wl_display_roundtrip_queue(struct wl_display *display, struct wl_event_queue *queue)
```

display

The display context object

queue

The queue on which to run the roundtrip

Returns:

The number of dispatched events on success or -1 on failure

This function blocks until the server has processed all currently issued requests by sending a request to the display server and waiting for a reply before returning.

This function uses [wl\_display\_dispatch\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a6d49ca71d5f61c10d68ef7ae6cc863b7) internally. It is not allowed to call this function while the thread is being prepared for reading events, and doing so will cause a dead lock.

*Note: This function may dispatch other events being received on the given queue.* See also: [wl\_display\_roundtrip()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a485ade9dcfbe03f5716f2a015faf9845)

wl\_display\_roundtrip - Block until all pending request are processed by the server.

```
WL_EXPORT int wl_display_roundtrip(struct wl_display *display)
```

display

The display context object

Returns:

The number of dispatched events on success or -1 on failure

This function blocks until the server has processed all currently issued requests by sending a request to the display server and waiting for a reply before returning.

This function uses [wl\_display\_dispatch\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a6d49ca71d5f61c10d68ef7ae6cc863b7) internally. It is not allowed to call this function while the thread is being prepared for reading events, and doing so will cause a dead lock.

*Note: This function may dispatch other events being received on the default queue.*

wl\_display\_read\_events - Read events from display file descriptor.

```
WL_EXPORT int wl_display_read_events(struct wl_display *display)
```

display

The display context object

Returns:

0 on success or -1 on error. In case of error errno will be set accordingly

Calling this function will result in data available on the display file descriptor being read and read events will be queued on their corresponding event queues.

Before calling this function, depending on what thread it is to be called from, [wl\_display\_prepare\_read\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a1b0d28cc0bd1a7e16854ec266d0b3c45) or [wl\_display\_prepare\_read()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1acacae9325099c07782e3b3f98b63336f) needs to be called. See [wl\_display\_prepare\_read\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a1b0d28cc0bd1a7e16854ec266d0b3c45) for more details.

When being called at a point where other threads have been prepared to read (using [wl\_display\_prepare\_read\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a1b0d28cc0bd1a7e16854ec266d0b3c45) or [wl\_display\_prepare\_read()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1acacae9325099c07782e3b3f98b63336f)) this function will sleep until all other prepared threads have either been cancelled (using [wl\_display\_cancel\_read()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1aaabd034ac507cb1fcb6b4a8b32166d2b)) or them self entered this function. The last thread that calls this function will then read and queue events on their corresponding event queues, and finally wake up all other [wl\_display\_read\_events()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1ae6e187d402b4a17ec29406f1ab91e635) calls causing them to return.

If a thread cancels a read preparation when all other threads that have prepared to read has either called [wl\_display\_cancel\_read()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1aaabd034ac507cb1fcb6b4a8b32166d2b) or [wl\_display\_read\_events()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1ae6e187d402b4a17ec29406f1ab91e635), all reader threads will return without having read any data.

To dispatch events that may have been queued, call [wl\_display\_dispatch\_pending()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a11e68d9f863ce375daf7a008223d2d34) or [wl\_display\_dispatch\_queue\_pending()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a532d3e1b436e5cc9e9f12daafc84f1b3).

See also: [wl\_display\_prepare\_read()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1acacae9325099c07782e3b3f98b63336f), [wl\_display\_cancel\_read()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1aaabd034ac507cb1fcb6b4a8b32166d2b), [wl\_display\_dispatch\_pending()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a11e68d9f863ce375daf7a008223d2d34), [wl\_display\_dispatch()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a8f85e2c5ec7431cbfd584c3e87350c5a)

wl\_display\_prepare\_read\_queue - Prepare to read events from the display's file descriptor to a queue.

```
WL_EXPORT int wl_display_prepare_read_queue(struct wl_display *display, struct wl_event_queue *queue)
```

display

The display context object

queue

The event queue to use

Returns:

0 on success or -1 if event queue was not empty

This function (or [wl\_display\_prepare\_read()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1acacae9325099c07782e3b3f98b63336f)) must be called before reading from the file descriptor using [wl\_display\_read\_events()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1ae6e187d402b4a17ec29406f1ab91e635). Calling [wl\_display\_prepare\_read\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a1b0d28cc0bd1a7e16854ec266d0b3c45) announces the calling thread's intention to read and ensures that until the thread is ready to read and calls [wl\_display\_read\_events()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1ae6e187d402b4a17ec29406f1ab91e635), no other thread will read from the file descriptor. This only succeeds if the event queue is empty, and if not -1 is returned and errno set to EAGAIN.

If a thread successfully calls [wl\_display\_prepare\_read\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a1b0d28cc0bd1a7e16854ec266d0b3c45), it must either call [wl\_display\_read\_events()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1ae6e187d402b4a17ec29406f1ab91e635) when it's ready or cancel the read intention by calling [wl\_display\_cancel\_read()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1aaabd034ac507cb1fcb6b4a8b32166d2b).

Use this function before polling on the display fd or integrate the fd into a toolkit event loop in a race-free way. A correct usage would be (with most error checking left out):

```
while (wl_display_prepare_read_queue(display, queue) != 0)
        wl_display_dispatch_queue_pending(display, queue);
wl_display_flush(display);

ret = poll(fds, nfds, -1);
if (has_error(ret))
        wl_display_cancel_read(display);
else
        wl_display_read_events(display);

wl_display_dispatch_queue_pending(display, queue);
```

Here we call [wl\_display\_prepare\_read\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a1b0d28cc0bd1a7e16854ec266d0b3c45), which ensures that between returning from that call and eventually calling [wl\_display\_read\_events()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1ae6e187d402b4a17ec29406f1ab91e635), no other thread will read from the fd and queue events in our queue. If the call to [wl\_display\_prepare\_read\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a1b0d28cc0bd1a7e16854ec266d0b3c45) fails, we dispatch the pending events and try again until we're successful.

The [wl\_display\_prepare\_read\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a1b0d28cc0bd1a7e16854ec266d0b3c45) function doesn't acquire exclusive access to the display's fd. It only registers that the thread calling this function has intention to read from fd. When all registered readers call [wl\_display\_read\_events()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1ae6e187d402b4a17ec29406f1ab91e635), only one (at random) eventually reads and queues the events and the others are sleeping meanwhile. This way we avoid races and still can read from more threads.

See also: [wl\_display\_cancel\_read()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1aaabd034ac507cb1fcb6b4a8b32166d2b), [wl\_display\_read\_events()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1ae6e187d402b4a17ec29406f1ab91e635), [wl\_display\_prepare\_read()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1acacae9325099c07782e3b3f98b63336f)

wl\_display\_prepare\_read - Prepare to read events from the display's file descriptor.

```
WL_EXPORT int wl_display_prepare_read(struct wl_display *display)
```

display

The display context object

Returns:

0 on success or -1 if event queue was not empty

This function does the same thing as [wl\_display\_prepare\_read\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a1b0d28cc0bd1a7e16854ec266d0b3c45) with the default queue passed as the queue.

See also: [wl\_display\_prepare\_read\_queue](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a1b0d28cc0bd1a7e16854ec266d0b3c45)

wl\_display\_cancel\_read - Cancel read intention on display's fd.

```
WL_EXPORT void wl_display_cancel_read(struct wl_display *display)
```

After a thread successfully called [wl\_display\_prepare\_read()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1acacae9325099c07782e3b3f98b63336f) it must either call [wl\_display\_read\_events()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1ae6e187d402b4a17ec29406f1ab91e635) or [wl\_display\_cancel\_read()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1aaabd034ac507cb1fcb6b4a8b32166d2b). If the threads do not follow this rule it will lead to deadlock.

See also: [wl\_display\_prepare\_read()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1acacae9325099c07782e3b3f98b63336f), [wl\_display\_read\_events()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1ae6e187d402b4a17ec29406f1ab91e635)

wl\_display\_dispatch\_queue\_timeout - Dispatch events in an event queue with a timeout.

```
WL_EXPORT int wl_display_dispatch_queue_timeout(struct wl_display *display, struct wl_event_queue *queue, const struct timespec *timeout)
```

display

The display context object

queue

The event queue to dispatch

timeout

A timeout describing how long the call should block trying to dispatch events

Returns:

The number of dispatched events on success, -1 on failure

This function behaves identical to [wl\_display\_dispatch\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a6d49ca71d5f61c10d68ef7ae6cc863b7) except that it also takes a timeout and returns 0 if the timeout elapsed.

Passing NULL as a timeout means an infinite timeout. An empty timespec causes [wl\_display\_dispatch\_queue\_timeout()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a6d7b0ad366241d8d75dad04930ce05fe) to return immediately even if no events have been dispatched.

If a timeout is passed to [wl\_display\_dispatch\_queue\_timeout()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a6d7b0ad366241d8d75dad04930ce05fe) it is updated to the remaining time.

See also: [wl\_display\_dispatch\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a6d49ca71d5f61c10d68ef7ae6cc863b7)

wl\_display\_dispatch\_queue - Dispatch events in an event queue.

```
WL_EXPORT int wl_display_dispatch_queue(struct wl_display *display, struct wl_event_queue *queue)
```

display

The display context object

queue

The event queue to dispatch

Returns:

The number of dispatched events on success or -1 on failure

Dispatch events on the given event queue.

If the given event queue is empty, this function blocks until there are events to be read from the display fd. Events are read and queued on the appropriate event queues. Finally, events on given event queue are dispatched. On failure -1 is returned and errno set appropriately.

In a multi threaded environment, do not manually wait using poll() (or equivalent) before calling this function, as doing so might cause a dead lock. If external reliance on poll() (or equivalent) is required, see [wl\_display\_prepare\_read\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a1b0d28cc0bd1a7e16854ec266d0b3c45) of how to do so.

This function is thread safe as long as it dispatches the right queue on the right thread. It is also compatible with the multi thread event reading preparation API (see [wl\_display\_prepare\_read\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a1b0d28cc0bd1a7e16854ec266d0b3c45)), and uses the equivalent functionality internally. It is not allowed to call this function while the thread is being prepared for reading events, and doing so will cause a dead lock.

It can be used as a helper function to ease the procedure of reading and dispatching events.

*Note: Since Wayland 1.5 the display has an extra queue for its own events (i. e. delete\_id). This queue is dispatched always, no matter what queue we passed as an argument to this function. That means that this function can return even when it has not dispatched any event for the given queue.* See also: [wl\_display\_dispatch()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a8f85e2c5ec7431cbfd584c3e87350c5a), [wl\_display\_dispatch\_pending()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a11e68d9f863ce375daf7a008223d2d34), [wl\_display\_dispatch\_queue\_pending()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a532d3e1b436e5cc9e9f12daafc84f1b3), [wl\_display\_prepare\_read\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a1b0d28cc0bd1a7e16854ec266d0b3c45)

wl\_display\_dispatch\_queue\_pending - Dispatch pending events in an event queue.

```
WL_EXPORT int wl_display_dispatch_queue_pending(struct wl_display *display, struct wl_event_queue *queue)
```

display

The display context object

queue

The event queue to dispatch

Returns:

The number of dispatched events on success or -1 on failure

Dispatch all incoming events for objects assigned to the given event queue. On failure -1 is returned and errno set appropriately. If there are no events queued, this function returns immediately.

Since: 1.0.2

wl\_display\_dispatch\_queue\_pending\_single - Dispatch at most one pending event in an event queue.

```
WL_EXPORT int wl_display_dispatch_queue_pending_single(struct wl_display *display, struct wl_event_queue *queue)
```

display

The display context object

queue

The event queue to dispatch

Returns:

The number of dispatched events (0 or 1) on success or -1 on failure

Dispatch at most one pending event for objects assigned to the given event queue. On failure -1 is returned and errno set appropriately. If there are no events queued, this function returns immediately.

Since: 1.25.0

wl\_display\_dispatch - Process incoming events.

```
WL_EXPORT int wl_display_dispatch(struct wl_display *display)
```

display

The display context object

Returns:

The number of dispatched events on success or -1 on failure

Dispatch events on the default event queue.

If the default event queue is empty, this function blocks until there are events to be read from the display fd. Events are read and queued on the appropriate event queues. Finally, events on the default event queue are dispatched. On failure -1 is returned and errno set appropriately.

In a multi threaded environment, do not manually wait using poll() (or equivalent) before calling this function, as doing so might cause a dead lock. If external reliance on poll() (or equivalent) is required, see [wl\_display\_prepare\_read\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a1b0d28cc0bd1a7e16854ec266d0b3c45) of how to do so.

This function is thread safe as long as it dispatches the right queue on the right thread. It is also compatible with the multi thread event reading preparation API (see [wl\_display\_prepare\_read\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a1b0d28cc0bd1a7e16854ec266d0b3c45)), and uses the equivalent functionality internally. It is not allowed to call this function while the thread is being prepared for reading events, and doing so will cause a dead lock.

*Note: It is not possible to check if there are events on the queue or not. For dispatching default queue events without blocking, see [wl\_display\_dispatch\_pending()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a11e68d9f863ce375daf7a008223d2d34).* See also: [wl\_display\_dispatch\_pending()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a11e68d9f863ce375daf7a008223d2d34), [wl\_display\_dispatch\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a6d49ca71d5f61c10d68ef7ae6cc863b7), [wl\_display\_read\_events()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1ae6e187d402b4a17ec29406f1ab91e635)

wl\_display\_dispatch\_pending - Dispatch default queue events without reading from the display fd.

```
WL_EXPORT int wl_display_dispatch_pending(struct wl_display *display)
```

display

The display context object

Returns:

The number of dispatched events or -1 on failure

This function dispatches events on the main event queue. It does not attempt to read the display fd and simply returns zero if the main queue is empty, i.e., it doesn't block.

See also: [wl\_display\_dispatch()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a8f85e2c5ec7431cbfd584c3e87350c5a), [wl\_display\_dispatch\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1a6d49ca71d5f61c10d68ef7ae6cc863b7), [wl\_display\_flush()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1ac97984c0e57dc56ac3d971b3542617af)

wl\_display\_dispatch\_pending\_single - Dispatch at most one pending event in the default event queue.

```
WL_EXPORT int wl_display_dispatch_pending_single(struct wl_display *display)
```

display

The display context object

Returns:

The number of dispatched events (0 or 1) on success or -1 on failure

Dispatch at most one pending event for objects assigned to the default event queue. On failure -1 is returned and errno set appropriately. If there are no events queued, this function returns immediately.

Since: 1.25.0

wl\_display\_get\_error - Retrieve the last error that occurred on a display.

```
WL_EXPORT int wl_display_get_error(struct wl_display *display)
```

display

The display context object

Returns:

The last error that occurred on display or 0 if no error occurred

Return the last error that occurred on the display. This may be an error sent by the server or caused by the local client.

*Note: Errors are fatal. If this function returns non-zero the display can no longer be used.*

wl\_display\_get\_protocol\_error - Retrieves the information about a protocol error:

```
WL_EXPORT uint32_t wl_display_get_protocol_error(struct wl_display *display, const struct wl_interface **interface, uint32_t *id)
```

display

The Wayland display

interface

if not NULL, stores the interface where the error occurred, or NULL, if unknown.

id

if not NULL, stores the object id that generated the error, or 0, if the object id is unknown. There's no guarantee the object is still valid; the client must know if it deleted the object.

Returns:

The error code as defined in the interface specification.

```
int err = wl_display_get_error(display);

if (err == EPROTO) {
       code = wl_display_get_protocol_error(display, &interface, &id);
       handle_error(code, interface, id);
}

...
```

wl\_display\_flush - Send all buffered requests on the display to the server.

```
WL_EXPORT int wl_display_flush(struct wl_display *display)
```

display

The display context object

Returns:

The number of bytes sent on success or -1 on failure

Send all buffered data on the client side to the server. Clients should always call this function before blocking on input from the display fd. On success, the number of bytes sent to the server is returned. On failure, this function returns -1 and errno is set appropriately.

[wl\_display\_flush()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display_1ac97984c0e57dc56ac3d971b3542617af) never blocks. It will write as much data as possible, but if all data could not be written, errno will be set to EAGAIN and -1 returned. In that case, use poll on the display file descriptor to wait for it to become writable again.

wl\_display\_set\_max\_buffer\_size - Adjust the maximum size of the client connection buffers.

```
WL_EXPORT void wl_display_set_max_buffer_size(struct wl_display *display, size_t max_buffer_size)
```

display

The display context object

max\_buffer\_size

The maximum size of the connection buffers

Client buffers are unbounded by default. This function sets a limit to the size of the connection buffers.

A value of 0 for max\_buffer\_size requests the buffers to be unbounded.

The actual size of the connection buffers is a power of two, the requested max\_buffer\_size is therefore rounded up to the nearest power of two value.

Lowering the maximum size may not take effect immediately if the current content of the buffer does not fit within the new size limit.

Since: 1.22.90

## wl\_event\_queue - A queue for wl\_proxy object events.

Event queues allows the events on a display to be handled in a thread-safe manner. See [wl\_display](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display "wl_display - Represents a connection to the compositor and acts as a proxy to the wl_display singleton object.") for details.

wl\_event\_queue\_destroy - Destroy an event queue.

```
WL_EXPORT void wl_event_queue_destroy(struct wl_event_queue *queue)
```

queue

The event queue to be destroyed

Destroy the given event queue. Any pending event on that queue is discarded.

The [wl\_display](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display "wl_display - Represents a connection to the compositor and acts as a proxy to the wl_display singleton object.") object used to create the queue should not be destroyed until all event queues created with it are destroyed with this function.

## wl\_interface - Protocol object interface.

A [wl\_interface](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__interface "wl_interface - Protocol object interface.") describes the API of a protocol object defined in the Wayland protocol specification. The protocol implementation uses a [wl\_interface](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__interface "wl_interface - Protocol object interface.") within its marshalling machinery for encoding client requests.

The name of a [wl\_interface](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__interface "wl_interface - Protocol object interface.") is the name of the corresponding protocol interface, and version represents the version of the interface. The members method\_count and event\_count represent the number of methods (requests) and events in the respective [wl\_message](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__message "wl_message - Protocol message signature.") members.

For example, consider a protocol interface foo, marked as version 1, with two requests and one event.

```
<interface name="foo" version="1">
  <request name="a"></request>
  <request name="b"></request>
  <event name="c"></event>
</interface>
```

Given two [wl\_message](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__message "wl_message - Protocol message signature.") arrays foo\_requests and foo\_events, a [wl\_interface](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__interface "wl_interface - Protocol object interface.") for foo might be:

```
struct wl_interface foo_interface = {
        "foo", 1,
        2, foo_requests,
        1, foo_events
};
```

*Note: The server side of the protocol may define interface implementation types that incorporate the term interface in their name. Take care to not confuse these server-side structs with a [wl\_interface](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__interface "wl_interface - Protocol object interface.") variable whose name also ends in interface. For example, while the server may define a type struct wl\_foo\_interface, the client may define a struct [wl\_interface](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__interface "wl_interface - Protocol object interface.") wl\_foo\_interface.* See also: [wl\_message](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__message "wl_message - Protocol message signature.") See also: [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") See also: Interfaces See also: Versioning

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

On its own, an instance of struct [wl\_list](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list "wl_list - Doubly-linked list.") represents the sentinel head of a doubly-linked list, and must be initialized using [wl\_list\_init()](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list_1a1d5c9d41e224538b2edf324c7f8b1ac8). When empty, the list head's next and prev members point to the list head itself, otherwise next references the first element in the list, and prev refers to the last element in the list.

Use the struct [wl\_list](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list "wl_list - Doubly-linked list.") type to represent both the list head and the links between elements within the list. Use [wl\_list\_empty()](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list_1a5c6aa8f61fa63374f1c77e7e4462a38a) to determine if the list is empty in O(1).

All elements in the list must be of the same type. The element type must have a struct [wl\_list](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list "wl_list - Doubly-linked list.") member, often named link by convention. Prior to insertion, there is no need to initialize an element's link - invoking [wl\_list\_init()](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list_1a1d5c9d41e224538b2edf324c7f8b1ac8) on an individual list element's struct [wl\_list](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list "wl_list - Doubly-linked list.") member is unnecessary if the very next operation is [wl\_list\_insert()](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list_1aa7eaac0d363c0473bfc3e8172b0dfd98). However, a common idiom is to initialize an element's link prior to removal - ensure safety by invoking [wl\_list\_init()](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list_1a1d5c9d41e224538b2edf324c7f8b1ac8) before [wl\_list\_remove()](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list_1aa16d739aaa041dde9d34ad4bcb4d4c83).

Consider a list reference struct [wl\_list](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list "wl_list - Doubly-linked list.") foo\_list, an element type as struct element, and an element's link member as struct [wl\_list](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list "wl_list - Doubly-linked list.") link.

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

The [wl\_list](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list "wl_list - Doubly-linked list.") API provides some iterator macros. For example, to iterate a list in ascending order:

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

This macro expresses a for-each iterator for [wl\_list](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list "wl_list - Doubly-linked list."). Given a list and [wl\_list](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list "wl_list - Doubly-linked list.") link member name (often named link by convention), this macro assigns each element in the list to pos, which can then be referenced in a trailing code block. For example, given a [wl\_list](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list "wl_list - Doubly-linked list.") of struct message elements:

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

*Note: Only removal of the current element, pos, is safe. Removing any other element during traversal may lead to a loop malfunction.* See also: [wl\_list\_for\_each()](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list_1a449407fe3c8f273e38bc2253093cb6fb)

pos

Cursor that each list element will be assigned to

tmp

Temporary pointer of the same type as pos

head

Head of the list to iterate over

member

Name of the link member within the element struct

wl\_list\_for\_each\_reverse - Iterates backwards over a list.

See also: [wl\_list\_for\_each()](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list_1a449407fe3c8f273e38bc2253093cb6fb)

pos

Cursor that each list element will be assigned to

head

Head of the list to iterate over

member

Name of the link member within the element struct

wl\_list\_for\_each\_reverse\_safe - Iterates backwards over a list, safe against removal of the list element.

*Note: Only removal of the current element, pos, is safe. Removing any other element during traversal may lead to a loop malfunction.* See also: [wl\_list\_for\_each()](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list_1a449407fe3c8f273e38bc2253093cb6fb)

pos

Cursor that each list element will be assigned to

tmp

Temporary pointer of the same type as pos

head

Head of the list to iterate over

member

Name of the link member within the element struct

## wl\_message - Protocol message signature.

A [wl\_message](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__message "wl_message - Protocol message signature.") describes the signature of an actual protocol message, such as a request or event, that adheres to the Wayland protocol wire format. The protocol implementation uses a [wl\_message](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__message "wl_message - Protocol message signature.") within its demarshal machinery for decoding messages between a compositor and its clients. In a sense, a [wl\_message](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__message "wl_message - Protocol message signature.") is to a protocol message like a class is to an object.

The name of a [wl\_message](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__message "wl_message - Protocol message signature.") is the name of the corresponding protocol message.

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

While demarshaling primitive arguments is straightforward, when demarshaling messages containing object or new\_id arguments, the protocol implementation often must determine the type of the object. The types of a [wl\_message](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__message "wl_message - Protocol message signature.") is an array of [wl\_interface](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__interface "wl_interface - Protocol object interface.") references that correspond to o and n arguments in signature, with NULL placeholders for arguments with non-object types.

Consider the protocol event [wl\_display](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display "wl_display - Represents a connection to the compositor and acts as a proxy to the wl_display singleton object.") delete\_id that has a single uint argument. The [wl\_message](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__message "wl_message - Protocol message signature.") is:

```
{ "delete_id", "u", [NULL] }
```

Here, the message name is "delete\_id", the signature is "u", and the argument types is \[NULL\], indicating that the uint argument has no corresponding [wl\_interface](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__interface "wl_interface - Protocol object interface.") since it is a primitive argument.

In contrast, consider a wl\_foo interface supporting protocol request bar that has existed since version 2, and has two arguments: a uint and an object of type wl\_baz\_interface that may be NULL. Such a [wl\_message](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__message "wl_message - Protocol message signature.") might be:

```
{ "bar", "2u?o", [NULL, &wl_baz_interface] }
```

Here, the message name is "bar", and the signature is "2u?o". Notice how the 2 indicates the protocol version, the u indicates the first argument type is uint, and the?o indicates that the second argument is an object that may be NULL. Lastly, the argument types array indicates that no [wl\_interface](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__interface "wl_interface - Protocol object interface.") corresponds to the first argument, while the type wl\_baz\_interface corresponds to the second argument.

See also: [wl\_argument](https://wayland.freedesktop.org/docs/html/apb.html#Client-unionwl__argument "wl_argument - Protocol message argument data types.") See also: [wl\_interface](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__interface "wl_interface - Protocol object interface.") See also: Wire Format

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

A [wl\_object](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__object "wl_object - A protocol object.") is an opaque struct identifying the protocol object underlying a [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") or wl\_resource.

*Note: Functions accessing a [wl\_object](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__object "wl_object - A protocol object.") are not normally used by client code. Clients should normally use the higher level interface generated by the scanner to interact with compositor objects.*

## wl\_proxy - Represents a protocol object on the client side.

A [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") acts as a client side proxy to an object existing in the compositor. The proxy is responsible for converting requests made by the clients with [wl\_proxy\_marshal()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy_1aed3b68759dae42a5ec7aca4e2c30c2fd) into Wayland's wire format. Events coming from the compositor are also handled by the proxy, which will in turn call the handler set with [wl\_proxy\_add\_listener()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy_1a4dfac731f4ead73549ccc0795006ed0c).

*Note: With the exception of function [wl\_proxy\_set\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy_1a1bf5804565741df784f9b7e95c675292), functions accessing a [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") are not normally used by client code. Clients should normally use the higher level interface generated by the scanner to interact with compositor objects.*

wl\_proxy\_create - Create a proxy object with a given interface.

```
WL_EXPORT struct wl_proxy * wl_proxy_create(struct wl_proxy *factory, const struct wl_interface *interface)
```

factory

Factory proxy object

interface

Interface the proxy object should use

Returns:

A newly allocated proxy object or NULL on failure

This function creates a new proxy object with the supplied interface. The proxy object will have an id assigned from the client id space. The id should be created on the compositor side by sending an appropriate request with [wl\_proxy\_marshal()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy_1aed3b68759dae42a5ec7aca4e2c30c2fd).

The proxy will inherit the display and event queue of the factory object.

*Note: This should not normally be used by non-generated code.* See also: [wl\_display](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display "wl_display - Represents a connection to the compositor and acts as a proxy to the wl_display singleton object."), [wl\_event\_queue](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__event__queue "wl_event_queue - A queue for wl_proxy object events."), [wl\_proxy\_marshal()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy_1aed3b68759dae42a5ec7aca4e2c30c2fd)

wl\_proxy\_destroy - Destroy a proxy object.

```
WL_EXPORT void wl_proxy_destroy(struct wl_proxy *proxy)
```

proxy

The proxy to be destroyed

proxy must not be a proxy wrapper.

*Note: This function will abort in response to egregious errors, and will do so with the display lock held. This means SIGABRT handlers must not perform any actions that would attempt to take that lock, or a deadlock would occur.*

wl\_proxy\_add\_listener - Set a proxy's listener.

```
WL_EXPORT int wl_proxy_add_listener(struct wl_proxy *proxy, void(**implementation)(void), void *data)
```

proxy

The proxy object

implementation

The listener to be added to proxy

data

User data to be associated with the proxy

Returns:

0 on success or -1 on failure

Set proxy's listener to implementation and its user data to data. If a listener has already been set, this function fails and nothing is changed.

implementation is a vector of function pointers. For an opcode n, implementation\[n\] should point to the handler of n for the given object.

proxy must not be a proxy wrapper.

wl\_proxy\_get\_listener - Get a proxy's listener.

```
WL_EXPORT const void * wl_proxy_get_listener(struct wl_proxy *proxy)
```

proxy

The proxy object

Returns:

The address of the proxy's listener or NULL if no listener is set

Gets the address to the proxy's listener; which is the listener set with [wl\_proxy\_add\_listener](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy_1a4dfac731f4ead73549ccc0795006ed0c).

This function is useful in clients with multiple listeners on the same interface to allow the identification of which code to execute.

If [wl\_proxy\_add\_dispatcher](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy_1a56f0b2216c02b7dbe63b1d6ecaf8bdce) was used, this function returns the dispatcher\_data pointer instead.

wl\_proxy\_add\_dispatcher - Set a proxy's listener (with dispatcher)

```
WL_EXPORT int wl_proxy_add_dispatcher(struct wl_proxy *proxy, wl_dispatcher_func_t dispatcher, const void *implementation, void *data)
```

proxy

The proxy object

dispatcher

The dispatcher to be used for this proxy

implementation

The dispatcher-specific listener implementation

data

User data to be associated with the proxy

Returns:

0 on success or -1 on failure

Set proxy's listener to use dispatcher\_func as its dispatcher and dispatcher\_data as its dispatcher-specific implementation and its user data to data. If a listener has already been set, this function fails and nothing is changed.

The exact details of dispatcher\_data depend on the dispatcher used. This function is intended to be used by language bindings, not user code.

proxy must not be a proxy wrapper.

wl\_proxy\_marshal\_array\_constructor - Prepare a request to be sent to the compositor.

```
WL_EXPORT struct wl_proxy * wl_proxy_marshal_array_constructor(struct wl_proxy *proxy, uint32_t opcode, union wl_argument *args, const struct wl_interface *interface)
```

proxy

The proxy object

opcode

Opcode of the request to be sent

args

Extra arguments for the given request

interface

The interface to use for the new proxy

This function translates a request given an opcode, an interface and a [wl\_argument](https://wayland.freedesktop.org/docs/html/apb.html#Client-unionwl__argument "wl_argument - Protocol message argument data types.") array to the wire format and writes it to the connection buffer.

For new-id arguments, this function will allocate a new [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") and send the ID to the server. The new [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") will be returned on success or NULL on error with errno set accordingly. The newly created proxy will inherit their version from their parent.

*Note: This is intended to be used by language bindings and not in non-generated code.* See also: [wl\_proxy\_marshal()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy_1aed3b68759dae42a5ec7aca4e2c30c2fd)

wl\_proxy\_marshal\_array\_constructor\_versioned - Prepare a request to be sent to the compositor.

```
WL_EXPORT struct wl_proxy * wl_proxy_marshal_array_constructor_versioned(struct wl_proxy *proxy, uint32_t opcode, union wl_argument *args, const struct wl_interface *interface, uint32_t version)
```

proxy

The proxy object

opcode

Opcode of the request to be sent

args

Extra arguments for the given request

interface

The interface to use for the new proxy

version

The protocol object version for the new proxy

Translates the request given by opcode and the extra arguments into the wire format and write it to the connection buffer. This version takes an array of the union type [wl\_argument](https://wayland.freedesktop.org/docs/html/apb.html#Client-unionwl__argument "wl_argument - Protocol message argument data types.").

For new-id arguments, this function will allocate a new [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") and send the ID to the server. The new [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") will be returned on success or NULL on error with errno set accordingly. The newly created proxy will have the version specified.

*Note: This is intended to be used by language bindings and not in non-generated code.* See also: [wl\_proxy\_marshal()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy_1aed3b68759dae42a5ec7aca4e2c30c2fd)

wl\_proxy\_marshal\_flags - Prepare a request to be sent to the compositor.

```
WL_EXPORT struct wl_proxy * wl_proxy_marshal_flags(struct wl_proxy *proxy, uint32_t opcode, const struct wl_interface *interface, uint32_t version, uint32_t flags,...)
```

proxy

The proxy object

opcode

Opcode of the request to be sent

interface

The interface to use for the new proxy

version

The protocol object version of the new proxy

flags

Flags that modify marshalling behaviour

...

Extra arguments for the given request

Returns:

A new [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") for the new\_id argument or NULL on error

Translates the request given by opcode and the extra arguments into the wire format and write it to the connection buffer.

For new-id arguments, this function will allocate a new [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") and send the ID to the server. The new [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") will be returned on success or NULL on error with errno set accordingly. The newly created proxy will have the version specified.

The flag WL\_MARSHAL\_FLAG\_DESTROY may be passed to ensure the proxy is destroyed atomically with the marshalling in order to prevent races that can occur if the display lock is dropped between the marshal and destroy operations.

*Note: This should not normally be used by non-generated code.*

wl\_proxy\_marshal\_array\_flags - Prepare a request to be sent to the compositor.

```
WL_EXPORT struct wl_proxy * wl_proxy_marshal_array_flags(struct wl_proxy *proxy, uint32_t opcode, const struct wl_interface *interface, uint32_t version, uint32_t flags, union wl_argument *args)
```

proxy

The proxy object

opcode

Opcode of the request to be sent

interface

The interface to use for the new proxy

version

The protocol object version for the new proxy

flags

Flags that modify marshalling behaviour

args

Extra arguments for the given request

Translates the request given by opcode and the extra arguments into the wire format and write it to the connection buffer. This version takes an array of the union type [wl\_argument](https://wayland.freedesktop.org/docs/html/apb.html#Client-unionwl__argument "wl_argument - Protocol message argument data types.").

For new-id arguments, this function will allocate a new [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") and send the ID to the server. The new [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") will be returned on success or NULL on error with errno set accordingly. The newly created proxy will have the version specified.

The flag WL\_MARSHAL\_FLAG\_DESTROY may be passed to ensure the proxy is destroyed atomically with the marshalling in order to prevent races that can occur if the display lock is dropped between the marshal and destroy operations.

*Note: This is intended to be used by language bindings and not in non-generated code.* See also: [wl\_proxy\_marshal\_flags()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy_1ad4c41c0e1c92a946206c5b479ebfbe16)

wl\_proxy\_marshal - Prepare a request to be sent to the compositor.

```
WL_EXPORT void wl_proxy_marshal(struct wl_proxy *proxy, uint32_t opcode,...)
```

proxy

The proxy object

opcode

Opcode of the request to be sent

...

Extra arguments for the given request

This function is similar to [wl\_proxy\_marshal\_constructor()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy_1a5c939a7d8545cde6ce0ba62cf64996aa), except it doesn't create proxies for new-id arguments.

*Note: This should not normally be used by non-generated code.* See also: [wl\_proxy\_create()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy_1a9d7a90dbff53e721b76b57331e884977)

wl\_proxy\_marshal\_constructor - Prepare a request to be sent to the compositor.

```
WL_EXPORT struct wl_proxy * wl_proxy_marshal_constructor(struct wl_proxy *proxy, uint32_t opcode, const struct wl_interface *interface,...)
```

proxy

The proxy object

opcode

Opcode of the request to be sent

interface

The interface to use for the new proxy

...

Extra arguments for the given request

Returns:

A new [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") for the new\_id argument or NULL on error

This function translates a request given an opcode, an interface and extra arguments to the wire format and writes it to the connection buffer. The types of the extra arguments must correspond to the argument types of the method associated with the opcode in the interface.

For new-id arguments, this function will allocate a new [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") and send the ID to the server. The new [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") will be returned on success or NULL on error with errno set accordingly. The newly created proxy will inherit their version from their parent.

*Note: This should not normally be used by non-generated code.*

wl\_proxy\_marshal\_constructor\_versioned - Prepare a request to be sent to the compositor.

```
WL_EXPORT struct wl_proxy * wl_proxy_marshal_constructor_versioned(struct wl_proxy *proxy, uint32_t opcode, const struct wl_interface *interface, uint32_t version,...)
```

proxy

The proxy object

opcode

Opcode of the request to be sent

interface

The interface to use for the new proxy

version

The protocol object version of the new proxy

...

Extra arguments for the given request

Returns:

A new [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") for the new\_id argument or NULL on error

Translates the request given by opcode and the extra arguments into the wire format and write it to the connection buffer.

For new-id arguments, this function will allocate a new [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") and send the ID to the server. The new [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") will be returned on success or NULL on error with errno set accordingly. The newly created proxy will have the version specified.

*Note: This should not normally be used by non-generated code.*

wl\_proxy\_marshal\_array - Prepare a request to be sent to the compositor.

```
WL_EXPORT void wl_proxy_marshal_array(struct wl_proxy *proxy, uint32_t opcode, union wl_argument *args)
```

proxy

The proxy object

opcode

Opcode of the request to be sent

args

Extra arguments for the given request

This function is similar to [wl\_proxy\_marshal\_array\_constructor()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy_1a11153751dcc324bebaee4c4f15051fd7), except it doesn't create proxies for new-id arguments.

*Note: This is intended to be used by language bindings and not in non-generated code.* See also: [wl\_proxy\_marshal()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy_1aed3b68759dae42a5ec7aca4e2c30c2fd)

wl\_proxy\_set\_user\_data - Set the user data associated with a proxy.

```
WL_EXPORT void wl_proxy_set_user_data(struct wl_proxy *proxy, void *user_data)
```

proxy

The proxy object

user\_data

The data to be associated with proxy

Set the user data associated with proxy. When events for this proxy are received, user\_data will be supplied to its listener.

wl\_proxy\_get\_user\_data - Get the user data associated with a proxy.

```
WL_EXPORT void * wl_proxy_get_user_data(struct wl_proxy *proxy)
```

Returns:

The user data associated with proxy

wl\_proxy\_get\_version - Get the protocol object version of a proxy object.

```
WL_EXPORT uint32_t wl_proxy_get_version(struct wl_proxy *proxy)
```

proxy

The proxy object

Returns:

The protocol object version of the proxy or 0

Gets the protocol object version of a proxy object, or 0 if the proxy was created with unversioned API.

A returned value of 0 means that no version information is available, so the caller must make safe assumptions about the object's real version.

[wl\_display](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display "wl_display - Represents a connection to the compositor and acts as a proxy to the wl_display singleton object.") 's version will always return 0.

wl\_proxy\_get\_id - Get the id of a proxy object.

```
WL_EXPORT uint32_t wl_proxy_get_id(struct wl_proxy *proxy)
```

Returns:

The id the object associated with the proxy

wl\_proxy\_set\_tag - Set the tag of a proxy object.

```
WL_EXPORT void wl_proxy_set_tag(struct wl_proxy *proxy, const char *const *tag)
```

A toolkit or application can set a unique tag on a proxy in order to identify whether an object is managed by itself or some external part.

To create a tag, the recommended way is to define a statically allocated constant char array containing some descriptive string. The tag will be the pointer to the non-const pointer to the beginning of the array.

For example, to define and set a tag on a surface managed by a certain subsystem: static const char \*my\_tag = "my tag"; wl\_proxy\_set\_tag((struct wl\_proxy \*) surface, &my\_tag);

Then, in a callback with wl\_surface as an argument, in order to check whether it's a surface managed by the same subsystem. const char \* const \*tag; tag = wl\_proxy\_get\_tag((struct wl\_proxy \*) surface); if (tag!= &my\_tag) return;...

For debugging purposes, a tag should be suitable to be included in a debug log entry, e.g. const char \* const \*tag; tag = wl\_proxy\_get\_tag((struct wl\_proxy \*) surface); printf("Got a surface with the tag %p (%s)\\n", tag, (tag && \*tag)? \*tag: "");

proxy

The proxy object

tag

The tag

Since: 1.17.90

wl\_proxy\_get\_tag - Get the tag of a proxy object.

```
WL_EXPORT const char *const  * wl_proxy_get_tag(struct wl_proxy *proxy)
```

See wl\_proxy\_set\_tag for details.

Since: 1.17.90

wl\_proxy\_get\_class - Get the interface name (class) of a proxy object.

```
WL_EXPORT const char * wl_proxy_get_class(struct wl_proxy *proxy)
```

Returns:

The interface name of the object associated with the proxy

wl\_proxy\_get\_interface - Get the interface of a proxy object.

```
WL_EXPORT const struct wl_interface * wl_proxy_get_interface(struct wl_proxy *proxy)
```

Returns:

The interface of the object associated with the proxy

Since: 1.24

wl\_proxy\_get\_display - Get the display of a proxy object.

```
WL_EXPORT struct wl_display * wl_proxy_get_display(struct wl_proxy *proxy)
```

Returns:

The [wl\_display](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display "wl_display - Represents a connection to the compositor and acts as a proxy to the wl_display singleton object.") the proxy is associated with

Since: 1.23

wl\_proxy\_set\_queue - Assign a proxy to an event queue.

```
WL_EXPORT void wl_proxy_set_queue(struct wl_proxy *proxy, struct wl_event_queue *queue)
```

proxy

The proxy object

queue

The event queue that will handle this proxy or NULL

Assign proxy to event queue. Events coming from proxy will be queued in queue from now. If queue is NULL, then the display's default queue is set to the proxy.

In order to guarantee proper handing of all events which were queued before the queue change takes effect, it is required to dispatch the proxy's old event queue after setting a new event queue.

This is particularly important for multi-threaded setups, where it is possible for events to be queued to the proxy's old queue from a different thread during the invocation of this function.

To ensure that all events for a newly created proxy are dispatched on a particular queue, it is necessary to use a proxy wrapper if events are read and dispatched on more than one thread. See [wl\_proxy\_create\_wrapper()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy_1a1edb19b7d532f730c2786a10c2b1032e) for more details.

*Note: By default, the queue set in proxy is the one inherited from parent.* See also: [wl\_display\_dispatch\_queue()](https://wayland.freedesktop.org/docs/html/apb.html#Client-wayland-client-core_8h_1ae027b09801474ac7c6b0f1ef25ff6e17)

wl\_event\_queue\_get\_name - Get the name of an event queue.

```
WL_EXPORT const char * wl_event_queue_get_name(const struct wl_event_queue *queue)
```

Return the human readable name for the event queue

This may be NULL if no name has been set.

wl\_proxy\_create\_wrapper - Create a proxy wrapper for making queue assignments thread-safe.

```
WL_EXPORT void * wl_proxy_create_wrapper(void *proxy)
```

proxy

The proxy object to be wrapped

Returns:

A proxy wrapper for the given proxy or NULL on failure

A proxy wrapper is type of 'struct [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") ' instance that can be used when sending requests instead of using the original proxy. A proxy wrapper does not have an implementation or dispatcher, and events received on the object is still emitted on the original proxy. Trying to set an implementation or dispatcher will have no effect but result in a warning being logged.

Setting the proxy queue of the proxy wrapper will make new objects created using the proxy wrapper use the set proxy queue. Even though there is no implementation nor dispatcher, the proxy queue can be changed. This will affect the default queue of new objects created by requests sent via the proxy wrapper.

A proxy wrapper can only be destroyed using [wl\_proxy\_wrapper\_destroy()](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy_1af9970e116c60117039a0eba1e52b4d08).

A proxy wrapper must be destroyed before the proxy it was created from.

If a user reads and dispatches events on more than one thread, it is necessary to use a proxy wrapper when sending requests on objects when the intention is that a newly created proxy is to use a proxy queue different from the proxy the request was sent on, as creating the new proxy and then setting the queue is not thread safe.

For example, a module that runs using its own proxy queue that needs to do display roundtrip must wrap the [wl\_display](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__display "wl_display - Represents a connection to the compositor and acts as a proxy to the wl_display singleton object.") proxy object before sending the wl\_display.sync request. For example:

```
struct wl_event_queue *queue = ...;
struct wl_display *wrapped_display;
struct wl_callback *callback;

wrapped_display = wl_proxy_create_wrapper(display);
wl_proxy_set_queue((struct wl_proxy *) wrapped_display, queue);
callback = wl_display_sync(wrapped_display);
wl_proxy_wrapper_destroy(wrapped_display);
wl_callback_add_listener(callback, ...);
```

wl\_proxy\_wrapper\_destroy - Destroy a proxy wrapper.

```
WL_EXPORT void wl_proxy_wrapper_destroy(void *proxy_wrapper)
```

proxy\_wrapper

The proxy wrapper to be destroyed

WL\_MARSHAL\_FLAG\_DESTROY - Destroy proxy after marshalling.

## Functions

wl\_event\_queue\_destroy

```
void wl_event_queue_destroy(struct wl_event_queue *queue)
```

wl\_proxy\_marshal\_flags

```
struct wl_proxy * wl_proxy_marshal_flags(struct wl_proxy *proxy, uint32_t opcode, const struct wl_interface *interface, uint32_t version, uint32_t flags,...)
```

wl\_proxy\_marshal\_array\_flags

```
struct wl_proxy * wl_proxy_marshal_array_flags(struct wl_proxy *proxy, uint32_t opcode, const struct wl_interface *interface, uint32_t version, uint32_t flags, union wl_argument *args)
```

wl\_proxy\_marshal

```
void wl_proxy_marshal(struct wl_proxy *p, uint32_t opcode,...)
```

wl\_proxy\_marshal\_array

```
void wl_proxy_marshal_array(struct wl_proxy *p, uint32_t opcode, union wl_argument *args)
```

wl\_proxy\_create

```
struct wl_proxy * wl_proxy_create(struct wl_proxy *factory, const struct wl_interface *interface)
```

wl\_proxy\_create\_wrapper

```
void * wl_proxy_create_wrapper(void *proxy)
```

wl\_proxy\_wrapper\_destroy

```
void wl_proxy_wrapper_destroy(void *proxy_wrapper)
```

wl\_proxy\_marshal\_constructor

```
struct wl_proxy * wl_proxy_marshal_constructor(struct wl_proxy *proxy, uint32_t opcode, const struct wl_interface *interface,...)
```

wl\_proxy\_marshal\_constructor\_versioned

```
struct wl_proxy * wl_proxy_marshal_constructor_versioned(struct wl_proxy *proxy, uint32_t opcode, const struct wl_interface *interface, uint32_t version,...)
```

wl\_proxy\_marshal\_array\_constructor

```
struct wl_proxy * wl_proxy_marshal_array_constructor(struct wl_proxy *proxy, uint32_t opcode, union wl_argument *args, const struct wl_interface *interface)
```

wl\_proxy\_marshal\_array\_constructor\_versioned

```
struct wl_proxy * wl_proxy_marshal_array_constructor_versioned(struct wl_proxy *proxy, uint32_t opcode, union wl_argument *args, const struct wl_interface *interface, uint32_t version)
```

wl\_proxy\_destroy

```
void wl_proxy_destroy(struct wl_proxy *proxy)
```

wl\_proxy\_add\_listener

```
int wl_proxy_add_listener(struct wl_proxy *proxy, void(**implementation)(void), void *data)
```

wl\_proxy\_get\_listener

```
const void * wl_proxy_get_listener(struct wl_proxy *proxy)
```

wl\_proxy\_add\_dispatcher

```
int wl_proxy_add_dispatcher(struct wl_proxy *proxy, wl_dispatcher_func_t dispatcher_func, const void *dispatcher_data, void *data)
```

wl\_proxy\_set\_user\_data

```
void wl_proxy_set_user_data(struct wl_proxy *proxy, void *user_data)
```

wl\_proxy\_get\_user\_data

```
void * wl_proxy_get_user_data(struct wl_proxy *proxy)
```

wl\_proxy\_get\_version

```
uint32_t wl_proxy_get_version(struct wl_proxy *proxy)
```

wl\_proxy\_get\_id

```
uint32_t wl_proxy_get_id(struct wl_proxy *proxy)
```

wl\_proxy\_set\_tag

```
void wl_proxy_set_tag(struct wl_proxy *proxy, const char *const *tag)
```

wl\_proxy\_get\_tag

```
const char *const  * wl_proxy_get_tag(struct wl_proxy *proxy)
```

wl\_proxy\_get\_class

```
const char * wl_proxy_get_class(struct wl_proxy *proxy)
```

wl\_proxy\_get\_interface

```
const struct wl_interface * wl_proxy_get_interface(struct wl_proxy *proxy)
```

wl\_proxy\_get\_display

```
struct wl_display * wl_proxy_get_display(struct wl_proxy *proxy)
```

wl\_proxy\_set\_queue

```
void wl_proxy_set_queue(struct wl_proxy *proxy, struct wl_event_queue *queue)
```

wl\_proxy\_get\_queue - Get a proxy's event queue.

```
struct wl_event_queue * wl_proxy_get_queue(const struct wl_proxy *proxy)
```

Return the event queue

wl\_event\_queue\_get\_name

```
const char * wl_event_queue_get_name(const struct wl_event_queue *queue)
```

wl\_display\_connect

```
struct wl_display * wl_display_connect(const char *name)
```

wl\_display\_connect\_to\_fd

```
struct wl_display * wl_display_connect_to_fd(int fd)
```

wl\_display\_disconnect

```
void wl_display_disconnect(struct wl_display *display)
```

wl\_display\_get\_fd

```
int wl_display_get_fd(struct wl_display *display)
```

wl\_display\_dispatch

```
int wl_display_dispatch(struct wl_display *display)
```

wl\_display\_dispatch\_queue

```
int wl_display_dispatch_queue(struct wl_display *display, struct wl_event_queue *queue)
```

wl\_display\_dispatch\_timeout

```
int wl_display_dispatch_timeout(struct wl_display *display, const struct timespec *timeout)
```

wl\_display\_dispatch\_queue\_timeout

```
int wl_display_dispatch_queue_timeout(struct wl_display *display, struct wl_event_queue *queue, const struct timespec *timeout)
```

wl\_display\_dispatch\_queue\_pending

```
int wl_display_dispatch_queue_pending(struct wl_display *display, struct wl_event_queue *queue)
```

wl\_display\_dispatch\_queue\_pending\_single

```
int wl_display_dispatch_queue_pending_single(struct wl_display *display, struct wl_event_queue *queue)
```

wl\_display\_dispatch\_pending

```
int wl_display_dispatch_pending(struct wl_display *display)
```

wl\_display\_dispatch\_pending\_single

```
int wl_display_dispatch_pending_single(struct wl_display *display)
```

wl\_display\_get\_error

```
int wl_display_get_error(struct wl_display *display)
```

wl\_display\_get\_protocol\_error

```
uint32_t wl_display_get_protocol_error(struct wl_display *display, const struct wl_interface **interface, uint32_t *id)
```

wl\_display\_flush

```
int wl_display_flush(struct wl_display *display)
```

wl\_display\_roundtrip\_queue

```
int wl_display_roundtrip_queue(struct wl_display *display, struct wl_event_queue *queue)
```

wl\_display\_roundtrip

```
int wl_display_roundtrip(struct wl_display *display)
```

wl\_display\_create\_queue

```
struct wl_event_queue * wl_display_create_queue(struct wl_display *display)
```

wl\_display\_create\_queue\_with\_name

```
struct wl_event_queue * wl_display_create_queue_with_name(struct wl_display *display, const char *name)
```

wl\_display\_prepare\_read\_queue

```
int wl_display_prepare_read_queue(struct wl_display *display, struct wl_event_queue *queue)
```

wl\_display\_prepare\_read

```
int wl_display_prepare_read(struct wl_display *display)
```

wl\_display\_cancel\_read

```
void wl_display_cancel_read(struct wl_display *display)
```

wl\_display\_read\_events

```
int wl_display_read_events(struct wl_display *display)
```

wl\_log\_set\_handler\_client

```
void wl_log_set_handler_client(wl_log_func_t handler)
```

wl\_display\_set\_max\_buffer\_size

```
void wl_display_set_max_buffer_size(struct wl_display *display, size_t max_buffer_size)
```

wl\_display\_dispatch\_timeout

```
WL_EXPORT int wl_display_dispatch_timeout(struct wl_display *display, const struct timespec *timeout)
```

wl\_proxy\_get\_queue - Get a proxy's event queue.

```
WL_EXPORT struct wl_event_queue * wl_proxy_get_queue(const struct wl_proxy *proxy)
```

Return the event queue

wl\_log\_set\_handler\_client

```
WL_EXPORT void wl_log_set_handler_client(wl_log_func_t handler)
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

This macro allows "conversion" from a pointer to a member to its containing struct. This is useful if you have a contained item like a [wl\_list](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__list "wl_list - Doubly-linked list."), wl\_listener, or wl\_signal, provided via a callback or other means, and would like to retrieve the struct that contains it.

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

See also: wl\_client\_for\_each\_resource\_iterator\_func\_t See also: wl\_client\_for\_each\_resource

wl\_fixed\_t - Fixed-point number.

```
typedef int32_t wl_fixed_t
```

A [wl\_fixed\_t](https://wayland.freedesktop.org/docs/html/apb.html#Client-wayland-util_8h_1a546c8b2b06f97d0617000db4fb4feeeb) is a 24.8 signed fixed-point number with a sign bit, 23 bits of integer precision and 8 bits of decimal precision. Consider [wl\_fixed\_t](https://wayland.freedesktop.org/docs/html/apb.html#Client-wayland-util_8h_1a546c8b2b06f97d0617000db4fb4feeeb) as an opaque struct with methods that facilitate conversion to and from double and int types.

wl\_dispatcher\_func\_t - Dispatcher function type alias.

```
typedef int(* wl_dispatcher_func_t) (const void *user_data, void *target, uint32_t opcode, const struct wl_message *msg, union wl_argument *args))(const void *user_data, void *target, uint32_t opcode, const struct wl_message *msg, union wl_argument *args)
```

A dispatcher is a function that handles the emitting of callbacks in client code. For programs directly using the C library, this is done by using libffi to call function pointers. When binding to languages other than C, dispatchers provide a way to abstract the function calling process to be friendlier to other function calling systems.

A dispatcher takes five arguments: The first is the dispatcher-specific implementation associated with the target object. The second is the object upon which the callback is being invoked (either [wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") or wl\_resource). The third and fourth arguments are the opcode and the [wl\_message](https://wayland.freedesktop.org/docs/html/apb.html#Client-structwl__message "wl_message - Protocol message signature.") corresponding to the callback. The final argument is an array of arguments received from the other process via the wire protocol.

user\_data

Dispatcher-specific implementation data

target

Callback invocation target ([wl\_proxy](https://wayland.freedesktop.org/docs/html/apb.html#Client-classwl__proxy "wl_proxy - Represents a protocol object on the client side.") or wl\_resource)

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

The C implementation of the Wayland protocol abstracts the details of logging. Users may customize the logging behavior, with a function conforming to the [wl\_log\_func\_t](https://wayland.freedesktop.org/docs/html/apb.html#Client-wayland-util_8h_1a84c4dc362eef1933db82226459636f2d) type, via wl\_log\_set\_handler\_client and wl\_log\_set\_handler\_server.

A [wl\_log\_func\_t](https://wayland.freedesktop.org/docs/html/apb.html#Client-wayland-util_8h_1a84c4dc362eef1933db82226459636f2d) must conform to the expectations of vprintf, and expects two arguments: a string to write and a corresponding variable argument list. While the string to write may contain format specifiers and use values in the variable argument list, the behavior of any [wl\_log\_func\_t](https://wayland.freedesktop.org/docs/html/apb.html#Client-wayland-util_8h_1a84c4dc362eef1933db82226459636f2d) depends on the implementation.

*Note: Take care to not confuse this with wl\_protocol\_logger\_func\_t, which is a specific server-side logger for requests and events.*

fmt

String to write to the log, containing optional format specifiers

args

Variable argument list

See also: [wl\_log\_set\_handler\_client](https://wayland.freedesktop.org/docs/html/apb.html#Client-wayland-client_8c_1a7a75b7351a49ca12159c49875e1a74dd) See also: wl\_log\_set\_handler\_server

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
