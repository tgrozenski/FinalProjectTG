import os
import sys
import subprocess
from search_module import searcher
import argparse

ACTIONS = {'match_line': 'self.match_line("{}","{}")'}

def parse_args() -> argparse.ArgumentParser:
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


def validate_file(file: str) -> bool:
    if os.path.exists(file):
        return True
    else: 
        return False


def main():
    args = parse_args()
    print("filename:", args.filename, "Verbose?", args.verbose, "ignore_case?", args.ignore_case)

    # validate user file
    if not validate_file(args.filename):
        raise FileExistsError(f'the file you provided {args.filename} could not be found')


    # instantiate searcher class
    my_searcher = searcher()
    my_searcher.iterate_file(args.filename, args.pattern, ACTIONS['match_line'])
    # print(ACTIONS['match_line'].format('string_a', 'string_b'))

    found_list: list = my_searcher.get_result_list()

    for item in found_list:
        print(item.get_formatted_result())



if __name__ == "__main__":
    main()