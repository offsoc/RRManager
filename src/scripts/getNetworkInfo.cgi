#!/usr/bin/env python

import os
import json


def read_file(path, default=None):
    try:
        if os.path.exists("/usr/sbin/rrmdo"):
            return os.popen(f"/usr/sbin/rrmdo cat {path}").read().strip()
        else:
            return os.popen(f"cat {path}").read().strip()
    except Exception:
        return default


def get_ethernet_interfaces():
    interfaces = []
    for eth in os.listdir("/sys/class/net/"):
        if eth.startswith("eth"):
            interface_info = {
                "interface": eth,
                "address": read_file(f"/sys/class/net/{eth}/address"),
                "operstate": read_file(f"/sys/class/net/{eth}/operstate"),
                "speed": read_file(f"/sys/class/net/{eth}/speed", "N/A"),
                "duplex": read_file(f"/sys/class/net/{eth}/duplex", "N/A"),
            }
            interfaces.append(interface_info)
    return interfaces


def get_boot_parameters():
    cmdline = read_file(f"/proc/cmdline")
    parameters = {}
    for param in cmdline.split():
        if "=" in param:
            key, value = param.split("=", 1)
            parameters[key] = value
        else:
            parameters[param] = ""
    return parameters


def get_syno_mac_addresses():
    mac_addresses = []
    syno_mac_addresses = read_file(f"/proc/sys/kernel/syno_mac_addresses")
    for line in syno_mac_addresses.split("\n"):
        mac_addresses.append(line.strip())
    return mac_addresses


if __name__ == "__main__":
    user = os.popen("/usr/syno/synoman/webman/modules/authenticate.cgi", "r").read().strip()

    # Debug
    if not user:
        import getpass

        user = getpass.getuser()
        if user != "root":
            user = ""

    response = {}

    if user:
        response["result"] = {
            "ethernetInterfaces": get_ethernet_interfaces(),
            "bootParameters": get_boot_parameters(),
            "syno_mac_addresses": get_syno_mac_addresses(),
        }

    print("Content-type: application/json\n")
    print(json.dumps(response, indent=4))
