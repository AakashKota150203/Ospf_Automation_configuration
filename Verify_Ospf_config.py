# verify_ospf_config.py

"""
This module verifies OSPF configuration across multiple Juniper devices.
It gathers information such as:
- OSPF neighbors
- OSPF interface status
- OSPF routes
- OSPF database

Each result is printed and stored for further use or analysis.
"""

from xml_parser import (
    fetch_ospf_interface, parse_ospf_interfaces,
    fetch_ospf_routes, parse_ospf_routes,
    fetch_ospf_neighbor, parse_ospf_neighbors,
    fetch_ospf_database, parse_ospf_database
)


def check_ospf_status(devices):
    """
    Checks and prints OSPF status for each device in the given list.

    Args:
        devices (list): A list of device dictionaries containing connection details.

    Returns:
        list: A list of dictionaries containing parsed OSPF data for each device.
    """
    all_results = []

    for device in devices:
        device_name = device["name"]
        print(f"\n🔍 Checking OSPF on {device_name}")
        device_result = {"device": device_name}

        try:
            # ───────────── OSPF Neighbors ─────────────
            status, xml_nbr = fetch_ospf_neighbor(device)
            if status == 200:
                neighbors = parse_ospf_neighbors(xml_nbr)
                print("\n📌 OSPF Neighbors:")
                for nbr in neighbors:
                    print(f"  {nbr['id']} ({nbr['address']}) via {nbr['interface']} - State: {nbr['state']}")
                device_result["neighbors"] = neighbors
            else:
                print(f"⚠️  Neighbor check failed (HTTP {status})")

            # ───────────── OSPF Interfaces ─────────────
            status, xml_intf = fetch_ospf_interface(device)
            if status == 200:
                interfaces = parse_ospf_interfaces(xml_intf)
                print("\n📡 OSPF Interfaces:")
                for intf in interfaces:
                    print(f"  {intf['name']} | Area {intf['area']} | DR: {intf['dr']} | Neighbors: {intf['neighbors']}")
                device_result["interfaces"] = interfaces

            # ───────────── OSPF Routes ─────────────
            status, xml_route = fetch_ospf_routes(device)
            if status == 200:
                routes = parse_ospf_routes(xml_route)
                print("\n🗺️  OSPF Routes:")
                for route in routes:
                    print(f"  {route['destination']} via {route['next_hop']} ({route['type']})")
                device_result["routes"] = routes

            # ───────────── OSPF Database ─────────────
            status, xml_db = fetch_ospf_database(device)
            if status == 200:
                databases = parse_ospf_database(xml_db)
                print("\n📘 OSPF Database:")
                for db in databases:
                    print(f"  LSA ID: {db['lsa_id']} | Adv: {db['advertising_router']} | Age: {db['age']}")
                device_result["database"] = databases

        except Exception as e:
            print(f"❌ Error processing {device_name}: {e}")
            device_result["error"] = str(e)

        all_results.append(device_result)

    return all_results
