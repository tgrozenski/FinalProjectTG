import os

# This file is to automate testing because I am tired of writing out shell commands
CMD_LINE_TEMPLATE = 'python3 src/main.py {arg} -f ./testing/data/{input_file} {pattern} >> ./testing/data/out.txt'

def test_file(arg, input_file, pattern_list: list[str]):
    os.system(f"echo '***BEGINNING OF TESTING FOR {input_file}***' >> ./testing/data/out.txt")
    for pattern in pattern_list:
        os.system(CMD_LINE_TEMPLATE.format(arg=arg, input_file=input_file, pattern=pattern))
    os.system(f"echo '***END OF TESTING FOR {input_file}***' >> ./testing/data/out.txt")

def main_test():

    # delete anything from before in out.txt
    os.system('echo '' > ./testing/data/out.txt')

    test_file('', 'test_match_case.txt', ["'ice cream'", "'cookies'", "'PATTERN123'"])
    test_file('-i', 'test_ignore_case.txt', ["'cookie'", "'IcE CrEaM'", "'TEA'"])
    test_file('-e', 'test_regex.txt', ["'CATS ... dogs'", "'[n|N]inja [t|T]..t..s'", "'.....BLASTOFF'"])
    test_file('-z', 'test_fuzzy.txt', ["'coagulation'", "'explicative'", "'california'"])
    print('THE RESULT OF RUNNING diff ./testing/data/out.txt ./testing/data/expected_out.txt BELOW')
    os.system('diff ./testing/data/out.txt ./testing/data/expected_out.txt')

if __name__ == "__main__":
    main_test()