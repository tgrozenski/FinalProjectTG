import os
import sys
import subprocess
from search_module import searcher
import argparse

ACTIONS = {'MATCH_LINE': 'match_line', 'MATCH_LINE_IGNORE_CASE': 'ignore_case_search'}

def get_args() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
                        prog='ProgramName',
                        description='What the program does',
                        epilog='Text at the bottom of help')
    parser.add_argument('-v', '--verbose',
                    action='store_true')
    parser.add_argument('-i', '--ignore_case',
                    action='store_true')
    parser.add_argument('filename')           # positional argument
    parser.add_argument('pattern')
    
    args = parser.parse_args()
    return args


def determine_action(args):
    """
    determines action based on the args passed
    """
    ...


def main():
    args = get_args()
    print("filename:", args.filename, "Verbose?", args.verbose, "ignore_case?", args.ignore_case)

    # validate user file
    if not os.path.exists(args.filename):
        raise FileExistsError(f'the file you provided {args.filename} could not be found')


    # instantiate searcher class
    my_searcher = searcher()

    # if match line is action
    my_searcher.iterate_file(args.filename, args.pattern, ACTIONS['MATCH_LINE'])

    # elif match line case insensitive

    # print(ACTIONS['match_line'].format('string_a', 'string_b'))

    found_list: list = my_searcher.get_result_list()

    for item in found_list:
        print(item.get_formatted_result())



if __name__ == "__main__":
    main()