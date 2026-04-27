---
title: "Appendix A. Wayland Protocol Specification"
source: "https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_display"
author:
published:
created: 2026-04-25
description:
tags:
  - "clippings"
---

Copyright © 2008-2011 Kristian Høgsberg
Copyright © 2010-2011 Intel Corporation
Copyright © 2012-2013 Collabora, Ltd.

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice (including the
next paragraph) shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## wl\_display - core global object

The core global object. This is a special singleton object. It is used for internal Wayland protocol features.

### Requests provided by wl\_display

#### wl\_display::sync - asynchronous roundtrip

callback

id for the new [wl\_callback](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_callback "wl_callback - callback object") - callback object for the sync request

The sync request asks the server to emit the 'done' event on the returned wl\_callback object. Since requests are handled in-order and events are delivered in-order, this can be used as a barrier to ensure all previous requests and the resulting events have been handled.

The object returned by this request will be destroyed by the compositor after the callback is fired and as such the client must not attempt to use it after that point.

The callback\_data passed in the callback is undefined and should be ignored.

#### wl\_display::get\_registry - get global registry object

registry

id for the new [wl\_registry](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_registry "wl_registry - global registry object") - global registry object

This request creates a registry object that allows the client to list and bind the global objects available from the compositor.

It should be noted that the server side resources consumed in response to a get\_registry request can only be released when the client disconnects, not when the client side proxy is destroyed. Therefore, clients should invoke get\_registry as infrequently as possible to avoid wasting memory.

### Events provided by wl\_display

#### wl\_display::error - fatal error event

object\_id

object - object where the error occurred

code

uint - error code

message

string - error description

The error event is sent out when a fatal (non-recoverable) error has occurred. The object\_id argument is the object where the error occurred, most often in response to a request to that object. The code identifies the error and is defined by the object interface. As such, each interface defines its own set of error codes. The message is a brief description of the error, for (debugging) convenience.

#### wl\_display::delete\_id - acknowledge object ID deletion

id

uint - deleted object ID

This event is used internally by the object ID management logic. When a client deletes an object that it had created, the server will send this event to acknowledge that it has seen the delete request. When the client receives this event, it will know that it can safely reuse the object ID.

### Enums provided by wl\_display

#### wl\_display::error - global error values

These errors are global and can be emitted in response to any server request.

invalid\_object

0 - server couldn't find object

invalid\_method

1 - method doesn't exist on the specified interface or malformed request

no\_memory

2 - server is out of memory

implementation

3 - implementation error in compositor

## wl\_registry - global registry object

The singleton global registry object. The server has a number of global objects that are available to all clients. These objects typically represent an actual object in the server (for example, an input device) or they are singleton objects that provide extension functionality.

When a client creates a registry object, the registry object will emit a global event for each global currently in the registry. Globals come and go as a result of device or monitor hotplugs, reconfiguration or other events, and the registry will send out global and global\_remove events to keep the client up to date with the changes. To mark the end of the initial burst of events, the client can use the wl\_display.sync request immediately after calling wl\_display.get\_registry.

A client can bind to a global object by using the bind request. This creates a client-side handle that lets the object emit events to the client and lets the client invoke requests on the object.

### Requests provided by wl\_registry

#### wl\_registry::bind - bind an object to the display

name

uint - unique numeric name of the object

id

new\_id - bounded object

Binds a new, client-created object to the server using the specified name as the identifier.

### Events provided by wl\_registry

#### wl\_registry::global - announce global object

name

uint - numeric name of the global object

interface

string - interface implemented by the object

version

uint - interface version

Notify the client of global objects.

The event notifies the client that a global object with the given name is now available, and it implements the given version of the given interface.

#### wl\_registry::global\_remove - announce removal of global object

name

uint - numeric name of the global object

Notify the client of removed global objects.

This event notifies the client that the global identified by name is no longer available. If the client bound to the global using the bind request, the client should now destroy that object.

The object remains valid and requests to the object will be ignored until the client destroys it, to avoid races between the global going away and a client sending a request to it.

## wl\_callback - callback object

Clients can handle the 'done' event to get notified when the related request is done.

Note, because wl\_callback objects are created from multiple independent factory interfaces, the wl\_callback interface is frozen at version 1.

### Events provided by wl\_callback

#### wl\_callback::done - done event

callback\_data

uint - request-specific data for the callback

Notify the client when the related request is done.

## wl\_compositor - the compositor singleton

A compositor. This object is a singleton global. The compositor is in charge of combining the contents of multiple surfaces into one displayable output.

### Requests provided by wl\_compositor

#### wl\_compositor::create\_surface - create new surface

id

id for the new [wl\_surface](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface "wl_surface - an onscreen surface") - the new surface

Ask the compositor to create a new surface.

#### wl\_compositor::create\_region - create new region

id

id for the new [wl\_region](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_region "wl_region - region interface") - the new region

Ask the compositor to create a new region.

#### wl\_compositor::release - destroy wl\_compositor

This request destroys the wl\_compositor. This has no effect on any other objects.

## wl\_shm\_pool - a shared memory pool

The wl\_shm\_pool object encapsulates a piece of memory shared between the compositor and client. Through the wl\_shm\_pool object, the client can allocate shared memory wl\_buffer objects. All objects created through the same pool share the same underlying mapped memory. Reusing the mapped memory avoids the setup/teardown overhead and is useful when interactively resizing a surface or for many small buffers.

### Requests provided by wl\_shm\_pool

#### wl\_shm\_pool::create\_buffer - create a buffer from the pool

id

id for the new [wl\_buffer](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_buffer "wl_buffer - content for a wl_surface") - buffer to create

offset

int - buffer byte offset within the pool

width

int - buffer width, in pixels

height

int - buffer height, in pixels

stride

int - number of bytes from the beginning of one row to the beginning of the next row

format

[wl\_shm::format](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_shm-enum-format "wl_shm::format - pixel formats") (uint) - buffer pixel format

Create a wl\_buffer object from the pool.

The buffer is created offset bytes into the pool and has width and height as specified. The stride argument specifies the number of bytes from the beginning of one row to the beginning of the next. The format is the pixel format of the buffer and must be one of those advertised through the wl\_shm.format event.

A buffer will keep a reference to the pool it was created from so it is valid to destroy the pool immediately after creating a buffer from it.

#### wl\_shm\_pool::destroy - destroy the pool

Destroy the shared memory pool.

The mmapped memory will be released when all buffers that have been created from this pool are gone.

#### wl\_shm\_pool::resize - change the size of the pool mapping

size

int - new size of the pool, in bytes

This request will cause the server to remap the backing memory for the pool from the file descriptor passed when the pool was created, but using the new size. This request can only be used to make the pool bigger.

This request only changes the amount of bytes that are mmapped by the server and does not touch the file corresponding to the file descriptor passed at creation time. It is the client's responsibility to ensure that the file is at least as big as the new pool size.

## wl\_shm - shared memory support

A singleton global object that provides support for shared memory.

Clients can create wl\_shm\_pool objects using the create\_pool request.

On binding the wl\_shm object one or more format events are emitted to inform clients about the valid pixel formats that can be used for buffers.

### Requests provided by wl\_shm

#### wl\_shm::create\_pool - create a shm pool

id

id for the new [wl\_shm\_pool](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_shm_pool "wl_shm_pool - a shared memory pool") - pool to create

fd

fd - file descriptor for the pool

size

int - pool size, in bytes

Create a new wl\_shm\_pool object.

The pool can be used to create shared memory based buffer objects. The server will mmap size bytes of the passed file descriptor, to use as backing memory for the pool.

#### wl\_shm::release - release the shm object

Using this request a client can tell the server that it is not going to use the shm object anymore.

Objects created via this interface remain unaffected.

### Events provided by wl\_shm

#### wl\_shm::format - pixel format description

format

[wl\_shm::format](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_shm-enum-format "wl_shm::format - pixel formats") (uint) - buffer pixel format

Informs the client about a valid pixel format that can be used for buffers. Known formats include argb8888 and xrgb8888.

Extensions to drm\_fourcc.h (or the format enum) do not require increasing the wl\_shm version; as a result, clients may receive format codes which were not in the list at the time the client was made.

### Enums provided by wl\_shm

#### wl\_shm::error - wl\_shm error values

These errors can be emitted in response to wl\_shm requests.

invalid\_format

0 - buffer format is not known

invalid\_stride

1 - invalid size or stride during pool or buffer creation

invalid\_fd

2 - mmapping the file descriptor failed

#### wl\_shm::format - pixel formats

This describes the memory layout of an individual pixel.

All renderers should support argb8888 and xrgb8888 but any other formats are optional and may not be supported by the particular renderer in use.

The drm format codes match the macros defined in drm\_fourcc.h, except argb8888 and xrgb8888. The formats actually supported by the compositor will be reported by the format event. See drm\_fourcc.h for more detailed format descriptions.

For all wl\_shm formats and unless specified in another protocol extension, pre-multiplied alpha is used for pixel values.

argb8888

0 - 32-bit ARGB format, \[31:0\] A:R:G:B 8:8:8:8 little endian

xrgb8888

1 - 32-bit RGB format, \[31:0\] x:R:G:B 8:8:8:8 little endian

c8

0x20203843 - 8-bit color index format, \[7:0\] C

rgb332

0x38424752 - 8-bit RGB format, \[7:0\] R:G:B 3:3:2

bgr233

0x38524742 - 8-bit BGR format, \[7:0\] B:G:R 2:3:3

xrgb4444

0x32315258 - 16-bit xRGB format, \[15:0\] x:R:G:B 4:4:4:4 little endian

xbgr4444

0x32314258 - 16-bit xBGR format, \[15:0\] x:B:G:R 4:4:4:4 little endian

rgbx4444

0x32315852 - 16-bit RGBx format, \[15:0\] R:G:B:x 4:4:4:4 little endian

bgrx4444

0x32315842 - 16-bit BGRx format, \[15:0\] B:G:R:x 4:4:4:4 little endian

argb4444

0x32315241 - 16-bit ARGB format, \[15:0\] A:R:G:B 4:4:4:4 little endian

abgr4444

0x32314241 - 16-bit ABGR format, \[15:0\] A:B:G:R 4:4:4:4 little endian

rgba4444

0x32314152 - 16-bit RBGA format, \[15:0\] R:G:B:A 4:4:4:4 little endian

bgra4444

0x32314142 - 16-bit BGRA format, \[15:0\] B:G:R:A 4:4:4:4 little endian

xrgb1555

0x35315258 - 16-bit xRGB format, \[15:0\] x:R:G:B 1:5:5:5 little endian

xbgr1555

0x35314258 - 16-bit xBGR 1555 format, \[15:0\] x:B:G:R 1:5:5:5 little endian

rgbx5551

0x35315852 - 16-bit RGBx 5551 format, \[15:0\] R:G:B:x 5:5:5:1 little endian

bgrx5551

0x35315842 - 16-bit BGRx 5551 format, \[15:0\] B:G:R:x 5:5:5:1 little endian

argb1555

0x35315241 - 16-bit ARGB 1555 format, \[15:0\] A:R:G:B 1:5:5:5 little endian

abgr1555

0x35314241 - 16-bit ABGR 1555 format, \[15:0\] A:B:G:R 1:5:5:5 little endian

rgba5551

0x35314152 - 16-bit RGBA 5551 format, \[15:0\] R:G:B:A 5:5:5:1 little endian

bgra5551

0x35314142 - 16-bit BGRA 5551 format, \[15:0\] B:G:R:A 5:5:5:1 little endian

rgb565

0x36314752 - 16-bit RGB 565 format, \[15:0\] R:G:B 5:6:5 little endian

bgr565

0x36314742 - 16-bit BGR 565 format, \[15:0\] B:G:R 5:6:5 little endian

rgb888

0x34324752 - 24-bit RGB format, \[23:0\] R:G:B little endian

bgr888

0x34324742 - 24-bit BGR format, \[23:0\] B:G:R little endian

xbgr8888

0x34324258 - 32-bit xBGR format, \[31:0\] x:B:G:R 8:8:8:8 little endian

rgbx8888

0x34325852 - 32-bit RGBx format, \[31:0\] R:G:B:x 8:8:8:8 little endian

bgrx8888

0x34325842 - 32-bit BGRx format, \[31:0\] B:G:R:x 8:8:8:8 little endian

abgr8888

0x34324241 - 32-bit ABGR format, \[31:0\] A:B:G:R 8:8:8:8 little endian

rgba8888

0x34324152 - 32-bit RGBA format, \[31:0\] R:G:B:A 8:8:8:8 little endian

bgra8888

0x34324142 - 32-bit BGRA format, \[31:0\] B:G:R:A 8:8:8:8 little endian

xrgb2101010

0x30335258 - 32-bit xRGB format, \[31:0\] x:R:G:B 2:10:10:10 little endian

xbgr2101010

0x30334258 - 32-bit xBGR format, \[31:0\] x:B:G:R 2:10:10:10 little endian

rgbx1010102

0x30335852 - 32-bit RGBx format, \[31:0\] R:G:B:x 10:10:10:2 little endian

bgrx1010102

0x30335842 - 32-bit BGRx format, \[31:0\] B:G:R:x 10:10:10:2 little endian

argb2101010

0x30335241 - 32-bit ARGB format, \[31:0\] A:R:G:B 2:10:10:10 little endian

abgr2101010

0x30334241 - 32-bit ABGR format, \[31:0\] A:B:G:R 2:10:10:10 little endian

rgba1010102

0x30334152 - 32-bit RGBA format, \[31:0\] R:G:B:A 10:10:10:2 little endian

bgra1010102

0x30334142 - 32-bit BGRA format, \[31:0\] B:G:R:A 10:10:10:2 little endian

yuyv

0x56595559 - packed YCbCr format, \[31:0\] Cr0:Y1:Cb0:Y0 8:8:8:8 little endian

yvyu

0x55595659 - packed YCbCr format, \[31:0\] Cb0:Y1:Cr0:Y0 8:8:8:8 little endian

uyvy

0x59565955 - packed YCbCr format, \[31:0\] Y1:Cr0:Y0:Cb0 8:8:8:8 little endian

vyuy

0x59555956 - packed YCbCr format, \[31:0\] Y1:Cb0:Y0:Cr0 8:8:8:8 little endian

ayuv

0x56555941 - packed AYCbCr format, \[31:0\] A:Y:Cb:Cr 8:8:8:8 little endian

nv12

0x3231564e - 2 plane YCbCr Cr:Cb format, 2x2 subsampled Cr:Cb plane

nv21

0x3132564e - 2 plane YCbCr Cb:Cr format, 2x2 subsampled Cb:Cr plane

nv16

0x3631564e - 2 plane YCbCr Cr:Cb format, 2x1 subsampled Cr:Cb plane

nv61

0x3136564e - 2 plane YCbCr Cb:Cr format, 2x1 subsampled Cb:Cr plane

yuv410

0x39565559 - 3 plane YCbCr format, 4x4 subsampled Cb (1) and Cr (2) planes

yvu410

0x39555659 - 3 plane YCbCr format, 4x4 subsampled Cr (1) and Cb (2) planes

yuv411

0x31315559 - 3 plane YCbCr format, 4x1 subsampled Cb (1) and Cr (2) planes

yvu411

0x31315659 - 3 plane YCbCr format, 4x1 subsampled Cr (1) and Cb (2) planes

yuv420

0x32315559 - 3 plane YCbCr format, 2x2 subsampled Cb (1) and Cr (2) planes

yvu420

0x32315659 - 3 plane YCbCr format, 2x2 subsampled Cr (1) and Cb (2) planes

yuv422

0x36315559 - 3 plane YCbCr format, 2x1 subsampled Cb (1) and Cr (2) planes

yvu422

0x36315659 - 3 plane YCbCr format, 2x1 subsampled Cr (1) and Cb (2) planes

yuv444

0x34325559 - 3 plane YCbCr format, non-subsampled Cb (1) and Cr (2) planes

yvu444

0x34325659 - 3 plane YCbCr format, non-subsampled Cr (1) and Cb (2) planes

r8

0x20203852 - \[7:0\] R

r16

0x20363152 - \[15:0\] R little endian

rg88

0x38384752 - \[15:0\] R:G 8:8 little endian

gr88

0x38385247 - \[15:0\] G:R 8:8 little endian

rg1616

0x32334752 - \[31:0\] R:G 16:16 little endian

gr1616

0x32335247 - \[31:0\] G:R 16:16 little endian

xrgb16161616f

0x48345258 - \[63:0\] x:R:G:B 16:16:16:16 little endian

xbgr16161616f

0x48344258 - \[63:0\] x:B:G:R 16:16:16:16 little endian

argb16161616f

0x48345241 - \[63:0\] A:R:G:B 16:16:16:16 little endian

abgr16161616f

0x48344241 - \[63:0\] A:B:G:R 16:16:16:16 little endian

xyuv8888

0x56555958 - \[31:0\] X:Y:Cb:Cr 8:8:8:8 little endian

vuy888

0x34325556 - \[23:0\] Cr:Cb:Y 8:8:8 little endian

vuy101010

0x30335556 - Y followed by U then V, 10:10:10. Non-linear modifier only

y210

0x30313259 - \[63:0\] Cr0:0:Y1:0:Cb0:0:Y0:0 10:6:10:6:10:6:10:6 little endian per 2 Y pixels

y212

0x32313259 - \[63:0\] Cr0:0:Y1:0:Cb0:0:Y0:0 12:4:12:4:12:4:12:4 little endian per 2 Y pixels

y216

0x36313259 - \[63:0\] Cr0:Y1:Cb0:Y0 16:16:16:16 little endian per 2 Y pixels

y410

0x30313459 - \[31:0\] A:Cr:Y:Cb 2:10:10:10 little endian

y412

0x32313459 - \[63:0\] A:0:Cr:0:Y:0:Cb:0 12:4:12:4:12:4:12:4 little endian

y416

0x36313459 - \[63:0\] A:Cr:Y:Cb 16:16:16:16 little endian

xvyu2101010

0x30335658 - \[31:0\] X:Cr:Y:Cb 2:10:10:10 little endian

xvyu12\_16161616

0x36335658 - \[63:0\] X:0:Cr:0:Y:0:Cb:0 12:4:12:4:12:4:12:4 little endian

xvyu16161616

0x38345658 - \[63:0\] X:Cr:Y:Cb 16:16:16:16 little endian

y0l0

0x304c3059 - \[63:0\] A3:A2:Y3:0:Cr0:0:Y2:0:A1:A0:Y1:0:Cb0:0:Y0:0 1:1:8:2:8:2:8:2:1:1:8:2:8:2:8:2 little endian

x0l0

0x304c3058 - \[63:0\] X3:X2:Y3:0:Cr0:0:Y2:0:X1:X0:Y1:0:Cb0:0:Y0:0 1:1:8:2:8:2:8:2:1:1:8:2:8:2:8:2 little endian

y0l2

0x324c3059 - \[63:0\] A3:A2:Y3:Cr0:Y2:A1:A0:Y1:Cb0:Y0 1:1:10:10:10:1:1:10:10:10 little endian

x0l2

0x324c3058 - \[63:0\] X3:X2:Y3:Cr0:Y2:X1:X0:Y1:Cb0:Y0 1:1:10:10:10:1:1:10:10:10 little endian

yuv420\_8bit

0x38305559

yuv420\_10bit

0x30315559

xrgb8888\_a8

0x38415258

xbgr8888\_a8

0x38414258

rgbx8888\_a8

0x38415852

bgrx8888\_a8

0x38415842

rgb888\_a8

0x38413852

bgr888\_a8

0x38413842

rgb565\_a8

0x38413552

bgr565\_a8

0x38413542

nv24

0x3432564e - non-subsampled Cr:Cb plane

nv42

0x3234564e - non-subsampled Cb:Cr plane

p210

0x30313250 - 2x1 subsampled Cr:Cb plane, 10 bit per channel

p010

0x30313050 - 2x2 subsampled Cr:Cb plane 10 bits per channel

p012

0x32313050 - 2x2 subsampled Cr:Cb plane 12 bits per channel

p016

0x36313050 - 2x2 subsampled Cr:Cb plane 16 bits per channel

axbxgxrx106106106106

0x30314241 - \[63:0\] A:x:B:x:G:x:R:x 10:6:10:6:10:6:10:6 little endian

nv15

0x3531564e - 2x2 subsampled Cr:Cb plane

q410

0x30313451

q401

0x31303451

xrgb16161616

0x38345258 - \[63:0\] x:R:G:B 16:16:16:16 little endian

xbgr16161616

0x38344258 - \[63:0\] x:B:G:R 16:16:16:16 little endian

argb16161616

0x38345241 - \[63:0\] A:R:G:B 16:16:16:16 little endian

abgr16161616

0x38344241 - \[63:0\] A:B:G:R 16:16:16:16 little endian

c1

0x20203143 - \[7:0\] C0:C1:C2:C3:C4:C5:C6:C7 1:1:1:1:1:1:1:1 eight pixels/byte

c2

0x20203243 - \[7:0\] C0:C1:C2:C3 2:2:2:2 four pixels/byte

c4

0x20203443 - \[7:0\] C0:C1 4:4 two pixels/byte

d1

0x20203144 - \[7:0\] D0:D1:D2:D3:D4:D5:D6:D7 1:1:1:1:1:1:1:1 eight pixels/byte

d2

0x20203244 - \[7:0\] D0:D1:D2:D3 2:2:2:2 four pixels/byte

d4

0x20203444 - \[7:0\] D0:D1 4:4 two pixels/byte

d8

0x20203844 - \[7:0\] D

r1

0x20203152 - \[7:0\] R0:R1:R2:R3:R4:R5:R6:R7 1:1:1:1:1:1:1:1 eight pixels/byte

r2

0x20203252 - \[7:0\] R0:R1:R2:R3 2:2:2:2 four pixels/byte

r4

0x20203452 - \[7:0\] R0:R1 4:4 two pixels/byte

r10

0x20303152 - \[15:0\] x:R 6:10 little endian

r12

0x20323152 - \[15:0\] x:R 4:12 little endian

avuy8888

0x59555641 - \[31:0\] A:Cr:Cb:Y 8:8:8:8 little endian

xvuy8888

0x59555658 - \[31:0\] X:Cr:Cb:Y 8:8:8:8 little endian

p030

0x30333050 - 2x2 subsampled Cr:Cb plane 10 bits per channel packed

rgb161616

0x38344752 - \[47:0\] R:G:B 16:16:16 little endian

bgr161616

0x38344742 - \[47:0\] B:G:R 16:16:16 little endian

r16f

0x48202052 - \[15:0\] R 16 little endian

gr1616f

0x48205247 - \[31:0\] G:R 16:16 little endian

bgr161616f

0x48524742 - \[47:0\] B:G:R 16:16:16 little endian

r32f

0x46202052 - \[31:0\] R 32 little endian

gr3232f

0x46205247 - \[63:0\] R:G 32:32 little endian

bgr323232f

0x46524742 - \[95:0\] R:G:B 32:32:32 little endian

abgr32323232f

0x46384241 - \[127:0\] R:G:B:A 32:32:32:32 little endian

nv20

0x3032564e - 2x1 subsampled Cr:Cb plane

nv30

0x3033564e - non-subsampled Cr:Cb plane

s010

0x30313053 - 2x2 subsampled Cb (1) and Cr (2) planes 10 bits per channel

s210

0x30313253 - 2x1 subsampled Cb (1) and Cr (2) planes 10 bits per channel

s410

0x30313453 - non-subsampled Cb (1) and Cr (2) planes 10 bits per channel

s012

0x32313053 - 2x2 subsampled Cb (1) and Cr (2) planes 12 bits per channel

s212

0x32313253 - 2x1 subsampled Cb (1) and Cr (2) planes 12 bits per channel

s412

0x32313453 - non-subsampled Cb (1) and Cr (2) planes 12 bits per channel

s016

0x36313053 - 2x2 subsampled Cb (1) and Cr (2) planes 16 bits per channel

s216

0x36313253 - 2x1 subsampled Cb (1) and Cr (2) planes 16 bits per channel

s416

0x36313453 - non-subsampled Cb (1) and Cr (2) planes 16 bits per channel

## wl\_buffer - content for a wl\_surface

A buffer provides the content for a wl\_surface. Buffers are created through factory interfaces such as wl\_shm, wp\_linux\_buffer\_params (from the linux-dmabuf protocol extension) or similar. It has a width and a height and can be attached to a wl\_surface, but the mechanism by which a client provides and updates the contents is defined by the buffer factory interface.

Color channels are assumed to be electrical rather than optical (in other words, encoded with a transfer function) unless otherwise specified. If the buffer uses a format that has an alpha channel, the alpha channel is assumed to be premultiplied into the electrical color channel values (after transfer function encoding) unless otherwise specified.

Note, because wl\_buffer objects are created from multiple independent factory interfaces, the wl\_buffer interface is frozen at version 1.

### Requests provided by wl\_buffer

#### wl\_buffer::destroy - destroy a buffer

Destroy a buffer. If and how you need to release the backing storage is defined by the buffer factory interface.

For possible side-effects to a surface, see wl\_surface.attach.

### Events provided by wl\_buffer

#### wl\_buffer::release - compositor releases buffer

Sent when this wl\_buffer is no longer used by the compositor.

For more information on when release events may or may not be sent, and what consequences it has, please see the description of wl\_surface.attach.

If a client receives a release event before the frame callback requested in the same wl\_surface.commit that attaches this wl\_buffer to a surface, then the client is immediately free to reuse the buffer and its backing storage, and does not need a second buffer for the next surface content update. Typically this is possible, when the compositor maintains a copy of the wl\_surface contents, e.g. as a GL texture. This is an important optimization for GL(ES) compositors with wl\_shm clients.

## wl\_data\_offer - offer to transfer data

A wl\_data\_offer represents a piece of data offered for transfer by another client (the source client). It is used by the copy-and-paste and drag-and-drop mechanisms. The offer describes the different mime types that the data can be converted to and provides the mechanism for transferring the data directly from the source client.

### Requests provided by wl\_data\_offer

#### wl\_data\_offer::accept - accept one of the offered mime types

serial

uint - serial number of the accept request

mime\_type

string - mime type accepted by the client

Indicate that the client can accept the given mime type, or NULL for not accepted.

For objects of version 2 or older, this request is used by the client to give feedback whether the client can receive the given mime type, or NULL if none is accepted; the feedback does not determine whether the drag-and-drop operation succeeds or not.

For objects of version 3 or newer, this request determines the final result of the drag-and-drop operation. If the end result is that no mime types were accepted, the drag-and-drop operation will be cancelled and the corresponding drag source will receive wl\_data\_source.cancelled. Clients may still use this event in conjunction with wl\_data\_source.action for feedback.

#### wl\_data\_offer::receive - request that the data is transferred

mime\_type

string - mime type desired by receiver

fd

fd - file descriptor for data transfer

To transfer the offered data, the client issues this request and indicates the mime type it wants to receive. The transfer happens through the passed file descriptor (typically created with the pipe system call). The source client writes the data in the mime type representation requested and then closes the file descriptor.

The receiving client reads from the read end of the pipe until EOF and then closes its end, at which point the transfer is complete.

This request may happen multiple times for different mime types, both before and after wl\_data\_device.drop. Drag-and-drop destination clients may preemptively fetch data or examine it more closely to determine acceptance.

#### wl\_data\_offer::destroy - destroy data offer

Destroy the data offer.

#### wl\_data\_offer::finish - the offer will no longer be used

Notifies the compositor that the drag destination successfully finished the drag-and-drop operation.

Upon receiving this request, the compositor will emit wl\_data\_source.dnd\_finished on the drag source client.

It is a client error to perform other requests than wl\_data\_offer.destroy after this one. It is also an error to perform this request after a NULL mime type has been set in wl\_data\_offer.accept or no action was received through wl\_data\_offer.action.

If wl\_data\_offer.finish request is received for a non drag and drop operation, the invalid\_finish protocol error is raised.

#### wl\_data\_offer::set\_actions - set the available/preferred drag-and-drop actions

dnd\_actions

[wl\_data\_device\_manager::dnd\_action](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_data_device_manager-enum-dnd_action "wl_data_device_manager::dnd_action - bitfield - drag and drop actions") (uint) - actions supported by the destination client

preferred\_action

[wl\_data\_device\_manager::dnd\_action](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_data_device_manager-enum-dnd_action "wl_data_device_manager::dnd_action - bitfield - drag and drop actions") (uint) - action preferred by the destination client

Sets the actions that the destination side client supports for this operation. This request may trigger the emission of wl\_data\_source.action and wl\_data\_offer.action events if the compositor needs to change the selected action.

This request can be called multiple times throughout the drag-and-drop operation, typically in response to wl\_data\_device.enter or wl\_data\_device.motion events.

This request determines the final result of the drag-and-drop operation. If the end result is that no action is accepted, the drag source will receive wl\_data\_source.cancelled.

The dnd\_actions argument must contain only values expressed in the wl\_data\_device\_manager.dnd\_actions enum, and the preferred\_action argument must only contain one of those values set, otherwise it will result in a protocol error.

While managing an "ask" action, the destination drag-and-drop client may perform further wl\_data\_offer.receive requests, and is expected to perform one last wl\_data\_offer.set\_actions request with a preferred action other than "ask" (and optionally wl\_data\_offer.accept) before requesting wl\_data\_offer.finish, in order to convey the action selected by the user. If the preferred action is not in the wl\_data\_offer.source\_actions mask, an error will be raised.

If the "ask" action is dismissed (e.g. user cancellation), the client is expected to perform wl\_data\_offer.destroy right away.

This request can only be made on drag-and-drop offers, a protocol error will be raised otherwise.

### Events provided by wl\_data\_offer

#### wl\_data\_offer::offer - advertise offered mime type

mime\_type

string - offered mime type

Sent immediately after creating the wl\_data\_offer object. One event per offered mime type.

#### wl\_data\_offer::source\_actions - notify the source-side available actions

source\_actions

[wl\_data\_device\_manager::dnd\_action](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_data_device_manager-enum-dnd_action "wl_data_device_manager::dnd_action - bitfield - drag and drop actions") (uint) - actions offered by the data source

This event indicates the actions offered by the data source. It will be sent immediately after creating the wl\_data\_offer object, or anytime the source side changes its offered actions through wl\_data\_source.set\_actions.

#### wl\_data\_offer::action - notify the selected action

dnd\_action

[wl\_data\_device\_manager::dnd\_action](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_data_device_manager-enum-dnd_action "wl_data_device_manager::dnd_action - bitfield - drag and drop actions") (uint) - action selected by the compositor

This event indicates the action selected by the compositor after matching the source/destination side actions. Only one action (or none) will be offered here.

This event can be emitted multiple times during the drag-and-drop operation in response to destination side action changes through wl\_data\_offer.set\_actions.

This event will no longer be emitted after wl\_data\_device.drop happened on the drag-and-drop destination, the client must honor the last action received, or the last preferred one set through wl\_data\_offer.set\_actions when handling an "ask" action.

Compositors may also change the selected action on the fly, mainly in response to keyboard modifier changes during the drag-and-drop operation.

The most recent action received is always the valid one. Prior to receiving wl\_data\_device.drop, the chosen action may change (e.g. due to keyboard modifiers being pressed). At the time of receiving wl\_data\_device.drop the drag-and-drop destination must honor the last action received.

Action changes may still happen after wl\_data\_device.drop, especially on "ask" actions, where the drag-and-drop destination may choose another action afterwards. Action changes happening at this stage are always the result of inter-client negotiation, the compositor shall no longer be able to induce a different action.

Upon "ask" actions, it is expected that the drag-and-drop destination may potentially choose a different action and/or mime type, based on wl\_data\_offer.source\_actions and finally chosen by the user (e.g. popping up a menu with the available options). The final wl\_data\_offer.set\_actions and wl\_data\_offer.accept requests must happen before the call to wl\_data\_offer.finish.

### Enums provided by wl\_data\_offer

#### wl\_data\_offer::error

invalid\_finish

0 - finish request was called untimely

invalid\_action\_mask

1 - action mask contains invalid values

invalid\_action

2 - action argument has an invalid value

invalid\_offer

3 - offer doesn't accept this request

## wl\_data\_source - offer to transfer data

The wl\_data\_source object is the source side of a wl\_data\_offer. It is created by the source client in a data transfer and provides a way to describe the offered data and a way to respond to requests to transfer the data.

### Requests provided by wl\_data\_source

#### wl\_data\_source::offer - add an offered mime type

mime\_type

string - mime type offered by the data source

This request adds a mime type to the set of mime types advertised to targets. Can be called several times to offer multiple types.

#### wl\_data\_source::destroy - destroy the data source

Destroy the data source.

#### wl\_data\_source::set\_actions - set the available drag-and-drop actions

dnd\_actions

[wl\_data\_device\_manager::dnd\_action](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_data_device_manager-enum-dnd_action "wl_data_device_manager::dnd_action - bitfield - drag and drop actions") (uint) - actions supported by the data source

Sets the actions that the source side client supports for this operation. This request may trigger wl\_data\_source.action and wl\_data\_offer.action events if the compositor needs to change the selected action.

The dnd\_actions argument must contain only values expressed in the wl\_data\_device\_manager.dnd\_actions enum, otherwise it will result in a protocol error.

This request must be made once only, and can only be made on sources used in drag-and-drop, so it must be performed before wl\_data\_device.start\_drag. Attempting to use the source other than for drag-and-drop will raise a protocol error.

### Events provided by wl\_data\_source

#### wl\_data\_source::target - a target accepts an offered mime type

mime\_type

string - mime type accepted by the target

Sent when a target accepts pointer\_focus or motion events. If a target does not accept any of the offered types, type is NULL.

Used for feedback during drag-and-drop.

#### wl\_data\_source::send - send the data

mime\_type

string - mime type for the data

fd

fd - file descriptor for the data

Request for data from the client. Send the data as the specified mime type over the passed file descriptor, then close it.

#### wl\_data\_source::cancelled - selection was cancelled

This data source is no longer valid. There are several reasons why this could happen:

\- The data source has been replaced by another data source. - The drag-and-drop operation was performed, but the drop destination did not accept any of the mime types offered through wl\_data\_source.target. - The drag-and-drop operation was performed, but the drop destination did not select any of the actions present in the mask offered through wl\_data\_source.action. - The drag-and-drop operation was performed but didn't happen over a surface. - The compositor cancelled the drag-and-drop operation (e.g. compositor dependent timeouts to avoid stale drag-and-drop transfers).

The client should clean up and destroy this data source.

For objects of version 2 or older, wl\_data\_source.cancelled will only be emitted if the data source was replaced by another data source.

#### wl\_data\_source::dnd\_drop\_performed - the drag-and-drop operation physically finished

The user performed the drop action. This event does not indicate acceptance, wl\_data\_source.cancelled may still be emitted afterwards if the drop destination does not accept any mime type.

However, this event might however not be received if the compositor cancelled the drag-and-drop operation before this event could happen.

Note that the data\_source may still be used in the future and should not be destroyed here.

#### wl\_data\_source::dnd\_finished - the drag-and-drop operation concluded

The drop destination finished interoperating with this data source, so the client is now free to destroy this data source and free all associated data.

If the action used to perform the operation was "move", the source can now delete the transferred data.

#### wl\_data\_source::action - notify the selected action

dnd\_action

[wl\_data\_device\_manager::dnd\_action](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_data_device_manager-enum-dnd_action "wl_data_device_manager::dnd_action - bitfield - drag and drop actions") (uint) - action selected by the compositor

This event indicates the action selected by the compositor after matching the source/destination side actions. Only one action (or none) will be offered here.

This event can be emitted multiple times during the drag-and-drop operation, mainly in response to destination side changes through wl\_data\_offer.set\_actions, and as the data device enters/leaves surfaces.

It is only possible to receive this event after wl\_data\_source.dnd\_drop\_performed if the drag-and-drop operation ended in an "ask" action, in which case the final wl\_data\_source.action event will happen immediately before wl\_data\_source.dnd\_finished.

Compositors may also change the selected action on the fly, mainly in response to keyboard modifier changes during the drag-and-drop operation.

The most recent action received is always the valid one. The chosen action may change alongside negotiation (e.g. an "ask" action can turn into a "move" operation), so the effects of the final action must always be applied in wl\_data\_offer.dnd\_finished.

Clients can trigger cursor surface changes from this point, so they reflect the current action.

### Enums provided by wl\_data\_source

#### wl\_data\_source::error

invalid\_action\_mask

0 - action mask contains invalid values

invalid\_source

1 - source doesn't accept this request

## wl\_data\_device - data transfer device

There is one wl\_data\_device per seat which can be obtained from the global wl\_data\_device\_manager singleton.

A wl\_data\_device provides access to inter-client data transfer mechanisms such as copy-and-paste and drag-and-drop.

### Requests provided by wl\_data\_device

#### wl\_data\_device::start\_drag - start drag-and-drop operation

source

[wl\_data\_source](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_data_source "wl_data_source - offer to transfer data") - data source for the eventual transfer

origin

[wl\_surface](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface "wl_surface - an onscreen surface") - surface where the drag originates

icon

[wl\_surface](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface "wl_surface - an onscreen surface") - drag-and-drop icon surface

serial

uint - serial number of the implicit grab on the origin

This request asks the compositor to start a drag-and-drop operation on behalf of the client.

The source argument is the data source that provides the data for the eventual data transfer. If source is NULL, enter, leave and motion events are sent only to the client that initiated the drag and the client is expected to handle the data passing internally. If source is destroyed, the drag-and-drop session will be cancelled.

The origin surface is the surface where the drag originates and the client must have an active implicit grab that matches the serial.

The icon surface is an optional (can be NULL) surface that provides an icon to be moved around with the cursor. Initially, the top-left corner of the icon surface is placed at the cursor hotspot, but subsequent wl\_surface.offset requests can move the relative position. Attach requests must be confirmed with wl\_surface.commit as usual. The icon surface is given the role of a drag-and-drop icon. If the icon surface already has another role, it raises a protocol error.

The input region is ignored for wl\_surfaces with the role of a drag-and-drop icon.

The given source may not be used in any further set\_selection or start\_drag requests. Attempting to reuse a previously-used source may send a used\_source error.

#### wl\_data\_device::set\_selection - copy data to the selection

source

[wl\_data\_source](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_data_source "wl_data_source - offer to transfer data") - data source for the selection

serial

uint - serial number of the event that triggered this request

This request asks the compositor to set the selection to the data from the source on behalf of the client.

To unset the selection, set the source to NULL.

The given source may not be used in any further set\_selection or start\_drag requests. Attempting to reuse a previously-used source may send a used\_source error.

#### wl\_data\_device::release - destroy data device

This request destroys the data device.

### Events provided by wl\_data\_device

#### wl\_data\_device::data\_offer - introduce a new wl\_data\_offer

id

id for the new [wl\_data\_offer](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_data_offer "wl_data_offer - offer to transfer data") - the new data\_offer object

The data\_offer event introduces a new wl\_data\_offer object, which will subsequently be used in either the data\_device.enter event (for drag-and-drop) or the data\_device.selection event (for selections). Immediately following the data\_device.data\_offer event, the new data\_offer object will send out data\_offer.offer events to describe the mime types it offers.

#### wl\_data\_device::enter - initiate drag-and-drop session

serial

uint - serial number of the enter event

surface

[wl\_surface](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface "wl_surface - an onscreen surface") - client surface entered

x

fixed - surface-local x coordinate

y

fixed - surface-local y coordinate

id

[wl\_data\_offer](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_data_offer "wl_data_offer - offer to transfer data") - source data\_offer object

This event is sent when an active drag-and-drop pointer enters a surface owned by the client. The position of the pointer at enter time is provided by the x and y arguments, in surface-local coordinates.

#### wl\_data\_device::leave - end drag-and-drop session

This event is sent when the drag-and-drop pointer leaves the surface and the session ends. The client must destroy the wl\_data\_offer introduced at enter time at this point.

#### wl\_data\_device::motion - drag-and-drop session motion

time

uint - timestamp with millisecond granularity

x

fixed - surface-local x coordinate

y

fixed - surface-local y coordinate

This event is sent when the drag-and-drop pointer moves within the currently focused surface. The new position of the pointer is provided by the x and y arguments, in surface-local coordinates.

#### wl\_data\_device::drop - end drag-and-drop session successfully

The event is sent when a drag-and-drop operation is ended because the implicit grab is removed.

The drag-and-drop destination is expected to honor the last action received through wl\_data\_offer.action, if the resulting action is "copy" or "move", the destination can still perform wl\_data\_offer.receive requests, and is expected to end all transfers with a wl\_data\_offer.finish request.

If the resulting action is "ask", the action will not be considered final. The drag-and-drop destination is expected to perform one last wl\_data\_offer.set\_actions request, or wl\_data\_offer.destroy in order to cancel the operation.

#### wl\_data\_device::selection - advertise new selection

id

[wl\_data\_offer](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_data_offer "wl_data_offer - offer to transfer data") - selection data\_offer object

The selection event is sent out to notify the client of a new wl\_data\_offer for the selection for this device. The data\_device.data\_offer and the data\_offer.offer events are sent out immediately before this event to introduce the data offer object. The selection event is sent to a client immediately before receiving keyboard focus and when a new selection is set while the client has keyboard focus. The data\_offer is valid until a new data\_offer or NULL is received or until the client loses keyboard focus. Switching surface with keyboard focus within the same client doesn't mean a new selection will be sent. The client must destroy the previous selection data\_offer, if any, upon receiving this event.

### Enums provided by wl\_data\_device

#### wl\_data\_device::error

role

0 - given wl\_surface has another role

used\_source

1 - source has already been used

## wl\_data\_device\_manager - data transfer interface

The wl\_data\_device\_manager is a singleton global object that provides access to inter-client data transfer mechanisms such as copy-and-paste and drag-and-drop. These mechanisms are tied to a wl\_seat and this interface lets a client get a wl\_data\_device corresponding to a wl\_seat.

Depending on the version bound, the objects created from the bound wl\_data\_device\_manager object will have different requirements for functioning properly. See wl\_data\_source.set\_actions, wl\_data\_offer.accept and wl\_data\_offer.finish for details.

### Requests provided by wl\_data\_device\_manager

#### wl\_data\_device\_manager::create\_data\_source - create a new data source

id

id for the new [wl\_data\_source](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_data_source "wl_data_source - offer to transfer data") - data source to create

Create a new data source.

#### wl\_data\_device\_manager::get\_data\_device - create a new data device

id

id for the new [wl\_data\_device](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_data_device "wl_data_device - data transfer device") - data device to create

seat

[wl\_seat](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_seat "wl_seat - group of input devices") - seat associated with the data device

Create a new data device for a given seat.

#### wl\_data\_device\_manager::release - destroy wl\_data\_device\_manager

This request destroys the wl\_data\_device\_manager. This has no effect on any other objects.

### Enums provided by wl\_data\_device\_manager

#### wl\_data\_device\_manager::dnd\_action - bitfield - drag and drop actions

This is a bitmask of the available/preferred actions in a drag-and-drop operation.

In the compositor, the selected action is a result of matching the actions offered by the source and destination sides. "action" events with a "none" action will be sent to both source and destination if there is no match. All further checks will effectively happen on (source actions ∩ destination actions).

In addition, compositors may also pick different actions in reaction to key modifiers being pressed. One common design that is used in major toolkits (and the behavior recommended for compositors) is:

\- If no modifiers are pressed, the first match (in bit order) will be used. - Pressing Shift selects "move", if enabled in the mask. - Pressing Control selects "copy", if enabled in the mask.

Behavior beyond that is considered implementation-dependent. Compositors may for example bind other modifiers (like Alt/Meta) or drags initiated with other buttons than BTN\_LEFT to specific actions (e.g. "ask").

none

0 - no action

copy

1 - copy action

move

2 - move action

ask

4 - ask action

## wl\_shell - create desktop-style surfaces

This interface is implemented by servers that provide desktop-style user interfaces.

It allows clients to associate a wl\_shell\_surface with a basic surface.

Note! This protocol is deprecated and not intended for production use. For desktop-style user interfaces, use xdg\_shell. Compositors and clients should not implement this interface.

### Requests provided by wl\_shell

#### wl\_shell::get\_shell\_surface - create a shell surface from a surface

id

id for the new [wl\_shell\_surface](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_shell_surface "wl_shell_surface - desktop-style metadata interface") - shell surface to create

surface

[wl\_surface](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface "wl_surface - an onscreen surface") - surface to be given the shell surface role

Create a shell surface for an existing surface. This gives the wl\_surface the role of a shell surface. If the wl\_surface already has another role, it raises a protocol error.

Only one shell surface can be associated with a given surface.

### Enums provided by wl\_shell

#### wl\_shell::error

role

0 - given wl\_surface has another role

## wl\_shell\_surface - desktop-style metadata interface

An interface that may be implemented by a wl\_surface, for implementations that provide a desktop-style user interface.

It provides requests to treat surfaces like toplevel, fullscreen or popup windows, move, resize or maximize them, associate metadata like title and class, etc.

On the server side the object is automatically destroyed when the related wl\_surface is destroyed. On the client side, wl\_shell\_surface\_destroy() must be called before destroying the wl\_surface object.

### Requests provided by wl\_shell\_surface

#### wl\_shell\_surface::pong - respond to a ping event

serial

uint - serial number of the ping event

A client must respond to a ping event with a pong request or the client may be deemed unresponsive.

#### wl\_shell\_surface::move - start an interactive move

seat

[wl\_seat](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_seat "wl_seat - group of input devices") - seat whose pointer is used

serial

uint - serial number of the implicit grab on the pointer

Start a pointer-driven move of the surface.

This request must be used in response to a button press event. The server may ignore move requests depending on the state of the surface (e.g. fullscreen or maximized).

#### wl\_shell\_surface::resize - start an interactive resize

seat

[wl\_seat](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_seat "wl_seat - group of input devices") - seat whose pointer is used

serial

uint - serial number of the implicit grab on the pointer

edges

[wl\_shell\_surface::resize](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_shell_surface-enum-resize "wl_shell_surface::resize - bitfield - edge values for resizing") (uint) - which edge or corner is being dragged

Start a pointer-driven resizing of the surface.

This request must be used in response to a button press event. The server may ignore resize requests depending on the state of the surface (e.g. fullscreen or maximized).

#### wl\_shell\_surface::set\_toplevel - make the surface a toplevel surface

Map the surface as a toplevel surface.

A toplevel surface is not fullscreen, maximized or transient.

#### wl\_shell\_surface::set\_transient - make the surface a transient surface

parent

[wl\_surface](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface "wl_surface - an onscreen surface") - parent surface

x

int - surface-local x coordinate

y

int - surface-local y coordinate

flags

[wl\_shell\_surface::transient](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_shell_surface-enum-transient "wl_shell_surface::transient - bitfield - details of transient behaviour") (uint) - transient surface behavior

Map the surface relative to an existing surface.

The x and y arguments specify the location of the upper left corner of the surface relative to the upper left corner of the parent surface, in surface-local coordinates.

The flags argument controls details of the transient behaviour.

#### wl\_shell\_surface::set\_fullscreen - make the surface a fullscreen surface

method

[wl\_shell\_surface::fullscreen\_method](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_shell_surface-enum-fullscreen_method "wl_shell_surface::fullscreen_method - different method to set the surface fullscreen") (uint) - method for resolving size conflict

framerate

uint - framerate in mHz

output

[wl\_output](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_output "wl_output - compositor output region") - output on which the surface is to be fullscreen

Map the surface as a fullscreen surface.

If an output parameter is given then the surface will be made fullscreen on that output. If the client does not specify the output then the compositor will apply its policy - usually choosing the output on which the surface has the biggest surface area.

The client may specify a method to resolve a size conflict between the output size and the surface size - this is provided through the method parameter.

The framerate parameter is used only when the method is set to "driver", to indicate the preferred framerate. A value of 0 indicates that the client does not care about framerate. The framerate is specified in mHz, that is framerate of 60000 is 60Hz.

A method of "scale" or "driver" implies a scaling operation of the surface, either via a direct scaling operation or a change of the output mode. This will override any kind of output scaling, so that mapping a surface with a buffer size equal to the mode can fill the screen independent of buffer\_scale.

A method of "fill" means we don't scale up the buffer, however any output scale is applied. This means that you may run into an edge case where the application maps a buffer with the same size of the output mode but buffer\_scale 1 (thus making a surface larger than the output). In this case it is allowed to downscale the results to fit the screen.

The compositor must reply to this request with a configure event with the dimensions for the output on which the surface will be made fullscreen.

#### wl\_shell\_surface::set\_popup - make the surface a popup surface

seat

[wl\_seat](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_seat "wl_seat - group of input devices") - seat whose pointer is used

serial

uint - serial number of the implicit grab on the pointer

parent

[wl\_surface](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface "wl_surface - an onscreen surface") - parent surface

x

int - surface-local x coordinate

y

int - surface-local y coordinate

flags

[wl\_shell\_surface::transient](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_shell_surface-enum-transient "wl_shell_surface::transient - bitfield - details of transient behaviour") (uint) - transient surface behavior

Map the surface as a popup.

A popup surface is a transient surface with an added pointer grab.

An existing implicit grab will be changed to owner-events mode, and the popup grab will continue after the implicit grab ends (i.e. releasing the mouse button does not cause the popup to be unmapped).

The popup grab continues until the window is destroyed or a mouse button is pressed in any other client's window. A click in any of the client's surfaces is reported as normal, however, clicks in other clients' surfaces will be discarded and trigger the callback.

The x and y arguments specify the location of the upper left corner of the surface relative to the upper left corner of the parent surface, in surface-local coordinates.

#### wl\_shell\_surface::set\_maximized - make the surface a maximized surface

output

[wl\_output](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_output "wl_output - compositor output region") - output on which the surface is to be maximized

Map the surface as a maximized surface.

If an output parameter is given then the surface will be maximized on that output. If the client does not specify the output then the compositor will apply its policy - usually choosing the output on which the surface has the biggest surface area.

The compositor will reply with a configure event telling the expected new surface size. The operation is completed on the next buffer attach to this surface.

A maximized surface typically fills the entire output it is bound to, except for desktop elements such as panels. This is the main difference between a maximized shell surface and a fullscreen shell surface.

The details depend on the compositor implementation.

#### wl\_shell\_surface::set\_title - set surface title

title

string - surface title

Set a short title for the surface.

This string may be used to identify the surface in a task bar, window list, or other user interface elements provided by the compositor.

The string must be encoded in UTF-8.

#### wl\_shell\_surface::set\_class - set surface class

class\_

string - surface class

Set a class for the surface.

The surface class identifies the general class of applications to which the surface belongs. A common convention is to use the file name (or the full path if it is a non-standard location) of the application's.desktop file as the class.

### Events provided by wl\_shell\_surface

#### wl\_shell\_surface::ping - ping client

serial

uint - serial number of the ping

Ping a client to check if it is receiving events and sending requests. A client is expected to reply with a pong request.

#### wl\_shell\_surface::configure - suggest resize

edges

[wl\_shell\_surface::resize](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_shell_surface-enum-resize "wl_shell_surface::resize - bitfield - edge values for resizing") (uint) - how the surface was resized

width

int - new width of the surface

height

int - new height of the surface

The configure event asks the client to resize its surface.

The size is a hint, in the sense that the client is free to ignore it if it doesn't resize, pick a smaller size (to satisfy aspect ratio or resize in steps of NxM pixels).

The edges parameter provides a hint about how the surface was resized. The client may use this information to decide how to adjust its content to the new size (e.g. a scrolling area might adjust its content position to leave the viewable content unmoved).

The client is free to dismiss all but the last configure event it received.

The width and height arguments specify the size of the window in surface-local coordinates.

#### wl\_shell\_surface::popup\_done - popup interaction is done

The popup\_done event is sent out when a popup grab is broken, that is, when the user clicks a surface that doesn't belong to the client owning the popup surface.

### Enums provided by wl\_shell\_surface

#### wl\_shell\_surface::resize - bitfield - edge values for resizing

These values are used to indicate which edge of a surface is being dragged in a resize operation. The server may use this information to adapt its behavior, e.g. choose an appropriate cursor image.

none

0 - no edge

top

1 - top edge

bottom

2 - bottom edge

left

4 - left edge

top\_left

5 - top and left edges

bottom\_left

6 - bottom and left edges

right

8 - right edge

top\_right

9 - top and right edges

bottom\_right

10 - bottom and right edges

#### wl\_shell\_surface::transient - bitfield - details of transient behaviour

These flags specify details of the expected behaviour of transient surfaces. Used in the set\_transient request.

inactive

0x1 - do not set keyboard focus

#### wl\_shell\_surface::fullscreen\_method - different method to set the surface fullscreen

Hints to indicate to the compositor how to deal with a conflict between the dimensions of the surface and the dimensions of the output. The compositor is free to ignore this parameter.

default

0 - no preference, apply default policy

scale

1 - scale, preserve the surface's aspect ratio and center on output

driver

2 - switch output mode to the smallest mode that can fit the surface, add black borders to compensate size mismatch

fill

3 - no upscaling, center on output and add black borders to compensate size mismatch

## wl\_surface - an onscreen surface

A surface is a rectangular area that may be displayed on zero or more outputs, and shown any number of times at the compositor's discretion. They can present wl\_buffers, receive user input, and define a local coordinate system.

The size of a surface (and relative positions on it) is described in surface-local coordinates, which may differ from the buffer coordinates of the pixel content, in case a buffer\_transform or a buffer\_scale is used.

A surface without a "role" is fairly useless: a compositor does not know where, when or how to present it. The role is the purpose of a wl\_surface. Examples of roles are a cursor for a pointer (as set by wl\_pointer.set\_cursor), a drag icon (wl\_data\_device.start\_drag), a sub-surface (wl\_subcompositor.get\_subsurface), and a window as defined by a shell protocol (e.g. wl\_shell.get\_shell\_surface).

A surface can have only one role at a time. Initially a wl\_surface does not have a role. Once a wl\_surface is given a role, it is set permanently for the whole lifetime of the wl\_surface object. Giving the current role again is allowed, unless explicitly forbidden by the relevant interface specification.

Surface roles are given by requests in other interfaces such as wl\_pointer.set\_cursor. The request should explicitly mention that this request gives a role to a wl\_surface. Often, this request also creates a new protocol object that represents the role and adds additional functionality to wl\_surface. When a client wants to destroy a wl\_surface, they must destroy this role object before the wl\_surface, otherwise a defunct\_role\_object error is sent.

Destroying the role object does not remove the role from the wl\_surface, but it may stop the wl\_surface from "playing the role". For instance, if a wl\_subsurface object is destroyed, the wl\_surface it was created for will be unmapped and forget its position and z-order. It is allowed to create a wl\_subsurface for the same wl\_surface again, but it is not allowed to use the wl\_surface as a cursor (cursor is a different role than sub-surface, and role switching is not allowed).

### Requests provided by wl\_surface

#### wl\_surface::destroy - delete surface

Deletes the surface and invalidates its object ID.

#### wl\_surface::attach - set the surface contents

buffer

[wl\_buffer](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_buffer "wl_buffer - content for a wl_surface") - buffer of surface contents

x

int - surface-local x coordinate

y

int - surface-local y coordinate

Set a buffer as the content of this surface.

The new size of the surface is calculated based on the buffer size transformed by the inverse buffer\_transform and the inverse buffer\_scale. This means that at commit time the supplied buffer size must be an integer multiple of the buffer\_scale. If that's not the case, an invalid\_size error is sent.

The x and y arguments specify the location of the new pending buffer's upper left corner, relative to the current buffer's upper left corner, in surface-local coordinates. In other words, the x and y, combined with the new surface size define in which directions the surface's size changes. Setting anything other than 0 as x and y arguments is discouraged, and should instead be replaced with using the separate wl\_surface.offset request.

When the bound wl\_surface version is 5 or higher, passing any non-zero x or y is a protocol violation, and will result in an 'invalid\_offset' error being raised. The x and y arguments are ignored and do not change the pending state. To achieve equivalent semantics, use wl\_surface.offset.

Surface contents are double-buffered state, see wl\_surface.commit.

The initial surface contents are void; there is no content. wl\_surface.attach assigns the given wl\_buffer as the pending wl\_buffer. wl\_surface.commit makes the pending wl\_buffer the new surface contents, and the size of the surface becomes the size calculated from the wl\_buffer, as described above. After commit, there is no pending buffer until the next attach.

Committing a pending wl\_buffer allows the compositor to read the pixels in the wl\_buffer. The compositor may access the pixels at any time after the wl\_surface.commit request. When the compositor will not access the pixels anymore, it will send the wl\_buffer.release event. Only after receiving wl\_buffer.release, the client may reuse the wl\_buffer. A wl\_buffer that has been attached and then replaced by another attach instead of committed will not receive a release event, and is not used by the compositor.

If a pending wl\_buffer has been committed to more than one wl\_surface, the delivery of wl\_buffer.release events becomes undefined. A well behaved client should not rely on wl\_buffer.release events in this case. Instead, clients hitting this case should use wl\_surface.get\_release or use a protocol extension providing per-commit release notifications (if none of these options are available, a fallback can be implemented by creating multiple wl\_buffer objects from the same backing storage).

Destroying the wl\_buffer after wl\_buffer.release does not change the surface contents. Destroying the wl\_buffer before wl\_buffer.release is allowed as long as the underlying buffer storage isn't re-used (this can happen e.g. on client process termination). However, if the client destroys the wl\_buffer before receiving the wl\_buffer.release event and mutates the underlying buffer storage, the surface contents become undefined immediately.

If wl\_surface.attach is sent with a NULL wl\_buffer, the following wl\_surface.commit will remove the surface content.

If a pending wl\_buffer has been destroyed, the result is not specified. Many compositors are known to remove the surface content on the following wl\_surface.commit, but this behaviour is not universal. Clients seeking to maximise compatibility should not destroy pending buffers and should ensure that they explicitly remove content from surfaces, even after destroying buffers.

#### wl\_surface::damage - mark part of the surface damaged

x

int - surface-local x coordinate

y

int - surface-local y coordinate

width

int - width of damage rectangle

height

int - height of damage rectangle

This request is used to describe the regions where the pending buffer is different from the current surface contents, and where the surface therefore needs to be repainted. The compositor ignores the parts of the damage that fall outside of the surface.

Damage is double-buffered state, see wl\_surface.commit.

The damage rectangle is specified in surface-local coordinates, where x and y specify the upper left corner of the damage rectangle.

The initial value for pending damage is empty: no damage. wl\_surface.damage adds pending damage: the new pending damage is the union of old pending damage and the given rectangle.

wl\_surface.commit assigns pending damage as the current damage, and clears pending damage. The server will clear the current damage as it repaints the surface.

Note! New clients should not use this request. Instead damage can be posted with wl\_surface.damage\_buffer which uses buffer coordinates instead of surface coordinates.

#### wl\_surface::frame - request a frame throttling hint

callback

id for the new [wl\_callback](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_callback "wl_callback - callback object") - callback object for the frame request

Request a notification when it is a good time to start drawing a new frame, by creating a frame callback. This is useful for throttling redrawing operations, and driving animations.

When a client is animating on a wl\_surface, it can use the 'frame' request to get notified when it is a good time to draw and commit the next frame of animation. If the client commits an update earlier than that, it is likely that some updates will not make it to the display, and the client is wasting resources by drawing too often.

The frame request will take effect on the next wl\_surface.commit. The notification will only be posted for one frame unless requested again. For a wl\_surface, the notifications are posted in the order the frame requests were committed.

The server must send the notifications so that a client will not send excessive updates, while still allowing the highest possible update rate for clients that wait for the reply before drawing again. The server should give some time for the client to draw and commit after sending the frame callback events to let it hit the next output refresh.

A server should avoid signaling the frame callbacks if the surface is not visible in any way, e.g. the surface is off-screen, or completely obscured by other opaque surfaces.

The object returned by this request will be destroyed by the compositor after the callback is fired and as such the client must not attempt to use it after that point.

The callback\_data passed in the callback is the current time, in milliseconds, with an undefined base.

#### wl\_surface::set\_opaque\_region - set opaque region

region

[wl\_region](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_region "wl_region - region interface") - opaque region of the surface

This request sets the region of the surface that contains opaque content.

The opaque region is an optimization hint for the compositor that lets it optimize the redrawing of content behind opaque regions. Setting an opaque region is not required for correct behaviour, but marking transparent content as opaque will result in repaint artifacts.

The opaque region is specified in surface-local coordinates.

The compositor ignores the parts of the opaque region that fall outside of the surface.

Opaque region is double-buffered state, see wl\_surface.commit.

wl\_surface.set\_opaque\_region changes the pending opaque region. wl\_surface.commit copies the pending region to the current region. Otherwise, the pending and current regions are never changed.

The initial value for an opaque region is empty. Setting the pending opaque region has copy semantics, and the wl\_region object can be destroyed immediately. A NULL wl\_region causes the pending opaque region to be set to empty.

#### wl\_surface::set\_input\_region - set input region

region

[wl\_region](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_region "wl_region - region interface") - input region of the surface

This request sets the region of the surface that can receive pointer and touch events.

Input events happening outside of this region will try the next surface in the server surface stack. The compositor ignores the parts of the input region that fall outside of the surface.

The input region is specified in surface-local coordinates.

Input region is double-buffered state, see wl\_surface.commit.

wl\_surface.set\_input\_region changes the pending input region. wl\_surface.commit copies the pending region to the current region. Otherwise the pending and current regions are never changed, except cursor and icon surfaces are special cases, see wl\_pointer.set\_cursor and wl\_data\_device.start\_drag.

The initial value for an input region is infinite. That means the whole surface will accept input. Setting the pending input region has copy semantics, and the wl\_region object can be destroyed immediately. A NULL wl\_region causes the input region to be set to infinite.

#### wl\_surface::commit - commit pending surface state

Surface state (input, opaque, and damage regions, attached buffers, etc.) is double-buffered. Protocol requests modify the pending state, as opposed to the active state in use by the compositor.

All requests that need a commit to become effective are documented to affect double-buffered state.

Other interfaces may add further double-buffered surface state.

A commit request atomically creates a Content Update (CU) from the pending state, even if the pending state has not been touched. The content update is placed at the end of a per-surface queue until it becomes active. After commit, the new pending state is as documented for each related request.

A CU is either a Desync Content Update (DCU) or a Sync Content Update (SCU). If the surface is effectively synchronized at the commit request, it is a SCU, otherwise a DCU.

When a surface transitions from effectively synchronized to effectively desynchronized, all SCUs in its queue which are not reachable by any DCU become DCUs and dependency edges from outside the queue to these CUs are removed.

See wl\_subsurface for the definition of 'effectively synchronized' and 'effectively desynchronized'.

When a CU is placed in the queue, the CU has a dependency on the CU in front of it and to the SCU at end of the queue of every direct child surface if that SCU exists and does not have another dependent. This can form a directed acyclic graph of CUs with dependencies as edges.

In addition to surface state, the CU can have constraints that must be satisfied before it can be applied. Other interfaces may add CU constraints.

All DCUs which do not have a SCU in front of themselves in their queue, are candidates. If the graph that's reachable by a candidate does not have any unsatisfied constraints, the entire graph must be applied atomically.

When a CU is applied, the wl\_buffer is applied before all other state. This means that all coordinates in double-buffered state are relative to the newly attached wl\_buffers, except for wl\_surface.attach itself. If there is no newly attached wl\_buffer, the coordinates are relative to the previous content update.

#### wl\_surface::set\_buffer\_transform - sets the buffer transformation

transform

[wl\_output::transform](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_output-enum-transform "wl_output::transform - transformation applied to buffer contents") (int) - transform for interpreting buffer contents

This request sets the transformation that the client has already applied to the content of the buffer. The accepted values for the transform parameter are the values for wl\_output.transform.

The compositor applies the inverse of this transformation whenever it uses the buffer contents.

Buffer transform is double-buffered state, see wl\_surface.commit.

A newly created surface has its buffer transformation set to normal.

wl\_surface.set\_buffer\_transform changes the pending buffer transformation. wl\_surface.commit copies the pending buffer transformation to the current one. Otherwise, the pending and current values are never changed.

The purpose of this request is to allow clients to render content according to the output transform, thus permitting the compositor to use certain optimizations even if the display is rotated. Using hardware overlays and scanning out a client buffer for fullscreen surfaces are examples of such optimizations. Those optimizations are highly dependent on the compositor implementation, so the use of this request should be considered on a case-by-case basis.

Note that if the transform value includes 90 or 270 degree rotation, the width of the buffer will become the surface height and the height of the buffer will become the surface width.

If transform is not one of the values from the wl\_output.transform enum the invalid\_transform protocol error is raised.

#### wl\_surface::set\_buffer\_scale - sets the buffer scaling factor

scale

int - scale for interpreting buffer contents

This request sets an optional scaling factor on how the compositor interprets the contents of the buffer attached to the window.

Buffer scale is double-buffered state, see wl\_surface.commit.

A newly created surface has its buffer scale set to 1.

wl\_surface.set\_buffer\_scale changes the pending buffer scale. wl\_surface.commit copies the pending buffer scale to the current one. Otherwise, the pending and current values are never changed.

The purpose of this request is to allow clients to supply higher resolution buffer data for use on high resolution outputs. It is intended that you pick the same buffer scale as the scale of the output that the surface is displayed on. This means the compositor can avoid scaling when rendering the surface on that output.

Note that if the scale is larger than 1, then you have to attach a buffer that is larger (by a factor of scale in each dimension) than the desired surface size.

If scale is not greater than 0 the invalid\_scale protocol error is raised.

#### wl\_surface::damage\_buffer - mark part of the surface damaged using buffer coordinates

x

int - buffer-local x coordinate

y

int - buffer-local y coordinate

width

int - width of damage rectangle

height

int - height of damage rectangle

This request is used to describe the regions where the pending buffer is different from the current surface contents, and where the surface therefore needs to be repainted. The compositor ignores the parts of the damage that fall outside of the surface.

Damage is double-buffered state, see wl\_surface.commit.

The damage rectangle is specified in buffer coordinates, where x and y specify the upper left corner of the damage rectangle.

The initial value for pending damage is empty: no damage. wl\_surface.damage\_buffer adds pending damage: the new pending damage is the union of old pending damage and the given rectangle.

wl\_surface.commit assigns pending damage as the current damage, and clears pending damage. The server will clear the current damage as it repaints the surface.

This request differs from wl\_surface.damage in only one way - it takes damage in buffer coordinates instead of surface-local coordinates. While this generally is more intuitive than surface coordinates, it is especially desirable when using wp\_viewport or when a drawing library (like EGL) is unaware of buffer scale and buffer transform.

Note: Because buffer transformation changes and damage requests may be interleaved in the protocol stream, it is impossible to determine the actual mapping between surface and buffer damage until wl\_surface.commit time. Therefore, compositors wishing to take both kinds of damage into account will have to accumulate damage from the two requests separately and only transform from one to the other after receiving the wl\_surface.commit.

#### wl\_surface::offset - set the surface contents offset

x

int - surface-local x coordinate

y

int - surface-local y coordinate

The x and y arguments specify the location of the new pending buffer's upper left corner, relative to the current buffer's upper left corner, in surface-local coordinates. In other words, the x and y, combined with the new surface size define in which directions the surface's size changes.

The exact semantics of wl\_surface.offset are role-specific. Refer to the documentation of specific roles for more information.

Surface location offset is double-buffered state, see wl\_surface.commit.

This request is semantically equivalent to and the replaces the x and y arguments in the wl\_surface.attach request in wl\_surface versions prior to 5. See wl\_surface.attach for details.

#### wl\_surface::get\_release - get a release callback

callback

id for the new [wl\_callback](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_callback "wl_callback - callback object") - callback object for the release

Create a callback for the release of the buffer attached by the client with wl\_surface.attach.

The compositor will release the buffer when it has finished its usage of the underlying storage for the relevant commit. Once the client receives this event, and assuming the associated buffer is not pending release from other wl\_surface.commit requests, the client can safely re-use the buffer.

Release callbacks are double-buffered state, and will be associated with the pending buffer at wl\_surface.commit time.

The callback\_data passed in the wl\_callback.done event is unused and is always zero.

Sending this request without attaching a non-null buffer in the same content update is a protocol error. The compositor will send the no\_buffer error in this case.

### Events provided by wl\_surface

#### wl\_surface::enter - surface enters an output

output

[wl\_output](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_output "wl_output - compositor output region") - output entered by the surface

This is emitted whenever a surface's creation, movement, or resizing results in some part of it being within the scanout region of an output.

Note that a surface may be overlapping with zero or more outputs.

#### wl\_surface::leave - surface leaves an output

output

[wl\_output](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_output "wl_output - compositor output region") - output left by the surface

This is emitted whenever a surface's creation, movement, or resizing results in it no longer having any part of it within the scanout region of an output.

Clients should not use the number of outputs the surface is on for frame throttling purposes. The surface might be hidden even if no leave event has been sent, and the compositor might expect new surface content updates even if no enter event has been sent. The frame event should be used instead.

#### wl\_surface::preferred\_buffer\_scale - preferred buffer scale for the surface

factor

int - preferred scaling factor

This event indicates the preferred buffer scale for this surface. It is sent whenever the compositor's preference changes.

Before receiving this event the preferred buffer scale for this surface is 1.

It is intended that scaling aware clients use this event to scale their content and use wl\_surface.set\_buffer\_scale to indicate the scale they have rendered with. This allows clients to supply a higher detail buffer.

The compositor shall emit a scale value greater than 0.

#### wl\_surface::preferred\_buffer\_transform - preferred buffer transform for the surface

transform

[wl\_output::transform](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_output-enum-transform "wl_output::transform - transformation applied to buffer contents") (uint) - preferred transform

This event indicates the preferred buffer transform for this surface. It is sent whenever the compositor's preference changes.

Before receiving this event the preferred buffer transform for this surface is normal.

Applying this transformation to the surface buffer contents and using wl\_surface.set\_buffer\_transform might allow the compositor to use the surface buffer more efficiently.

### Enums provided by wl\_surface

#### wl\_surface::error - wl\_surface error values

These errors can be emitted in response to wl\_surface requests.

invalid\_scale

0 - buffer scale value is invalid

invalid\_transform

1 - buffer transform value is invalid

invalid\_size

2 - buffer size is invalid

invalid\_offset

3 - buffer offset is invalid

defunct\_role\_object

4 - surface was destroyed before its role object

no\_buffer

5 - no buffer was attached

## wl\_seat - group of input devices

A seat is a group of keyboards, pointer and touch devices. This object is published as a global during start up, or when such a device is hot plugged. A seat typically has a pointer and maintains a keyboard focus and a pointer focus.

### Requests provided by wl\_seat

#### wl\_seat::get\_pointer - return pointer object

id

id for the new [wl\_pointer](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_pointer "wl_pointer - pointer input device") - seat pointer

The ID provided will be initialized to the wl\_pointer interface for this seat.

This request only takes effect if the seat has the pointer capability, or has had the pointer capability in the past. It is a protocol violation to issue this request on a seat that has never had the pointer capability. The missing\_capability error will be sent in this case.

#### wl\_seat::get\_keyboard - return keyboard object

id

id for the new [wl\_keyboard](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_keyboard "wl_keyboard - keyboard input device") - seat keyboard

The ID provided will be initialized to the wl\_keyboard interface for this seat.

This request only takes effect if the seat has the keyboard capability, or has had the keyboard capability in the past. It is a protocol violation to issue this request on a seat that has never had the keyboard capability. The missing\_capability error will be sent in this case.

#### wl\_seat::get\_touch - return touch object

id

id for the new [wl\_touch](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_touch "wl_touch - touchscreen input device") - seat touch interface

The ID provided will be initialized to the wl\_touch interface for this seat.

This request only takes effect if the seat has the touch capability, or has had the touch capability in the past. It is a protocol violation to issue this request on a seat that has never had the touch capability. The missing\_capability error will be sent in this case.

#### wl\_seat::release - release the seat object

Using this request a client can tell the server that it is not going to use the seat object anymore.

### Events provided by wl\_seat

#### wl\_seat::capabilities - seat capabilities changed

capabilities

[wl\_seat::capability](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_seat-enum-capability "wl_seat::capability - bitfield - seat capability bitmask") (uint) - capabilities of the seat

This is sent on binding to the seat global or whenever a seat gains or loses the pointer, keyboard or touch capabilities. The argument is a capability enum containing the complete set of capabilities this seat has.

When the pointer capability is added, a client may create a wl\_pointer object using the wl\_seat.get\_pointer request. This object will receive pointer events until the capability is removed in the future.

When the pointer capability is removed, a client should destroy the wl\_pointer objects associated with the seat where the capability was removed, using the wl\_pointer.release request. No further pointer events will be received on these objects.

In some compositors, if a seat regains the pointer capability and a client has a previously obtained wl\_pointer object of version 4 or less, that object may start sending pointer events again. This behavior is considered a misinterpretation of the intended behavior and must not be relied upon by the client. wl\_pointer objects of version 5 or later must not send events if created before the most recent event notifying the client of an added pointer capability.

The above behavior also applies to wl\_keyboard and wl\_touch with the keyboard and touch capabilities, respectively.

#### wl\_seat::name - unique identifier for this seat

name

string - seat identifier

In a multi-seat configuration the seat name can be used by clients to help identify which physical devices the seat represents.

The seat name is a UTF-8 string with no convention defined for its contents. Each name is unique among all wl\_seat globals. The name is only guaranteed to be unique for the current compositor instance.

The same seat names are used for all clients. Thus, the name can be shared across processes to refer to a specific wl\_seat global.

The name event is sent after binding to the seat global, and should be sent before announcing capabilities. This event only sent once per seat object, and the name does not change over the lifetime of the wl\_seat global.

Compositors may re-use the same seat name if the wl\_seat global is destroyed and re-created later.

### Enums provided by wl\_seat

#### wl\_seat::capability - bitfield - seat capability bitmask

This is a bitmask of capabilities this seat has; if a member is set, then it is present on the seat.

pointer

1 - the seat has pointer devices

keyboard

2 - the seat has one or more keyboards

touch

4 - the seat has touch devices

#### wl\_seat::error - wl\_seat error values

These errors can be emitted in response to wl\_seat requests.

missing\_capability

0 - get\_pointer, get\_keyboard or get\_touch called on seat without the matching capability

## wl\_pointer - pointer input device

The wl\_pointer interface represents one or more input devices, such as mice, which control the pointer location and pointer\_focus of a seat.

The wl\_pointer interface generates motion, enter and leave events for the surfaces that the pointer is located over, and button and axis events for button presses, button releases and scrolling.

### Requests provided by wl\_pointer

#### wl\_pointer::set\_cursor - set the pointer surface

serial

uint - serial number of the enter event

surface

[wl\_surface](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface "wl_surface - an onscreen surface") - pointer surface

hotspot\_x

int - surface-local x coordinate

hotspot\_y

int - surface-local y coordinate

Set the pointer surface, i.e., the surface that contains the pointer image (cursor). This request gives the surface the role of a cursor. If the surface already has another role, it raises a protocol error.

The cursor actually changes only if the pointer focus for this device is one of the requesting client's surfaces or the surface parameter is the current pointer surface. If there was a previous surface set with this request it is replaced. If surface is NULL, the pointer image is hidden.

The parameters hotspot\_x and hotspot\_y define the position of the pointer surface relative to the pointer location. Its top-left corner is always at (x, y) - (hotspot\_x, hotspot\_y), where (x, y) are the coordinates of the pointer location, in surface-local coordinates.

On wl\_surface.offset requests to the pointer surface, hotspot\_x and hotspot\_y are decremented by the x and y parameters passed to the request. The offset must be applied by wl\_surface.commit as usual.

The hotspot can also be updated by passing the currently set pointer surface to this request with new values for hotspot\_x and hotspot\_y.

The input region is ignored for wl\_surfaces with the role of a cursor. When the use as a cursor ends, the wl\_surface is unmapped.

The serial parameter must match the latest wl\_pointer.enter serial number sent to the client. Otherwise the request will be ignored.

#### wl\_pointer::release - release the pointer object

Using this request a client can tell the server that it is not going to use the pointer object anymore.

This request destroys the pointer proxy object, so clients must not call wl\_pointer\_destroy() after using this request.

### Events provided by wl\_pointer

#### wl\_pointer::enter - enter event

serial

uint - serial number of the enter event

surface

[wl\_surface](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface "wl_surface - an onscreen surface") - surface entered by the pointer

surface\_x

fixed - surface-local x coordinate

surface\_y

fixed - surface-local y coordinate

Notification that this seat's pointer is focused on a certain surface.

When a seat's focus enters a surface, the pointer image is undefined and a client should respond to this event by setting an appropriate pointer image with the set\_cursor request.

#### wl\_pointer::leave - leave event

serial

uint - serial number of the leave event

surface

[wl\_surface](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface "wl_surface - an onscreen surface") - surface left by the pointer

Notification that this seat's pointer is no longer focused on a certain surface.

The leave notification is sent before the enter notification for the new focus.

#### wl\_pointer::motion - pointer motion event

time

uint - timestamp with millisecond granularity

surface\_x

fixed - surface-local x coordinate

surface\_y

fixed - surface-local y coordinate

Notification of pointer location change. The arguments surface\_x and surface\_y are the location relative to the focused surface.

#### wl\_pointer::button - pointer button event

serial

uint - serial number of the button event

time

uint - timestamp with millisecond granularity

button

uint - button that produced the event

state

[wl\_pointer::button\_state](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_pointer-enum-button_state "wl_pointer::button_state - physical button state") (uint) - physical state of the button

Mouse button click and release notifications.

The location of the click is given by the last motion or enter event. The time argument is a timestamp with millisecond granularity, with an undefined base.

The button is a button code as defined in the Linux kernel's linux/input-event-codes.h header file, e.g. BTN\_LEFT.

Any 16-bit button code value is reserved for future additions to the kernel's event code list. All other button codes above 0xFFFF are currently undefined but may be used in future versions of this protocol.

#### wl\_pointer::axis - axis event

time

uint - timestamp with millisecond granularity

axis

[wl\_pointer::axis](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_pointer-enum-axis "wl_pointer::axis - axis types") (uint) - axis type

value

fixed - length of vector in surface-local coordinate space

Scroll and other axis notifications.

For scroll events (vertical and horizontal scroll axes), the value parameter is the length of a vector along the specified axis in a coordinate space identical to those of motion events, representing a relative movement along the specified axis.

For devices that support movements non-parallel to axes multiple axis events will be emitted.

When applicable, for example for touch pads, the server can choose to emit scroll events where the motion vector is equivalent to a motion event vector.

When applicable, a client can transform its content relative to the scroll distance.

#### wl\_pointer::frame - end of a pointer event sequence

Indicates the end of a set of events that logically belong together. A client is expected to accumulate the data in all events within the frame before proceeding.

All wl\_pointer events before a wl\_pointer.frame event belong logically together. For example, in a diagonal scroll motion the compositor will send an optional wl\_pointer.axis\_source event, two wl\_pointer.axis events (horizontal and vertical) and finally a wl\_pointer.frame event. The client may use this information to calculate a diagonal vector for scrolling.

When multiple wl\_pointer.axis events occur within the same frame, the motion vector is the combined motion of all events. When a wl\_pointer.axis and a wl\_pointer.axis\_stop event occur within the same frame, this indicates that axis movement in one axis has stopped but continues in the other axis. When multiple wl\_pointer.axis\_stop events occur within the same frame, this indicates that these axes stopped in the same instance.

A wl\_pointer.frame event is sent for every logical event group, even if the group only contains a single wl\_pointer event. Specifically, a client may get a sequence: motion, frame, button, frame, axis, frame, axis\_stop, frame.

The wl\_pointer.enter and wl\_pointer.leave events are logical events generated by the compositor and not the hardware. These events are also grouped by a wl\_pointer.frame. When a pointer moves from one surface to another, a compositor should group the wl\_pointer.leave event within the same wl\_pointer.frame. However, a client must not rely on wl\_pointer.leave and wl\_pointer.enter being in the same wl\_pointer.frame. Compositor-specific policies may require the wl\_pointer.leave and wl\_pointer.enter event being split across multiple wl\_pointer.frame groups.

#### wl\_pointer::axis\_source - axis source event

axis\_source

[wl\_pointer::axis\_source](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_pointer-enum-axis_source "wl_pointer::axis_source - axis source types") (uint) - source of the axis event

Source information for scroll and other axes.

This event does not occur on its own. It is sent before a wl\_pointer.frame event and carries the source information for all events within that frame.

The source specifies how this event was generated. If the source is wl\_pointer.axis\_source.finger, a wl\_pointer.axis\_stop event will be sent when the user lifts the finger off the device.

If the source is wl\_pointer.axis\_source.wheel, wl\_pointer.axis\_source.wheel\_tilt or wl\_pointer.axis\_source.continuous, a wl\_pointer.axis\_stop event may or may not be sent. Whether a compositor sends an axis\_stop event for these sources is hardware-specific and implementation-dependent; clients must not rely on receiving an axis\_stop event for these scroll sources and should treat scroll sequences from these scroll sources as unterminated by default.

This event is optional. If the source is unknown for a particular axis event sequence, no event is sent. Only one wl\_pointer.axis\_source event is permitted per frame.

The order of wl\_pointer.axis\_discrete and wl\_pointer.axis\_source is not guaranteed.

#### wl\_pointer::axis\_stop - axis stop event

time

uint - timestamp with millisecond granularity

axis

[wl\_pointer::axis](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_pointer-enum-axis "wl_pointer::axis - axis types") (uint) - the axis stopped with this event

Stop notification for scroll and other axes.

For some wl\_pointer.axis\_source types, a wl\_pointer.axis\_stop event is sent to notify a client that the axis sequence has terminated. This enables the client to implement kinetic scrolling. See the wl\_pointer.axis\_source documentation for information on when this event may be generated.

Any wl\_pointer.axis events with the same axis\_source after this event should be considered as the start of a new axis motion.

The timestamp is to be interpreted identical to the timestamp in the wl\_pointer.axis event. The timestamp value may be the same as a preceding wl\_pointer.axis event.

#### wl\_pointer::axis\_discrete - axis click event

axis

[wl\_pointer::axis](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_pointer-enum-axis "wl_pointer::axis - axis types") (uint) - axis type

discrete

int - number of steps

Discrete step information for scroll and other axes.

This event carries the axis value of the wl\_pointer.axis event in discrete steps (e.g. mouse wheel clicks).

This event is deprecated with wl\_pointer version 8 - this event is not sent to clients supporting version 8 or later.

This event does not occur on its own, it is coupled with a wl\_pointer.axis event that represents this axis value on a continuous scale. The protocol guarantees that each axis\_discrete event is always followed by exactly one axis event with the same axis number within the same wl\_pointer.frame. Note that the protocol allows for other events to occur between the axis\_discrete and its coupled axis event, including other axis\_discrete or axis events. A wl\_pointer.frame must not contain more than one axis\_discrete event per axis type.

This event is optional; continuous scrolling devices like two-finger scrolling on touchpads do not have discrete steps and do not generate this event.

The discrete value carries the directional information. e.g. a value of -2 is two steps towards the negative direction of this axis.

The axis number is identical to the axis number in the associated axis event.

The order of wl\_pointer.axis\_discrete and wl\_pointer.axis\_source is not guaranteed.

#### wl\_pointer::axis\_value120 - axis high-resolution scroll event

axis

[wl\_pointer::axis](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_pointer-enum-axis "wl_pointer::axis - axis types") (uint) - axis type

value120

int - scroll distance as fraction of 120

Discrete high-resolution scroll information.

This event carries high-resolution wheel scroll information, with each multiple of 120 representing one logical scroll step (a wheel detent). For example, an axis\_value120 of 30 is one quarter of a logical scroll step in the positive direction, a value120 of -240 are two logical scroll steps in the negative direction within the same hardware event. Clients that rely on discrete scrolling should accumulate the value120 to multiples of 120 before processing the event.

The value120 must not be zero.

This event replaces the wl\_pointer.axis\_discrete event in clients supporting wl\_pointer version 8 or later.

Where a wl\_pointer.axis\_source event occurs in the same wl\_pointer.frame, the axis source applies to this event.

The order of wl\_pointer.axis\_value120 and wl\_pointer.axis\_source is not guaranteed.

#### wl\_pointer::axis\_relative\_direction - axis relative physical direction event

axis

[wl\_pointer::axis](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_pointer-enum-axis "wl_pointer::axis - axis types") (uint) - axis type

direction

[wl\_pointer::axis\_relative\_direction](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_pointer-enum-axis_relative_direction "wl_pointer::axis_relative_direction - axis relative direction") (uint) - physical direction relative to axis motion

Relative directional information of the entity causing the axis motion.

For a wl\_pointer.axis event, the wl\_pointer.axis\_relative\_direction event specifies the movement direction of the entity causing the wl\_pointer.axis event. For example: - if a user's fingers on a touchpad move down and this causes a wl\_pointer.axis vertical\_scroll down event, the physical direction is 'identical' - if a user's fingers on a touchpad move down and this causes a wl\_pointer.axis vertical\_scroll up scroll up event ('natural scrolling'), the physical direction is 'inverted'.

A client may use this information to adjust scroll motion of components. Specifically, enabling natural scrolling causes the content to change direction compared to traditional scrolling. Some widgets like volume control sliders should usually match the physical direction regardless of whether natural scrolling is active. This event enables clients to match the scroll direction of a widget to the physical direction.

This event does not occur on its own, it is coupled with a wl\_pointer.axis event that represents this axis value. The protocol guarantees that each axis\_relative\_direction event is always followed by exactly one axis event with the same axis number within the same wl\_pointer.frame. Note that the protocol allows for other events to occur between the axis\_relative\_direction and its coupled axis event.

The axis number is identical to the axis number in the associated axis event.

The order of wl\_pointer.axis\_relative\_direction, wl\_pointer.axis\_discrete and wl\_pointer.axis\_source is not guaranteed.

### Enums provided by wl\_pointer

#### wl\_pointer::error

role

0 - given wl\_surface has another role

#### wl\_pointer::button\_state - physical button state

Describes the physical state of a button that produced the button event.

released

0 - the button is not pressed

pressed

1 - the button is pressed

#### wl\_pointer::axis - axis types

Describes the axis types of scroll events.

vertical\_scroll

0 - vertical axis

horizontal\_scroll

1 - horizontal axis

#### wl\_pointer::axis\_source - axis source types

Describes the source types for axis events. This indicates to the client how an axis event was physically generated; a client may adjust the user interface accordingly. For example, scroll events from a "finger" source may be in a smooth coordinate space with kinetic scrolling whereas a "wheel" source may be in discrete steps of a number of lines.

The "continuous" axis source is a device generating events in a continuous coordinate space, but using something other than a finger. One example for this source is button-based scrolling where the vertical motion of a device is converted to scroll events while a button is held down.

The "wheel tilt" axis source indicates that the actual device is a wheel but the scroll event is not caused by a rotation but a (usually sideways) tilt of the wheel.

wheel

0 - a physical wheel rotation

finger

1 - finger on a touch surface

continuous

2 - continuous coordinate space

wheel\_tilt

3 - a physical wheel tilt

#### wl\_pointer::axis\_relative\_direction - axis relative direction

This specifies the direction of the physical motion that caused a wl\_pointer.axis event, relative to the wl\_pointer.axis direction.

identical

0 - physical motion matches axis direction

inverted

1 - physical motion is the inverse of the axis direction

## wl\_keyboard - keyboard input device

The wl\_keyboard interface represents one or more keyboards associated with a seat.

Each wl\_keyboard has the following logical state:

\- an active surface (possibly null), - the keys currently logically down, - the active modifiers, - the active group.

By default, the active surface is null, the keys currently logically down are empty, the active modifiers and the active group are 0.

### Requests provided by wl\_keyboard

#### wl\_keyboard::release - release the keyboard object

### Events provided by wl\_keyboard

#### wl\_keyboard::keymap - keyboard mapping

format

[wl\_keyboard::keymap\_format](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_keyboard-enum-keymap_format "wl_keyboard::keymap_format - keyboard mapping format") (uint) - keymap format

fd

fd - keymap file descriptor

size

uint - keymap size, in bytes

This event provides a file descriptor to the client which can be memory-mapped in read-only mode to provide a keyboard mapping description.

From version 7 onwards, the fd must be mapped with MAP\_PRIVATE by the recipient, as MAP\_SHARED may fail.

#### wl\_keyboard::enter - enter event

serial

uint - serial number of the enter event

surface

[wl\_surface](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface "wl_surface - an onscreen surface") - surface gaining keyboard focus

keys

array - the keys currently logically down

Notification that this seat's keyboard focus is on a certain surface.

The compositor must send the wl\_keyboard.modifiers event after this event.

In the wl\_keyboard logical state, this event sets the active surface to the surface argument and the keys currently logically down to the keys in the keys argument. The compositor must not send this event if the wl\_keyboard already had an active surface immediately before this event.

Clients should not use the list of pressed keys to emulate key-press events. The order of keys in the list is unspecified.

#### wl\_keyboard::leave - leave event

serial

uint - serial number of the leave event

surface

[wl\_surface](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface "wl_surface - an onscreen surface") - surface that lost keyboard focus

Notification that this seat's keyboard focus is no longer on a certain surface.

The leave notification is sent before the enter notification for the new focus.

In the wl\_keyboard logical state, this event resets all values to their defaults. The compositor must not send this event if the active surface of the wl\_keyboard was not equal to the surface argument immediately before this event.

#### wl\_keyboard::key - key event

serial

uint - serial number of the key event

time

uint - timestamp with millisecond granularity

key

uint - key that produced the event

state

[wl\_keyboard::key\_state](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_keyboard-enum-key_state "wl_keyboard::key_state - physical key state") (uint) - physical state of the key

A key was pressed or released. The time argument is a timestamp with millisecond granularity, with an undefined base.

The key is a platform-specific key code that can be interpreted by feeding it to the keyboard mapping (see the keymap event).

If this event produces a change in modifiers, then the resulting wl\_keyboard.modifiers event must be sent after this event.

In the wl\_keyboard logical state, this event adds the key to the keys currently logically down (if the state argument is pressed) or removes the key from the keys currently logically down (if the state argument is released). The compositor must not send this event if the wl\_keyboard did not have an active surface immediately before this event. The compositor must not send this event if state is pressed (resp. released) and the key was already logically down (resp. was not logically down) immediately before this event.

Since version 10, compositors may send key events with the "repeated" key state when a wl\_keyboard.repeat\_info event with a rate argument of 0 has been received. This allows the compositor to take over the responsibility of key repetition.

#### wl\_keyboard::modifiers - modifier and group state

serial

uint - serial number of the modifiers event

mods\_depressed

uint - depressed modifiers

mods\_latched

uint - latched modifiers

mods\_locked

uint - locked modifiers

group

uint - keyboard layout

Notifies clients that the modifier and/or group state has changed, and it should update its local state.

The compositor may send this event without a surface of the client having keyboard focus, for example to tie modifier information to pointer focus instead. If a modifier event with pressed modifiers is sent without a prior enter event, the client can assume the modifier state is valid until it receives the next wl\_keyboard.modifiers event. In order to reset the modifier state again, the compositor can send a wl\_keyboard.modifiers event with no pressed modifiers.

In the wl\_keyboard logical state, this event updates the modifiers and group.

#### wl\_keyboard::repeat\_info - repeat rate and delay

rate

int - the rate of repeating keys in characters per second

delay

int - delay in milliseconds since key down until repeating starts

Informs the client about the keyboard's repeat rate and delay.

This event is sent as soon as the wl\_keyboard object has been created, and is guaranteed to be received by the client before any key press event.

Negative values for either rate or delay are illegal. A rate of zero will disable any repeating (regardless of the value of delay).

This event can be sent later on as well with a new value if necessary, so clients should continue listening for the event past the creation of wl\_keyboard.

### Enums provided by wl\_keyboard

#### wl\_keyboard::keymap\_format - keyboard mapping format

This specifies the format of the keymap provided to the client with the wl\_keyboard.keymap event.

no\_keymap

0 - no keymap; client must understand how to interpret the raw keycode

xkb\_v1

1 - libxkbcommon compatible, null-terminated string; to determine the xkb keycode, clients must add 8 to the key event keycode

#### wl\_keyboard::key\_state - physical key state

Describes the physical state of a key that produced the key event.

Since version 10, the key can be in a "repeated" pseudo-state which means the same as "pressed", but is used to signal repetition in the key event.

The key may only enter the repeated state after entering the pressed state and before entering the released state. This event may be generated multiple times while the key is down.

released

0 - key is not pressed

pressed

1 - key is pressed

repeated

2 - key was repeated

## wl\_touch - touchscreen input device

The wl\_touch interface represents a touchscreen associated with a seat.

Touch interactions can consist of one or more contacts. For each contact, a series of events is generated, starting with a down event, followed by zero or more motion events, and ending with an up event. Events relating to the same contact point can be identified by the ID of the sequence.

### Requests provided by wl\_touch

#### wl\_touch::release - release the touch object

### Events provided by wl\_touch

#### wl\_touch::down - touch down event and beginning of a touch sequence

serial

uint - serial number of the touch down event

time

uint - timestamp with millisecond granularity

surface

[wl\_surface](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface "wl_surface - an onscreen surface") - surface touched

id

int - the unique ID of this touch point

x

fixed - surface-local x coordinate

y

fixed - surface-local y coordinate

A new touch point has appeared on the surface. This touch point is assigned a unique ID. Future events from this touch point reference this ID. The ID ceases to be valid after a touch up event and may be reused in the future.

#### wl\_touch::up - end of a touch event sequence

serial

uint - serial number of the touch up event

time

uint - timestamp with millisecond granularity

id

int - the unique ID of this touch point

The touch point has disappeared. No further events will be sent for this touch point and the touch point's ID is released and may be reused in a future touch down event.

#### wl\_touch::motion - update of touch point coordinates

time

uint - timestamp with millisecond granularity

id

int - the unique ID of this touch point

x

fixed - surface-local x coordinate

y

fixed - surface-local y coordinate

A touch point has changed coordinates.

#### wl\_touch::frame - end of touch frame event

Indicates the end of a set of events that logically belong together. A client is expected to accumulate the data in all events within the frame before proceeding.

A wl\_touch.frame terminates at least one event but otherwise no guarantee is provided about the set of events within a frame. A client must assume that any state not updated in a frame is unchanged from the previously known state.

#### wl\_touch::cancel - touch session cancelled

Sent if the compositor decides the touch stream is a global gesture. No further events are sent to the clients from that particular gesture. Touch cancellation applies to all touch points currently active on this client's surface. The client is responsible for finalizing the touch points, future touch points on this surface may reuse the touch point ID.

No frame event is required after the cancel event.

#### wl\_touch::shape - update shape of touch point

id

int - the unique ID of this touch point

major

fixed - length of the major axis in surface-local coordinates

minor

fixed - length of the minor axis in surface-local coordinates

Sent when a touchpoint has changed its shape.

This event does not occur on its own. It is sent before a wl\_touch.frame event and carries the new shape information for any previously reported, or new touch points of that frame.

Other events describing the touch point such as wl\_touch.down, wl\_touch.motion or wl\_touch.orientation may be sent within the same wl\_touch.frame. A client should treat these events as a single logical touch point update. The order of wl\_touch.shape, wl\_touch.orientation and wl\_touch.motion is not guaranteed. A wl\_touch.down event is guaranteed to occur before the first wl\_touch.shape event for this touch ID but both events may occur within the same wl\_touch.frame.

A touchpoint shape is approximated by an ellipse through the major and minor axis length. The major axis length describes the longer diameter of the ellipse, while the minor axis length describes the shorter diameter. Major and minor are orthogonal and both are specified in surface-local coordinates. The center of the ellipse is always at the touchpoint location as reported by wl\_touch.down or wl\_touch.move.

This event is only sent by the compositor if the touch device supports shape reports. The client has to make reasonable assumptions about the shape if it did not receive this event.

#### wl\_touch::orientation - update orientation of touch point

id

int - the unique ID of this touch point

orientation

fixed - angle between major axis and positive surface y-axis in degrees

Sent when a touchpoint has changed its orientation.

This event does not occur on its own. It is sent before a wl\_touch.frame event and carries the new shape information for any previously reported, or new touch points of that frame.

Other events describing the touch point such as wl\_touch.down, wl\_touch.motion or wl\_touch.shape may be sent within the same wl\_touch.frame. A client should treat these events as a single logical touch point update. The order of wl\_touch.shape, wl\_touch.orientation and wl\_touch.motion is not guaranteed. A wl\_touch.down event is guaranteed to occur before the first wl\_touch.orientation event for this touch ID but both events may occur within the same wl\_touch.frame.

The orientation describes the clockwise angle of a touchpoint's major axis to the positive surface y-axis and is normalized to the -180 to +180 degree range. The granularity of orientation depends on the touch device, some devices only support binary rotation values between 0 and 90 degrees.

This event is only sent by the compositor if the touch device supports orientation reports.

## wl\_output - compositor output region

An output describes part of the compositor geometry. The compositor works in the 'compositor coordinate system' and an output corresponds to a rectangular area in that space that is actually visible. This typically corresponds to a monitor that displays part of the compositor space. This object is published as global during start up, or when a monitor is hotplugged.

### Requests provided by wl\_output

#### wl\_output::release - release the output object

Using this request a client can tell the server that it is not going to use the output object anymore.

### Events provided by wl\_output

#### wl\_output::geometry - properties of the output

x

int - x position within the global compositor space

y

int - y position within the global compositor space

physical\_width

int - width in millimeters of the output

physical\_height

int - height in millimeters of the output

subpixel

[wl\_output::subpixel](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_output-enum-subpixel "wl_output::subpixel - subpixel geometry information") (int) - subpixel orientation of the output

make

string - textual description of the manufacturer

model

string - textual description of the model

transform

[wl\_output::transform](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_output-enum-transform "wl_output::transform - transformation applied to buffer contents") (int) - additional transformation applied to buffer contents during presentation

The geometry event describes geometric properties of the output. The event is sent when binding to the output object and whenever any of the properties change.

The physical size can be set to zero if it doesn't make sense for this output (e.g. for projectors or virtual outputs).

The geometry event will be followed by a done event (starting from version 2).

Clients should use wl\_surface.preferred\_buffer\_transform instead of the transform advertised by this event to find the preferred buffer transform to use for a surface.

Note: wl\_output only advertises partial information about the output position and identification. Some compositors, for instance those not implementing a desktop-style output layout or those exposing virtual outputs, might fake this information. Instead of using x and y, clients should use xdg\_output.logical\_position. Instead of using make and model, clients should use name and description.

#### wl\_output::mode - advertise available modes for the output

flags

[wl\_output::mode](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_output-enum-mode "wl_output::mode - bitfield - mode information") (uint) - bitfield of mode flags

width

int - width of the mode in hardware units

height

int - height of the mode in hardware units

refresh

int - vertical refresh rate in mHz

The mode event describes an available mode for the output.

The event is sent when binding to the output object and there will always be one mode, the current mode. The event is sent again if an output changes mode, for the mode that is now current. In other words, the current mode is always the last mode that was received with the current flag set.

Non-current modes are deprecated. A compositor can decide to only advertise the current mode and never send other modes. Clients should not rely on non-current modes.

The size of a mode is given in physical hardware units of the output device. This is not necessarily the same as the output size in the global compositor space. For instance, the output may be scaled, as described in wl\_output.scale, or transformed, as described in wl\_output.transform. Clients willing to retrieve the output size in the global compositor space should use xdg\_output.logical\_size instead.

The vertical refresh rate can be set to zero if it doesn't make sense for this output (e.g. for virtual outputs).

The mode event will be followed by a done event (starting from version 2).

Clients should not use the refresh rate to schedule frames. Instead, they should use the wl\_surface.frame event or the presentation-time protocol.

Note: this information is not always meaningful for all outputs. Some compositors, such as those exposing virtual outputs, might fake the refresh rate or the size.

#### wl\_output::done - sent all information about output

This event is sent after all other properties have been sent after binding to the output object and after any other property changes done after that. This allows changes to the output properties to be seen as atomic, even if they happen via multiple events.

#### wl\_output::scale - output scaling properties

factor

int - scaling factor of output

This event contains scaling geometry information that is not in the geometry event. It may be sent after binding the output object or if the output scale changes later. The compositor will emit a non-zero, positive value for scale. If it is not sent, the client should assume a scale of 1.

A scale larger than 1 means that the compositor will automatically scale surface buffers by this amount when rendering. This is used for very high resolution displays where applications rendering at the native resolution would be too small to be legible.

Clients should use wl\_surface.preferred\_buffer\_scale instead of this event to find the preferred buffer scale to use for a surface.

The scale event will be followed by a done event.

#### wl\_output::name - name of this output

name

string - output name

Many compositors will assign user-friendly names to their outputs, show them to the user, allow the user to refer to an output, etc. The client may wish to know this name as well to offer the user similar behaviors.

The name is a UTF-8 string with no convention defined for its contents. Each name is unique among all wl\_output globals. The name is only guaranteed to be unique for the compositor instance.

The same output name is used for all clients for a given wl\_output global. Thus, the name can be shared across processes to refer to a specific wl\_output global.

The name is not guaranteed to be persistent across sessions, thus cannot be used to reliably identify an output in e.g. configuration files.

Examples of names include 'HDMI-A-1', 'WL-1', 'X11-1', etc. However, do not assume that the name is a reflection of an underlying DRM connector, X11 connection, etc.

The name event is sent after binding the output object. This event is only sent once per output object, and the name does not change over the lifetime of the wl\_output global.

Compositors may re-use the same output name if the wl\_output global is destroyed and re-created later. Compositors should avoid re-using the same name if possible.

The name event will be followed by a done event.

#### wl\_output::description - human-readable description of this output

description

string - output description

Many compositors can produce human-readable descriptions of their outputs. The client may wish to know this description as well, e.g. for output selection purposes.

The description is a UTF-8 string with no convention defined for its contents. The description is not guaranteed to be unique among all wl\_output globals. Examples might include 'Foocorp 11" Display' or 'Virtual X11 output via:1'.

The description event is sent after binding the output object and whenever the description changes. The description is optional, and may not be sent at all.

The description event will be followed by a done event.

### Enums provided by wl\_output

#### wl\_output::subpixel - subpixel geometry information

This enumeration describes how the physical pixels on an output are laid out.

unknown

0 - unknown geometry

none

1 - no geometry

horizontal\_rgb

2 - horizontal RGB

horizontal\_bgr

3 - horizontal BGR

vertical\_rgb

4 - vertical RGB

vertical\_bgr

5 - vertical BGR

#### wl\_output::transform - transformation applied to buffer contents

This describes transformations that clients and compositors apply to buffer contents.

The flipped values correspond to an initial flip around a vertical axis followed by rotation.

The purpose is mainly to allow clients to render accordingly and tell the compositor, so that for fullscreen surfaces, the compositor will still be able to scan out directly from client surfaces.

normal

0 - no transform

90

1 - 90 degrees counter-clockwise

180

2 - 180 degrees counter-clockwise

270

3 - 270 degrees counter-clockwise

flipped

4 - 180 degree flip around a vertical axis

flipped\_90

5 - flip and rotate 90 degrees counter-clockwise

flipped\_180

6 - flip and rotate 180 degrees counter-clockwise

flipped\_270

7 - flip and rotate 270 degrees counter-clockwise

#### wl\_output::mode - bitfield - mode information

These flags describe properties of an output mode. They are used in the flags bitfield of the mode event.

current

0x1 - indicates this is the current mode

preferred

0x2 - indicates this is the preferred mode

## wl\_region - region interface

A region object describes an area.

Region objects are used to describe the opaque and input regions of a surface.

### Requests provided by wl\_region

#### wl\_region::destroy - destroy region

Destroy the region. This will invalidate the object ID.

#### wl\_region::add - add rectangle to region

x

int - region-local x coordinate

y

int - region-local y coordinate

width

int - rectangle width

height

int - rectangle height

Add the specified rectangle to the region.

#### wl\_region::subtract - subtract rectangle from region

x

int - region-local x coordinate

y

int - region-local y coordinate

width

int - rectangle width

height

int - rectangle height

Subtract the specified rectangle from the region.

## wl\_subcompositor - sub-surface compositing

The global interface exposing sub-surface compositing capabilities. A wl\_surface, that has sub-surfaces associated, is called the parent surface. Sub-surfaces can be arbitrarily nested and create a tree of sub-surfaces.

The root surface in a tree of sub-surfaces is the main surface. The main surface cannot be a sub-surface, because sub-surfaces must always have a parent.

A main surface with its sub-surfaces forms a (compound) window. For window management purposes, this set of wl\_surface objects is to be considered as a single window, and it should also behave as such.

The aim of sub-surfaces is to offload some of the compositing work within a window from clients to the compositor. A prime example is a video player with decorations and video in separate wl\_surface objects. This should allow the compositor to pass YUV video buffer processing to dedicated overlay hardware when possible.

### Requests provided by wl\_subcompositor

#### wl\_subcompositor::destroy - unbind from the subcompositor interface

Informs the server that the client will not be using this protocol object anymore. This does not affect any other objects, wl\_subsurface objects included.

#### wl\_subcompositor::get\_subsurface - give a surface the role sub-surface

id

id for the new [wl\_subsurface](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_subsurface "wl_subsurface - sub-surface interface to a wl_surface") - the new sub-surface object ID

surface

[wl\_surface](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface "wl_surface - an onscreen surface") - the surface to be turned into a sub-surface

parent

[wl\_surface](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface "wl_surface - an onscreen surface") - the parent surface

Create a sub-surface interface for the given surface, and associate it with the given parent surface. This turns a plain wl\_surface into a sub-surface.

The to-be sub-surface must not already have another role, and it must not have an existing wl\_subsurface object. Otherwise the bad\_surface protocol error is raised.

Adding sub-surfaces to a parent is a double-buffered operation on the parent (see wl\_surface.commit). The effect of adding a sub-surface becomes visible on the next time the state of the parent surface is applied.

The parent surface must not be one of the child surface's descendants, and the parent must be different from the child surface, otherwise the bad\_parent protocol error is raised.

This request modifies the behaviour of wl\_surface.commit request on the sub-surface, see the documentation on wl\_subsurface interface.

### Enums provided by wl\_subcompositor

#### wl\_subcompositor::error

bad\_surface

0 - the to-be sub-surface is invalid

bad\_parent

1 - the to-be sub-surface parent is invalid

## wl\_subsurface - sub-surface interface to a wl\_surface

An additional interface to a wl\_surface object, which has been made a sub-surface. A sub-surface has one parent surface. A sub-surface's size and position are not limited to that of the parent. Particularly, a sub-surface is not automatically clipped to its parent's area.

A sub-surface becomes mapped, when a non-NULL wl\_buffer is applied and the parent surface is mapped. The order of which one happens first is irrelevant. A sub-surface is hidden if the parent becomes hidden, or if a NULL wl\_buffer is applied. These rules apply recursively through the tree of surfaces.

A sub-surface can be in one of two modes. The possible modes are synchronized and desynchronized, see methods wl\_subsurface.set\_sync and wl\_subsurface.set\_desync.

The main surface can be thought to be always in desynchronized mode, since it does not have a parent in the sub-surfaces sense.

Even if a sub-surface is in desynchronized mode, it will behave as in synchronized mode, if its parent surface behaves as in synchronized mode. This rule is applied recursively throughout the tree of surfaces. This means, that one can set a sub-surface into synchronized mode, and then assume that all its child and grand-child sub-surfaces are synchronized, too, without explicitly setting them.

If a surface behaves as in synchronized mode, it is effectively synchronized, otherwise it is effectively desynchronized.

A sub-surface is initially in the synchronized mode.

The wl\_subsurface interface has requests which modify double-buffered state of the parent surface (wl\_subsurface.set\_position,.place\_above and.place\_below).

Destroying a sub-surface takes effect immediately. If you need to synchronize the removal of a sub-surface to the parent surface update, unmap the sub-surface first by attaching a NULL wl\_buffer, update parent, and then destroy the sub-surface.

If the parent wl\_surface object is destroyed, the sub-surface is unmapped.

A sub-surface never has the keyboard focus of any seat.

The wl\_surface.offset request is ignored: clients must use set\_position instead to move the sub-surface.

### Requests provided by wl\_subsurface

#### wl\_subsurface::destroy - remove sub-surface interface

The sub-surface interface is removed from the wl\_surface object that was turned into a sub-surface with a wl\_subcompositor.get\_subsurface request. The wl\_surface's association to the parent is deleted. The wl\_surface is unmapped immediately.

#### wl\_subsurface::set\_position - reposition the sub-surface

x

int - x coordinate in the parent surface

y

int - y coordinate in the parent surface

This sets the position of the sub-surface, relative to the parent surface.

The sub-surface will be moved so that its origin (top left corner pixel) will be at the location x, y of the parent surface coordinate system. The coordinates are not restricted to the parent surface area. Negative values are allowed.

The initial position is 0, 0.

Position is double-buffered state on the parent surface, see wl\_subsurface and wl\_surface.commit for more information.

#### wl\_subsurface::place\_above - restack the sub-surface

sibling

[wl\_surface](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface "wl_surface - an onscreen surface") - the reference surface

This sub-surface is taken from the stack, and put back just above the reference surface, changing the z-order of the sub-surfaces. The reference surface must be one of the sibling surfaces, or the parent surface. Using any other surface, including this sub-surface, will cause a protocol error.

A new sub-surface is initially added as the top-most in the stack of its siblings and parent.

Z-order is double-buffered state on the parent surface, see wl\_subsurface and wl\_surface.commit for more information.

#### wl\_subsurface::place\_below - restack the sub-surface

sibling

[wl\_surface](https://wayland.freedesktop.org/docs/html/apa.html#protocol-spec-wl_surface "wl_surface - an onscreen surface") - the reference surface

The sub-surface is placed just below the reference surface.

See wl\_subsurface.place\_above.

#### wl\_subsurface::set\_sync - set sub-surface to synchronized mode

Change the commit behaviour of the sub-surface to synchronized mode.

See wl\_subsurface and wl\_surface.commit for more information.

#### wl\_subsurface::set\_desync - set sub-surface to desynchronized mode

Change the commit behaviour of the sub-surface to desynchronized mode.

See wl\_subsurface and wl\_surface.commit for more information.

### Enums provided by wl\_subsurface

#### wl\_subsurface::error

bad\_surface

0 - wl\_surface is not a sibling or the parent

## wl\_fixes - wayland protocol fixes

This global fixes problems with other core-protocol interfaces that cannot be fixed in these interfaces themselves.

### Requests provided by wl\_fixes

#### wl\_fixes::destroy - destroys this object

#### wl\_fixes::destroy\_registry - destroy a wl\_registry

This request destroys a wl\_registry object.

The client should no longer use the wl\_registry after making this request.

The compositor will emit a wl\_display.delete\_id event with the object ID of the registry and will no longer emit any events on the registry. The client should re-use the object ID once it receives the wl\_display.delete\_id event.
