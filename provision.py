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

import csv
from meraki_functions import *
from rich.console import Console
from rich.progress import Progress
from rich.panel import Panel

console = Console()


def main():
    console.print(Panel.fit("VMX Migration Tool"))

    # Selection of tag mode or all mode
    console.print('To use this tool, please enter (1) to migrate based on a [green]network tag[/], or (2) to migrate '
                  '[bold blue]all[/] VMX networks.')
    val = console.input('Selection: ')

    tag = None
    if val == '1':
        console.print('Please enter which [green]network tag[/] you would like to match ([yellow]ensure this tag is '
                      'present and applied to target networks![/])')
        tag = console.input('[green]Tag:[/] ')

    # Get org id's
    org_id = get_org_id(ORG_NAME)

    if org_id is None:
        console.print("[red]No organization was found with that name[/], please check the organization name.")
        exit(1)

    # Get old vmx device inventory
    console.print(Panel.fit("Get VMX Inventory", title="Step 1"))
    devices = get_org_vmx_inventory(org_id)

    # No devices found
    if len(devices) == 0:
        console.print('[red]No devices found.. please check the model number is correct.[/]')
        exit(-1)

    # Define csv file. This csv file will hold: new vmx serial number, vmx token, old vmx network id,
    # and new vmx network id
    with open('tokens.csv', 'w') as fp:
        # Create csv writer
        writer = csv.writer(fp)

        # create csv file headers
        writer.writerow(['New VMX Serial', 'VMX Token'])

        # For devices in a valid network, remove device from network and claim new device into it,
        # enable site-to-site vpn
        console.print(Panel.fit("Migrate VMX Devices", title="Step 2"))

        i = 0
        counter = 1
        with Progress() as progress:
            overall_progress = progress.add_task("Overall Progress", total=len(devices), transient=True)

            for device in devices:
                progress.console.print(
                    "Processing: [green]{}[/]. ({} of {})".format(device['serial'], str(counter), len(devices)))

                if device['networkId']:
                    # Get device details (device removal overwrites details)
                    details = get_device_details(device['serial'])

                    # Get network details
                    net_details = get_network_details(device['networkId'], progress)

                    # If tag is not present in network details (and not none, meaning - tag mode)
                    if tag and tag not in net_details['tags']:
                        progress.console.print(
                            'Tag not present in network tags for network {}... [yellow]skipping[/].'.format(
                                net_details['name']))
                    else:
                        # Get site-to-site config
                        config = get_site_to_site_config(device['networkId'], progress)

                        # Remove old device from network
                        remove_old_vmx(device['networkId'], device['serial'], progress)

                        # claim vmx into network
                        new_vmx = claim_vmx(device['networkId'], progress)

                        # If we are out of vmx licenses, then break
                        if new_vmx == 'No licenses':
                            break

                        # Update device details
                        i += 1
                        update_device_details(new_vmx['serial'], details, progress, tag)

                        # Update site-to-site config
                        update_site_to_site_config(device['networkId'], config, progress)

                        # Generate vmx tokens
                        token = generate_vmx_token(new_vmx['serial'], progress)

                        # write tokens and information to csv
                        writer.writerow([new_vmx['serial'], token['token']])

                else:
                    progress.console.print(
                        'Device [yellow]{}[/] not present in network... [yellow]skipping[/].'.format(device['serial']))

                progress.console.print('')
                counter += 1
                progress.update(overall_progress, advance=1)

    console.print(Panel.fit("Write Tokens to File", title="Step 3"))
    console.print('Wrote {} token(s) to tokens.csv'.format(i))


if __name__ == "__main__":
    main()
