import yaml
import xml.etree.ElementTree as ET
from rest_client import get_rpc_output
from xml_parse import fetch_ospf_interface,parse_ospf_interfaces,parse_ospf_routes,parse_ospf_neighbors,parse_ospf_database,fetch_ospf_database,fetch_ospf_neighbor,fetch_ospf_route
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)
    devices = config["devices"]
    
with open("payloads.yaml") as f:
    payloads = yaml.safe_load(f)
ns = {'junos': 'http://xml.juniper.net/junos/21.1R0/junos-routing'}

def check_ospf_status():
    """Comprehensive OSPF status checker"""
    with open("config.yaml", "r") as file:
        devices = yaml.safe_load(file)["devices"]

    for device in devices:
        device_name = device["name"]
        print(f"\n🔍 Checking OSPF on {device_name}")
        
        try:
            # Check Neighbors
            status, xml_nbr = fetch_ospf_neighbor(device)
            if status == 200:
                neighbors = parse_ospf_neighbors(xml_nbr)
                print("\n📌 OSPF Neighbors:")
                for nbr in neighbors:
                    print(f"  {nbr['id']} ({nbr['address']}) via {nbr['interface']} - State: {nbr['state']}")
            else:
                print(f"⚠️  Neighbor check failed (HTTP {status})")

            # Check Interfaces
            status, xml_intf = fetch_ospf_interface(device)
            

            if status == 200:
                interfaces = parse_ospf_interfaces(xml_intf)
                print("\n📡 OSPF Interfaces:")
                for intf in interfaces:
                    print(f"  {intf['name']} | Area {intf['area']} | DR: {intf['dr']} | Neighbors: {intf['neighbors']}")
            
            # Check Routes
            status, xml_route = fetch_ospf_route(device)
            if status == 200:
                routes = parse_ospf_routes(xml_route)
                print("\n🗺️  OSPF Routes:")
                for route in routes:
                    print(f"  {route['destination']} via {route['next_hop']} ({route['type']})")
                    
            status, xml_database = fetch_ospf_database(device)
            if status == 200:
                databases = parse_ospf_database(xml_database)
                print("\n  OSPF Database:")
                for database in databases:
                    print(f"Lsa Id {database['lsa_id']} | Advertising router {database['advertising_router']}  | Age {database['age']} ")

        except Exception as e:
            print(f"❌ Error processing {device_name}: {str(e)}")

if __name__ == "__main__":
    check_ospf_status()
