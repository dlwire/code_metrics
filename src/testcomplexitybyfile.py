import unittest
from complexitybyfile import *

class TestParseComplexityLine(unittest.TestCase):
    def setUp(self):
        self.good_line = '   17    12   5  FnName@23@/this/is/a/repository/path/to/source.cpp'

    def test_ignores_garbage_input(self):
        o = parse_line('')
        self.assertEquals(None, o)

    def test_fetches_lines_of_code_from_good_input(self):
        actual = parse_line(self.good_line)
        self.assertEquals(17, actual.loc)

    def test_fetches_cyclomatic_complexity_from_good_input(self):
        actual = parse_line(self.good_line)
        self.assertEquals(12, actual.ccn) 

    def test_fetches_filename_under_repo(self):
        actual = parse_line(self.good_line, '.*repository')
        self.assertEquals('path/to/source.cpp', actual.relative_path)

class TestAccumulateLinesByRelativePath(unittest.TestCase):
    def test_nothing_in_nothing_out(self):
        o = accumulate_lines([])
        self.assertEquals({}, o)
        
    def test_returns_map_with_path_as_key_with_one_input(self):
        fc = FileComplexity(1, 2, 'path/to/my/file.cpp')
        o = accumulate_lines([fc])
        self.assertEquals({'path/to/my/file.cpp': fc}, o)

    def test_returns_map_with_path_as_key_with_two_inputs(self):
        fc1 = FileComplexity(1, 2, 'path/to/my/file.cpp')
        fc2 = FileComplexity(3, 4, 'path/to/my/other/file.cpp')
        o = accumulate_lines([fc1, fc2])
        self.assertEquals({'path/to/my/file.cpp': fc1, 'path/to/my/other/file.cpp': fc2}, o)
        
    def test_return_contains_a_path_only_ones(self):
        fc1 = FileComplexity(1, 2, 'path/to/my/file.cpp')
        fc2 = FileComplexity(3, 4, 'path/to/my/file.cpp')
        o = accumulate_lines([fc1, fc2])
        self.assertEquals(['path/to/my/file.cpp'], o.keys())

    def test_return_accumulates_loc_and_ccn_for_matching_paths(self):
        fc1 = FileComplexity(1, 2, 'path/to/my/file.cpp')
        fc2 = FileComplexity(3, 4, 'path/to/my/file.cpp')
        o = accumulate_lines([fc1, fc2])
        self.assertEquals(4, o['path/to/my/file.cpp'].loc)
        self.assertEquals(6, o['path/to/my/file.cpp'].ccn)

class TestComplexityByFileParsesFiles(unittest.TestCase):
    def setUp(self):
        self.inputData = """
==============================================================
NLOC    CCN   token          function@line@file
--------------------------------------------------------------
     6     1    27 function1@14@/root/dir/anotherdir/repo/public/Package/Component/SubComponentOne/ClassOne.cpp
     3     1     0 function2@21@/root/dir/anotherdir/repo/public/Package/Component/SubComponentOne/ClassOne.cpp
     4     1     2 function3@25@/root/dir/anotherdir/repo/public/Package/Component/SubComponentOne/ClassOne.cpp
     3     1     0 function4@16@/root/dir/anotherdir/repo/public/Package/Component/SubComponentTwo/ClassTwo.cpp
     3     1     0 function5@21@/root/dir/anotherdir/repo/public/Package/Component/SubComponentTwo/ClassTwo.cpp
     4     1     2 function6@26@/root/dir/anotherdir/repo/public/Package/Component/SubComponentTwo/ClassTwo.cpp
     4     1     2 function7@32@/root/dir/anotherdir/repo/public/Package/Component/SubComponentTwo/ClassTwo.cpp
     4     1     2 function8@38@/root/dir/anotherdir/repo/public/Package/Component/SubComponentTwo/ClassTwo.cpp

"""
    
    def test_returns_array_of_accumulated_data(self):
        expected = [
            "18,5,public/Package/Component/SubComponentTwo/ClassTwo.cpp",
            "13,3,public/Package/Component/SubComponentOne/ClassOne.cpp"
        ]
        actual = process_file(self.inputData.split("\n"), '.*repo')
        self.assertTrue(expected[0] in actual)
        self.assertTrue(expected[1] in actual)
            

if __name__ == '__main__':
    unittest.main()

