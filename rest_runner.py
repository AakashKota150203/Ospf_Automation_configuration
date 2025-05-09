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

def configure_all_devices():
    """
    Configures interfaces and OSPF on all devices, commits them,
    and prints a summary per device. Returns a list of summary results.
    """
    summary = []

    for i in range(1, len(devices) + 1):
        name = f"vmx{i}"
        device = devices[name]

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

a = get_rpc_output(devices[0], )