import os
import sys
import subprocess
import argparse


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
    ...


def ignore_case_search(file: str, pattern: str) -> str:
    ...


def match_search(file: str, pattern: str) -> str:
    if os.path.exists(file):
        line_count = 1
        with open(file) as user_file:
            for line in user_file:
                if (pattern in line):
                    print( 'found pattern', pattern, 'on line', line_count)
                line_count += 1
    else: 
        raise FileExistsError(f'The file you provided {file} cannot be found')


def main():
    args = parse_args()
    print(args.filename, args.verbose, args.ignore_case)
    match_search(args.filename, args.pattern, args.ignore_case)
    ...


if __name__ == "__main__":
    main()