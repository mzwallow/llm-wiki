# OpenWrt

OpenWrt is an open-source project for embedded operating systems based on Linux, primarily used on embedded devices to route network traffic.

## Core Features
- **Package Management**: Uses `opkg` to install additional software from a repository of thousands of packages.
- **Writable Root Filesystem**: Allows users to customize the system and install new packages without reflashing.
- **Unified Configuration Interface (UCI)**: A small C library and CLI intended to centralize the whole configuration of a device.
- **Extensibility**: Supports a wide range of hardware, from small home routers to powerful single-board computers.

## Key Concepts
- **Targets/Subtargets**: Hardware-specific build configurations (e.g., `bcm27xx` for Raspberry Pi).
- **LuCI**: The web-based graphical user interface for OpenWrt.
- **DSA (Distributed Switch Architecture)**: The modern way OpenWrt handles network switches and VLANs.

## See Also
- [[openwrt-raspberry-pi]]
- [[openwrt-sqm]]
- [[openwrt-wireless]]
