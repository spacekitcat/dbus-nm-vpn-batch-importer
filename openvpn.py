import sys
import re
import logging

logger = logging.getLogger('ovpn2nm')

COMMENT_CHAR = '#'
def is_comment_line(line):
  return line.strip().startswith(COMMENT_CHAR)

def is_empty_line(line):
  return line.isspace()

def is_ignored_line(line):
  return is_comment_line(line) or is_empty_line(line)

def strip_file_extension(filename):
  tokens = filename.rsplit('.', maxsplit=1)
  if len(tokens) > 0:
    return tokens[0]

RE_XML_OPEN = re.compile('^<([A-Z\-a-z]+)>$')
def is_xml_open(line):
  return RE_XML_OPEN.match(line)

RE_XML_CLOSE = re.compile('^</[A-Z\-a-z]+>$')
def get_xml_tag_name(line):
  result = RE_XML_OPEN.match(line)
  re_groups = result.groups()
  tag_name = ''
  if len(re_groups) > 0:
    tag_name = re_groups[0]

  return tag_name

def read_xml_block(line_iter):
  xml_content = ''
  line = next(line_iter)
  while not RE_XML_CLOSE.match(line):
    xml_content = xml_content + line
    line = next(line_iter)

  return xml_content

def splitline_field_value(line):
  tokens = line.split(' ', maxsplit=1)
  field_name = ''
  if len(tokens) > 0:
    field_name = tokens[0]
  
  field_value = ''
  if field_name and len(tokens) > 1:
    field_value = tokens[1]
  
  return (field_name, field_value)

def conditional_fileize(field_name, field_value):
  return _fileizer.conditional_fileize(field_name, field_value)

def process_ovpn_file(ovpn_file):
  profile = dict()
  logger.debug('Reading ' + ovpn_file.path + '.')
  
  with open(ovpn_file) as ovpn_handle:
    
    all_lines = ovpn_handle.readlines();
    
    logger.debug('Read ' + str(len(all_lines)) + ' raw lines.')

    line_iter = iter(all_lines)
    for line in line_iter:
      if is_ignored_line(line):
        continue
      
      if is_xml_open(line):
        field_name = get_xml_tag_name(line)
        field_value = read_xml_block(line_iter)
      else:
        field = splitline_field_value(line)
        field_name = field[0]
        field_value = ''
        if len(field) > 1:
          field_value = field[1]
      
      profile[field_name.strip('\n')] = field_value.strip('\n')
    
    logger.debug('Extracted ' + str(len(profile)) + ' properties.')

    return profile

STDOUT_PROFILE_LEN = 80
def process_ovpn_list(all_ovpn_files):
  all_profiles = dict()
  
  print()
  for ovpn_file in all_ovpn_files:
    if not ovpn_file.name.startswith('.'):
      profile_id = strip_file_extension(ovpn_file.name)
      sys.stdout.write(str('Processing ovpn files: Reading ' + profile_id)[:STDOUT_PROFILE_LEN].ljust(STDOUT_PROFILE_LEN, ' ') + '    \r')
      all_profiles[profile_id] = process_ovpn_file(ovpn_file)
  
  sys.stdout.write('Processing ovpn files: Done.'.ljust(STDOUT_PROFILE_LEN, ' '))
  print()

  return all_profiles
