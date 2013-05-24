import unittest
from pathgroomer import *

class TestPathGroomer(unittest.TestCase):
    def test_returns_input_if_no_prefix_given(self):
        self.assertEquals('this/is/my/path', groom('this/is/my/path'))
    
    def test_returns_input_if_empty_prefix_given(self):
        self.assertEquals('this/is/my/path', groom('this/is/my/path', ''))

    def test_returns_empty_string_if_prefix_matches_input(self):
        self.assertEquals('', groom('this/is/my/path', 'this/is/my/path')) 

    def test_does_not_strip_out_middle_of_input(self):
        self.assertEquals('this/is/my/ninja/prefix/path', groom('this/is/my/ninja/prefix/path', 'ninja/prefix'))

    def test_does_not_remove_prefix_from_the_end_of_input(self):
        self.assertEquals('path/prefix', groom('prefix/path/prefix', 'prefix'))

    def test_removes_extra_slash_after_prefix(self):
        self.assertEquals('path', groom('prefix/path', 'prefix'))

    def test_does_not_remove_prefixed_slash_if_no_prefix_given(self):
        self.assertEquals('/this/is/an/absolute/path', groom('/this/is/an/absolute/path'))

    def test_does_not_remove_two_prefixes_only_removes_first(self):
        self.assertEquals('that', groom('/this/is/an/absolute/path/that', '/this/is/an/absolute/path'))

if __name__ == '__main__': 
    unittest.main()
