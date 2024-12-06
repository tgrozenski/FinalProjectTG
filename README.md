# Final Project Report

* Student Name: Tyler Grozenski
* Github Username: tgrozenski
* Semester: Fall 2024
* Course: CS5001



## Description 
General overview of the project, what you did, why you did it, etc. 
- the command line program grep is my favorite tool to use in a unix shell environment. It is incredibly useful in a wide variety of situations when you need to sift through large outputs to the stdout, and can search files and display relevant information. In my my project I set out to create a python program that can search for identical matches, case insensitive matches, search for regex expressions, and search for expression that are "fuzzy" matches.
I wanted to recreate some of this functionality to understand more about concepts like distance algorithms, stdin, search, and much more. 

## Key Features
Highlight some key features of this project that you want to show off/talk about/focus on. 

A key feature I am proud of is the ability to read data from the stdin. If you wanted to search the output of the ls command ignoring case you could do something like:
```bash
ls | python3 src/main.py -i INSTRUCTIONS
```
You will get the following result: 
```text
Result in this LINE: instructions

Found result "instructions" from pattern "INSTRUCTIONS" on line: 2 index: 0 match percentage: 100%
```
You can 'pipe' the output of the ls command (or any other command that outputs to the stdout) into the program to be searched. This feature to me is incredibly important because it makes the program compatible with a wide variety of other tools. My favorite part about the unix shell environment is how you can do anything using piping, redirects, and a wide variety of simple but effective command line programs. 

## Guide
How do we run your project? What should we do to see it in action? - Note this isn't installing, this is actual use of the project.. If it is a website, you can point towards the gui, use screenshots, etc talking about features. 

I would recommend that users begin by running the program with the help argument to see the order to get a helpful usage message from the argparser module.  
```bash
python3 src/main.py -h
```
The program outputs the following: 
```text
usage: TFinder [-h] [-i] [-e] [-z] [-f FILENAME] pattern

Finds a pattern in a file

positional arguments:
  pattern

options:
  -h, --help            show this help message and exit
  -i, --ignore_case
  -e, --regex
  -z, --fuzzy
  -f, --filename FILENAME

This program also allows piping from the stdin with a variety of search options
```
The program has five optional arguments which are help which displays the usages, ignore_case which does a case insensitive match, regex which allows you to input a regular expression to be searched for, z/fuzzy which which will do a fuzzy search using the Levenshtein module to find words that are close to the pattern given. The filename is another optional parameter, if the stdin is empty and no filename is provided the program will throw a user error to tell the user they need to provide some input to be searched. 


## Installation Instructions
If we wanted to run this project locally, what would we need to do?  If we need to get API key's include that information, and also command line startup commands to execute the project. If you have a lot of dependencies, you can also include a requirements.txt file, but make sure to include that we need to run `pip install -r requirements.txt` or something similar.

You can run 
```bash
pip install -r requirements.txt
```
Or alternatively since the project has only one dependency you can run: 
```bash
pip install python-Levenshtein
```

## Code Review
Go over key aspects of code in this section. Both link to the file, include snippets in this report (make sure to use the [coding blocks](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#code)).  Grading wise, we are looking for that you understand your code and what you did. 

### Key Code Aspect 3
[result](./src/result_module.py)
```python
class result:
  def __init__(self, found_str: str, pattern: str, match_percentage: float, line_location: int, line_index: int) -> None:
      self.found_str: str = found_str
      self.pattern: str = pattern
      self.match_percentage: float = match_percentage
      self.line_number: int = line_location
      self.line_index: int = line_index

  def __str__(self) -> str:
      return f'Found result "{self.found_str}" from pattern "{self.pattern}" on line: {self.line_number} index: {self.line_index} match percentage: {self.match_percentage}'

  def __repr__(self) -> str:
      return f'Found result "{self.found_str}" from pattern "{self.pattern}" on line: {self.line_number} index: {self.line_index}match percentage: {self.match_percentage}'
```
This file contains the result class which is the backbone of many other methods. I wanted a way to organize all the results which would be the same as each other. This class offers a neat way to organize, test, and print results using the __str__() and __repr__() methods. I use this [source](https://www.geeksforgeeks.org/print-objects-of-a-class-in-python/) to learn how to print out objects easily. I decided to add the fields what was found, the original pattern, the line_index of the first character, the line number, and the match percentage. These are the aspects of a result I determined are important for the end user, but an argument could be made to include and exclude others. 

### Key Code Aspect 2
[match_line](./src/search_module.py)
```python
def match_line(self, line: str, pattern: str, line_number: int) -> result:
  index = 0
  pattern_len = len(pattern)
  while index <= len(line) - pattern_len:
      if line[index:index + pattern_len] == pattern:
          return result(pattern, pattern, PERFECT_MATCH, line_number, index)
      index += 1
  return None
```
This code takes a pattern and finds an identical match, it iterates though the line taking a slice the size of the pattern and comparing the two. It stops when the slice that will be taken would end up being larger than length of the line minus the pattern. This could save a bit of runtime and deal with the ending of searching for the pattern.

### Key Code Aspect 3
[fuzzy_match](./src/search_module.py)
```python
def fuzzy_match(self, line: str, pattern: str, line_number: int) -> result:
  lower_line = line.casefold()
  lower_pattern = pattern.casefold()

  # filter non alphanum characters from the pattern (in case of regex)
  filtered_pattern = [char for char in lower_pattern if char.isalnum()]
  word_list: list[str] = lower_line.split()

  for word in word_list:
      score_cutoff = math.floor(len(word) / 2)
      score: int = distance(word, lower_pattern, score_cutoff=score_cutoff)
      if score <= score_cutoff:
          word_index = self.get_index_from_line(lower_line, word)
          match_percentage = self.calculate_match(word, filtered_pattern)
          if int(match_percentage[:-1]) > 50:
              return result(line[word_index:word_index + len(word)], pattern, match_percentage, 
                      line_number, word_index)
```
This is by far the most complex method I made. This code uses the distance method from the Levenshtein to calculate how similar words are. For this method I opted to split the line and use another helper method I made to get the index of the first character back. I also needed to use the .casefold() method to make a copy of the lines that is lowercase, I had to retain the original line because the result object needs to keep what was actually found and the actual pattern the user entered. Even though this should not matter much if we are fuzzy matching I wanted to keep result objects consistent. In reading the documentation for the distance method I saw that you can set a score_cutoff which will return the cutoff + 1 if it is exceeded ending the algorithm early. I decided to do this as a small optimization, I was concerned about the expense of this method but luckily the module is written in C which should help a log. The method also uses helper methods I wrote such as get index from line, and calculate match. I decided to set the score cutoff to the half of the word's length rounded down, this was one of the more difficult parts because I was not sure the exact science for how loose or strict a fuzzy finding method should be. 
### Major Challenges
Key aspects could include pieces that your struggled on and/or pieces that you are proud of and want to show off.
A major challenge for me was writing the calculate match percentage not because it was hard to quantify something like how similar two words are. I settled on averaging the percentage of characters that are present in both the pattern and match and the number of characters that were in the right order. I used a dictionary as a neater way to count the shared letters, the first word is read into the dictionary with the numbers as values, then the pattern is read in and if a matching character is found it is taken out. After that all numbers are added up to any number positive or negative is indicates a difference in characters with 0 as a perfect score. I believe this idea is close to a two pass hash table, instead of O(n^2) this algorithm can compare the two strings in roughly O(3n). The second portion of the method finds the shorter of the two and makes sure to stop before the last index, an order score is given every time a value is found to match the lesser string. This was the way I figured out how to take into account that a substring could be present anywhere in the larger string. 
[calculate_match](./src/search_module.py)
```python
def calculate_match(self, match: str, pattern: str) -> str:
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
```

## Example Runs
Explain how you documented running the project, and what we need to look for in your repository (text output from the project, small videos, links to videos on youtube of you running it, etc)

## Testing
How did you test your code? What did you do to make sure your code was correct? If you wrote unit tests, you can link to them here. If you did run tests, make sure you document them as text files, and include them in your submission. 

> _Make it easy for us to know you *ran the project* and *tested the project* before you submitted this report!_


## Missing Features / What's Next
Focus on what you didn't get to do, and what you would do if you had more time, or things you would implement in the future. 

## Final Reflection
Write at least a paragraph about your experience in this course. What did you learn? What do you need to do to learn more? Key takeaways? etc.