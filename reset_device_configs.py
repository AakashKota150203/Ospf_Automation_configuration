# reset_device_configs.py
"""
This script connects to all Junos devices defined in config.yaml and issues
'delete' commands to reset specific interface and OSPF configurations via NETCONF using PyEZ.

It handles:
- Loading device info from YAML
- Deleting ge-0/0/0 through ge-0/0/4, lo0, and protocols ospf
- Committing the changes with proper error handling
"""

import yaml
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import ConnectError, ConfigLoadError, CommitError

# ───────────────────────────────────────────────────────────────
# Load device configurations from YAML
# ───────────────────────────────────────────────────────────────
with open("config.yaml") as f:
    config = yaml.safe_load(f)

devices = config['devices']

# ───────────────────────────────────────────────────────────────
# List of 'set' format delete commands to reset OSPF and interfaces
# ───────────────────────────────────────────────────────────────
reset_cmds = [
    "delete interfaces ge-0/0/0",
    "delete interfaces ge-0/0/1",
    "delete interfaces ge-0/0/2",
    "delete interfaces ge-0/0/3",
    "delete interfaces ge-0/0/4",
    "delete interfaces lo0",
    "delete protocols ospf"
]

# ───────────────────────────────────────────────────────────────
# Execute Reset on All Devices
# ───────────────────────────────────────────────────────────────
for device in devices:
    name = device['name']
    print(f"\n🔁 === Resetting config on {name} ===")

    try:
        dev = Device(
            host=device['ip'],
            user=device['username'],
            passwd=device['password'],
            port=device['netconf_port']
        )
        dev.open()
        dev.bind(cfg=Config)
        dev.cfg.lock()

        for cmd in reset_cmds:
            try:
                dev.cfg.load(cmd, format="set")
                print(f"[{name}] ✔ Loaded: {cmd}")
            except ConfigLoadError as e:
                if "statement not found" in str(e):
                    print(f"[{name}] Skipped (not found): {cmd}")
                else:
                    print(f"[{name}] ERROR loading cmd: {cmd} => {e}")

        dev.cfg.commit()
        print(f"[{name}] ✅ Configuration committed successfully.")

    except (ConnectError, CommitError) as e:
        print(f"[ERROR] on {name}: {e}")

    finally:
        try:
            dev.cfg.unlock()
        except:
            pass
        dev.close()
