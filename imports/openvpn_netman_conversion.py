class Fileizer():
  def __init__(self, output_path, profile_id):
    self.output_path = output_path
    self.profile_id = profile_id
    self.properties_to_fileize = dict()

  def _get_output_filename(self, postfix):
    return self.profile_id + postfix

  def _get_fullpath_target(self, postfix):
    if not self.output_path.rfind('/'):
      self.output_path = self.output_path + '/'

    return self.output_path + self._get_output_filename(postfix)

  def add_fileize_condition(self, property_name, file_postfix):
    self.properties_to_fileize[property_name] = file_postfix

  def conditional_fileize(self, property_name, property_value):
    return_value = property_value
    if property_name in self.properties_to_fileize:
      postfix = self.properties_to_fileize[property_name]
      
      full_target_path = self._get_fullpath_target(postfix)
      with open(full_target_path, 'w') as fh:
        fh.write(property_value)
      
      return_value = self.output_path + self._get_output_filename(postfix)
    
    return return_value


class FieldTranslationRule():
  def __init__(self, target_field_name, replace_field_name):
    self.target_field_name = target_field_name
    self.replace_field_name = replace_field_name

    # Character replacements are performed by maketrans, so for instance,
    #   character_target_chars[0] gets replaced with character_substitute_chars[0]
    self.character_target_chars = ''
    self.character_subst_chars = ''
    self.value_replacements = dict()

  def add_char_replace_mapping(self, target_char, replace_with_char):
    self.character_target_chars = self.character_target_chars + target_char
    self.character_subst_chars = self.character_subst_chars + replace_with_char

  def add_word_replace_mapping(self, target_word, replace_target_word):
    self.value_replacements[target_word] = replace_target_word

  def _do_char_replace(self, target_value):
    ch_translation_table = str.maketrans(self.character_target_chars, self.character_subst_chars)

    return target_value.translate(ch_translation_table)
  
  def _do_word_replace(self, target_value):
    return_field_value = target_value

    if target_value in self.value_replacements:
      return_field_value = self.value_replacements[target_value]

    return return_field_value

  def do_trans(self, target_field_name, target_field_value):
    return_field_name = target_field_name
    return_field_value = target_field_value

    if target_field_name == self.target_field_name:
      return_field_name = self.replace_field_name
      return_field_value = self._do_char_replace(target_field_value)
      return_field_value = self._do_word_replace(return_field_value)

    return (return_field_name, return_field_value)

proto_field_rule = FieldTranslationRule('proto', 'proto-tcp')
proto_field_rule.add_word_replace_mapping('udp', 'no')
proto_field_rule.add_word_replace_mapping('tcp', 'yes')

remote_field_rule = FieldTranslationRule('remote', 'remote')
remote_field_rule.add_char_replace_mapping(' ', ':')

tls_auth_field_rule = FieldTranslationRule('tls-auth', 'ta')

comp_lzo_rule = FieldTranslationRule('comp-lzo', 'comp-lzo')
comp_lzo_rule.add_word_replace_mapping('', 'adaptive')

RULE_LIST = [proto_field_rule, remote_field_rule, tls_auth_field_rule, comp_lzo_rule]

def ovpn_to_netman_field_trans(key, value):
  for rule in RULE_LIST:
    key, value = rule.do_trans(key, value)

  return (key, value)

def openvpn_to_netman(openvpn_profile, pem_output_path, profile_id):
  fileizer = Fileizer(pem_output_path, profile_id)
  fileizer.add_fileize_condition('ca', '-ca.pem') 
  fileizer.add_fileize_condition('ta', '-tls-auth.pem') 
  
  netman_profile = dict()
  for key, value in openvpn_profile.items():
    field_name, field_value = ovpn_to_netman_field_trans(key, value)
    field_value = fileizer.conditional_fileize(field_name, field_value)
    netman_profile[field_name] = field_value

  return netman_profile
