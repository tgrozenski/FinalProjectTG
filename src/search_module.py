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
        if pattern in line:
            return True
        return False

    # needs refactoring, trying to find a way to reduce code duplication for the iterating step
    def iterate_file(self, file: str, pattern: str, action: str) -> str:
        line_count = 1
        with open(file) as user_file:
            for line in user_file:
                print(action.format(line.strip(), pattern))
                if eval(action.format(line.strip(), pattern)):
                    result_list.append(result(pattern, pattern, PERFECT_MATCH, line_count))
                line_count += 1


    def ignore_case_search(self, file: str, pattern: str) -> str:
        ...