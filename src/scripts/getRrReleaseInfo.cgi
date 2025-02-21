#!/usr/bin/env python

import os
import json
import requests

# Function to read the local version from /usr/rr/VERSION
def get_local_version():
    try:
        with open("/usr/rr/VERSION", "r") as f:
            for line in f:
                if "LOADERVERSION" in line:
                    return line.split("=")[1].strip()
    except FileNotFoundError:
        return None

# Authenticate user
user = os.popen("/usr/syno/synoman/webman/modules/authenticate.cgi").read().strip()
if not user:
    print("Content-type: application/json\n")
    print(json.dumps({"error": "Security: user not authenticated"}))
    exit()

# Read proxy configuration
proxy_config = {}
try:
    with open("/etc/proxy.conf", "r") as f:
        for line in f:
            key, value = line.strip().split("=", 1)
            proxy_config[key] = value
except FileNotFoundError:
    pass

proxy_enabled = proxy_config.get("proxy_enabled", "no") == "yes"
proxy_host = proxy_config.get("http_host", "")
proxy_port = proxy_config.get("http_port", "")
proxy_user = proxy_config.get("proxy_user", "")
proxy_password = proxy_config.get("proxy_pwd", "")

proxy = None
if proxy_enabled and proxy_host and proxy_port:
    if proxy_user and proxy_password:
        proxy = {"http": f"http://{proxy_user}:{proxy_password}@{proxy_host}:{proxy_port}"}
    else:
        proxy = {"http": f"http://{proxy_host}:{proxy_port}"}

# GitHub API URL
url = "https://api.github.com/repos/RROrg/rr/releases/latest"

# Fetch release info from GitHub
try:
    response = requests.get(url, proxies=proxy if proxy else None, timeout=10)
    response.raise_for_status()
    data = response.json()
    tag = data.get("tag_name", "Unknown")
    release_link = data.get("html_url", "")
    release_notes = data.get("body", "")
    download_link = f"https://github.com/RROrg/rr/releases/download/{tag}/updateall-{tag}.zip"
except requests.RequestException as e:
    print("Content-type: application/json\n")
    print(json.dumps({"error": f"Failed to fetch release info: {e}"}))
    exit()

# Get local version
local_tag = get_local_version()
if not local_tag:
    print("Content-type: application/json\n")
    print(json.dumps({"error": "Unknown bootloader version!"}))
    exit()

# Construct response JSON
result = {
    "tag": tag,
    "url": release_link,
    "updateAllUrl": download_link,
    "proxyUsed": proxy_enabled,
}

if tag == local_tag:
    result["status"] = "up-to-date"
    result["message"] = f"Actual version is {tag}"
else:
    result["status"] = "update available"
    result["notes"] = release_notes

# Output JSON response
print("Content-type: application/json\n")
print(json.dumps(result, indent=4))
