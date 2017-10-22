import os
import sys
import argparse
import logging
import getpass
import pprint as pp

from imports.networkmanager import NetworkManagerConnectionConfig
from imports.openvpn import process_ovpn_list
from imports.openvpn_netman_conversion import openvpn_to_netman

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

def ask_password():
  password = ''
  try:
    password = getpass.getpass(prompt='Enter the password for your VPN account: ')
  except Exception as err:
    sys.exit(1)

  return password

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
      '--vpn_ask_password', 
      action='store_true',
      help='Triggers a secure password promt to read the VPN login password.')

  parser.add_argument(
      '--cert_path', 
      metavar='cert_path',
      default=os.path.expanduser('~/.cert/nm-openvpn/'),
      help='Certificate store output target (usually ~/.cert/nm-openvpn)')
  
  args = parser.parse_args()
 
  cert_path = fix_trailing_slash(args.cert_path)

  create_ifnot_exist(cert_path)

  vpn_login_password = ''
  if args.vpn_ask_password:
    vpn_login_password = ask_password()

  sys.stdout.write('Scanning for *.ovpn files in ' + args.input_directory)
  ovpn_input_files = os.scandir(args.input_directory)
  vpn_profiles = process_ovpn_list(ovpn_input_files)

  counter = 1
  profile_count = len(vpn_profiles)
  sys.stdout.write('Loaded ' + str(profile_count) + ' VPN connections. \n')
  status_line_prefix = 'Adding profiles to Network Manager: '
  
  for profile_id, profile in vpn_profiles.items():
    sys.stdout.write(status_line_prefix + str(counter) + ' of ' + str(profile_count) + '                     \r')
    
    netman_config = NetworkManagerConnectionConfig(profile_id + '_', args.vpn_login_id, vpn_login_password)
    trans_profile = openvpn_to_netman(profile, cert_path, profile_id + '_')
    netman_config.sync_with(trans_profile)
    path = NetworkManager.Settings.AddConnection(netman_config.get_settings())
    
    counter = counter + 1

  sys.stdout.write(status_line_prefix + ' Done.                                                 \n')
  
  sys.stdout.write('Reloading connections: ...                                                  \r')
  NetworkManager.Settings.ReloadConnections()
  sys.stdout.write('Reloading connections: Done.                                                \n')

if __name__ == '__main__':
  main()

