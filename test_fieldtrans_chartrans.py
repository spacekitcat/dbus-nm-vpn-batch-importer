import unittest
from openvpn_netman_conversion import FieldTranslationRule 

class TestFieldTransCharTrans(unittest.TestCase):
  def setUp(self):
    sut = FieldTranslationRule('remote', 'addr')
    sut.add_char_replace_mapping(' ', ':')
    
    self.sut = sut

  def test_fieldNameValueBlank_returnsInput(self):
    self.assertEqual(self.sut.do_trans('', ''), ('', '')) 

  def test_fieldNameBlank_returnsInput(self):
    self.assertEqual(self.sut.do_trans('', 'remote'), ('', 'remote')) 

  def test_fieldNameNotFound_returnsInput(self):
    self.assertEqual(self.sut.do_trans('NotFoundField', 'x x x'), ('NotFoundField', 'x x x')) 

  def test_fieldNameNotFoundBlankValue_returnsInput(self):
    self.assertEqual(self.sut.do_trans('NotFoundField', ''), ('NotFoundField', '')) 

  def test_hasFieldBlankValue_translatesfield(self):
    self.assertEqual(self.sut.do_trans('remote', ''), ('addr', '')) 

  def test_hasFieldBlank_translatesfieldvalue(self):
    self.assertEqual(self.sut.do_trans('remote', 'x x x'), ('addr', 'x:x:x')) 

if __name__ == '__main__':
  unittest.main()
