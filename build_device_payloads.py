"""
This script loads device configuration and Jinja2 XML templates to generate
interface and OSPF configuration payloads for Juniper devices using REST API.

Structure:
- Loads 'config.yaml' (device and interface data)
- Loads 'payloads.yaml' (Jinja2 XML templates)
- Generates payloads for each device
"""

import yaml
from jinja2 import Template

# ───────────────────────────────────────────────────────────────
# Load Config and Template Files
# ───────────────────────────────────────────────────────────────

with open("config.yaml") as f:
    config = yaml.safe_load(f)

with open("payloads.yaml") as f:
    payloads = yaml.safe_load(f)

# ───────────────────────────────────────────────────────────────
# Create Device Lookup Dictionary (by name)
# ───────────────────────────────────────────────────────────────

devices = {d['name']: d for d in config['devices']}

# ───────────────────────────────────────────────────────────────
# Template Rendering Functions
# ───────────────────────────────────────────────────────────────

def generate_interface_config_payload(template_string, interfaces):
    """
    Renders XML payload to configure all interfaces on a device.
    """
    template = Template(template_string)
    return template.render(interfaces=interfaces)

def generate_ospf_config_payload(template_string, interfaces, router_id):
    """
    Renders XML payload to configure OSPF on a device.
    """
    template = Template(template_string)
    return template.render(interfaces=interfaces, router_id=router_id)

# ───────────────────────────────────────────────────────────────
# Device-Level Payload Builders
# ───────────────────────────────────────────────────────────────

def build_interface_payload(device, template_string):
    """
    Builds interface config payload for a given device.
    """
    return generate_interface_config_payload(template_string, device['interfaces'])

def build_ospf_payload(device, template_string):
    """
    Builds OSPF config payload for a given device.
    """
    return generate_ospf_config_payload(template_string, device['interfaces'], device["router-id"])

# ───────────────────────────────────────────────────────────────
# Generate Payloads for All Devices
# ───────────────────────────────────────────────────────────────

interface_template = payloads["interface_config"]["template"]
ospf_template = payloads["ospf_config"]["template"]

interface_payloads = {}
ospf_payloads = {}

for i in range(1, len(config['devices']) + 1):
    name = f"vmx{i}"
    device = devices[name]
    interface_payloads[name] = build_interface_payload(device, interface_template)
    ospf_payloads[name] = build_ospf_payload(device, ospf_template)
