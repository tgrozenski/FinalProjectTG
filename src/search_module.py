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
        Returns a result object if line is found, else returns an None 
        """
        if pattern in line:
            return result(pattern, pattern, PERFECT_MATCH, line_number)
        return None


    def ignore_case_match(self, file: str, pattern: str, line_number: int) -> str:
        ...


    def iterate_file(self, file: str, pattern: str, action: str) -> str:
        line_count = 1
        selected_method = self.__getattribute__(action)
        # https://stackoverflow.com/questions/2283210/python-function-pointer
        with open(file) as user_file:
            for line in user_file:
                found = selected_method(line, pattern, line_count)
                if found != None:
                    result_list.append(found)
                line_count += 1
