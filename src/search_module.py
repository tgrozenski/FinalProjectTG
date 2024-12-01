import re
import math
from result_module import result

from Levenshtein import distance

result_list: list[result] = []
PERFECT_MATCH: str = '100%'

class searcher:
    def __init__(self) -> None:
        pass


    def get_result_list(self) -> list:
        return result_list


    def append_result_list(self, string: str) -> None:
        result_list.append(string)


    def match_line(self, line: str, pattern: str, line_number: int) -> result:
        """
        Returns a result object if an exact match is found, else returns an None 

        args:
        line: str, A stripped line to be compared
        pattern: str, the search term
        line_number, the current line number necessary for the result object

        Examples:
        >>> match_line("This is a test line 123", '123', 4)
        'Found result "123" from pattern "123" on line: 4 match percentage: 1.0'
        >>> match_line("This is a test line 123", 'cookies', 4)
        None
       
        Returns:
        None if no result found,
        else it returns the result object
        """
        # rewrite using .split()
        index = 0
        pattern_len = len(pattern)
        while index <= len(line) - pattern_len:
            if line[index:index + pattern_len] == pattern:
                return result(pattern, pattern, PERFECT_MATCH, line_number, index)
            index += 1
        return None


    def regex_expression_match(self, line: str, pattern: str, line_number: int) -> result:
        """
        Returns a result object from a regular expression

        args:
        line: str, A stripped line to be compared
        pattern: str, the search term
        line_number, the current line number necessary for the result object

        Examples:
        >>> regex_expression_match("hey this is a test line cookies", 'hi|hello|hey', 4)
        'Found result "hey" from pattern "'hi|hello|hey'" on line: 4 index: 0 match percentage: 1.0'
        >>> regex_expression_match("This is a test line COOKIE", 'cokies', 4)
        None
        >>> regex_expression_match("This is a test line that is hArDeR", 'harder', 4)
        'Found result "hArdeR" from pattern "harder" on line: 4 match percentage: 1.0'
       
        Returns:
        None if no result found,
        else it returns the result object
        """ 
        match = re.search(pattern, line)

        if match == None:
            return None

        return result(match[0], pattern, self.calculate_match_percentage(match[0], pattern), 
                            line_number, match.span()[0])


    def ignore_case_match(self, line: str, pattern: str, line_number: int) -> result:
        """
        Returns a result object if a case insensitive match is found, else returns None 

        args:
        line: str, A stripped line to be compared
        pattern: str, the search term
        line_number, the current line number necessary for the result object

        Examples:
        >>> ignore_case_match("This is a test line cookies", 'COOKIES', 4)
        'Found result "cookies" from pattern "COOKIE" on line: 4 match percentage: 1.0'
        >>> ignore_case_match("This is a test line COOKIE", 'cokies', 4)
        None
        >>> ignore_case_match("This is a test line that is hArDeR", 'harder', 4)
        'Found result "hArdeR" from pattern "harder" on line: 4 match percentage: 1.0'
       
        Returns:
        None if no result found,
        else it returns the result object
        """

        potential_match: result = self.match_line(line.casefold(), pattern.casefold(), line_number)

        if potential_match == None:
            return None

        potential_match.pattern = pattern
        start_of_str = potential_match.line_index
        end_of_str = potential_match.line_index + len(pattern)
        potential_match.found_str = line[start_of_str : end_of_str]

        return potential_match


    def fuzzy_match(self, line: str, pattern: str, line_number: int) -> result:

        word_list: list[str] = line.split()

        for word in word_list:
            word.strip()
            dist: int = distance(word, pattern, score_cutoff=math.floor(len(word) / 2))
            if dist <= math.floor(len(word) / 2):
                print("This is a match", dist, word, pattern, "Match Percentage", self.calculate_fuzzy_match(word, pattern))
    

    def calculate_fuzzy_match(self, match: str, pattern: str) -> str:
        """
        reads pattern into memory as a dictionary, calculates the average of the 
        percentage of shared characters and number of characters in order 

        Args:
        the match to be compared, string
        the pattern to be compared, string

        Examples:   
        >>> calculate_fuzzy_match('hello', 'hello')
        '100%'
        >>> calculate_fuzzy_match('olleh', 'hello')
        '60%'
        >>> calculate_fuzzy_match('ld', 'world')
        '40%'
        >>> calculate_fuzzy_match('dl', 'world')
        '30%'
        >>> calculate_fuzzy_match('x', 'world')
        '0%'

        Returns:
        the match percentage taking into account the order and shared characters 
        """
        # shared character score
        pattern_dict: dict = {}
        for char in pattern:
            if char in pattern_dict.keys():
                pattern_dict[char] += 1
            else:
                pattern_dict[char] = 1

        score = 0
        for char in match:
            if char in pattern_dict.keys():
                pattern_dict[char] -= 1

        for value in pattern_dict.values():
            score += value
        
        pattern_len = len(pattern)
        sameness_score = (pattern_len - abs(score)) / pattern_len

        # character order score
        greater, lesser = '', ''
        if len(match) >= len(pattern):
            greater = match
            lesser = pattern
        else: 
            greater = pattern
            lesser = match

        order, lesser_index = 0, 0
        for i in range(len(greater)):
            if lesser_index == len(lesser):
                break
            if lesser[lesser_index] == greater[i]:
                order += 1
                lesser_index += 1

        order_score = order / len(greater)
        avg = (sameness_score + order_score) / 2
        if avg == 1.0:
            return '100%'
        else:
            return str(round(avg * 100)) + '%'


    def calculate_match_percentage(self, match: str , pattern: str) -> str:
        """
        Calculates how close the pattern and match are in length filtered down to only alphanumeric characters

        Args:
        match: str, the string match found
        pattern: str, the string pattern used to find the match

        Examples:
        >>> calculate_match_percentage('batman', 'batman')
        100%
        >>> calculate_match_percentage('catsanddogs', 'cats')
        36%
        >>> calculate_match_percentage('12cats12', '...cats....')
        50%
        >>> calculate_match_percentage('12ca103', '..ca...')
        29%
        >>> calculate_match_percentage('cats', '!@#$!cats&dogs!@#@$@@')
        50%

        Returns:
        A percentage in string formatted
        
        """
        match_len = len(match)
        pattern = pattern.casefold()
        pattern_len = len([char for char in pattern if char.isalnum()])

        if match_len < pattern_len:
            result = round((match_len / pattern_len) * 100)
        elif pattern_len < match_len:
            result = round((pattern_len / match_len) * 100)
        else:
            result = 100

        return str(result) + '%'


    def iterate_file(self, file: str, pattern: str, action: str) -> None:
        """
        Iterates over a given file, impure function because it uses the
        getattribute method to call the correct search method based on the
        action string that gets passed in. Keeps track of line number. 

        args:
        file: str, the file to be read and 
        pattern: str, the search query
        action: str, the action method as defined in main.py

        returns: 
        None
        """
        line_count = 1
        # https://stackoverflow.com/questions/2283210/python-function-pointer
        selected_method = self.__getattribute__(action)
        with open(file) as user_file:
            for line in user_file:
                found = selected_method(line.strip(), pattern, line_count)
                if found != None:
                    result_list.append(found)
                    print('found on LINE', line)
                line_count += 1
