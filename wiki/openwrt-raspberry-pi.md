# OpenWrt on Raspberry Pi

Support for Raspberry Pi (RPi) in OpenWrt is handled under the **bcm27xx** target.

## Hardware Support

| Model | Subtarget | SoC | Architecture |
|-------|-----------|-----|--------------|
| Raspberry Pi 1 | `bcm2708` | BCM2835 | ARMv6 |
| Raspberry Pi 2 | `bcm2709` | BCM2836 | ARMv7 |
| Raspberry Pi 3 | `bcm2710` | BCM2837 | ARMv8 (64-bit) |
| Raspberry Pi 4 | `bcm2711` | BCM2711 | ARMv8 (64-bit) |
| Raspberry Pi 5 | `bcm2712` | BCM2712 | ARMv8 (64-bit) |

### Key Improvements by Model
- **RPi 4**: Higher spec CPU/RAM, USB 3.0. Exceeds many top-tier routers in performance but lacks integrated Ethernet switch.
- **RPi 5**: 2-3x performance of Pi 4, power button, and integrated Real-Time Clock (RTC).

## Installation

1. Download the appropriate image for the model from the [OpenWrt Firmware Selector](https://firmware-selector.openwrt.org/).
2. Flash to a micro SD card using tools like **Raspberry Pi Imager** or `dd`.
3. Default IP is `192.168.1.1`. DHCP client is disabled by default.

## Networking

### WAN Connectivity
Since RPi boards typically have only one Ethernet port, adding a WAN port usually requires a **USB 3.0 to Gigabit Ethernet adapter**. Common chips include:
- RTL8153 (`kmod-usb-net-rtl8152`)
- AX88179 (`kmod-usb-net-asix-ax88179`)

### VLANs
Users can also use VLAN tagging on the single onboard port to separate LAN and WAN traffic (router-on-a-stick configuration).

## Wireless Configuration

- **Firmware**: RPi Zero 2 W requires manual firmware installation due to licensing.
- **Country Code**: Must often be set in the official Raspberry Pi OS first; OpenWrt LuCI settings may not apply correctly to the hardware.
- **5 GHz Channels**: RPi 4 may require updated firmware files in `/lib/firmware/brcm/` to connect to higher 5 GHz channels on older OpenWrt versions.

## Hardware Configuration

### Peripherals
- **I2C/SPI/I2S**: Enabled via `dtparam` in `/boot/config.txt`.
- **RTC**: RPi 1-4 require external RTC (e.g., ds1307) via I2C. RPi 5 has an embedded RTC.
- **Fan Control**: Supported via `kmod-hwmon-gpiofan` and `dtoverlay=gpio-fan`. RPi 5 has a dedicated PWM fan connector.

### Serial Console
Available via GPIO:
- **Pin 6**: Ground
- **Pin 8**: TX
- **Pin 10**: RX
- **Settings**: 115200 bps, 8N1, 3.3V.

## EEPROM Updates
Recommended for RPi 4 and 5 to improve performance, fix bugs, and optimize power/thermal management. Use `bcm27xx-eeprom` package or Raspberry Pi Imager.

## References
- [OpenWrt Wiki: Raspberry Pi](https://openwrt.org/toh/raspberry_pi_foundation/raspberry_pi)
