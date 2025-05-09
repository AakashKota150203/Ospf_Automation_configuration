# orchestrator.py

"""
Orchestrator module to automate:
1. Configuration of all Juniper devices via REST API.
2. Ping verification of all loopback interfaces (full mesh).
3. Retrieval and verification of OSPF-related information (neighbors, interfaces, routes, database).

This acts as the top-level controller for full lifecycle management of the network lab.
"""

from build_device_payloads import devices, interface_payloads, ospf_payloads, config
from rest_client import send_payload, commit_configuration, ping_host
from xml_parser import parse_ping_results
from verify_ospf_config import check_ospf_status


def configure_all_devices():
    """
    Sends interface and OSPF configuration to all devices, followed by a commit.

    Returns:
        List[str]: Status messages for each device's configuration outcome.
    """
    summary = []

    for name, device in devices.items():
        try:
            send_payload(device, interface_payloads[name])
            send_payload(device, ospf_payloads[name])
            commit_configuration(device)
            result = f"{name} → Configured successfully ✅"
        except Exception as e:
            result = f"{name} → Configuration failed ❌ ({e})"
        print(result)
        summary.append(result)

    return summary


def verify_all_device_pings():
    """
    Executes ping tests between all loopbacks of each device.

    Returns:
        List[dict]: Summary of ping results (packet loss and average RTT).
    """
    results = []

    for src_name, src_device in devices.items():
        for dst_name, dst_device in devices.items():
            if src_name == dst_name:
                continue

            status, xml = ping_host(src_device, dst_device["router-id"])

            if status == 200:
                stats = parse_ping_results(xml)
                result = {
                    "source": src_name,
                    "target": dst_name,
                    "target_ip": dst_device["router-id"],
                    "packet_loss": stats.get("packet_loss", "N/A") if stats else "N/A",
                    "rtt_avg": stats.get("rtt_avg", "N/A") if stats else "N/A"
                }
            else:
                result = {
                    "source": src_name,
                    "target": dst_name,
                    "target_ip": dst_device["router-id"],
                    "packet_loss": "N/A",
                    "rtt_avg": "N/A"
                }

            print(f"{result['source']} → {result['target']} ({result['target_ip']}): "
                  f"Loss = {result['packet_loss']}%, Avg RTT = {result['rtt_avg']} ms")

            results.append(result)

    return results


def verify_ospf_all_devices():
    """
    Calls the OSPF verification function for all devices using full device config list.

    Returns:
        List[dict]: OSPF details per device (neighbors, interfaces, routes, etc.)
    """
    return check_ospf_status(config["devices"])
