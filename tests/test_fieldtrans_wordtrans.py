import unittest

from imports.openvpn_netman_conversion import FieldTranslationRule 

class TestFieldTransWordTrans(unittest.TestCase):
  def setUp(self):
    sut = FieldTranslationRule('proto', 'tcp')
    sut.add_word_replace_mapping('tcp', 'yes')
    sut.add_word_replace_mapping('udp', 'no')
    
    self.sut = sut

  def test_fieldNameValueBlank_returnsInput(self):
    self.assertEqual(self.sut.do_trans('', ''), ('', '')) 

  def test_fieldNameBlank_returnsInput(self):
    self.assertEqual(self.sut.do_trans('', 'remote'), ('', 'remote')) 

  def test_fieldNameNotFound_returnsInput(self):
    self.assertEqual(self.sut.do_trans('NotFoundField', 'tcp'), ('NotFoundField', 'tcp')) 

  def test_fieldNameNotFoundBlankValue_returnsInput(self):
    self.assertEqual(self.sut.do_trans('NotFoundField', ''), ('NotFoundField', '')) 

  def test_hasFieldBlankValue_translatesfield(self):
    self.assertEqual(self.sut.do_trans('proto', ''), ('tcp', '')) 

  def test_hasFieldRecogValue1_translatesfieldvalue(self):
    self.assertEqual(self.sut.do_trans('proto', 'udp'), ('tcp', 'no')) 

  def test_hasFieldRecogValue2_translatesfieldvalue(self):
    self.assertEqual(self.sut.do_trans('proto', 'tcp'), ('tcp', 'yes')) 
  
  def test_hasFieldUnrecVal_translatesfieldvalue(self):
    self.assertEqual(self.sut.do_trans('proto', 'rrrp'), ('tcp', 'rrrp')) 

if __name__ == '__main__':
  unittest.main()
