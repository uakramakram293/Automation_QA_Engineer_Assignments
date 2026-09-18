"""
Pytest suite validating mDNS device discovery.

Uses discovery_results.json as mocked mDNS discovery output.
"""
from pathlib import Path
from typing import Any

import json
import re

import pytest

from mdns_discovery import validate_device, filter_devices_by_service


DATA_FILE = "discovery_results.json"
EXPECTED_SERVICE = "_speaker._tcp.local"


@pytest.fixture
def devices() -> list[dict[str, Any]]:
    """Load the mocked mDNS discovery results."""
    return json.loads(Path(DATA_FILE).read_text())


def test_device_is_discoverable(devices: list[dict[str, Any]]) -> None:
    """Objective 1: verify at least one device was discovered on the network."""
    assert len(devices) > 0


def test_correct_service_type_is_advertised(devices: list[dict[str, Any]]) -> None:
    """Objective 2: verify every discovered device advertises the expected speaker service."""
    speakers = filter_devices_by_service(devices, EXPECTED_SERVICE)
    assert len(speakers) == len(devices), (
        "One or more discovered devices are not advertising the expected service type"
    )


def test_ip_addresses_are_valid(devices: list[dict[str, Any]]) -> None:
    """Objective 3: verify every device passes full validation, including having
    a well-formed IP address."""
    for device in devices:
        validate_device(device)


def test_hostname_ends_with_local(devices: list[dict[str, Any]]) -> None:
    """Additional test: verify every hostname correctly ends in '.local',
    as required for a valid mDNS advertisement."""
    for device in devices:
        assert device["hostname"].endswith(".local"), (
            f"Invalid hostname: {device['hostname']}"
        )


def test_txt_record_mac_address_format(devices: list[dict[str, Any]]) -> None:
    """Additional test: verify the 'wa' field inside txt_records is a valid
    MAC address, since this is not checked by validate_device()."""
    mac_pattern = r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$"
    for device in devices:
        mac = device.get("txt_records", {}).get("wa", "")
        assert re.match(mac_pattern, mac), f"Invalid MAC address in txt_records: {mac}"


def test_txt_records_contain_required_fields(devices: list[dict[str, Any]]) -> None:
    """Additional test: verify every device advertises the full set of
    required txt_records fields: wa, sn, pt, fv, fn."""
    required_txt_fields = ["wa", "sn", "pt", "fv", "fn"]
    for device in devices:
        txt_records = device.get("txt_records", {})
        for field in required_txt_fields:
            assert field in txt_records, f"Missing txt_records field: {field}"


def test_txt_record_serial_number_is_present(devices: list[dict[str, Any]]) -> None:
    """Additional test: verify the 'sn' (serial number) field inside
    txt_records is a non-empty string."""
    for device in devices:
        sn = device.get("txt_records", {}).get("sn", "")
        assert len(sn) > 0, "Serial number in txt_records must not be empty"


def test_txt_record_production_timestamp_format(devices: list[dict[str, Any]]) -> None:
    """Additional test: verify the 'pt' (production time) field inside
    txt_records is a valid ISO 8601 UTC timestamp, e.g. 2026-08-26T00:02:13Z."""
    pt_pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
    for device in devices:
        pt = device.get("txt_records", {}).get("pt", "")
        assert re.match(pt_pattern, pt), f"Invalid production timestamp in txt_records: {pt}"


def test_txt_record_firmware_version_format(devices: list[dict[str, Any]]) -> None:
    """Additional test: verify the 'fv' (firmware version) field inside
    txt_records follows a dotted numeric version format, e.g. 6.3.0.31."""
    fv_pattern = r"^\d+(\.\d+)+$"
    for device in devices:
        fv = device.get("txt_records", {}).get("fv", "")
        assert re.match(fv_pattern, fv), f"Invalid firmware version in txt_records: {fv}"


def test_txt_record_friendly_name_matches_device_name(devices: list[dict[str, Any]]) -> None:
    """Additional test: verify the 'fn' (friendly name) field inside
    txt_records is non-empty and matches the device's advertised name."""
    for device in devices:
        fn = device.get("txt_records", {}).get("fn", "")
        assert len(fn) > 0, "Friendly name in txt_records must not be empty"
        assert fn == device["name"], (
            f"Friendly name '{fn}' does not match device name '{device['name']}'"
        )