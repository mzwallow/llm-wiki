---
title: "[OpenWrt Wiki] Tailscale"
source: "https://openwrt.org/docs/guide-user/services/vpn/tailscale/start#tailscale"
author:
published:
created: 2026-05-02
description:
tags:
  - "clippings"
---
Tailscale creates a virtual network between hosts. It can be used as a simple mechanism to allow remote administration without port forwarding or even be configured to allow peers in your virtual network to proxy traffic through connected devices as an ad-hoc vpn.

You can read more about [how Tailscale works here](https://tailscale.com/blog/how-tailscale-works/ "https://tailscale.com/blog/how-tailscale-works/").

Depending on your OpenWrt version the package included may be outdated and missing security updates. You can find instructions on how to update to the latest Tailscale package via your [Tailscale Admin Console page](https://login.tailscale.com/admin/machines "https://login.tailscale.com/admin/machines").

```js
apk update
apk add tailscale
```

After installing Tailscale, run the command below and finish device registration by pasting the given link into a web browser and authenticating via a supported method:

```js
tailscale up
```

Once registered, device connectivity can be seen by using the “status” command:

```js
tailscale status
```

Additional configuration may be necessary to communicate with other machines in your Tailnet depending on your default forwarding rules. The following instructions can be used to add a new unmanaged interface and firewall zone so that you can classify and apply forwarding rules to Tailscale traffic.

Create a new unmanaged interface via LuCI: **Network** → **Interfaces** → **Add new interface**

- Name: **tailscale**
- Protocol: **Unmanaged**
- Device: **tailscale0**

Verify that the interface has had your Tailscale address assigned:

```js
ip address show tailscale0
```

Create a new firewall zone via LuCI: **Network** → **Firewall** → **Zones** → **Add**

- Name: **tailscale**
- Input: **ACCEPT**
- Output: **ACCEPT**
- Forward: any (only matters if you have multiple interfaces in the tailscale firewall zone)
- Masquerading: **on** (optionally restrict this to relevant source subnets in advanced options, e.g. corresponding to **LAN**)
- MSS Clamping: **on**
- Covered networks: **tailscale**
- Allow forward to destination zones: Select your **LAN** (and/or other internal zones; and/or WAN if you plan on using this device as an exit node)
- Allow forward from source zones: Select your **LAN** (and/or other internal zones; or leave it blank if you do not want to route LAN traffic to other tailscale hosts/exit nodes)

Click **Save & Apply**

In order to get tailscale to cooperate well with LuCI, you will need to create a new managed interface and firewall zone for tailscale.

1\. Add the interface and firewall zone as per the [Initial Setup](#initial_setup "docs:guide-user:services:vpn:tailscale:start ↵") section

2\. Restart `tailscale` and add the routes you want to advertise to peers using the `--advertise-routes` option with a comma separated list of network addresses and CIDRs. The example below is advertising `10.0.0.0/24` and `10.0.1.0/24` yours are likely to be different. Since Masquarading is enabled in the firewall zone settings, tailscale SNAT should be disabled.

```js
tailscale up --advertise-routes=10.0.0.0/24,10.0.1.0/24 --snat-subnet-routes=false
```

Adding an additional `--accept-routes` option will manage adding static routes for other subnet routes within your tailnet. If [configuring multiple subnet routers which advertise the same subnets for high-availability](https://tailscale.com/kb/1115/high-availability#step-1-set-up-multiple-subnet-routers "https://tailscale.com/kb/1115/high-availability#step-1-set-up-multiple-subnet-routers"), do not include the `--accept-routes` option as this can cause routing issues and/or loss of connectivity on peer subnet routers.

You can also also add on the additional option of `--advertise-exit-node` node here to offer also a WAN gateway to your tailscale network.

3\. Open the [Machines](https://login.tailscale.com/admin/machines "https://login.tailscale.com/admin/machines") page in the Tailscale admin interface. Once you've found the machine from the ellipsis icon menu, open the `Edit route settings..` panel, and approve exported routes and or enable the `Use as exit node` option.

![](https://openwrt.org/_media/media/docs/howto/screenshot_2023-03-12_at_5.09.51_am.png?w=200&tok=8be3cc) ![](https://openwrt.org/_media/media/docs/howto/screenshot_2023-04-05_at_2.54.48_pm.png?w=400&tok=433990)

4\. Devices on either subnet should be able to route traffic over the VPN. If you've configured this device to be an exit node, it should now be selectable from your tailscale apps as an `Exit Node`. You can test connectivity with tools like `ping` or `traceroute`.

To use the device as a VPN gateway, configure Tailscale to use an exit node. This will route all LAN traffic to go through your exit node only.

0\. Verify that packet forwarding is disabled by default (this is the OpenWRT default): **Network** → **Firewall** → **General Settings** → Forward: **reject** or **drop**

1\. Add the interface and firewall zone as per the [Initial Setup](#initial_setup "docs:guide-user:services:vpn:tailscale:start ↵") section

2\. Start tailscale with `tailscale up --exit-node=MY-EXIT-NODE --exit-node-allow-lan-access=true`

3\. Disable LAN -to- WAN forwarding: **Network** → **Firewall** → **Zones** → **lan** → **Edit**

- Allow forward to destination zones: Ensure that your **WAN** zone is **unselected**.

You can verify that all traffic is being forced over your remote Tailscale exit node by running traceroute. You should see your Tailscale exit node in the second or so hop. If your Tailscale connected OpenWrt router is sending all traffic to the exit node but not LAN clients:

1\. Double check that your LAN firewall zone does not include the WAN for destination forwarding.

2\. Make sure to have a specified DNS server in your LAN interface otherwise the LAN clients would not be able to connect the internet through Tailscale. If insure what to use, [Cloudflare](https://1.1.1.1/ "https://1.1.1.1") or [Google Public DNS](https://developers.google.com/speed/public-dns "https://developers.google.com/speed/public-dns") are reasonable choices.

3\. You may have unexpected iptables or nftables stale rules. Reboot your OpenWrt device so you get a clean boot and application of rules.

*NB: To force most traffic through tailscale, but have some go elsewhere, you should be able to use tailscale together with [pbr\_app](https://openwrt.org/docs/guide-user/network/routing/pbr_app "docs:guide-user:network:routing:pbr_app") as long as you follow the tailscale-specific mentioned in its wiki page. You* should *even be able set up [pbr\_app](https://openwrt.org/docs/guide-user/network/routing/pbr_app "docs:guide-user:network:routing:pbr_app") to achieve a similar outcome as the selective tunneling described below, but it's not necessarily intuitive.*

The other scenario of selective tunneling is unfortunately not supported easily out of the box, but here's how I implemented it with tailscale 1.80.3 and openwrt 24.10. Note that my configuration is unsuitable for accessing devices actually on your tailnet (which I didn't care about) - please update the section if you manage a configuration that achieves both.

1\. Follow the **Initial Setup** instructions for adding an unmanaged interface for tailscale and configuring a new tailscale firewall zone. I also disabled “Use default gateway” in the interface Advanced Settings.

2\. Start tailscale with `tailscale up --exit-node=xxx --exit-node-allow-lan-access=true`.

At this point, all traffic will route through the exit node, since tailscale configures an associated ip route. The next steps are needed to override this.

3\. In the **System** → **Software** menu, install `coreutils-sleep`.

4\. Using your preferred method, create a shell script, e.g. `/root/ts-strip-default-route.sh`, with the following content:

```js
#!/bin/sh
#
# Remove "default" routes that get added by tailscale with --exit-node
# Use ip monitor to pause execution until changes are detected
# Rely on procd for looping

set -e

sleep 0.005

>&2 echo "Tailscale Route Stripping in Progress"
ip route del default dev tailscale0 table 52 2>/dev/null || true
ip -6 route del default dev tailscale0 table 52 2>/dev/null || true

FIFO=/tmp/tsmon.$$
trap 'kill "$MON_PID" 2>/dev/null || true; rm -f "$FIFO"' EXIT INT TERM
mkfifo "$FIFO"
ip monitor route dev tailscale0 > "$FIFO" & MON_PID=$!
read -r <"$FIFO"
kill "$MON_PID" 2>/dev/null || true
```

5\. Create a new service, e.g. `/etc/init.d/ts-strip-default-route`, with the following content:

```js
#!/bin/sh /etc/rc.common
START=90
USE_PROCD=1

start_service() {
    procd_open_instance
    procd_set_param command /root/ts-strip-default-route.sh
    procd_set_param stdout 1
    procd_set_param stderr 1
    procd_set_param respawn 0 0 0 #restart immediately on exit
    procd_close_instance
}
```

6\. Make sure both of these are set as executable (-x) by/for root. Enable and Start the new service under **System** → **Startup**.

7\. Finally, configure your custom routing. Either use [pbr\_app](https://openwrt.org/docs/guide-user/network/routing/pbr_app "docs:guide-user:network:routing:pbr_app") (out of the box), or static routes under **Network** → **Routing**, e.g.:

```js
Interface: tailscale
Route type: unicast
Target: x.x.x.x/x
Gateway: 0.0.0.0
```

OpenWrt 22.03 and later, use [nftables](https://openwrt.org/docs/guide-user/firewall/misc/nftables "docs:guide-user:firewall:misc:nftables") (superseding iptables) as a backend to [firewall4](https://openwrt.org/releases/22.03/notes-22.03.0#firewall4_based_on_nftables "releases:22.03:notes-22.03.0"). Tailscale is [unable to configure nftables automatically](https://github.com/tailscale/tailscale/issues/4086 "https://github.com/tailscale/tailscale/issues/4086") on the package included for 22.03 and this prevents the tailscale daemon from initializing properly and forwarding traffic.

A workaround for this issue [has been applied to the master branch](https://github.com/openwrt/packages/commit/aabfc3f51027d653455bca91587774e47f26e3b7 "https://github.com/openwrt/packages/commit/aabfc3f51027d653455bca91587774e47f26e3b7"). If you're unable or unwilling to run an image built from the master branch, the following steps can be used as a manual workaround on 22.03.x Credit: [aricade, csrutil, youngt2](https://github.com/tailscale/tailscale/issues/391#issuecomment-1312351292 "https://github.com/tailscale/tailscale/issues/391#issuecomment-1312351292"):

This fix is not required for OpenWRT `23.0.5` or later as the package has been fixed. **If using OpenWrt 23+ you do NOT need to apply `--netfliter-mode=off`**.

When starting Tailscale, you must prevent iptables rules from being created with the `--netfilter-mode=off` flag. This setting will be preserved in `/etc/tailscale/tailscaled.state` for future boots.

```bash
tailscale up --netfilter-mode=off
```

Restart the daemon

```bash
service tailscale restart
```

Verify no Kernel errors occur:

```bash
tailscale status
```

Continue with [initial\_setup](https://openwrt.org/docs/guide-user/services/vpn/tailscale/start#initial_setup "docs:guide-user:services:vpn:tailscale:start") but keep in mind that you will need to add `--netfilter-mode=off` for each invocation of tailscale in the guide.

For Tailscale versions before `1.58.2-1` the init script may need to be modified to force tailscale to assign an IP to the `tailscale0` interface.

- Edit `/etc/init.d/tailscale`
- After the last `procd_append_param` add: `procd_append_param command --tun tailscale0`

When using IPv6 with the exit node to WAN, default routes may be set up such that they are only routed for the LAN prefix:

```js
# ip addr
default from 2607:dead:beef::1 via fe80::ff:fecb:f5c3 dev eth1  metric 512
default from 2607:dead:beef::/64 via fe80::ff:fecb:f5c3 dev eth1  metric 512
```

You can workaround this by disabling IPv6 Source Routing (note that this may not be ideal if you have multiple upstream IPv6 connections): Eg: Network→Interfaces→(WAN6) Edit → Advanced Settings → IPv6 source routing (Uncheck) → Apply/Save.

Tailscale version 1.54 or later used with OpenWrt 24.10 or later (which uses kernel 6.6) enables [UDP throughput improvements via transport layer offloading](https://tailscale.com/s/ethtool-config-udp-gro "https://tailscale.com/s/ethtool-config-udp-gro").

Namely, tuning two features may show improved throughput:

- `rx-udp-gro-forwarding`: Enables UDP Generic Receive Offload (GRO) forwarding, which aggregates incoming UDP packets to reduce CPU overhead on receive.
- `rx-gro-list`: If disabled (off), it prevents multiple flows from being aggregated simultaneously which simplifies flow handling and performance on some workloads.

These changes should be applied to your physical WAN interfaces which will actually be performing the UDP encapsulation of tailscale traffic

1\. Install `ethtool`

```js
opkg update
opkg install ethtool
```

2\. Apply the changes:

Substitute `eth1` below for your WAN interface.

```js
ethtool -K eth1 rx-gro-list off
ethtool -K eth1 rx-udp-gro-forwarding on
```

3\. Test the changes before and after before committing them permanently with something similar to the following commands.

You want to verify:

- Packet aggregation is working as measured by reduced packets/sec on the wire with GRO enabled (verify with tools like: `ethtool -S <interface> | grep udp` or `netstat -su`)
- CPU usage is reduced. Lower CPU usage on the receiver compared to same test with `rx-udp-gro-forwarding` turned off
- High throughput is achieved near line rate (e.g., 1 Gbps, 10Gbps, etc) without packetloss.

You will need the `iperf3` package installed for this

**Receiver**

```js
iperf3 -s
```

**Sender**

```js
iperf3 -c <remote_addr> -u -b 1G -l 1400 -t 10
```

If you're satisfied with the results and want it to persist across reboots.

4\. Create `/etc/config/ethtool` ether using [uci](https://openwrt.org/docs/guide-user/base-system/uci "docs:guide-user:base-system:uci") or by creating the file manually. The following example will use `uci`:

Substitute `eth1` below for your WAN interface.

```js
touch /etc/config/ethtool
uci set ethtool.eth1=device
uci set ethtool.eth1.rx_gro_list='off'
uci set ethtool.eth1.rx_udp_gro_forwarding='on'
uci commit
```

5\. Create the following file in `/etc/hotplug.d/iface/90-ethtool`:

```bash
#!/bin/sh
# shellcheck disable=SC3043
#
# Author: Josh Enders <josh.enders@gmail.com>
# License: CC BY-NC 4.0
# https://gist.github.com/joshenders/1baa9de07c1b7af489f14c30d4667e40

[ "${ACTION}" = "ifup" ] || exit 0

# shellcheck source=/dev/null
. /lib/functions.sh

config_load ethtool

log_crit() { logger -t "$0" -p crit "$1"; }
log_info() { logger -t "$0" -p info "$1"; }

apply_settings() {
    local config feature ifname option value
    ifname="$1"
    config=$(uci show ethtool."${ifname}" | sed -n "s/^ethtool.${ifname}\.\([^=]*\)=.*/\1/p")

    for option in ${config}; do
        config_get value "${ifname}" "${option}"
        feature=$(echo "${option}" | tr '_' '-')
        if [ -n "${value}" ]; then
            {
                ethtool -K "${ifname}" "${feature}" "${value}" \
                && log_info "${feature} set to ${value} on ${ifname}";
            } || log_crit "Failed to set ${feature} to ${value} on ${ifname}"
        else
            log_crit "Failed to set ${feature} to ${value} on ${ifname}"
        fi
    done
}

config_foreach apply_settings device
```

6\. Append `/etc/hotplug.d/iface/90-ethtool` to `/etc/sysupgrade.conf` to preserve this file during upgrades.

```js
echo '/etc/hotplug.d/iface/90-ethtool' >> /etc/sysupgrade.conf
```

Tailscale cannot be installed on devices with 16MB or less of flash memory because the package and its dependencies consume too much space. Until the day that there is a separate “tailscale-lite” build, your best bet is to compile (or cross-compile) it yourself from upstream sources and use the [multicall binary](https://flameeyes.blog/2009/10/19/multicall-binaries/ "https://flameeyes.blog/2009/10/19/multicall-binaries/") build target.

To reduce the filesize further, you can strip debugging symbols and run the resulting binary through a packer, like *[upx](https://github.com/upx/upx "https://github.com/upx/upx")*. As of `1.56.1`, this will result in ~98% reduction in size (from ~33MB to ~5.2MB).

Instead of running the optimized binaries directly, it is recommend that you repack the `tailscale.ipk`, and `tailscaled.ipk` packages with smaller, optimized binaries. This will let you benefit from OpenWrt conventions like init scripts, opkg installation receipts, etc, keeping your installation sane and consistent while still being able to use the smaller binaries.

If your device has 16MB of flash or less, the tailscale build system offers a “multicall” binary target that can be used to share a single binary between both of the official OpenWrt `tailscale` and `tailscaled` packages and reduces the storage footprint by nearly half. What follows is a brief summary but more detailed, step-by-step copy/paste style instructions are also provided below.

1. Unpack the current official OpenWrt `tailscale` and `tailscaled` packages and “stub” out the large `/usr/sbin/tailscale{d}` binaries contained within them with a small shell script that always returns `true`.
2. Repack both packages
3. Install both packages
4. Manually copy the multicall binary to the device
5. Replace the stubs installed previously with symlinks to the shared multicall binary

The official Tailscale small binary build guide is here:

- [https://tailscale.com/kb/1207/small-tailscale/](https://tailscale.com/kb/1207/small-tailscale/ "https://tailscale.com/kb/1207/small-tailscale/")

Other useful links:

- [https://zyfdegh.github.io/post/202002-go-compile-for-mips/](https://zyfdegh.github.io/post/202002-go-compile-for-mips/ "https://zyfdegh.github.io/post/202002-go-compile-for-mips/")
- [https://serverfault.com/questions/163487/how-to-tell-if-a-linux-system-is-big-endian-or-little-endian/749469#749469](https://serverfault.com/questions/163487/how-to-tell-if-a-linux-system-is-big-endian-or-little-endian/749469#749469 "https://serverfault.com/questions/163487/how-to-tell-if-a-linux-system-is-big-endian-or-little-endian/749469#749469")

Tips:

- You should reset your git checkout of Tailscale to a tagged stable release to ensure compatibility with the OpenWrt package you're repacking. This also makes troubleshooting easier on yourself in the future and is best practice.
- [upx 3.96 produces broken mips binaries](https://github.com/upx/upx/issues/342 "https://github.com/upx/upx/issues/342"), use the latest version. Upx can handle all executable formats, so you don't need to run it under the target architecture.
- You can shave off an additional MB or so with `strip --strip-all`. This strips even more than when using `go build` ldflags alone. Look for the `binutils` package of your target architecture. For my MIPS target on Linux, that was `binutils-mips-linux-gnu`, on macOS the same MacPorts package is called `mips-elf-binutils`.
- Be very careful when repacking your `.ipk` not to include leading paths. An absolute path in the root of the package will produce an unusable `.ipk`.
- Don't forget to symlink `/usr/sbin/talescale.multicall` to `/usr/sbin/tailscale` and `/usr/sbin/tailscaled`.
- If installing on >= 22.03, don't forget to apply the work arounds listed earlier on this page.
- **On slow devices, upx packed executables may appear to hang at first when you run them but this is normal; higher startup time for lower storage costs. If having trouble try compressing without `--best`**
- It's a good idea to check that your `tailscale.multicall` actually runs on your target architecture with a simple `./tailscaled --version` on the target device before going to the trouble of repacking.

Shell history on macOS where I built tailscale from source for a big endian mips target:

```bash
sudo port install go mips-elf-binutils upx
git clone https://github.com/tailscale/tailscale.git
cd tailscale
git checkout tags/v1.56.1 -b v1.56.1
env GOOS=linux GOARCH=mips GOMIPS=softfloat go build -o tailscale.multicall -tags ts_include_cli,ts_omit_aws,ts_omit_bird,ts_omit_tap,ts_omit_kube -trimpath -ldflags="-s -w" ./cmd/tailscaled
/opt/local/bin/mips-elf-strip --strip-all tailscale.multicall
upx --lzma --best tailscale.multicall # (v3.96 has deadlock bug)
```

The steps below were performed on Debian Linux. I repacked the OpenWrt `.ipk` for the `tailscale` and `tailscaled` packages and replaced the large binaries with small stub scripts that always return true. I did this so that the pre/post scripts will run successfully and the opkg database at `/usr/lib/opkg` will be consistent. The packages were installed manually and stub files deleted post installation. The multicall binary was then uploaded and symlinks created.

```bash
# convenience variables
export package=tailscaled_1.56.1-1_mips_24kc.ipk
export release=23.05.2
export arch=mips_24kc

# download .ipk
wget https://downloads.openwrt.org/releases/${release}/packages/${arch}/packages/${package}
mkdir ${package%%.ipk}
pushd ${package%%.ipk}
tar -xvf ../${package}

# data
mkdir data
pushd data
tar -xvf ../data.tar.gz
echo -e '#!/bin/sh\ntrue\n' > usr/sbin/${package%%_*}
tar --numeric-owner --group=0 --owner=0 -czf ../data.tar.gz *
popd
size=$(du -sb data | awk '{ print $1 }')
rm -rf data

# control
mkdir control
pushd control
tar -xvf ../control.tar.gz
sed -i "s/^Installed-Size.*/Installed-Size: ${size}/g" control
tar --numeric-owner --group=0 --owner=0 -czf ../control.tar.gz *
popd
rm -rf control

# repack .ipk
tar --numeric-owner --group=0 --owner=0 -cvzf ../${package} debian-binary data.tar.gz control.tar.gz
popd
```

You should now have a repacked package named `tailscaled_1.56.1-1_mips_24kc.ipk`. You will need to repeat this process for the `tailscale` package.

Set a new package variable:

```js
export package=tailscale_1.56.1-1_mips_24kc.ipk
```

Repeat the repack process above to create the repacked `tailscale` package.

You should now have two repacked packages similar to `tailscale_1.56.1-1_mips_24kc.ipk` and `tailscaled_1.56.1-1_mips_24kc.ipk`. Copy these files to `/tmp` on your device. Since sftp-server is not included with dropbear/OpenWrt, if you're scp from a relatively recent version of OpenSSH you'll need to either use `scp -O` to use the legacy scp fallback mode, or do this ***from*** the OpenWrt device.

```bash
# convenience variables
export version=1.56.1
export arch=mips_24kc

# copy files
scp remote:/tmp/tailscale.multicall /tmp
scp remote:/tmp/tailscaled_${version}-1_${arch}.ipk /tmp
scp remote:/tmp/tailscale_${version}-1_${arch}.ipk /tmp

# install dependencies
opkg install kmod-tun

# install repacked packages
opkg install /tmp/tailscaled_${version}-1_${arch}.ipk
opkg install /tmp/tailscale_${version}-1_${arch}.ipk

# remove stubs and link multicall binary
rm /usr/sbin/tailscaled
rm /usr/sbin/tailscale
cd /usr/sbin
cp /tmp/tailscale.multicall .
ln -s tailscale.multicall tailscaled
ln -s tailscale.multicall tailscale

# verify
tailscale --version
tailscaled --version
```

You're now ready to continue to [initial\_setup](https://openwrt.org/docs/guide-user/services/vpn/tailscale/start#initial_setup "docs:guide-user:services:vpn:tailscale:start").
