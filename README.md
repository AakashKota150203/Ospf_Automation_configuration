# ospf_cfg_rest
Configure OSPF in Juniper routers using REST Api

# 🚀 Juniper OSPF Configuration & Verification Toolkit

This project provides a modular framework to **configure**, **verify**, and **validate** OSPF routing across a network of Juniper vMX devices using both **REST API** and **PyEZ**.

It is designed for automation enthusiasts, network engineers, and students working on scalable network deployments and automation using Junos.

---

## 🧠 Features

- 🔧 Configure interfaces and OSPF using REST RPC XML payloads.
- 📡 Validate connectivity by pinging loopback addresses of all routers.
- 🧭 Parse and display OSPF neighbors, interfaces, routes, and LSDB entries.
- 🧼 Rollback/reset device config using PyEZ.
- ⚙️ Orchestrator script to tie it all together.
- 🧾 YAML-based configs and Jinja2 templates for full modularity.

---

## 🗂️ Project Structure

```
.
├── config.yaml                  # Device metadata (IP, ports, interfaces, OSPF areas)
├── payloads.yaml                # XML templates for REST calls (interface, OSPF, RPCs)
├── build_device_payloads.py     # Builds payloads using config + templates
├── rest_client.py               # REST operations (POST, commit, RPCs, ping)
├── verify_ping.py               # Parses and verifies ping results between routers
├── xml_parser.py                # Parses RPC XML for neighbors, interfaces, routes, LSDB
├── verify_ospf_config.py        # Runs and prints OSPF diagnostics for all devices
├── rollback_initial.py          # Deletes old config using PyEZ
├── orchestrator.py              # Bundles config/ping/ospf checks in one callable
├── main.py                      # Entry point for automation
```

---

## 🧰 Requirements

- Python 3.8+
- Juniper vMX devices with REST & NETCONF enabled
- Libraries:
  - `requests`
  - `jinja2`
  - `PyYAML`
  - `jnpr.junos`
  - `lxml` (for `etree` parsing)

Install requirements via:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Setup

1. **Configure Devices**  
   Edit `config.yaml` with your vMX IPs, ports, usernames, interfaces, and router IDs.

2. **Define Payloads**  
   Modify `payloads.yaml` to update or add your REST RPC templates.

3. **Reset Devices** *(optional)*  
   To clear old configuration:
   ```bash
   python rollback_initial.py
   ```

4. **Run Main Automation**
   ```bash
   python main.py
   ```

---

## 🧪 What Happens on `main.py`?

- Pushes interface and OSPF config via REST to all devices
- Waits for OSPF to converge (with a loading bar ⏳)
- Verifies loopback reachability with ping (REST)
- Parses and prints:
  - OSPF Neighbors
  - OSPF Interfaces
  - OSPF Routes
  - OSPF LSDB

---

## 📋 Example Output

```
🔄 Verifying reachability FROM vmx1 (10.100.100.1)
vmx1 → vmx2 (10.100.100.2): Loss = 0%, Avg RTT = 1102 ms
...

📌 OSPF Neighbors:
  10.100.100.2 (10.100.12.2) via ge-0/0/0.0 - State: Full
📡 OSPF Interfaces:
  ge-0/0/0.0 | Area 0.0.0.0 | DR: 10.100.100.2 | Neighbors: 1
🗺️  OSPF Routes:
  10.100.100.2 via 10.100.12.2 (Intra)
📘 OSPF Database:
  LSA ID: 10.100.12.0/24 | Adv: 10.100.100.2 | Age: 119
```

---


## 🧑‍💻 Author

Aniruddha Kulkarni  
📧 aak@umd.edu  
🔗 [LinkedIn](https://www.linkedin.com/in/anirudddhakulk/)

Aakash Kota  
📧 kota15@umd.edu  
🔗 [LinkedIn](https://www.linkedin.com/in/aakash-kota-177004185/)

---

