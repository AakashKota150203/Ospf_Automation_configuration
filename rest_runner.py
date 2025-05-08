# run_rest_push.py
"""
This script pushes interface and OSPF configuration payloads to all devices
defined in the config.yaml using Juniper's REST API and commits the changes.

It imports:
- Payloads from `build_device_payloads.py`
- REST functions from `rest_client.py`
"""

from build_device_payloads import interface_payloads, ospf_payloads, devices
from rest_client import send_payload, commit_configuration, get_rpc_output

# ───────────────────────────────────────────────────────────────
# Push Payloads and Commit for All Devices
# ───────────────────────────────────────────────────────────────

# for i in range(1, len(devices) + 1):
#     name = f"vmx{i}"
#     device = devices[name]
#
#
#     print(f"\n{'='*60}")
#     print(f"Starting configuration push for {name}")
#     print(f"{'='*60}")
#
#     # Send interface configuration
#     print(f"\nSending Interface Config to {name}")
#     send_payload(device, interface_payloads[name])
#
#     # Send OSPF configuration
#     print(f"\nSending OSPF Config to {name}")
#     send_payload(device, ospf_payloads[name])
#
#     # Commit configuration
#     print(f"\nCommitting Config on {name}")
#     commit_configuration(device)
#
#     print(f"\nFinished with {name}\n{'-'*60}")

