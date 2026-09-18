# Part 4 – System Thinking: Automating mDNS Validation in CI

## Goal
Take the mocked pytest suite from Part 2 and run it for real, against real
devices, automatically, on every code change and on a schedule.

## 1. Linux systems
- mDNS uses local network multicast, so it can't be tested from a
  cloud runner. We need a **self-hosted Linux runner** sitting on the
  same network as the devices (a lab PC or a Raspberry Pi works).
- On that runner, use `avahi-browse` or Python's `zeroconf` library to
  do a **real mDNS scan** instead of reading `discovery_results.json`.
- Keep the same pytest checks from Part 2 (`validate_device`,
  `filter_devices_by_service`). Only the data source changes — the
  test logic doesn't.

## 2. Hardware test equipment
- We need to physically control the device to test real failure cases
  from Part 1: power cycle, Wi-Fi drop, router reboot.
- A **network-controlled power switch** lets tests turn the speaker
  off/on.
- A **managed router/switch with an API** lets tests kill Wi-Fi or
  force a new DHCP lease.
- Each action becomes a small helper function (e.g. `power_cycle()`,
  `disable_wifi()`) called before running the mDNS checks.

## 3. GitHub Actions
- Run the job on a **self-hosted runner** (not `ubuntu-latest`), since
  it needs LAN and hardware access.
- Trigger on:
  - **Every PR/push** touching firmware or app code — fast feedback.
  - **A nightly schedule** — catches issues that only show up over
    time, like the device silently dropping off mDNS.
- On failure, upload logs and the mDNS scan output as build artifacts,
  so the issue can be debugged without needing lab access.

## 4. Network infrastructure
- Use a **separate test Wi-Fi/VLAN**, so test traffic doesn't clash
  with production and multiple devices don't get duplicate hostname
  conflicts.
- Use a router that can be **scripted** to simulate a reboot or force a
  new IP lease.
- Add **packet capture** (`tcpdump`) on the test network, so a failed
  test shows the actual mDNS traffic (or lack of it) — turning "test
  failed" into "here's proof the device never re-announced itself."

## Summary
The pytest logic from Part 2 stays the same. What changes for CI is the
environment: a self-hosted Linux runner with access to real devices,
network hardware to simulate outages, and GitHub Actions triggering
runs on every change and on a schedule — all on an isolated test
network with packet capture for debugging.
