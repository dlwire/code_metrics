import unittest
from parsearguments import parse

class TestParseArguments(unittest.TestCase):
    def test_with_no_arguments_raises_an_exception(self):
        raisedException = False

        try:
            args = parse(['script.py'])
        except:
            raisedException = True

        self.assertTrue(raisedException)

    def test_with_data_argument_returns_path_to_data(self):
        self.assertEquals('this/is/the.path', parse(['script.py', '--data', 'this/is/the.path']).data)

    def test_with_repo_argument_returns_path_to_data_and_repo(self):
        args = parse(['script.py', '--data', 'this/is/the/path.to.data', '--repo', 'this/is/the/repo/root'])
        self.assertEquals('this/is/the/path.to.data', args.data)
        self.assertEquals('this/is/the/repo/root', args.repo)
    
    def test_the_default_value_of_repo_is_empty_string(self):
        args = parse(['script.py', '--data', 'this/path'])
        self.assertEquals('', args.repo)

if __name__ == '__main__':
    unittest.main()
