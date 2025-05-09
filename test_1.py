import yaml
from build_device_payloads import interface_payloads, ospf_payloads, devices
from rest_client import send_payload, commit_configuration, get_rpc_output

with open("payloads.yaml") as f:
    payloads = yaml.safe_load(f)

print(payloads["ospf_overview"])

print(devices["vmx1"]['ip'])

a = get_rpc_output(devices["vmx1"], payloads["ospf_overview"])
print(a)