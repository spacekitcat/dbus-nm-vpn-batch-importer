import os
import sys
import argparse
import logging

from networkmanager import NetworkManagerConnectionConfig
from openvpn import process_ovpn_list
from openvpn_netman_conversion import openvpn_to_netman

import NetworkManager

NetworkManager.NetworkManager.GetPermissions()

logger = logging.getLogger('ovpn2nm')
logger_fh = logging.FileHandler('ovpn2nm.log')
logger.setLevel(logging.DEBUG)
logger.addHandler(logger_fh)

def create_ifnot_exist(path):
  if not os.path.exists(path):
    os.makedirs(path)

def fix_trailing_slash(path):
  if not path.rfind('/') == len(path)-1:
    path = path + '/'
  return path

def main():
  parser = argparse.ArgumentParser(description='Converts *.opvn files in a \
      specified directory to NetworkManager connection profiles.')

  parser.add_argument(
      'input_directory', 
      metavar='input_folder', 
      help='Input directory')
  
  parser.add_argument(
      'vpn_login_id', 
      metavar='vpn_login_id', 
      help='VPN login name')
  
  parser.add_argument(
      'cert_path', 
      metavar='cert_path', 
      help='Certificate store output target (usually ~/.cert/nm-openvpn)')
  
  args = parser.parse_args()
 
  cert_path = fix_trailing_slash(args.cert_path)

  create_ifnot_exist(cert_path)
 
  sys.stdout.write('Scanning for *.ovpn files in ' + args.input_directory)
  ovpn_input_files = os.scandir(args.input_directory)
  vpn_profiles = process_ovpn_list(ovpn_input_files)

  for profile_id, profile in vpn_profiles.items():
    netman_config = NetworkManagerConnectionConfig(profile_id + '_', args.vpn_login_id)
    trans_profile = openvpn_to_netman(profile, cert_path, profile_id)
    netman_config.sync_with(trans_profile)
    NetworkManager.Settings.AddConnection(netman_config.get_settings())

if __name__ == '__main__':
  main()

