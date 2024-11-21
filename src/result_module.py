class result:
    def __init__(self, found, pattern, match_percentage, line_location) -> None:
        self.found: str = found 
        self.pattern: str = pattern
        self.match_percentage: float = match_percentage
        self.line_location: int = line_location
    

    def get_formatted_result(self) -> str:
        return f'Found result "{self.found}" from pattern "{self.pattern}" on line: {self.line_location} match percentage: {self.match_percentage}'
