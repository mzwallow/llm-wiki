# Xwayland

Xwayland is an X server that acts as a Wayland client, providing backward compatibility for X11 applications within a Wayland environment.

## How it works
Most Wayland compositors launch a single instance of Xwayland. X11 applications connect to Xwayland normally. Xwayland processes the X11 requests and translates the rendering and input into Wayland protocol messages to communicate with the Wayland compositor.

To provide a seamless "rootless" experience (where X11 windows mix with Wayland windows), the Wayland compositor runs an internal X Window Manager (XWM). The XWM synchronizes window state between Xwayland and the compositor's own window manager.

## See Also
- [[wayland]]
- [[wayland-book]]