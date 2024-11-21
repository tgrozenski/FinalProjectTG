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
        else it returns the result
        """
        index = 0
        pattern_len = len(pattern)
        while index <= len(line) - pattern_len:
            if line[index:index + pattern_len] == pattern:
                return result(pattern, pattern, PERFECT_MATCH, line_number, index)
            index += 1
        return None


    def ignore_case_match(self, line: str, pattern: str, line_number: int) -> result:
        print(potential_match)
        potential_match: result = self.match_line(pattern.casefold(), line.casefold(), line_number)
        if potential_match == None:
            return None

        potential_match.pattern = pattern
        potential_match.found_str = line[potential_match.line_index: len(pattern)]

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