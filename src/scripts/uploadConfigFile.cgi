#!/usr/bin/env python

import os
import json
import sys
import cgi
import cgitb
from pathlib import Path

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root) + "/libs")
import libs.yaml as yaml

cgitb.enable()  # Enable CGI error reporting

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
        try:
            if os.environ.get("REQUEST_METHOD") == "POST":
                ctype, pdict = cgi.parse_header(os.environ["CONTENT_TYPE"])
                if ctype == "application/json":
                    message = ""
                    length = int(os.environ["CONTENT_LENGTH"])
                    request_body = sys.stdin.read(length)
                    data = json.loads(request_body)
                    # Convert JSON data to YAML using the custom dumper
                    yaml_data = yaml.dump(data, sort_keys=False)
                    # existing_config = read_user_config()
                    # message ='after read existing_config'
                    # Define the file path
                    file_path = "/tmp/user-config.yml"
                    # existing_config['addons'] = data.addons
                    # message ='after remap existing_config'
                    response["addons"] = data
                    # Write the YAML data to a file
                    with open(file_path, "w") as yaml_file:
                        yaml_file.write(yaml_data)
                        message = "after write existing_config"

                    with open("/tmp/.build", "w") as build_file:
                        build_file.write("")
                        message = "after write build"

                    response["success"] = True
                    response["message"] = message
                else:
                    response["success"] = False
                    response["message"] = "Invalid content type"
            else:
                response["success"] = False
                response["message"] = "Invalid request method"
        except Exception as e:
            response["success"] = False
            response["message"] = str(e)
    else:
        response["success"] = False
        response = {"status": "not authenticated"}

    print("Content-type: application/json\n")
    print(json.dumps(response, indent=4))

