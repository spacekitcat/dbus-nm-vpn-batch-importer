import uuid
import configparser

import NetworkManager
NetworkManager.NetworkManager.GetPermissions()
import dbus.mainloop.glib

class NetworkManagerConnectionConfigGroup:
  # - initialised_data_layout defines the white list of valid keys and safe defaults.
  #   dbus will abort if provided with unrecognised keys.
  # - root_node_key defines the top-level key, for instance, the vpn uses 'data'.
  def __init__(self, initialised_data_layout, root_node_key=None):
    self.data = dict(initialised_data_layout)
    self.root_node_key = root_node_key

  def set_value(self, key, value):
    
    current_root = self.data
    if not self.root_node_key is None:
      current_root = self.data[self.root_node_key]

    if key in current_root:
      current_root[key] = value

  def sync_with(self, sync_target):
    for key, value in sync_target.items():
      self.set_value(key, value)

  def get_value(self, key):
    return self.data[key]

  def get_settings(self):
    return self.data


class NetworkManagerConnectionConfig:
  def __init__(self, connection_id, vpn_login_id):
    
    self.connection_id = connection_id
    
    self.settings = dict()
    self.settings['connection'] = self.init_connection_group()
    self.settings['vpn']        = self.init_vpn_group(vpn_login_id)
    self.settings['ipv4']       = self.init_ipv4_group()
    self.settings['ipv6']       = self.init_ipv6_group()

  def init_connection_group(self):
    return NetworkManagerConnectionConfigGroup({'autoconnect': False, 'id': self.connection_id, 'permissions': [], 'type': 'vpn', 'uuid': str(uuid.uuid4())})
 
  def init_ipv4_group(self):
    return NetworkManagerConnectionConfigGroup({'address-data': [], 'addresses': [], 'dns': [], 'dns-search': [], 'method': 'auto', 'route-data': [], 'routes': []})

  def init_ipv6_group(self):
    return NetworkManagerConnectionConfigGroup({'address-data': [], 'addresses': [], 'dns': [], 'dns-search': [], 'ip6-privacy': 0, 'method': 'auto', 
      'route-data': [], 'routes': []})

  def init_vpn_group(self, user_name):
    return NetworkManagerConnectionConfigGroup({
          'data': 
            {
              'ca': '',
              'cipher': '',
              'auth': '',
              'comp-lzo': 'adaptive',
              'connection-type': 'password',
              'dev': 'tun',
              'mssfix': '1450',
              'password-flags': '1',
              'ping': '15',
              'ping-restart': '0',
              'proto-tcp': 'yes',
              'remote': '',
              'remote-cert-tls': 'server',
              'remote-random': 'yes',
              'reneg-seconds': '0',
              'ta': '',
              'ta-dir': '1',
              'tunnel-mtu': '1500',
              'username': user_name
            },

          'service-type': 'org.freedesktop.NetworkManager.openvpn'}, 'data')

  def get_settings(self):
    dict_for_dbus = dict()
    for key, val in self.settings.items():
      dict_for_dbus[key] = val.get_settings()

    return dict_for_dbus

  def sync_with(self, values_dict):
    for key, settings_group in self.settings.items():
      settings_group.sync_with(values_dict)
      
  def write_to_disk(self, output_path):
    for key, section in self.sections():
      self.connection_config_parser.add_section(section.section_name)
      for key, value in section.getvalues_list().items():
        self.connection_config_parser.set(section.section_name, key, value)

    with open(output_path, 'w') as output_fp:
      self.connection_config_parser.write(output_fp)

