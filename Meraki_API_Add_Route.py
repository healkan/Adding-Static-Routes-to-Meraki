"""
Copyright (c) 2018 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.0 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Healkan Cheung"
__copyright__ = "Copyright (c) 2018 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.0"

import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()
import csv
import json

meraki_api_key = "ENTER API KEY HERE"

#Getting Org Id
num = 0
url = "https://api.meraki.com/api/v0/organizations"
headers = {
    'X-Cisco-Meraki-API-Key': meraki_api_key,
    'Content-Type': "application/json",
    'Cache-Control': "no-cache",
    }
response = requests.request("GET", url, headers=headers, verify=False)
org_list = json.loads(response.text)
print " "
print "Please Select Organization"
for org in org_list:
  print "Enter  ",num," for  Org Name: ", org["name"]
  num = num + 1
pick = input("Please enter selection:  ")
org_id = org_list[pick]["id"]


#Getting Network Id
num = 0
url = "https://api.meraki.com/api/v0/organizations/" + str(org_id) + "/networks"
headers = {
    'X-Cisco-Meraki-API-Key': meraki_api_key,
    'Content-Type': "application/json",
    'Cache-Control': "no-cache",
    }
response = requests.request("GET", url, headers=headers)
net_list = json.loads(response.text)
print " "
print "Please Select Network"
for net in net_list:
  print "Enter  ",num," for Network Name: ", net["name"]
  num = num + 1
pick = input("Please enter selection:  ")
net_id = net_list[pick]["id"]

  
# Adding routes
network_id = net_id
file_name = "merakiroutes_test3.csv"
file = open(file_name,'r')
csv_data = csv.reader(file)

url = "https://dashboard.meraki.com/api/v0/networks/" + network_id + "/staticRoutes"

print ""
print "Attempting to add routes"
for static_route in csv_data:
  route_name = static_route[0]
  network = static_route[1]
  gateway = static_route[2]
  payload = "{\n  \"name\":\"" + route_name + "\",\n  \"subnet\":\"" + network + "\",\n  \"gatewayIp\":\"" + gateway + "\",\n  \"enabled\":\"true\"\n}"
  headers = {
    'X-Cisco-Meraki-API-Key': meraki_api_key,
    'Content-Type': "application/json",
    'Cache-Control': "no-cache"
    }
  response = requests.request("POST", url, data=payload, headers=headers, verify=False)
  print(response.text)
  
file.close()
