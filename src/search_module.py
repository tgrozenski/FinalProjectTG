import re
from result_module import result

result_list: list[result] = []
PERFECT_MATCH: float = 1.0

class searcher:
    def __init__(self) -> None:
        pass


    def get_result_list(self) -> list:
        return result_list


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


    def calculate_match_percentage(self, match: str , pattern: str) -> str:
        """
        returns the match percentage, the length of all characters present in both the match
        and pattern divided by the pattern filtered down to only alphanumeric characters. 

        Args:
        match: str, the string match found
        pattern: str, the string pattern used to find the match

        Examples:
        >>> calculate_match_percentage('he lives in gotham his name is batman', 'batman')
        100%
        >>> calculate_match_percentage('catsanddogs', 'cats')
        100%
        >>> calculate_match_percentage('12cats12', 'cats')
        100%
        >>> calculate_match_percentage('12ca103', 'cats')
        50%
        >>> calculate_match_percentage('cats', '!@#$!cats&dogs!@#@$@@')
        50%


        Returns:
        A percentage formatted as a string
        
        """
        match = match.casefold()
        pattern = pattern.casefold()

        filtered_match_len: int = len([x for x in match if x in pattern])
        filtered_pattern_len: int = len([x for x in pattern if x.isalnum()])

        result = round((filtered_match_len / filtered_pattern_len) * 100)

        if result >= 100:
            return '100%'

        return str(result) + '%'


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
        selected_method = self.__getattribute__(action)
        # https://stackoverflow.com/questions/2283210/python-function-pointer
        with open(file) as user_file:
            for line in user_file:
                found = selected_method(line.strip(), pattern, line_count)
                if found != None:
                    result_list.append(found)
                line_count += 1
