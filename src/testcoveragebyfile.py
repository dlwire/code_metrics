import unittest
from xml.etree import ElementTree as ET
from coveragebyfile import *

class TestCoverageReport(unittest.TestCase):
    def setUp(self):
        self.empty_xml = ET.fromstring("<BullseyeFakeXml></BullseyeFakeXml>")
        self.single_item = ET.fromstring("<BullseyeFakeXml><src name='Bob.cpp' fn_total='2' fn_cov='1' d_total='4' d_cov='3'></src></BullseyeFakeXml>")
        self.two_items = ET.fromstring("<BullseyeFakeXml><src name='Bob.cpp' fn_total='2' fn_cov='1' d_total='4' d_cov='3'></src><src name='Sue.cpp' fn_total='4' fn_cov='1' d_total='2' d_cov='2'></src></BullseyeFakeXml>")
        self.with_one_folder = ET.fromstring("<BullseyeFakeXml><folder name='foo'><src name='Baz.cpp' fn_total='2' fn_cov='1' d_total='4' d_cov='3'></src></folder></BullseyeFakeXml>")
        self.with_two_folders = ET.fromstring("<BullseyeFakeXml><folder name='foo'><folder name='bar'><src name='Baz.cpp' fn_total='2' fn_cov='1' d_total='4' d_cov='3'></src></folder></folder></BullseyeFakeXml>")

    def test_empty_tree_returns_empty_list(self):
        self.assertEquals([], process_xml_tree(self.empty_xml))

    def test_single_source_file_returns_single_item_list(self):
        o = process_xml_tree(self.single_item)
        self.assertEquals(1, len(o))
        self.assertEquals('Bob.cpp', o[0].relative_path)
        self.assertEquals(2, o[0].function_count)
        self.assertEquals(50, o[0].function_coverage)
        self.assertEquals(4, o[0].branch_count)
        self.assertEquals(75, o[0].branch_coverage)

    def test_two_source_files_returns_two_item_list(self):
        o = process_xml_tree(self.two_items)
        self.assertEquals(2, len(o))

        
    def test_source_files_add_folder_names_from_above(self):
        o = process_xml_tree(self.with_one_folder)
        self.assertEquals("foo/Baz.cpp", o[0].relative_path)

    def test_source_files_add_multiple_folder_names_from_above(self):
        o = process_xml_tree(self.with_two_folders)
        self.assertEquals("foo/bar/Baz.cpp", o[0].relative_path)

    def test_source_files_add_multiple_folder_names_from_above_and_strip_repo(self):
        o = process_xml_tree(self.with_two_folders, repo_path='foo')
        self.assertEquals("bar/Baz.cpp", o[0].relative_path)

    def test_fn_ratio_is_zero_when_total_is_zero(self):
        data = namedtuple('mocknode', ['attrib'])
        data.attrib = {'fn_cov':'0', 'fn_total':'0', 'd_cov':'0', 'd_total':'0', 'name':''}
        cov = to_file_coverage(data, None)
        self.assertEquals(0, cov.function_coverage)
        self.assertEquals(0, cov.branch_coverage)

    def test_coverage_can_be_stringified(self):
        o = process_xml_tree(self.single_item)
        self.assertEquals('2,50,4,75,Bob.cpp', str(o[0]))

if __name__ == '__main__':
    unittest.main()
