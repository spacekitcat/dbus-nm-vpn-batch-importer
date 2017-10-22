import unittest
from networkmanager import NetworkManagerConnectionConfigGroup

class TestDefaultStateNetworkManagerNetworkManagerConnectionConfigGroup(unittest.TestCase):
  def setUp(self):
    self.sut = NetworkManagerConnectionConfigGroup( { 'simple_int_value' : 1, 'child_obj_value' : { 'child_int_field' : 2 } } )

  def test_assertthat__simple_int_value__equals_default(self):
    result = self.sut.get_value('simple_int_value')
    self.assertEqual(1, result)

  def test_assertthat__child_obj_value__equals_default(self):
    result = self.sut.get_value('child_obj_value')
    self.assertEqual( { 'child_int_field' : 2 }, result)
  
  def test_assertthat__update_simple_int_value__equals_updateval(self):
    self.sut.set_value('simple_int_value', 2)
    result = self.sut.get_value('simple_int_value')
    self.assertEqual(2, result)

  def test_assertthat__unknown_key__throws_exception(self):
    self.assertRaises(KeyError, self.sut.get_value, 'this_key_does_not_exist')

#class TestObjectUpdatesNetworkManagerNetworkManagerConnectionConfigGroup(unittest.TestCase):
#  def setUp(self):
#    self.sut = NetworkManagerConnectionConfigGroup( { 'obj_value' : { 'child_int': 0, 'child_str': 'hi!' } } )
#
#  def test_assertthat__update_objval_blankobj__equals_original(self):
#    self.sut.set_value('obj_value', {} )
#    result = self.sut.get_value('obj_value')
#    self.assertEqual( { 'child_int': 0, 'child_str': 'hi!' }, result)
#
#  def test_assertthat__update_objval_firstkey_match__matchedkey_updated(self):
#    self.sut.set_value('obj_value', { 'child_int': 5 } )
#    result = self.sut.get_value('obj_value')
#    self.assertEqual( { 'child_int': 5, 'child_str': 'hi!' }, result)
#
#  def test_assertthat__update_objval_secondkey_match__matchedkey_updated(self):
#    self.sut.set_value('obj_value', { 'child_str': 'bye!' } )
#    result = self.sut.get_value('obj_value')
#    self.assertEqual( { 'child_int': 0, 'child_str': 'bye!' }, result)
#
#  def test_assertthat__update_objval_bothkey_match__matchedkey_updated(self):
#    self.sut.set_value('obj_value', { 'child_int': 3, 'child_str': 'Buhbye!' } )
#    result = self.sut.get_value('obj_value')
#    self.assertEqual( { 'child_int': 3, 'child_str': 'Buhbye!' }, result)
#
#  def test_assertthat__update_objval_newkey__newkey_rejected(self):
#    self.sut.set_value('obj_value', { 'new_child': 7 } )
#    result = self.sut.get_value('obj_value')
#    self.assertEqual( { 'child_int': 0, 'child_str': 'hi!' }, result)
#
#  def test_assertthat__update_objval_newkeys_and_matched_key__newkey_rejected_added_mathedkeys_updated(self):
#    self.sut.set_value('obj_value', { 'child_str': 'Oh ya?','new_child': 7 } )
#    result = self.sut.get_value('obj_value')
#    self.assertEqual( { 'child_int': 0, 'child_str': 'Oh ya?' }, result)
#
if __name__ == '__main__':
  unittest.main()
