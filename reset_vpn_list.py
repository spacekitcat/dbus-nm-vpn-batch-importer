#!/bin/bash

sudo find /etc/NetworkManager/system-connections/ -name '*_' -exec rm {} +
sudo systemctl restart NetworkManager
