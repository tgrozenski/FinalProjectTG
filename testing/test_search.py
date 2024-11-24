import unittest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join
(os.path.dirname(__file__), '../src')))

from search_module import searcher
search = searcher()

RESULT_TEMPLATE = 'Found result "{}" from pattern "{}" on line: {} index: {} match percentage: {}'


class TestSearch(unittest.TestCase):
    def test_match_line(self):
        expected = RESULT_TEMPLATE.format('123', '123', 4, 20, 1.0)
        actual = search.match_line("This is a test line 123", '123', 4)
        self.assertEqual(str(actual), expected)

        actual = search.match_line("This is a test line 123", 'cookies', 4)
        expected = None
        self.assertEqual(actual, expected)

        expected = RESULT_TEMPLATE.format('cookies', 'cookies', 1, 30, 1.0)
        actual = search.match_line('hello world i definitely love cookies', 'cookies', 1)
        self.assertEqual(str(actual), expected)


    def test_ignore_case_match(self):
        expected = RESULT_TEMPLATE.format('cookies', 'COOKIES', 1, 30, 1.0)
        actual = search.ignore_case_match('hello world i definitely love cookies', 'COOKIES', 1)
        self.assertEqual(str(actual), expected)

        actual = search.ignore_case_match("This is a test Cookies line 123", 'cokies', 4)
        expected = None
        self.assertEqual(actual, expected)

        actual = search.ignore_case_match("This is a test that is more hARdEr", 'harder', 4)
        expected = RESULT_TEMPLATE.format('hARdEr', 'harder', 4, 28, 1.0)
        self.assertEqual(str(actual), expected)


    def test_regex_expression_match(self):
        actual = search.regex_expression_match('12312424-hey-1234141335', '(hi|hello|hey)', 4)
        expected = RESULT_TEMPLATE.format('hey', '(hi|hello|hey)', 9, 4, '21%')
        self.assertEqual(str(actual), expected)



if __name__ == "__main__":
    unittest.main()