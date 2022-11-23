# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2022 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
               https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.
"""

__author__ = "Trevor Maco <tmaco@cisco.com>, Jorge Banegas <jbanegas@cisco.com>"
__copyright__ = "Copyright (c) 2022 Cisco and/or its affiliates."
__license__ = "Cisco Sample Code License, Version 1.1"

# Imports
import meraki

from config import *
from rich import print

# Dictionary to translate model to a format recognized by claim api call
claim_key = {"VMX-S": "small", "VMX-M": "medium", "VMX-L": "large", "VMX-100": "100"}

dashboard = meraki.DashboardAPI(MERAKI_API_KEY, suppress_logging=True)


# Get Org Id
def get_org_id(org_name):
    orgs = dashboard.organizations.getOrganizations()

    for org in orgs:
        if org['name'] == org_name:
            return org['id']

    return None


# Get org inventory per model
def get_org_vmx_inventory(org_id):
    inventory = dashboard.organizations.getOrganizationInventoryDevices(org_id, models=[OLD_MODEL])
    print("Found {} devices in inventory.".format(len(inventory)))
    return inventory


# Get device details
def get_device_details(serial):
    details = dashboard.devices.getDevice(serial)
    return details


# Get network details
def get_network_details(net_id, progress):
    response = dashboard.networks.getNetwork(net_id)
    progress.console.print("Retrieved network details for: [magenta]{}[/].".format(net_id))

    return response


# Remove old vmx device from network
def remove_old_vmx(net_id, serial, progress):
    response = dashboard.networks.removeNetworkDevices(net_id, serial)

    progress.console.print("Device [green]{}[/] removed.".format(serial))


# Claim a new vmx into a network
def claim_vmx(net_id, progress):
    size = claim_key[NEW_MODEL]

    try:
        claim = dashboard.networks.vmxNetworkDevicesClaim(net_id, size)

        progress.console.print("Claimed new vmx [yellow]{}[/].".format(claim['serial']))
        return claim

    except meraki.APIError as e:
        error = e.message['errors'][0]
        if "no available licenses" in error:
            print(f'[red]{error}[/]' + ', skipping.')
            return 'No licenses'


# Set new device name, following convention
def update_device_details(serial, details, progress, tag):
    # Tag list (remove target tag, keep other tags)
    if tag and tag in details['tags']:
        details['tags'].remove(tag)

    tags = ['migrated'] + details['tags']

    notes = ''
    # Copy over notes
    if 'notes' in details:
        notes = details['notes']

    response = dashboard.devices.updateDevice(serial, tags=tags, notes=notes)
    progress.console.print("Updated device details for: [green]{}[/]".format(serial))


# Get site-to-site vpn config for network
def get_site_to_site_config(net_id, progress):
    config = dashboard.appliance.getNetworkApplianceVpnSiteToSiteVpn(net_id)

    progress.console.print("Obtained site-to-site vpn config for network id [magenta]{}[/]".format(net_id))
    return config


# Enable site-to-site vpn config for network in whatever mode (note: contents saved, we just need to turn on the
# right mode)
def update_site_to_site_config(net_id, config, progress):
    response = dashboard.appliance.updateNetworkApplianceVpnSiteToSiteVpn(net_id, mode=config['mode'])

    progress.console.print("Updated site-to-site vpn config for: [magenta]{}[/]".format(net_id))


# Generate a vmx token after claiming a vmx device into a network
def generate_vmx_token(serial, progress):
    token = dashboard.appliance.createDeviceApplianceVmxAuthenticationToken(serial)

    progress.console.print("Generated new token: [green]{}[/].".format(token['token']))
    return token
