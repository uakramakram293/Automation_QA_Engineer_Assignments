"""
Pytest suite validating BLE and Wi-Fi onboarding connectivity status.

Uses connectivity_status.json as mocked device output.
"""
from pathlib import Path
from typing import Any

import ipaddress
import json
import re

import pytest



DATA_FILE = "connectivity_status.json"


@pytest.fixture
def setup_data() -> dict[str, Any]:
    """Load the mocked connectivity status output for the device under test."""
    return json.loads(Path(DATA_FILE).read_text())


def test_ble_connection_established(setup_data: dict[str, Any]) -> None:
    """Objective 1: verify the device successfully connected over BLE."""
    assert setup_data["ble_connected"] is True


def test_wifi_provisioning_successful(setup_data: dict[str, Any]) -> None:
    """Objective 2: verify the device was successfully provisioned onto Wi-Fi."""
    assert setup_data["wifi_provisioned"] is True


def test_device_received_valid_ip_address(setup_data: dict[str, Any]) -> None:
    """Objective 3: verify the device received a well-formed IP address."""
    ipaddress.ip_address(setup_data["ip_address"])


def test_device_status_is_online(setup_data: dict[str, Any]) -> None:
    """Additional test: verify the overall reported status is 'online',
    consistent with a fully successful onboarding."""
    assert setup_data["status"] == "online"


def test_mac_address_format(setup_data: dict[str, Any]) -> None:
    """Additional test: verify mac_address follows standard MAC format
    (six colon-separated hex byte pairs, e.g. 00:09:A7:12:34:42)."""
    mac_pattern = r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$"
    assert re.match(mac_pattern, setup_data["mac_address"]), (
        f"mac_address '{setup_data['mac_address']}' is not a valid MAC address"
    )


def test_ssid_is_not_empty(setup_data: dict[str, Any]) -> None:
    """Additional test: verify the device reports the SSID it provisioned to,
    and that it is not empty."""
    assert len(setup_data["ssid"]) > 0


def test_device_id_is_not_empty(setup_data: dict[str, Any]) -> None:
    """Additional test: verify the device reports a non-empty device_id."""
    assert len(setup_data["device_id"]) > 0