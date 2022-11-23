# Meraki VMX Migration Tool

This prototype automates migration between VMX models, and it supports the follow settings migrations: Appliance Configuration, L3 Firewall Rules, L7 Firewall Rules, and Site-to-Site VPN. 

## Contacts
* Trevor Maco
* Jorge Benegas

## Solution Components
* Meraki API
* VMX
* Python3

## Prerequisites
* API Key: In order to use the Meraki API, you need to enable the API for your organization first. After enabling API access, you can generate an API key. Follow these instructions to enable API access and generate an API key:
  * Login to the Meraki dashboard
  * In the left-hand menu, navigate to Organization > Settings > Dashboard API access
  * Click on Enable access to the Cisco Meraki Dashboard API
  * Go to My Profile > API access
  * Under API access, click on Generate API key
  * Save the API key in a safe place. The API key will only be shown once for security purposes, so it is very important to take note of the key then. In case you lose the key, then you have to revoke the key and a generate a new key. Moreover, there is a limit of only two API keys per profile.

* This program assumes the new VMX devices have **already been claimed** and are **unassigned** in the inventory.

For more information on how to generate an API key, please click [here](https://developer.cisco.com/meraki/api-v1/#!authorization/authorization).

**Note**: You can add your account as Full Organization Admin to your organizations by following the instructions [here](https://documentation.meraki.com/General_Administration/Managing_Dashboard_Access/Managing_Dashboard_Administrators_and_Permissions).


## Installation/Configuration
1. Clone this repository with `git clone https://github.com/gve-sw/gve_devnet_meraki_vmx_migration`
2. Set up a Python virtual environment. Make sure Python 3 is installed in your environment, and if not, you may download Python [here](https://www.python.org/downloads/). Once Python 3 is installed in your environment, you can activate the virtual environment with the instructions found [here](https://docs.python.org/3/tutorial/venv.html).
3. Install the requirements with:
    ``` bash
   pip3 install -r requirements.txt
   ```
4. Fill in the `config.py` parameters. These include: Bot Token, Bot Name, and the name of the Webex Help Space.
    ``` python
    API_KEY = "<your api key>"
    ORG_NAME = "<your org name>"
    OLD_MODEL = "<old vmx model>"
    NEW_MODEL = "<new vmx model>"
    ```

## Usage

This program does an 'in network' swap of either all networks containing the old VMX or select networks specified by network tag. 

Workflow:

![/IMAGES/workflow.png](/IMAGES/workflow.png)

**Note**: a 'migrated' tag is applied to all new vmx's for convenience!

1. Launch the program with the command:
    ``` python
     python3 provison.py
    ```

2. Select 'Tag Mode' or 'All Mode' with the prompt. If Tag Mode is selected, enter a valid network tag.

![/IMAGES/selection.png](/IMAGES/selection.png)

3. Meraki networks are modified, and the output file `token.csv` will be created. This file contains the VMX tokens mapped to the VMX serial numbers. Each new VMX also includes a `migrated` tag.

Modified Network:

![/IMAGES/new_network.png](/IMAGES/new_network.png)

Tokens:

![/IMAGES/tokens.png](/IMAGES/tokens.png)

4. Input the VMX Tokens into the cloud platform of choice, and ensure devices come online in the Meraki Dashboard.
  
---
**For assistance in cloud deployment, follow the respective guides:**

* Azure: https://documentation.meraki.com/MX/MX_Installation_Guides/vMX_Setup_Guide_for_Microsoft_Azure
* AWS: https://documentation.meraki.com/MX/MX_Installation_Guides/vMX_Setup_Guide_for_Amazon_Web_Services_(AWS)

---

Output:

![/IMAGES/terminal.png](/IMAGES/terminal.png)

Migrated Configuration Example:

* Old Firewall Rules:

![/IMAGES/old_firewall_rules.png](/IMAGES/old_firewall_rules.png)

* New Firewall Rules:

![/IMAGES/new_firewall_rules.png](/IMAGES/new_firewall_rules.png)



# Screenshots

![/IMAGES/0image.png](/IMAGES/0image.png)

### LICENSE

Provided under Cisco Sample Code License, for details see [LICENSE](LICENSE.md)

### CODE_OF_CONDUCT

Our code of conduct is available [here](CODE_OF_CONDUCT.md)

### CONTRIBUTING

See our contributing guidelines [here](CONTRIBUTING.md)

#### DISCLAIMER:
<b>Please note:</b> This script is meant for demo purposes only. All tools/ scripts in this repo are released for use "AS IS" without any warranties of any kind, including, but not limited to their installation, use, or performance. Any use of these scripts and tools is at your own risk. There is no guarantee that they have been through thorough testing in a comparable environment and we are not responsible for any damage or data loss incurred with their use.
You are responsible for reviewing and testing any scripts you run thoroughly before use in any non-testing environment.