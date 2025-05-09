# xml_parser.py

"""
This module handles:
1. Parsing Junos XML output for ping and OSPF.
2. Fetching raw XML data for OSPF-related RPCs via REST API.
"""

import xml.etree.ElementTree as ET
import yaml
from rest_client import get_rpc_output

# ────────────────────────────────
# Load RPC payload names from YAML
# ────────────────────────────────
with open("payloads.yaml") as f:
    payloads = yaml.safe_load(f)

# ────────────────────────────────
# XML Namespaces for Junos
# ────────────────────────────────
NS_ROUTING = {'junos': 'http://xml.juniper.net/junos/21.1R0/junos-routing'}
NS_PROBE = {'junos': 'http://xml.juniper.net/junos/21.1R0/junos-probe-tests'}


# ===================================================
# PING PARSING
# ===================================================

def parse_ping_results(xml_data):
    """
    Parse ping result XML and extract summary stats.
    """
    root = ET.fromstring(xml_data)
    try:
        summary = root.find('junos:probe-results-summary', NS_PROBE)
        return {
            "probes_sent": int(summary.findtext('junos:probes-sent', default="0", namespaces=NS_PROBE)),
            "responses": int(summary.findtext('junos:responses-received', default="0", namespaces=NS_PROBE)),
            "packet_loss": int(summary.findtext('junos:packet-loss', default="0", namespaces=NS_PROBE)),
            "rtt_avg": int(summary.findtext('junos:rtt-average', default="0", namespaces=NS_PROBE))
        }
    except Exception as e:
        print(f"❌ Failed to parse ping output: {e}")
        return None


# ===================================================
# OSPF FETCH WRAPPERS (via get_rpc_output)
# ===================================================

def fetch_ospf_interface(device):
    """
    Retrieve OSPF interface XML from a device.
    """
    return get_rpc_output(device, payloads["ospf_interface"])

def fetch_ospf_database(device):
    """
    Retrieve OSPF database XML from a device.
    """
    return get_rpc_output(device, payloads["ospf_database"])

def fetch_ospf_neighbor(device):
    """
    Retrieve OSPF neighbor XML from a device.
    """
    return get_rpc_output(device, payloads["ospf_neighbor"])

def fetch_ospf_routes(device):
    """
    Retrieve OSPF route XML from a device.
    """
    return get_rpc_output(device, payloads["ospf_route"])


# ===================================================
# OSPF XML PARSERS
# ===================================================

def parse_ospf_neighbors(xml_data):
    """
    Parse OSPF neighbor XML and return neighbor summary.
    """
    root = ET.fromstring(xml_data)
    neighbors = []

    for nbr in root.findall(".//junos:ospf-neighbor", NS_ROUTING):
        neighbors.append({
            'id': nbr.findtext("junos:neighbor-id", default="N/A", namespaces=NS_ROUTING),
            'address': nbr.findtext("junos:neighbor-address", default="N/A", namespaces=NS_ROUTING),
            'interface': nbr.findtext("junos:interface-name", default="N/A", namespaces=NS_ROUTING),
            'state': nbr.findtext("junos:ospf-neighbor-state", default="N/A", namespaces=NS_ROUTING),
            'priority': nbr.findtext("junos:neighbor-priority", default="0", namespaces=NS_ROUTING)
        })

    return neighbors


def parse_ospf_interfaces(xml_data):
    """
    Parse OSPF interface XML and extract interface-level info.
    """
    root = ET.fromstring(xml_data)
    interfaces = []

    for intf in root.findall(".//junos:ospf-interface/junos:interface-name/..", NS_ROUTING):
        interfaces.append({
            'name': intf.findtext("junos:interface-name", default="N/A", namespaces=NS_ROUTING),
            'state': intf.findtext("junos:interface-state", default="N/A", namespaces=NS_ROUTING),
            'area': intf.findtext("junos:ospf-area", default="N/A", namespaces=NS_ROUTING),
            'dr': intf.findtext("junos:dr-id", default="N/A", namespaces=NS_ROUTING),
            'bdr': intf.findtext("junos:bdr-id", default="N/A", namespaces=NS_ROUTING),
            'neighbors': intf.findtext("junos:neighbor-count", default="0", namespaces=NS_ROUTING)
        })

    return interfaces


def parse_ospf_routes(xml_data):
    """
    Parse OSPF route XML and return routing entries.
    """
    root = ET.fromstring(xml_data)
    routes = []

    for route in root.findall(".//junos:ospf-route/junos:ospf-route-entry", NS_ROUTING):
        routes.append({
            'destination': route.findtext("junos:address-prefix", default="N/A", namespaces=NS_ROUTING),
            'next_hop': route.findtext("junos:ospf-next-hop/junos:next-hop-address/junos:interface-address", default="N/A", namespaces=NS_ROUTING),
            'type': route.findtext("junos:route-type", default="N/A", namespaces=NS_ROUTING),
            'metric': route.findtext("junos:interface-cost", default="0", namespaces=NS_ROUTING)
        })

    return routes


def parse_ospf_database(xml_data):
    """
    Parse OSPF database entries including LSA details.
    """
    root = ET.fromstring(xml_data)
    databases = []

    for entry in root.findall(".//junos:ospf-database", NS_ROUTING):
        databases.append({
            'lsa_type': entry.findtext("junos:lsa-type", default="N/A", namespaces=NS_ROUTING),
            'lsa_id': entry.findtext("junos:lsa-id", default="N/A", namespaces=NS_ROUTING),
            'advertising_router': entry.findtext("junos:advertising-router", default="N/A", namespaces=NS_ROUTING),
            'sequence_number': entry.findtext("junos:sequence-number", default="N/A", namespaces=NS_ROUTING),
            'age': entry.findtext("junos:age", default="N/A", namespaces=NS_ROUTING),
            'options': entry.findtext("junos:options", default="N/A", namespaces=NS_ROUTING),
            'checksum': entry.findtext("junos:checksum", default="N/A", namespaces=NS_ROUTING),
            'lsa_length': entry.findtext("junos:lsa-length", default="N/A", namespaces=NS_ROUTING)
        })

    return databases
