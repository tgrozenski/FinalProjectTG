import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join
(os.path.dirname(__file__), '../src')))

from search_module import searcher
search = searcher()

class TestSearch(unittest.TestCase):
    def test_match_line(self):
        expected = 'Found result "123" from pattern "123" on line: 4 index: 20 match percentage: 1.0'
        actual = search.match_line("This is a test line 123", '123', 4)
        self.assertEqual(str(actual), expected)

        actual = search.match_line("This is a test line 123", 'cookies', 4)
        expected = None
        self.assertEqual(actual, expected)

    def test_ignore_case_match(self):
        expected = 'Found result "cookies" from pattern "COOKIES" on line: 1 index: 20 match percentage: 1.0'
        actual = search.ignore_case_match('hello world i definitely love cookies', 'COOKIES', 1)
        self.assertEqual(str(actual), expected)

        # actual = search.match_line("This is a test Cookies line 123", 'cookie', 4)
        # expected = None
        # self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()