import sys
import os
from search_module import searcher
import argparse

MATCH_ACTION = 'match_line'
REGEX_ACTION = 'regex_expression_match'
IGNORE_CASE_ACTION = 'ignore_case_match'
FUZZY_ACTION = 'fuzzy_match'

def get_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
                        prog='TylerFinder',
                        description='Finds a pattern in a file',
                        epilog='Text at the bottom of help')
    parser.add_argument('-v', '--verbose',  # optional arguments
                    action='store_true')
    parser.add_argument('-i', '--ignore_case',
                    action='store_true')
    parser.add_argument('-e', '--regex',
                    action='store_true')
    parser.add_argument('-z', '--fuzzy',
                    action='store_true')
    parser.add_argument('-f', '--filename',
                    action='store')           
    parser.add_argument('pattern')      # positional argument
    
    return parser.parse_args()


def iterate_stdin(my_searcher, action: str, pattern: str):
    line_count = 1
    method = my_searcher.__getattribute__(action)
    for line in sys.stdin:
        found = method(line, pattern, line_count)
        if found != None:
            my_searcher.append_result_list(found)
            print("Result in this LINE:", line)
        line_count += 1


def main():
    args = get_args()
    my_searcher = searcher()

    args_count = 0
    action = MATCH_ACTION
    if args.regex == True:
        action = REGEX_ACTION
        args_count += 1
    if args.ignore_case == True:
        action = IGNORE_CASE_ACTION 
        args_count += 1
    if args.fuzzy == True:
        action = FUZZY_ACTION
        args_count += 1

    if args_count > 1:
        raise UserWarning('you cannot have more than one of the following options: regex, case insensitive')

    pattern = args.pattern

    # validate user file
    if args.filename != None and not os.path.exists(args.filename):
        raise FileExistsError(f'the file you provided {args.filename} could not be found')

    # https://stackoverflow.com/questions/3762881/how-do-i-check-if-stdin-has-some-data#:~:text=isatty(0)%20can%20not%20only,if%20there%20is%20data%20available.&text=and%20after%20that%20uses%20os,)%20%2C%20it%20still%20returns%20True.
    if not os.isatty(0):
        iterate_stdin(my_searcher, action, pattern)
    elif args.filename != None: 
        my_searcher.iterate_file(args.filename, pattern, action)
        print('iterating file with the following action', action)
    else: 
        raise UserWarning('Must provide input to search')
        
    for result in my_searcher.get_result_list():
        print(result)


if __name__ == "__main__":
    main()