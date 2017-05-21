import glob
import subprocess
import difflib
import colorama
from colorama import Fore, Back, Style
import requests
import os
import zipfile
import io
import sys
import itertools
from docopt import docopt

doc = """Autokattis

Usage:
    autokattis.py init [--program=<NAME>] 
    autokattis.py test [--program=<NAME>] <PROGRAM>
    autokattis.py (-h | --help)

Options:
    (-p | --problem) <NAME>       The name of the kattis problem
                                (if unspecified, uses directory name)

Subcommands:
    init                        Download samples for the given problem
    test <PROGRAM>                       Run PROGRAM on all samples
"""
SAMPLES_DIR = 'samples'


def download_samples(problem, directory=SAMPLES_DIR):
    r = requests.get(f'https://open.kattis.com/problems/{problem}/file/statement/samples.zip')
    if r.status_code != 200:
        raise IOError(f"Kattis request for problem '{problem}' unsuccessful with error code: {r.status_code}")
    file = zipfile.ZipFile(io.BytesIO(r.content))
    file.extractall(directory)


def current_dir_name():
    return os.path.basename(os.getcwd())

def c(msg, color):
    return color+msg+Style.RESET_ALL

def test(program, input_file, expected_file):
    inp = open(input_file).read()
    expected = open(expected_file).read()
    outp = run(program, inp)
    sys.stdout.write(c(input_file, Style.DIM))
    sys.stdout.write("... ")
    diff = [d for d in difflib.unified_diff(outp.split('\n'), expected.split('\n'))]
    if diff:
        print(c("Fail!", Fore.RED))
        for line in diff:
            sys.stdout.write('\t'+line)
    else:
        print(c("Success!", Fore.GREEN))


def run(program, inp):
    p = subprocess.Popen(program.split(), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outp, err = p.communicate(inp.encode('utf-8'))
    if err:
        raise ChildProcessError(err)
    return outp.decode('utf-8')


def run_tests(program, input_dir=SAMPLES_DIR):
    for inp in glob.glob(f'{input_dir}/*.in'):
        outp = inp.replace('.in', '.ans')
        test(program, inp, outp)


def samples_dir_exists():
    return os.path.isdir(SAMPLES_DIR)


def main():
    colorama.init()
    args = docopt(doc)
    print(args)
    if args['-h']:
        print(doc)
        return
    problem = args['--program'] if args['--program'] else current_dir_name()
    if args['init']:
        download_samples(problem)
    elif args['test']:
        run_tests(args['<PROGRAM>'])


if __name__ == "__main__":
    main()

