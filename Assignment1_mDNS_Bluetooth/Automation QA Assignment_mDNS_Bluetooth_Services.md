# Automation QA Assignment: mDNS & Bluetooth Services

## Part 1 – Test Design & Risk Analysis

### Assumptions

- The internet connection is stable and has no interruptions.
- Whenever the device boots, it automatically announces itself.
- The mobile app continuously searches or sends a query whenever it is opened, or whenever a nearby device becomes available.
- The router does not block multicast announcements and allows the device to send its advertisement.

### Test Scenarios

#### 1. Device Boot / First Connection
1. Press and hold the device's power button for 5 seconds.
2. Verify that the blue LED starts blinking.
3. Open the mobile app and connect it to the local network.
4. Verify that the device/speaker advertisement appears in the app.
5. Verify that the address, hostname, and service type are shown correctly.
6. Select the device in the app and verify that it shows as connected, and that the blinking light stops.

#### 2. Wi-Fi Disconnect / Reconnect
1. Turn off Wi-Fi on the phone and wait 5 seconds.
2. Turn Wi-Fi back on and verify that the phone reconnects to the network.
3. Verify that the blue LED starts blinking again due to the disconnection.
4. Open the app and verify that the speaker re-announces itself, with the hostname and address appearing again.
5. Click on the device in the app and verify that it connects successfully.

#### 3. Power Cycle
1. Press and hold the device's power button for 5 seconds to power it off.
2. Verify that the device sends a final "goodbye" announcement.
3. Verify in the app that the device disappears and shows as disconnected.
4. Power the device back on by pressing and holding the button for 5 seconds.
5. Verify that the blue LED starts blinking again.
6. Check in the app that a new announcement is made by the speaker.
7. Click on the device in the app to connect.
8. Verify that it connects successfully and the blue LED stops blinking.

#### 4. Multiple Devices on the Same Network
1. Press and hold the power button on each of the three devices for 5 seconds.
2. Verify that the blue LED starts blinking on all three devices.
3. Open the app and check that all three devices are advertising.
4. Verify that each device has a unique/distinct hostname and address.
5. Select the device you want to connect to.
6. Verify that the connection is established successfully.
7. Verify that the blue LED on that specific speaker stops blinking.

#### 5. IP Address Change (DHCP Renewal)
1. Update the mobile app to the newer version.
2. Open the app and verify that it asks for the Wi-Fi password again.
3. Enter the password and verify that the app connects to the Wi-Fi network.
4. Verify that no old/previous device entries are already shown in the discovery list.
5. Power on the speaker and hold the button for 5 seconds.
6. Verify that the blue LED starts blinking, indicating the device is advertising.
7. Check the app to confirm the device appears with its hostname and a new IP address.
8. Click on the device and verify that it connects successfully.
9. Verify that the LED on the speaker stops blinking.

#### 6. Router Reboot
1. Power off the Wi-Fi router and wait for 10 seconds.
2. Verify that the speaker's LED starts blinking, indicating loss of connection.
3. Verify that the app either fails to load the device list or shows a "no Wi-Fi" error message.
4. Power the router back on and wait 5 seconds.
5. Verify that the app opens successfully and the speaker automatically reconnects and appears in the app.

#### 7. Duplicate Hostname / Service Conflict
1. Open the mobile app.
2. Power on two adjacent speakers and hold the power button on both for 5 seconds at the same time.
3. Manually set the same hostname on both speakers.
4. Verify that both speakers' LEDs start blinking and that both begin advertising simultaneously.
5. Open the app and check whether both speakers with the same hostname appear, and observe how the conflict is handled.
6. Verify that the device which detects the conflict automatically renames itself (e.g., appends "-2" to the hostname) and re-announces under the new, unique hostname.
7. Verify that both speakers appear as two distinct entries in the app, each independently connectable, rather than one entry overwriting the other.
8. If no automatic renaming occurs, note whether only one speaker appears in the app (the second silently dropped or overwritten), or both appear under the identical hostname with only one actually reachable.

### Risk Assessment

Risk is categorized by criticality (how severe the failure is for the user) and frequency (how often the situation occurs in real-world use).

**High Level**
- **IP address change (DHCP renewal):** High severity because the failure is silent — the device is powered on and functioning normally, but becomes invisible to the app, which matches the exact symptom reported by customers. It is also high frequency, since DHCP leases renew routinely on any home network, often without the user doing anything or noticing.
- **Wi-Fi disconnect/reconnect:** Extremely common in real-world use — a phone moving out of range, temporary interference, or brief signal drops happen regularly during normal daily use, so any gap in re-announcement behavior affects a large share of users.
- **Router reboot:** Can happen due to power outages, ISP-triggered resets, scheduled maintenance restarts, or a user manually resetting the router. Less frequent than day-to-day Wi-Fi hiccups, but the impact is high because it affects every device on the network at once, not just a single speaker.

**Medium Level**
- **Power cycle:** Very common, since users routinely turn the speaker off and on. Severity is medium rather than high because the expected behavior (a goodbye announcement on power-off, a fresh advertisement on power-on) is well defined and testable, and unlike the silent failures above, the user is aware the device is off, so a temporary disappearance from the app is expected and less likely to be mistaken for a fault.

**Low Level**
- **Duplicate hostname / service conflict:** Low probability of occurring, since it requires two devices to probe for the same name at nearly the same instant, which is uncommon in typical home setups with only a handful of devices. Most mDNS implementations also include built-in conflict resolution, further reducing real-world impact.
- **Multiple devices on the same network:** Lower risk for the average household, since most homes have only one or two speakers rather than many. It remains a valid scenario to cover for larger setups, but naming collisions or congestion-related issues here are closer to edge cases than everyday occurrences.

### Automation Priority

I will automate the test cases in the following order:

1. **Device boot / first connection** – Automated first to establish that the baseline connection works. Every other scenario builds on this, so it needs to be solid before anything else.
2. **Power cycle** – Automate the process of the device booting up and turning off correctly, with the initial advertisement sent on power-on and the goodbye advertisement sent on power-off.
3. **IP address change (DHCP renewal)** – Create a trigger for the IP change in the lab and replicate the real scenario reported by customers. This is prioritized early because it directly matches the reported issue.
4. **Wi-Fi disconnect/reconnect** – Automate next, since it is very common in daily use and easy to trigger reliably in a lab setup.
5. **Router reboot** – Automate after the above, since it is less common and has a longer test runtime, but it still provides valuable regression coverage.
6. **Multiple devices on the same network** – After the single-device test cases are working, automate this scenario, since it requires multiple physical units and more test rig investment.
7. **Duplicate hostname / service conflict** – Automate last, since it is a rare, timing-dependent scenario that is difficult to trigger reliably. I will treat this as exploratory/manual testing first, and only invest in full automation if it turns out to be a recurring real-world issue.

## Part 3 – Troubleshooting

### Most Likely Root Cause

When the router restart is detected, Wi-Fi disconnects and then reconnects with a new IP address. An app discovery request is issued immediately after reconnecting, but the log shows it is only queried for around 1 second. This suggests the app stops listening for devices too early and misses the device's re-announcement, resulting in the device not appearing in the app, despite being connected and functioning correctly.

### Additional Information Required

- App-side logs, to confirm whether the app actually received any mDNS response from the multicast query, or whether the request simply timed out before a response arrived.

### Regression Tests

1. Verify that the device appears with its new IP address in the app after a router restart.
2. Measure how long after the IP change the device sends its re-announcement, to confirm this falls within the app's discovery window.
3. Repeat the router restart multiple times to observe how consistently the device responds each time.

## Part 4 – System Thinking

### System-Level Test Architecture

At a system level, the goal is to remove manual/human action from every scenario in Part 1 and replace it with controllable, scriptable hardware and network infrastructure, all orchestrated from a Linux-based test rig.

**Linux Systems**
A Linux test-controller machine runs the pytest suite, drives the physical hardware over USB/serial/network interfaces, and, importantly for mDNS specifically, runs a packet capture tool (such as `tcpdump` or Python's `zeroconf`/`scapy` libraries) to listen directly on the network for the actual multicast announcements. This gives the test rig ground-truth visibility into whether the device really sent an mDNS packet, rather than relying only on what the mobile app displays.

**Hardware Test Equipment**
- **Controllable power switch:** Used to power the device on and off on command, needed for the "device boot" and "power cycle" scenarios, so the test controls exactly when and for how long the device loses power.
- **Multiple physical device units:** Needed for the "multiple devices on the same network" scenario, since this behavior can only be properly verified with real, simultaneously operating hardware rather than a single unit.
- **Network tap or a managed switch with a mirror/SPAN port:** Placed between the devices and the router so the Linux host can passively capture all mDNS multicast traffic on the network without interfering with it, giving an independent, packet-level view of every announcement, query, and response.

**GitHub Actions**
GitHub Actions triggers the pipeline automatically whenever new firmware is pushed: it checks out the code, deploys the firmware to the device under test through a self-hosted runner connected to the lab rig, runs the pytest suite against the physical setup, and publishes a pass/fail report along with logs and captured packet data as build artifacts.

**Network Infrastructure**
Rather than a normal home router, the lab uses a programmable access point/router that exposes an API or SSH interface, allowing the test scripts to:
- Force a full router reboot programmatically, for the router-reboot scenario
- Trigger a Wi-Fi disconnect/reconnect and a DHCP lease renewal on demand, for the IP-address-change scenario
- Keep the test network isolated from other traffic, so results stay repeatable and are not affected by unrelated devices

### Summary

This setup — a Linux host with packet capture, a controllable power switch, multiple physical units, and a programmable router — lets every scenario from Part 1 run and be verified automatically, without any manual button presses or router unplugging. GitHub Actions runs this pipeline on every firmware change.
