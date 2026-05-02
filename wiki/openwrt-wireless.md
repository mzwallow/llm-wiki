# OpenWrt Wireless

OpenWrt manages Wi-Fi through the Unified Configuration Interface (UCI) and `hostapd`.

## Configuration Structure (`/etc/config/wireless`)
The configuration is split into two primary section types:

### `wifi-device`
Represents the physical radio hardware.
- **`type`**: Usually `mac80211` or `broadcom`.
- **`band`**: `2g`, `5g`, `6g`, or `60g` (replaced deprecated `hwmode`).
- **`channel`**: Specific channel number or `auto`.
- **`htmode`**: Channel width and mode (e.g., `HT20`, `VHT80`, `HE160`).
- **`country`**: Two-letter country code (crucial for regulatory compliance/DFS).

### `wifi-iface`
Defines a virtual wireless network on a specific `wifi-device`.
- **`mode`**: `ap` (Access Point), `sta` (Station/Client), `mesh`, or `adhoc`.
- **`ssid`**: The network name.
- **`encryption`**: Security protocol (e.g., `psk2`, `sae`, `sae-mixed`).
- **`network`**: The logical network interface it attaches to (usually `lan`).

## Key Technologies
- **HT/VHT/HE**: High Throughput (802.11n), Very High Throughput (802.11ac), and High Efficiency (802.11ax). Larger channel widths (e.g., 80/160MHz) offer more speed but are more prone to interference.
- **DFS (Dynamic Frequency Selection)**: Required for certain 5GHz channels to avoid radar interference.
    - **CAC (Channel Availability Check)**: A mandatory delay (usually 60s) when starting on a DFS channel to scan for radar. The interface will appear disabled during this time.
- **802.11r (Fast BSS Transition)**: Reduces roaming time between APs (15-75ms vs 150ms+). Useful for VoIP and gaming.
- **WPS (Wi-Fi Protected Setup)**: Simplified connection method. Requires `hostapd-utils` and the full `wpad` or `hostapd` package (not `wpad-mini`).

## Command Line Management
- **`wifi`**: Apply wireless configuration changes.
- **`wifi down`**: Disable all wireless radios.
- **`wifi config`**: Re-detect hardware and rebuild the default configuration.
- **`iw reg get`**: Check the current regulatory domain.

## See Also
- [[openwrt]]
- [[openwrt-raspberry-pi]]
- [[openwrt-sqm]]
- [[openwrt-tailscale]]
