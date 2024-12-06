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
Users should begin by running the program with the help argument to see the command line argument order to get a helpful usage message from the argparser module.  
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

### Example Usage 1
```bash
python3 src/main.py -f requirements.txt levenshtein
```
This is a default usage that provides only a filename to be searched, the program defaults to a case_sensitive perfect match.

### Example Usage 2
```bash
history | python3 src/main.py -f GREEP
```
This will search the output of the history command to find a fuzzy match (if any exist) to GREEP.

### Example Usage 3
```bash
python3 src/main.py -e '[hey|hi|hello] world'
```
patterns containing a regular expression and/or spaces should be put in single quotes to prevent errors. 

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

### [Aspect 1](./src/result_module.py)
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
This file contains the result class which is the backbone of how results data are stored and represented. I wanted a way to create a standard for results since there would be many of them, all of which would be very similar. This class offers a neat way to organize, test, and print results using the __str__() and __repr__() methods. I use this [source](https://www.geeksforgeeks.org/print-objects-of-a-class-in-python/) to learn how to print out objects easily. I decided to add the following fields: what was found, the original pattern, the line_index of the first character, the line number, and the match percentage. These are the aspects of a result I determined are important for the end user, but an argument could be made to include and exclude others. 

### [Aspect 2](./src/search_module.py)
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
This code takes a pattern and finds an identical match, it iterates though the line taking a slice the size of the pattern and comparing the slice with the pattern. It stops when the slice that will be taken would end up being larger than length of the line minus the pattern. This could save a bit of runtime and deal with the ending of searching for the pattern it also preserves the index to be added to the result object.

### [Aspect 3](./src/search_module.py)
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
I was also proud of this solution which uses the concept of a functional pointer to let me use this one method to use all the various different search methods. I think it was a neat way to reduce code duplication. 
```python
def iterate_file(self, file: str, pattern: str, action: str) -> None:
    line_count = 1
    # https://stackoverflow.com/questions/2283210/python-function-pointer
    selected_method = self.__getattribute__(action)
    with open(file) as user_file:
        for line in user_file:
            found = selected_method(line.strip(), pattern, line_count)
            if found != None:
                result_list.append(found)
            line_count += 1
```

## Example Runs
Explain how you documented running the project, and what we need to look for in your repository (text output from the project, small videos, links to videos on youtube of you running it, etc)
I ran the following command to 

## Testing
How did you test your code? What did you do to make sure your code was correct? If you wrote unit tests, you can link to them here. If you did run tests, make sure you document them as text files, and include them in your submission. 

> _Make it easy for us to know you *ran the project* and *tested the project* before you submitted this report!_

I used unit tests to test all of the individual search components in [test_search.py](./testing/test_search.py). I also wrote doc tests but they are just for someone reading the code trying to understand it, I prefer using a unit test class. I wrote this file because it was important to make sure that all the search pieces were working flawlessly before using them on a larger scale. Being able to unit test each individual method made brought the complexity down a lot. For reading files and finding patterns I decided to write a text file with patterns hidden for each of the search options like this example for the [fuzzy search](./testing/data/test_fuzzy.txt). I then use redirection to append the output with `>>` to [out.txt](./testing/data/out.txt). I can then run diff against that file with the expected file. This maybe isn't the best approach because it requires everything to be in the same order, but it was the best I could come up with. 


## Missing Features / What's Next
I really wanted to get the feature of searching a directory recursively, which is my favorite grep feature. Unfortunately, it was a very complex feature and my algorithm and unix chops are just not there at this point. I look forward to taking the classes I will next semester because I think I should be able to do this by then. I also had the challenge when it comes to what to do with results when they are found. I chose to keep all functions pure in the search class, but I think maybe it would have been right to keep some sort of global list. I avoided that because I thought it would be a pain to test. Because of this choice the program will only return the first instance of a pattern found on a line. I think that this is mostly ok because the point is mostly to point users to the line, I wasn't able to implement a feature like grep where the line is displayed with the pattern in a different color. 

## Final Reflection
Write at least a paragraph about your experience in this course. What did you learn? What do you need to do to learn more? Key takeaways? etc.

I learned a lot over these past few months, I was already programming quite a lot going into this so not everything was entirely new information to me. The class' focus on computational thinking was something that was very valuable to me because it really summed up what I have been learning it means to program. I learned a lot of python and I enjoyed working on all the projects. The most valuable thing I learned by far was the idea of testing driven development. I learned how to write a docstring before a function that will make my code understandable to those who attempt to read it. The idea of pure and impure functions was another valuable, I know now that it is best practice to keep functions as pure as we can to limit side effects and make testing easier. I also had a very rudimentary understanding of absolute and relative paths, this class clarified a lot of confusion I had about that. I think that the greatest area I have to grow in is in algorithms and data structures, I have a solid entry level grasp of object oriented programming. I am really looking forward to what I will get the chance to learn next semester and feel prepared for the challenge. 
