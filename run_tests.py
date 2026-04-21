#! /usr/bin/env python3

import filecmp
import json
import sys
import os
import argparse
import subprocess
from  subprocess import TimeoutExpired
from  subprocess import CalledProcessError

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

TIMEOUT = 10
MAX_INSTRUCTIONS = 50000000
AE_CODE = 127
SE_CODE = 126

# all files except main entry point
SOURCES = [
    "src/iban2knr.s",
    "src/knr2iban.s",
    "src/moduloStr.s",
    "src/util.s",
    "src/validateChecksum.s",
]

RULE = 60 * "="


def find_tests(dir):
    tests = []
    for t in os.listdir(dir):
        if t.endswith('.s'):
            tests.append(os.path.join(dir, t.replace('.s', '')))
    tests.sort()
    return tests

def run_test(test, timeout):
    asmfile = test + ".s"
    reffile = test + ".ref"

    if not os.path.isfile(asmfile):
        return False, f"Test file missing for test {test}! Expected {asmfile}"

    if not os.path.isfile(reffile):
        return False, f"Reference file missing for test {test}!"

    try:
        # subprocess.run(["java", "-jar", "mars.jar", f"ae{AE_CODE}", f"se{SE_CODE}", "me", "nc", "sm", str(MAX_INSTRUCTIONS), *SOURCES, test + ".s"],
        #     stdout=stdout_file,  stderr=stderr_file, timeout=timeout, check=True)
        stdout_file = open("stdout.log", 'w+')
        stderr_file = open("stderr.log", 'w+')
        args = ["java", "-jar", "venus-61c.dev.jar", test + ".s"]
        # if test.endswith("_cc"):
        args.extend(["-cc", "--retToAllA"])
        subprocess.run(args,
            stdout=stdout_file,  stderr=stderr_file, timeout=timeout, check=True)

        a = open(reffile).read()
        b = open("stdout.log").read()

        if a.strip() == b.strip():
            print(f"{colors.BOLD}{colors.OKGREEN}PASSED{colors.ENDC}")
            return True, "Test passed."
        else:
            print(f"{colors.BOLD}{colors.FAIL}FAILED{colors.ENDC}")
            return False, f"{RULE}\n{colors.BOLD}Expected output:{colors.ENDC}\n{a}\n{RULE}\n{colors.BOLD}Actual output was:{colors.ENDC}\n{b}\n{RULE}"

    except TimeoutExpired:
        print(f"{colors.BOLD}{colors.WARNING}TIMEOUT{colors.ENDC}")
        return False, f"Timeout of {TIMEOUT} seconds was exceeded.\n"

    except CalledProcessError as error:
        print(f"{colors.BOLD}{colors.FAIL}ERROR{colors.ENDC}")
        stdout_file.seek(0)
        stderr_file.seek(0)

        if error.returncode == SE_CODE:
            return False, f"error: runtime failure, error message was: \n{stderr_file.read()}"

        if error.returncode == AE_CODE:
            return False, f"error: assembler failed, error message was: \n{stderr_file.read()}"

        return False, f"error: venus terminated with value {error.returncode}, error message was: \n{error.stderr}"
    finally:
        stdout_file.close()
        stderr_file.close()
        os.remove("stdout.log")
        os.remove("stderr.log")


parser = argparse.ArgumentParser()
parser.add_argument('-l', '--list', action='store_true', help='list all available tests')
parser.add_argument('-t', '--tests', nargs='+', help='execute only the specified tests')
parser.add_argument('-nc', '--nocolor', action='store_true', help='do not use colored output')
parser.add_argument('-d', '--dirs', default=['pub'], nargs='+', help='test directories')
# parser.add_argument('-b', '--bonus', action='store_true', help='run tests with bonus file')

args = parser.parse_args()

num_tests = 0
num_passed = 0

if args.nocolor:
    colors.HEADER = ''
    colors.OKBLUE = ''
    colors.OKCYAN = ''
    colors.OKGREEN = ''
    colors.WARNING = ''
    colors.FAIL = ''
    colors.ENDC = ''
    colors.BOLD = ''
    colors.UNDERLINE = ''
    
# if args.bonus:
#     print("Running tests with bonus file.\nThis only tests whether the bonus file is correct. Not whether all restrictions are met.")
#     for i, s in enumerate(SOURCES):
#         bonus_path = s.replace('src/', 'src/bonus/')
#         if os.path.isfile(bonus_path):
#             SOURCES[i] = bonus_path

testdirs = [os.path.join("tests", d) for d in args.dirs]

if args.tests:
    if not len(testdirs) == 1:
        print("You must specify a single test directory when running a single test!")
        sys.exit(1)

    tests = [os.path.join(testdirs[0], t) for t in args.tests]
else:
    tests = [t for d in testdirs for t in find_tests(d)]

for test in tests:
    if args.list:
        print(test.split(os.path.sep)[-1])
        continue

    print(colors.HEADER, colors.BOLD, "Running ", test.split(os.path.sep)[-1], "...", colors.ENDC, sep='')
    num_tests += 1

    try:
        result, message = run_test(test, timeout=TIMEOUT)

        if result:
            num_passed += 1
        else:
            print(message)
    except KeyboardInterrupt:
        print("Keyboard interrupt. Aborting test execution...")
        sys.exit(1)
    except Exception as e:
        print(f'Unexpected error while invoking the test:\n{e}')

    print()

if not args.list:
    print(RULE)
    print(f"===> Passed {num_passed} out of {num_tests} tests.")


if num_tests == num_passed:
    sys.exit(0)
else:
    sys.exit(1)
