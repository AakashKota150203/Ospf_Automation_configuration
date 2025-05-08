import xml.etree.ElementTree as ET
import yaml
from rest_client import get_rpc_output
with open("payloads.yaml") as f:
    payloads = yaml.safe_load(f)
ns = {'junos': 'http://xml.juniper.net/junos/21.1R0/junos-routing'}
def parse_ping_results(xml_data):
    ns = {'junos': 'http://xml.juniper.net/junos/21.1R0/junos-probe-tests'}
    root = ET.fromstring(xml_data)

    try:
        summary = root.find('junos:probe-results-summary', ns)
        loss = summary.find('junos:packet-loss', ns).text
        rtt_avg = summary.find('junos:rtt-average', ns).text
        probes = summary.find('junos:probes-sent', ns).text
        responses = summary.find('junos:responses-received', ns).text

        print(f"📡 Ping Success: {responses}/{probes} received")
        print(f"📉 Packet Loss: {loss}")
        print(f"⏱️ Avg RTT: {rtt_avg} ms")
        return {
            "probes_sent": int(probes),
            "responses": int(responses),
            "loss": int(loss),
            "rtt_avg": int(rtt_avg)
        }

    except Exception as e:
        print(f"❌ Failed to parse ping output: {e}")
        return None
    
    
    
def fetch_ospf_interface(device):
    return get_rpc_output(device, payloads["ospf_interface"])

def fetch_ospf_database(device):
    return get_rpc_output(device, payloads["ospf_database"])

def fetch_ospf_neighbor(device):
    """Fetch OSPF neighbor information"""
    return get_rpc_output(device, payloads["ospf_neighbor"])

def fetch_ospf_route(device):
    """Fetch OSPF route information"""
    return get_rpc_output(device, payloads["ospf_route"])




def parse_ospf_neighbors(xml_data):
    """Parse OSPF neighbor information with proper element names"""
    root = ET.fromstring(xml_data)
    neighbors = []
    
    ospf_ns = {'junos': 'http://xml.juniper.net/junos/21.1R0/junos-routing'}
    
    for nbr in root.findall(".//junos:ospf-neighbor", ospf_ns):
        neighbor_data = {
            'id': nbr.findtext("junos:neighbor-id", default="N/A", namespaces=ospf_ns),
            'address': nbr.findtext("junos:neighbor-address", default="N/A", namespaces=ospf_ns),
            'interface': nbr.findtext("junos:interface-name", default="N/A", namespaces=ospf_ns),
            'state': nbr.findtext("junos:ospf-neighbor-state", default="N/A", namespaces=ospf_ns),  # Corrected element
            'priority': nbr.findtext("junos:neighbor-priority", default="0", namespaces=ospf_ns)
        }
        neighbors.append(neighbor_data)
    
    return neighbors


def parse_ospf_interfaces(xml_data):
    """Parse OSPF interface information with proper XML paths"""
    root = ET.fromstring(xml_data)
    interfaces = []
    
    # Correct XML path and elements
    for intf in root.findall(".//junos:ospf-interface/junos:interface-name/..", ns):
        interface_data = {
            'name': intf.findtext("junos:interface-name", default="N/A", namespaces=ns),
            'state': intf.findtext("junos:interface-state", default="N/A", namespaces=ns),
            'area': intf.findtext("junos:area", default="N/A", namespaces=ns),
            'dr': intf.findtext("junos:dr-id", default="N/A", namespaces=ns),
            'bdr': intf.findtext("junos:bdr-id", default="N/A", namespaces=ns),
            'neighbors': intf.findtext("junos:neighbor-count", default="0", namespaces=ns)
        }
        interfaces.append(interface_data)
    
    return interfaces


def parse_ospf_routes(xml_data):
    """Parse OSPF route information with proper XML structure"""
    root = ET.fromstring(xml_data)
    routes = []

    # Correct XML path for OSPF routes
    for route in root.findall(".//junos:ospf-route/junos:ospf-route-entry", ns):
        route_data = {
            'destination': route.findtext("junos:address-prefix", default="N/A", namespaces=ns),
            'next_hop': route.findtext("junos:ospf-next-hop/junos:next-hop-address/junos:interface-address", default="N/A", namespaces=ns),
            'type': route.findtext("junos:route-type", default="N/A", namespaces=ns),
            'metric': route.findtext("junos:interface-cost", default="0", namespaces=ns)
        }
        routes.append(route_data)
    
    return routes



def parse_ospf_database(xml_data):
    root = ET.fromstring(xml_data)
    ospf_database_info = []    
    for ospf_entry in root.findall(".//junos:ospf-database",ns):
        entry_data = {
            'lsa_type': ospf_entry.findtext("junos:lsa-type", default="N/A", namespaces=ns),
            'lsa_id': ospf_entry.findtext("junos:lsa-id", default="N/A", namespaces=ns),
            'advertising_router': ospf_entry.findtext("junos:advertising-router", default="N/A", namespaces=ns),
            'sequence_number': ospf_entry.findtext("junos:sequence-number", default="N/A", namespaces=ns),
            'age': ospf_entry.findtext("junos:age", default="N/A", namespaces=ns),
            'options': ospf_entry.findtext("junos:options", default="N/A",namespaces=ns),
            'checksum': ospf_entry.findtext("junos:checksum", default="N/A", namespaces=ns),
            'lsa_length': ospf_entry.findtext("junos:lsa-length", default="N/A",namespaces=ns)
        }
        ospf_database_info.append(entry_data)

    return ospf_database_info