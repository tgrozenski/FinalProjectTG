import unittest
import os
import sys

# got this line from past homeworks
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from search_module import searcher
search = searcher()

RESULT_TEMPLATE = 'Found result "{}" from pattern "{}" on line: {} index: {} match percentage: {}'


class TestSearch(unittest.TestCase):
    def test_match_line(self):
        expected = RESULT_TEMPLATE.format('123', '123', 4, 20, '100%')
        actual = search.match_line("This is a test line 123", '123', 4)
        self.assertEqual(str(actual), expected)

        actual = search.match_line("This is a test line 123", 'cookies', 4)
        expected = None
        self.assertEqual(actual, expected)

        expected = RESULT_TEMPLATE.format('cookies', 'cookies', 1, 30, '100%')
        actual = search.match_line('hello world i definitely love cookies', 'cookies', 1)
        self.assertEqual(str(actual), expected)


    def test_ignore_case_match(self):
        expected = RESULT_TEMPLATE.format('cookies', 'COOKIES', 1, 30, '100%')
        actual = search.ignore_case_match('hello world i definitely love cookies', 'COOKIES', 1)
        self.assertEqual(str(actual), expected)

        actual = search.ignore_case_match("This is a test Cookies line 123", 'cokies', 4)
        expected = None
        self.assertEqual(actual, expected)

        actual = search.ignore_case_match("This is a test that is more hARdEr", 'harder', 4)
        expected = RESULT_TEMPLATE.format('hARdEr', 'harder', 4, 28, '100%')
        self.assertEqual(str(actual), expected)


    def test_regex_expression_match(self):
        actual = search.regex_expression_match('12312424-hey-1234141335', '(hi|hello|hey)', 4)
        expected = RESULT_TEMPLATE.format('hey', '(hi|hello|hey)', 4, 9, '30%')
        self.assertEqual(str(actual), expected)

        actual = search.regex_expression_match('Batman', '[bB]atman', 4)
        expected = RESULT_TEMPLATE.format('Batman', '[bB]atman', 4, 0, '86%')
        self.assertEqual(str(actual), expected)

        actual = search.regex_expression_match('my Favorite videoGAME is minecraft _____', 'mine.....', 4)
        expected = RESULT_TEMPLATE.format('minecraft', 'mine.....', 4, 25, '44%')
        self.assertEqual(str(actual), expected)

    
    def test_fuzzy_match(self):
        self.assertEqual(str(search.fuzzy_match('SP@@@m', 'spam', 1)), 
                         RESULT_TEMPLATE.format('SP@@@m', 'spam', 1, 0, '54%'))
        self.assertEqual(str(search.fuzzy_match("hey hi holle ", "hello", 5)), 
                         RESULT_TEMPLATE.format('holle', 'hello', 5, 7, '70%'))
        self.assertEqual(str(search.fuzzy_match("i love ttles", "TURTLES", 5)), 
                         RESULT_TEMPLATE.format('ttles', 'TURTLES', 5, 7, '71%'))
        self.assertEqual(str(search.fuzzy_match("my favorite pet is dogs", "dogs", 5)), 
                         RESULT_TEMPLATE.format('dogs', 'dogs', 5, 19, '100%'))
    
    
    def test_calc_match(self):
        self.assertEqual(search.calculate_match('hello', 'hello'), '100%')
        self.assertEqual(search.calculate_match('olleh', 'hello'), '60%')
        self.assertEqual(search.calculate_match('ld', 'world'), '40%')
        self.assertEqual(search.calculate_match('dl', 'world'), '30%')
        self.assertEqual(search.calculate_match('x', 'world'), '0%')
    

    def test_get_index_from_word_list(self):
        self.assertEqual(0, search.get_index_from_line('word4', 'word4'))
        self.assertEqual(5, search.get_index_from_line('01234word4', 'word4'))
        self.assertEqual(10, search.get_index_from_line('0123456789word4', 'word4'))

if __name__ == "__main__":
    unittest.main()