class result:
    def __init__(self, found_str: str, pattern: str, match_percentage: float, line_location: int, line_index: int) -> None:
        self.found_str: str = found_str
        self.pattern: str = pattern
        self.match_percentage: float = match_percentage
        self.line_number: int = line_location
        self.line_index: int = line_index

    def __str__(self) -> str:  # https://www.geeksforgeeks.org/print-objects-of-a-class-in-python/
        return f'Found result "{self.found_str}" from pattern "{self.pattern}" on line: {self.line_number} index: {self.line_index} match percentage: {self.match_percentage}'

    def __repr__(self) -> str:
        return f'Found result "{self.found_str}" from pattern "{self.pattern}" on line: {self.line_number} index: {self.line_index}match percentage: {self.match_percentage}'
