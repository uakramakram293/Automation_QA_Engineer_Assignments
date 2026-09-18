# Automation QA Assignment: BLE & Wi-Fi Onboarding

## Part 1 – Test Design & Risk Analysis

### Assumptions

- The device is unconfigured (factory state) and ready for first-time setup.
- The phone is within normal BLE range of the device during onboarding.
- The mobile app has the required Bluetooth and network permissions enabled to scan and connect.
- The Wi-Fi credentials entered by the user are correct, unless a scenario is specifically testing an incorrect password.
- The BLE connection stays active until the device reports its Wi-Fi connection status back to the phone.
- "Weak signal" refers to weak Wi-Fi signal strength during network association, since BLE connectivity issues are already covered separately under "BLE disconnect during provisioning."

### Test Scenarios

#### 1. First-Time Setup
1. Press and hold the device's power button for 5 seconds.
2. Verify that the device's LED starts blinking, indicating it has entered pairing/setup mode.
3. Turn on Bluetooth on the phone.
4. Verify that the device appears in the list of available Bluetooth devices.
5. Select the device and pair with it to establish a BLE connection.
6. Once the BLE connection is established, verify that the phone queries the device for its available services.
7. Verify that the phone identifies the correct service for sending Wi-Fi credentials.
8. Send the Wi-Fi network name (SSID) and password to the device over the BLE connection.
9. Verify that the device successfully joins the Wi-Fi network using the provided credentials.
10. Verify that the device requests an IP address from the network.
11. Verify that the network assigns a valid IP address to the device.
12. Verify that the device reports a successful Wi-Fi connection back to the phone over the BLE connection.
13. Verify that the BLE connection is then closed, and the device becomes discoverable and manageable over Wi-Fi.

#### 2. Incorrect Password
1. Press and hold the device's power button and verify that the LED starts blinking.
2. Turn on Bluetooth on the phone.
3. Select and pair with the device to establish a BLE connection.
4. Verify that the device is connected.
5. Verify that the device requests the Wi-Fi name and password.
6. Send the Wi-Fi name and an incorrect password to the device over the BLE connection.
7. Verify that the device attempts to join the network using the provided credentials.
8. Verify that the device fails to join the network.
9. Verify that the device sends a message to the phone over BLE indicating that the password is incorrect.
10. Enter the correct password on the phone.
11. Send the correct password to the device over the BLE connection.
12. Verify that the device receives the correct password and successfully joins the network.
13. Verify that the device reports a successful Wi-Fi connection back to the phone over the BLE connection.
14. Verify that the BLE connection is then closed, and the device becomes discoverable and manageable over Wi-Fi.

#### 3. Weak Signal (Wi-Fi)
1. Press and hold the device's power button for 5 seconds.
2. Verify that the device's LED starts blinking.
3. Turn on Bluetooth on the phone.
4. Select and pair with the device from the available devices menu.
5. Verify that the BLE connection is established with the device.
6. Verify that the device requests the Wi-Fi name and password.
7. Enter and send the Wi-Fi name and password to the device.
8. Verify that the device receives the credentials and attempts to join the network.
9. Verify that the device fails to join due to weak Wi-Fi signal, and reports this failure to the phone over the BLE connection.
10. Check the Wi-Fi signal strength and reboot the router.
11. Wait 10 seconds and verify that the Wi-Fi signal is restored and working.
12. Send the Wi-Fi name and password to the device again.
13. Verify that the device receives the credentials and attempts to join the network again.
14. Verify that the device successfully joins the network this time.
15. Verify that the device reports a successful Wi-Fi connection back to the phone over the BLE connection.
16. Verify that the BLE connection is then closed, and the device becomes discoverable and manageable over Wi-Fi.

#### 4. BLE Disconnect During Provisioning
1. Press and hold the device's power button for 5 seconds.
2. Verify that the device's LED starts blinking.
3. Turn on Bluetooth on the phone.
4. Verify that the device appears in the list of available devices.
5. Select and pair with the device, and verify that the BLE connection is established.
6. Send the Wi-Fi credentials to the device.
7. Verify that the device receives the credentials.
8. Verify that the device successfully joins the Wi-Fi network.
9. Turn off Bluetooth on the phone for 5 seconds, disconnecting the BLE link right after the device has joined the network but before it can confirm this back to the phone.
10. Verify that the device's LED starts blinking again, and that the BLE connection is broken.
11. Turn Bluetooth back on and verify that the device automatically reconnects with the phone.
12. Verify that the device does not ask for the Wi-Fi credentials again, and instead correctly reports that it has already successfully joined the network.
13. Verify that the BLE connection is then closed, and the device becomes discoverable and manageable over Wi-Fi.

#### 5. SSID Changes
1. Press and hold the device's power button for 5 seconds, and verify the LED starts blinking.
2. Turn on Bluetooth on the phone and pair with the device, verifying the BLE connection is established.
3. Verify that the device requests the Wi-Fi name and password.
4. Rename the router's SSID (e.g., from "HomeWiFi" to "HomeWiFi_New") before sending the credentials to the device.
5. Send the original, now outdated, Wi-Fi name and password to the device over BLE.
6. Verify that the device attempts to join the network using the outdated SSID.
7. Verify that the device fails to find or join the network, since that SSID is no longer being broadcast.
8. Verify that the device reports this failure clearly to the phone over BLE (e.g., "network not found").
9. Send the updated SSID and password to the device.
10. Verify that the device successfully joins the Wi-Fi network using the updated SSID.
11. Verify that the device reports a successful Wi-Fi connection back to the phone over the BLE connection.
12. Verify that the BLE connection is then closed, and the device becomes discoverable and manageable over Wi-Fi.

#### 6. DHCP Delays
1. Press and hold the device's power button for 5 seconds, and verify the LED starts blinking.
2. Turn on Bluetooth on the phone and pair with the device, verifying the BLE connection is established.
3. Send the Wi-Fi credentials to the device.
4. Verify that the device receives the credentials and successfully authenticates onto the Wi-Fi network.
5. Verify that the device then requests an IP address from the router via DHCP.
6. Introduce a delay in the DHCP server's response, simulating a slow or congested network.
7. Verify that the device continues waiting for the IP address without disconnecting or reporting failure prematurely.
8. Once the IP address is eventually assigned, verify that the device correctly reports a successful Wi-Fi connection back to the phone over BLE.
9. Verify that the BLE connection is then closed, and the device becomes discoverable and manageable over Wi-Fi.

#### 7. Multiple Devices Onboarding Simultaneously
1. Press and hold the power button on three devices at the same time, and verify the LED blinks on all three.
2. Turn on Bluetooth on the phone and verify that all three devices appear as distinct entries in the available devices list.
3. Pair with each device individually and send its respective Wi-Fi credentials.
4. Verify that each device independently receives its own credentials without interference or mix-up between devices.
5. Verify that each device successfully joins the Wi-Fi network and receives its own unique IP address.
6. Verify that each device reports its own successful connection back over its own BLE link, with no cross-talk or status mix-up between devices.
7. Verify that all three devices become discoverable and manageable over Wi-Fi once onboarding completes.

#### 8. Device Reboot During Setup
1. Press and hold the device's power button for 5 seconds, and verify the LED starts blinking.
2. Turn on Bluetooth on the phone and pair with the device, verifying the BLE connection is established.
3. Send the Wi-Fi credentials to the device.
4. Verify that the device receives the credentials and begins attempting to join the network.
5. While the device is mid-connection, before it reports success or failure, force the device to reboot.
6. Verify that after rebooting, the device returns cleanly to pairing/setup mode, rather than getting stuck in a half-configured state.
7. Verify that the LED indicates the device is back in pairing mode.
8. Re-pair with the device over BLE and resend the Wi-Fi credentials.
9. Verify that the device successfully joins the network this time and reports success back to the phone.
10. Verify that the BLE connection is then closed, and the device becomes discoverable and manageable over Wi-Fi.

### Risk Assessment

**High Level**
- **BLE disconnect during provisioning:** High risk because it can produce a silent failure — the device may have actually joined the network successfully, but the phone never receives confirmation, leaving the user thinking setup failed. This is likely to occur whenever BLE range is marginal or a phone's Bluetooth connection briefly drops, which is common in real-world use.
- **Device reboot during setup:** High severity because an unexpected reboot mid-provisioning could leave the device in a corrupted or half-configured state, potentially requiring a factory reset to recover. Less frequent than a BLE drop, but the impact on the user is severe.
- **Incorrect password:** Very common user error (typos, outdated passwords), and if the failure message isn't clear, users may assume the device itself is faulty rather than realizing it's a credential issue.

**Medium Level**
- **Weak Wi-Fi signal:** Fairly common in real homes where the device is set up far from the router. Generally recoverable once the user notices and moves the device or fixes the signal, and the failure is reported clearly rather than silently.
- **DHCP delays:** Moderately common on congested or slow networks. Usually resolves on its own once the router responds, but risk increases if the device's internal timeout is too short and it gives up before the IP is actually assigned.

**Low Level**
- **SSID changes:** Low probability of occurring in practice, since it requires the router's network name to be changed in the narrow window between the user selecting it and the device attempting to join. When it does happen, the device reports a clear "network not found" style failure rather than failing silently, which limits real-world impact.
- **Multiple devices onboarding simultaneously:** Less common for a typical single-device household, but relevant for multi-room audio setups. Main risk is BLE interference or congestion when several devices advertise and pair in close proximity at the same time.
- **First-time setup:** This is the happy path and the most exercised flow in real-world use, so it is generally low risk in normal conditions — but it remains the essential baseline that every other scenario builds on.

## Part 3 – Troubleshooting

### Probable Root Cause

The device received the Wi-Fi credentials successfully, just before the BLE connection disconnected unexpectedly. The device then attempted to join the Wi-Fi network, and authentication was successful, since it reached the DHCP stage. The device then failed to receive an IP address from the router within the expected time, causing a DHCP timeout and the overall setup to fail. The BLE disconnect appears to be a separate issue and not the actual cause of the setup failure.

### Additional Debug Data Required

- Router/DHCP server logs, to check if a DHCP request was received from the device and why no IP address was given.
- App-side logs, to check whether the failure was reported by the device itself, or is just the app's own timeout after losing the BLE connection.
- Signal strength logs at the time of the BLE disconnect, to check if it was caused by range or interference.
- Device network stack logs, to confirm Wi-Fi authentication was actually successful before the DHCP request was sent.

### Regression Tests

1. Verify that if BLE disconnects right after credentials are sent, the device still completes the Wi-Fi join and DHCP process on its own.
2. Simulate a delayed or dropped DHCP response in the lab to check that the device's timeout value is reasonable, and that it reports a clear DHCP failure reason instead of a generic error.
3. Verify that once BLE reconnects after such a failure, the device reports the DHCP failure clearly back to the phone.

## Part 4 – System Thinking

### System-Level Test Architecture

At a system level, the goal is to remove any manual/human action from the test loop and replace every physical interaction with a piece of controllable, scriptable hardware, all orchestrated from a single Linux-based control host.

**Linux Systems**
A Linux test-controller machine sits at the center of the rig. It runs the pytest suite, drives every piece of hardware over USB/serial/network interfaces (using Python libraries such as PyVISA or pyserial), collects logs from the device under test, and reports results back to CI. Linux is the standard choice here because of its strong USB/serial driver support, easy SSH-based control of network equipment, and smooth integration with Python-based test frameworks.

**Hardware Test Equipment**
- **BLE adapter (acting as the "phone"):** A USB Bluetooth adapter connected to the Linux host runs a scripted BLE client that plays the role of the mobile app — scanning for the device, pairing, discovering services, and writing Wi-Fi credentials to the correct characteristic, exactly as a real phone app would.
- **Controllable power switch:** Used to power-cycle the device under test on command. This is essential for the "device reboot during setup" scenario, since it lets the test control exactly when and for how long the device loses power.
- **RF attenuator:** Placed in the Wi-Fi signal path to programmatically reduce signal strength on demand, simulating the "weak signal" scenario in a precise, repeatable way, instead of physically moving the device around a room.
- **Vector spectrum analyzer:** Connected downstream of the attenuator to measure the actual RF power level and signal quality reaching the device at each attenuation step. This gives the rig a calibrated, trustworthy signal strength value rather than relying on the attenuator's dial setting alone, which keeps the weak-signal test repeatable across runs and hardware batches.

**GitHub Actions**
GitHub Actions is the trigger and orchestration layer. A workflow runs automatically whenever new firmware is pushed: it checks out the code, deploys the new firmware to the device under test through a self-hosted runner connected to the lab rig, executes the pytest suite against the physical setup, and publishes a pass/fail report with logs and pytest output as build artifacts.

**Controlled Network Infrastructure**
Instead of a normal home router, the lab uses a programmable access point that exposes an API or SSH interface, allowing the test scripts to:
- Rename the SSID on demand, for the SSID-change scenario
- Inject artificial DHCP delay or drop DHCP responses, for the DHCP-delay scenario
- Trigger a full router reboot programmatically, for the router-reboot scenario
- Keep the test network isolated from other traffic, so test runs stay repeatable and are not affected by unrelated devices

### Summary

This setup — a Linux host, BLE adapter, controllable power switch, RF attenuator with vector spectrum analyzer, and a programmable access point — lets every onboarding scenario from Part 1 run and be verified automatically, without any manual button presses, device moving, or Wi-Fi renaming. GitHub Actions runs this pipeline on every firmware change.
