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

if __name__ == '__main__':
  unittest.main()
