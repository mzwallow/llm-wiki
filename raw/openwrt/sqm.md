---
title: "[OpenWrt Wiki] SQM (Smart Queue Management)"
source: "https://openwrt.org/docs/guide-user/network/traffic-shaping/sqm"
author:
published:
created: 2026-04-29
description:
tags:
  - "clippings"
---
OpenWrt supports SQM for mitigating [bufferbloat](https://en.wikipedia.org/wiki/bufferbloat "https://en.wikipedia.org/wiki/bufferbloat"), the undesirable latency that arises when your router buffers too much data.

Bufferbloat is most evident when a connection is heavily loaded with downloads or uploads. This causes increased latency (ping), resulting in poor performance for realtime tasks like VoIP, Wi-Fi calling, video chat, lag in online gaming, and generally makes the internet less responsive. This latency can be mitigated with SQM.

SQM is an integrated system that performs per-packet/per-flow network scheduling, active queue management (AQM), traffic shaping, rate limiting, and QoS prioritization. In comparison, “classic” AQM only manages queue length, and “classic” QoS only does prioritization.

SQM is performed on the CPU, as such slower devices may be unable to [keep up](https://forum.openwrt.org/t/so-you-have-500mbps-1gbps-fiber-and-need-a-router-read-this-first/90305 "https://forum.openwrt.org/t/so-you-have-500mbps-1gbps-fiber-and-need-a-router-read-this-first/90305") with your peak internet speed.

SQM is incompatible with hardware flow offloading which bypasses part of the kernel as discussed in [this thread](https://forum.openwrt.org/t/sqm-and-non-sqm-queue-issues-lan-vs-wlan/15433/10 "https://forum.openwrt.org/t/sqm-and-non-sqm-queue-issues-lan-vs-wlan/15433/10"). Be sure that is disabled on the LuCI → Network → Firewall dropdown box. Note that SQM does work with software flow offloading selected.

Before you can optimize your network, you need to test its initial state.

- To maximize performance most modern devices will benefit from enabling Packet Steering (all CPUs) under LuCI → Network → Interfaces → Global network options.
- When your internet is unused run a speed test at [Waveform](https://www.waveform.com/tools/bufferbloat "https://www.waveform.com/tools/bufferbloat") or [Speedtest](https://speedtest.net/ "https://speedtest.net"). This is to determine your peak download/upload speeds, latency, and grade your bufferbloat.
- If you are using this OpenWrt device as an [Extender, Repeater, or Bridge](https://openwrt.org/docs/guide-user/network/wifi/relay_configuration "docs:guide-user:network:wifi:relay_configuration"), test your upstream router (OpenWrt or otherwise) and determine if an issue is present there first.
- If you are on a [wireless AP](https://openwrt.org/docs/guide-user/network/wifi/wifiextenders/bridgedap "docs:guide-user:network:wifi:wifiextenders:bridgedap"), test your upstream router separately. If your AP wifi driver supports AQL limits (e.g. [mt76](https://openwrt.org/docs/techref/driver.wlan/mt76 "docs:techref:driver.wlan:mt76") does) adjust/reduce those seperately to improve wifi latency.

[Install](https://openwrt.org/docs/guide-user/additional-software/managing_packages "docs:guide-user:additional-software:managing_packages") the package `luci-app-sqm` (or `sqm-scripts` if you don't want LuCI) and follow below.

In LuCI go to **Network → SQM QoS**:

1. In the **Basic Settings** tab:
	- Check the **Enable** box
		- Set the **Interface** to your internet (WAN) link in the dropdown. Check Network → Interfaces if you need to determine your WAN port.
		- Enter your **Download** and **Upload** speeds to 90% of the results you tested during Preparation.
2. In the **Queue Discipline** tab:
	- Choose *cake* as the Queueing Discipline (or *fq\_codel*, consider [note 3](https://openwrt.org/docs/guide-user/network/traffic-shaping/sqm#a_little_more_tuning "docs:guide-user:network:traffic-shaping:sqm"))
		- Choose *piece\_of\_cake.qos* as the Queue Setup Script
		- Advanced Configuration may be left unchecked (see notes for advanced settings)
3. In the **Link Layer Adaptation** tab, select your link type and overhead (setting mpu is optional see [note 1](https://openwrt.org/docs/guide-user/network/traffic-shaping/sqm#a_little_more_tuning "docs:guide-user:network:traffic-shaping:sqm")):
	- *VDSL* - choose **Ethernet**, and set overhead 34 (or 26 if you're not using PPPoE) (mpu 68). If the link is 100 Mbps Ethernet set overhead 42 (mpu 84).
		- *DSL of any other type* - choose **ATM**, and set overhead 44 (mpu 96).
		- *DOCSIS Cable* - choose **Ethernet**, and for rates < 760 Mbps set overhead 22 (mpu 64), for rates >= 760 Mbps set overhead 42 (mpu 84).
		- *Fiber* - choose **Ethernet**, and set overhead 44 (mpu 84).
		- *Ethernet* - choose **Ethernet**, and set overhead 44 (mpu 84).
		- If you are unsure, it's better to overestimate, choose **Ethernet**, and set overhead 44 (mpu 96).
4. Click **Save & Apply**.

Done! You can confirm results by re-running the speedtest. Any increased ping during download/uploads will now be minimal.

As an example, the user below is running OpenWrt on a [WRT32X](https://openwrt.org/toh/linksys/wrt_ac_series "toh:linksys:wrt_ac_series") router. The internet connection is a DOCSIS cable modem with 500/35 Mbit service and this ISP includes over-provisioning. SQM cake was selected with 90% dl/ul limits on baseline speedtest values. Packet Steering (all CPUs)/RPS 128 is also enabled. Latency increase under load dropped to zero, lower ping with no packet loss is observed during VoIP and online gaming during heavy internet usage. The user's [speedtest results with SQM](https://www.waveform.com/tools/bufferbloat?test-id=e101a8fc-f017-4eef-8f90-b27bcb783d62 "https://www.waveform.com/tools/bufferbloat?test-id=e101a8fc-f017-4eef-8f90-b27bcb783d62") and summary of tests below:

<table><thead><tr><th colspan="8">Speedtest Results</th></tr></thead><tbody><tr><td><abbr>QoS</abbr></td><td>Download</td><td>Upload</td><td>Unloaded Ping</td><td>DL Latency</td><td>UL Latency</td><td>Quality grade</td><td>Bufferbloat grade</td></tr><tr><td>None</td><td>532 Mbits</td><td>37 Mbits</td><td>12 ms</td><td>+18 ms</td><td>+38 ms</td><td>B</td><td>B</td></tr><tr><td>SQM</td><td>495 Mbits</td><td>28 Mbits</td><td>12 ms</td><td>+0 ms</td><td>+0 ms</td><td>A+</td><td>A +</td></tr></tbody></table>

1\. Set your **mpu** to ensure rate shaping is correct for small packets in LuCI under SQM QoS → Link Layer Adaptation → Advanced Linklayer Options. See [SQM Details](https://openwrt.org/docs/guide-user/network/traffic-shaping/sqm-details "docs:guide-user:network:traffic-shaping:sqm-details") and [SQM setting question](https://forum.openwrt.org/t/sqm-setting-question-link-layer-adaptation/2514/9 "https://forum.openwrt.org/t/sqm-setting-question-link-layer-adaptation/2514/9") for more details.

2\. The steps above will handle latency well but you may improve it further with these steps:

- Increase your Download and Upload speed settings and retest until bufferbloat latency occurs, then go back to a slightly lower value. Note that the settings are gross rates which include overhead, so measured speedtests will be a bit lower.
- Test using [Waveform](https://www.waveform.com/tools/bufferbloat "https://www.waveform.com/tools/bufferbloat") speedtest to achieve A+ quality and A+ bufferbloat grades when optimal settings are found.
- For DSL, this may produce download/upload values that are actually *higher* than the original speed test. This is ok, ATM framing bytes of a DSL link add an average of 9% overhead, and these settings tell SQM how to make up for that overhead.
- For DOCSIS cable, know that some providers trick speed tests by adding 10% over-provisioning for the first 10 seconds (so speed tests look better!).

3\. While [Cake](https://www.bufferbloat.net/projects/codel/wiki/Cake/ "https://www.bufferbloat.net/projects/codel/wiki/Cake/") is the preferred queue discipline as it is excellent at mitigating bufferbloat, fq\_codel is a faster, albeit less comprehensive option. One user found fq\_codel gave [about 15% higher throughput when CPU limited](https://forum.openwrt.org/t/netgear-r6220-sqm-results-downstream-cut-in-half-and-my-optimal-settings/114301 "https://forum.openwrt.org/t/netgear-r6220-sqm-results-downstream-cut-in-half-and-my-optimal-settings/114301") and this [thread](https://lists.bufferbloat.net/pipermail/cake/2018-April/003384.html "https://lists.bufferbloat.net/pipermail/cake/2018-April/003384.html") showed similar results. See discussion of these algorithms on this [forum post](https://forum.openwrt.org/t/sqm-codel-and-sfq/219100/4 "https://forum.openwrt.org/t/sqm-codel-and-sfq/219100/4").

4\. See [SQM configuration](https://openwrt.org/docs/guide-user/network/traffic-shaping/sqm_configuration "docs:guide-user:network:traffic-shaping:sqm_configuration") for more advanced settings.
