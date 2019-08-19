def fmc_csv2acp():
    import sys
    import json
    import requests
    from jinja2 import Template, Environment, FileSystemLoader
    import fmcenv
    import csv

    args = sys.argv

    server = "https://" + fmcenv.SERVER_IP

    username = fmcenv.USERNAME
    password = fmcenv.PASSWORD

    r = None
    headers = {'Content-Type': 'application/json'}
    api_auth_path = "/api/fmc_platform/v1/auth/generatetoken"
    auth_url = server + api_auth_path


    try:
        r = requests.post(auth_url, headers=headers, auth=requests.auth.HTTPBasicAuth(username,password), verify=False)
        auth_headers = r.headers
        auth_token = auth_headers.get('X-auth-access-token', default=None)
        if auth_token == None:
            print("auth_token not found. Exiting...")
            sys.exit()
    except Exception as err:
        print("Error in generating auth token --> " + str(err))
        sys.exit()

    headers['X-auth-access-token'] = auth_token

    # Create ACP Operation
    post_data = {
        "type": "AccessPolicy",
        "name": args[2],
        "defaultAction": {
            "action": "BLOCK"
        }
    }

    api_path = "/api/fmc_config/v1/domain/" + fmcenv.GDOMAIN + "/policy/accesspolicies/"
    url = server + api_path
    if (url[-1] == '/'):
        url = url[:-1]

    try:
        r = requests.post(url, data=json.dumps(post_data), headers=headers, verify=False)
        status_code = r.status_code
        resp = r.text
        print("Status code is: " + str(status_code))
        if status_code == 201 or status_code == 202:
            print("ACP Creation was successful...")
            json_resp = json.loads(resp)
            # print(json_resp["id"])
            # print(json.dumps(json_resp, sort_keys=True, indent=4, separators=(',', ': ')))
        else:
            r.raise_for_status()
            print("ACP Creation Error occurred in POST --> " + resp)
    except requests.exceptions.HTTPError as err:
        print("Error in connection --> " + str(err))

    # Create Rules Operation

    api_path = "/api/fmc_config/v1/domain/" + fmcenv.GDOMAIN + "/policy/accesspolicies/" + json_resp["id"] + "/accessrules?bulk=true"  # param
    url = server + api_path
    if (url[-1] == '/'):
        url = url[:-1]

    env = Environment(loader=FileSystemLoader('./templates'))
    template = env.get_template('policy.j2')

    data = [i for i in csv.DictReader(open(args[1]))]
    post_data = template.render({"data": data})

    try:
        r = requests.post(url, data=post_data, headers=headers, verify=False)
        status_code = r.status_code
        resp = r.text
        print("Status code is: " + str(status_code))
        if status_code == 201 or status_code == 202:
            print("Rule Post was successful...")
            # json_resp = json.loads(resp)
            # print(json.dumps(json_resp, sort_keys=True, indent=4, separators=(',', ': ')))
        else:
            # r.raise_for_status()
            print("Error occurred in Rule POST --> " + resp)
    except requests.exceptions.HTTPError as err:
        print("Error in connection --> " + str(err))
    finally:
        if r: r.close()

if __name__ == '__main__':
    fmc_csv2acp()