#!/bin/bash

sudo find /etc/NetworkManager/system-connections/ -name '*_' -exec rm {} +
find ~/.cert/nm-openvpn/ -name '*.*' -exec rm {} +
sudo systemctl restart NetworkManager
