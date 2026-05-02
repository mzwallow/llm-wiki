# Tailscale on OpenWrt

Tailscale is a zero-config VPN that creates a secure virtual network (Tailnet) between devices. On OpenWrt, it can be used for remote administration, site-to-site networking (subnet routing), or as an exit node.

## Installation
Tailscale can be installed via the package manager:
```bash
opkg update
opkg install tailscale
```
*Note: In some versions, `apk` may be used instead of `opkg`.*

To start and authenticate:
```bash
tailscale up
```

## Initial Setup (LuCI)
To properly integrate Tailscale with OpenWrt's firewall and routing, it is recommended to create a dedicated interface and firewall zone.

### 1. Interface
- **Name**: `tailscale`
- **Protocol**: `Unmanaged`
- **Device**: `tailscale0`

### 2. Firewall Zone
- **Name**: `tailscale`
- **Input/Output**: `ACCEPT`
- **Forward**: `ACCEPT` (optional)
- **Masquerading**: `on`
- **MSS Clamping**: `on`
- **Covered Networks**: `tailscale`
- **Allow forward to/from destination zones**: Usually `lan`.

## Advanced Features

### Subnet Routing
Allows peers in the Tailnet to access your local LAN without installing Tailscale on every device.
```bash
tailscale up --advertise-routes=10.0.0.0/24 --snat-subnet-routes=false
```
*Note: Routes must also be approved in the Tailscale Admin Console.*

### Exit Nodes
Allows Tailnet peers to route all their internet traffic through your OpenWrt router.
```bash
tailscale up --advertise-exit-node
```

### Throughput Optimization (UDP Offloading)
For Kernel 6.6+ (OpenWrt 24.10+), performance can be improved using `ethtool` to enable UDP GRO (Generic Receive Offload):
```bash
ethtool -K eth1 rx-gro-list off
ethtool -K eth1 rx-udp-gro-forwarding on
```

## Low-Flash Devices (<16MB)
Standard Tailscale packages are too large for devices with limited flash.
- **Multicall Binary**: A single binary shared between `tailscale` and `tailscaled`.
- **Compression**: Using `upx` and `strip` can reduce binary size by ~98% (from ~33MB to ~5MB).
- **Repacking**: Repack `.ipk` files with optimized binaries to maintain compatibility with OpenWrt's init scripts.

## Troubleshooting
- **nftables (OpenWrt 22.03)**: Tailscale may fail to configure firewall rules automatically. Use `--netfilter-mode=off` as a workaround.
- **IPv6 Source Routing**: If exit node traffic fails, try disabling IPv6 source routing on the WAN interface.

## See Also
- [[openwrt]]
- [[openwrt-raspberry-pi]]
- [[openwrt-wireless]]
- [[openwrt-sqm]]
