#!/usr/bin/python

import os
import json
import sys
import zipfile
from pathlib import Path
from urllib.parse import parse_qs, unquote

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root) + "/libs")
import libs.yaml as yaml


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
        response["status"] = "authenticated"
        response["user"] = user
        # Extract query string from environment variable
        query_string = os.environ.get("QUERY_STRING", "")
        query_params = parse_qs(query_string)
        file_name_encoded = query_params.get("file", [None])[0]
        file_name = unquote(file_name_encoded)
        # response["file_from_params"] = file_name
        try:
            with zipfile.ZipFile(file_name, mode="r") as zif:
                if "RR_VERSION" in zif.namelist():
                    for lines in zif.read("RR_VERSION").split(b"\r\n"):
                        response["updateVersion"] = lines.strip().decode("utf-8")
                        response["success"] = True
                else:
                    raise Exception("'RR_VERSION' file not found in the zip file.")
        except Exception as e:
            response["error"] = str(e)
    else:
        response["status"] = "not authenticated"

    print("Content-type: application/json\n")
    print(json.dumps(response, indent=4))
