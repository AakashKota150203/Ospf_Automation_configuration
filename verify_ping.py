# verify_ping.py

"""
This module verifies end-to-end loopback reachability across all configured devices.
It performs:
- A full mesh ping test between router loopbacks.
- Parsing of XML results for RTT and packet loss.
- Displays and returns a summary table of ping success.
"""

from build_device_payloads import devices
from rest_client import ping_host
from xml_parser import parse_ping_results


def verify_all_device_pings():
    """
    Executes ping tests from every device to all others.

    Returns:
        List[dict]: A list of ping result dictionaries with fields:
                    - source
                    - target
                    - target_ip
                    - packet_loss (%)
                    - rtt_avg (ms)
    """
    results = []

    for src_name, src_device in devices.items():
        print(f"\n🔄 Verifying reachability FROM {src_name} ({src_device['router-id']})")

        for dst_name, dst_device in devices.items():
            if src_name == dst_name:
                continue  # Skip self-ping

            # Send ping RPC
            status, xml = ping_host(src_device, dst_device["router-id"])

            # Parse and summarize result
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

            # Print formatted output
            print(f"{result['source']} → {result['target']} ({result['target_ip']}): "
                  f"Loss = {result['packet_loss']}%, Avg RTT = {result['rtt_avg']} ms")

            results.append(result)

    return results
