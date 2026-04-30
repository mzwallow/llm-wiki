# OpenWrt SQM (Smart Queue Management)

SQM is a system to mitigate **bufferbloat**—increased latency (ping) that occurs when a network link is saturated with traffic.

## Core Mechanisms
- **Active Queue Management (AQM)**: Manages packet queues to prevent excessive buffering.
- **Traffic Shaping/Rate Limiting**: Constrains traffic to slightly below the link's physical capacity (typically 90%) to ensure the router, not the modem, stays in control of the queue.
- **Packet Scheduling**: Prioritizes latency-sensitive traffic (VoIP, gaming) over bulk transfers.

## Requirements & Constraints
- **CPU Intensive**: SQM is performed in software. Older or low-power routers may struggle with high-speed links (e.g., Gigabit).
- **Flow Offloading**:
    - **Hardware Flow Offloading**: **Incompatible**. Must be disabled in LuCI (Network → Firewall).
    - **Software Flow Offloading**: Compatible and recommended for higher throughput.
- **Packet Steering**: Enabling Packet Steering (all CPUs) is recommended for modern multi-core devices.

## Implementation (cake vs. fq_codel)
- **cake**: The preferred discipline. Highly effective at mitigating bufferbloat with minimal configuration.
- **fq_codel**: Faster and uses less CPU, but less comprehensive than cake. Recommended if the router is CPU-limited on high-speed lines.

## Configuration Steps
1. **Preparation**: Test peak download/upload speeds using tools like Waveform or Speedtest.
2. **Installation**: Install `luci-app-sqm`.
3. **Basic Settings**:
    - Select the WAN interface.
    - Set Download/Upload limits to ~90% of measured peak speeds.
4. **Queue Discipline**:
    - Queueing Discipline: `cake`.
    - Queue Setup Script: `piece_of_cake.qos`.
5. **Link Layer Adaptation**:
    - Crucial for correct rate shaping.
    - **VDSL/Fiber/Ethernet**: Usually "Ethernet" with overhead (34-44 bytes).
    - **Cable (DOCSIS)**: "Ethernet" with overhead (22-42 bytes).
    - **DSL (ATM)**: "ATM" with overhead (44 bytes).

## See Also
- [[openwrt]]
- [[openwrt-raspberry-pi]]
