# WARNING: This script takes a long time to execute if you have a high count
#          of active servers.
# Author: Leslie Devlin 
# Version 2.1.0
# Date 06.06.2017
##############################################################################

# Import Python Modules
import json, csv, base64, requests, os, argparse
import cloudpassage
import yaml
import time
from time import sleep
global api_session

# Set variable types
user_credential_b64 = ''
headers = {}
api_key_description = ''


# Define Methods
def create_api_session(session):
    config_file_loc = "cloudpassage.yml"
    config_info = cloudpassage.ApiKeyManager(config_file=config_file_loc)
    session = cloudpassage.HaloSession(config_info.key_id, config_info.secret_key)
    return session


# Create headers
def get_headers():
    with open('cloudpassage.yml') as config_settings:
        api_info = yaml.load(config_settings)
        api_key_token = api_info['defaults']['key_id'] + ":" + api_info['defaults']['secret_key']
        api_request_url = "https://" + api_info['defaults']['api_hostname'] + ":443"
    user_credential_b64 = "Basic " + base64.b64encode(api_key_token)
    reply = get_access_token(api_request_url, "/oauth/access_token?grant_type=client_credentials",
                             {"Authorization": user_credential_b64})
    reply_clean = reply.encode('utf-8')
    headers = {"Content-type": "application/json", "Authorization": "Bearer " + reply_clean}
    return headers



# Request Bearer token and return access_token
def get_access_token(url, query_string, headers):
    retry_loop_counter = 0
    while retry_loop_counter < 5:
        reply = requests.post(url + query_string, headers=headers)
        if reply.status_code == 200:
            return reply.json()["access_token"]
            retry_loop_counter = 10
        else:
            retry_loop_counter += 1
            time.sleep(30)


# get root group info
def get_root_group_id(session):
    get_root_id = cloudpassage.HttpHelper(session)
    root_id_reply=get_root_id.get_paginated("/v2/groups","groups",30)
    return_value = ''
    for group in root_id_reply:
        group_name = group['name']
        group_id = group['id']
        parent_id = group['parent_id']
        if parent_id == None:
            return_value = group_id
            break
    return return_value


# start file for writing
def start_csv_file(file_name, data):
    field_names = ['Hostname', 'Halo Agent Version', 'Agent Started At', 'OS Name', 
                   'OS Version', 'OS Distribution', 'OS Architecture', 'OS Service Pack',
                   'Group Name', 'Group ID']
    with open(file_name, 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=field_names)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
#            print row


# append 
def append_csv_file(file_name, data):
    field_names = ['Hostname', 'Halo Agent Version', 'Agent Started At', 'OS Name', 
                   'OS Version', 'OS Distribution', 'OS Architecture', 'OS Service Pack',
                   'Group Name', 'Group ID']
    with open(file_name, 'a') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=field_names)
        for row in data:
            writer.writerow(row)
#            print row


# 
def gen_servers_report(group_reply,out_file):
    # count servers - if 0, then remove file
    server_count=0
    for server in group_reply:
        if server:
            row = {'Hostname':server['hostname'],
                   'Halo Agent Version':server['agent_version'],
                   'Agent Started At':server['agent_started_at'],
                   'OS Name':server['os_name'],
                   'OS Version':server['os_version'],
                   'OS Distribution':server['os_distribution'],
                   'OS Architecture':server['os_architecture'],
                   'OS Service Pack':server['os_servicepack'],
                   'Group Name':server['group_name'],
                   'Group ID':server['group_id']}
            server_count += 1
            append_csv_file(out_file, [row])
    if server_count == 0:
        os.remove(out_file)
#        print "No outdated agents present. File %s removed.\n\n" % out_file


# Query Halo API /v1/groups to get list of groups to generate reports for
def get_halo_groups(session):
    old_agent_count = 0
    if not os.path.exists("reports"):
          os.makedirs("reports")
    get_halo_groups_list = cloudpassage.HttpHelper(session)

    root_group_id = get_root_group_id(session)
    print root_group_id
 
    # Set agent_version to the highest version you wish to report on.
    # Default is 3.9.7
    agent_version = '4.0.0'

    # write report for top level group
    get_halo_servers_list = cloudpassage.HttpHelper(session)
    root_group_reply=get_halo_servers_list.get_paginated("/v2/servers?group_id=" + root_group_id + "&state=active&agent_version_lt=" + agent_version + "&descendants=false","servers",30)
    out_file = "reports/Agents_Report_Ungrouped_" + time.strftime("%Y%m%d") + ".csv"
    start_csv_file(out_file, [])
    gen_servers_report(root_group_reply,out_file)

    # write reports for subgroups 
    subgroup_reply=get_halo_groups_list.get_paginated("/v2/groups?parent_id=" + root_group_id + "&descendants=true","groups",15)
    for group in subgroup_reply:
        group_id = group['id']
        group_name = group['name']
#        print "\nGroup %s:\n" % group['name']

        out_file = "reports/Agents_Report_" + group_name + "_" + time.strftime("%Y%m%d") + ".csv"
        start_csv_file(out_file, [])
        get_halo_servers_list = cloudpassage.HttpHelper(session)
        servers_reply=get_halo_servers_list.get_paginated("/v2/servers?group_id=" + group_id + "&state=active&agent_version_lt=" + agent_version + "&descendants=true","servers",30)
        gen_servers_report(servers_reply,out_file)




### MAIN

if __name__ == "__main__":
    api_session = None
    api_session = create_api_session(api_session)
    get_headers()
    get_halo_groups(api_session)
