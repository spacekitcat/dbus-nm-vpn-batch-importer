# VPN Batch Importer for Network Manager (dbus-nm-vpn-batch-importer)
Imports large sets of OpenVPN formatted VPN files into Dbus Network Manager.

# Requirements (without pip)
Python 3.x
pip (gets dbus_python 1.2.x)

# Setup
$ cd dbus-nm-vpn-batch-importer/
$ python -m pip install -r requirements.txt

# Usage
$ cd dbus-nm-vpn-batch-importer/
$ python netman_ovpn_importer.py FOLDER_WITH_OVPN_FILES YOUR_VPN_LOGIN_ID

# Usage example
$ cd dbus-nm-vpn-batch-importer/
$ python netman_ovpn_importer.py ../vpn/ pikachu@spacekitcat.com
Scanning for *.ovpn files in ../vpn/
Processing ovpn files: Done.                                                        
Adding profiles to Network Manager:  Done.                                                 
All done. Please restart NetworkManager or reboot your system. Example: sudo systemctl restart NetworkManager.

# License
MIT

