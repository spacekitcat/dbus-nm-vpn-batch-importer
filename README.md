# VPN Batch Importer for Network Manager (dbus-nm-vpn-batch-importer)
Imports large sets of OpenVPN formatted VPN files into Dbus Network Manager.

# Requirements
Python 3.x  
pip (gets dbus_python 1.2.x)  

# Setup
$ cd dbus-nm-vpn-batch-importer/  
$ python -m pip install -r requirements.txt  

# Usage

## Mandatory arguments  
Argument 1: Input folder  
Argument 2: VPN Service username  

## Optional Flags  
--vpn_ask_password  # Asks you to enter a password for your VPN service via a secure prompt  


$ cd dbus-nm-vpn-batch-importer/  
$ python netman_ovpn_importer.py FOLDER_WITH_OVPN_FILES YOUR_VPN_LOGIN_ID --vpn_ask_password  

# Usage example
$ cd dbus-nm-vpn-batch-importer/  
$ python netman_ovpn_importer.py ../vpn/ pikachu@spacekitcat.com --vpn_ask_password  

Enter the password for your VPN account:  
Scanning for *.ovpn files in ../vpn/  
Processing ovpn files: Done.                                                          
Loaded 2256 oVPN connections.  
Adding profiles to Network Manager:  Done.                                                   
Reloading connections: Done.      

# Unit tests
$ cd dbus-nm-vpn-batch-importer/  
$ python -m unittest

# License
MIT  

