from rest_client import ping_host
from build_device_payloads import devices
from xml_parse import parse_ping_results

# Ping vmx5 lo0 from vmx6
# ping_host(devices["vmx6"], devices["vmx5"]["router-id"])

status, ping_xml = ping_host(devices["vmx6"], devices["vmx5"]["router-id"])
if status == 200:
    stats = parse_ping_results(ping_xml)