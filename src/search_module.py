import re
from result_module import result

result_list: list = []
PERFECT_MATCH: float = 1.0

class searcher:
    def __init__(self) -> None:
        pass


    def get_result_list(self) -> list:
        return result_list


    def match_line(self, line: str, pattern: str) -> bool:
        """
        Returns a formatted result object if line is found, else returns an empty string ''
        """
        if pattern in line:
            return True
        return False


    def iterate_file(self, file: str, pattern: str, action: str) -> str:
        line_count = 1
        comparison = self.__getattribute__(action)
        with open(file) as user_file:
            for line in user_file:
                if comparison(line, pattern) != '':
                    print('found', pattern, 'on line', line_count)
                line_count += 1


    def ignore_case_search(self, file: str, pattern: str) -> str:
        ...