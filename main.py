# main.py

"""
Main entry point for full automation:
- Configures all devices (interface + OSPF)
- Waits for OSPF convergence
- Verifies full-mesh reachability via ping
- Displays OSPF state from each router

Intended for use in Juniper vMX lab setups using REST API.
"""

from orchestrator import (
    configure_all_devices,
    verify_all_device_pings,
    verify_ospf_all_devices
)
from wait_with_progress import wait_with_progress
import time


def main():
    print("\n🚀 Starting full provisioning and validation...\n")

    # Step 1: Push interface and OSPF configs to all routers
    configure_all_devices()

    # Step 2: Pause to allow OSPF convergence
    wait_with_progress(120)

    # Step 3: Verify ping connectivity across all loopbacks
    print("\n🔁 Verifying full-mesh loopback reachability via ping...\n")
    verify_all_device_pings()

    # Step 4: Retrieve and print OSPF details
    print("\n📡 Verifying OSPF neighbor/interface/route/database status...\n")
    verify_ospf_all_devices()


if __name__ == "__main__":
    main()
