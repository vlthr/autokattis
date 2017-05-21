from bs4 import BeautifulSoup
import requests
import sys
import itertools


def grouper(iterable, n, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)


def main():
    problem = sys.argv[1]
    r = requests.get(f'https://open.kattis.com/problems/{problem}')
    if r.status_code != 200:
        print(f"Error: Kattis request for problem '{problem}' unsuccessful with error code: {r.status_code}")
        return
    html = r.text
    soup = BeautifulSoup(html, "lxml")
    samples = soup.select('.sample pre')
    for inp, outp in grouper(samples, 2):
        print(inp.text.strip())
        print(outp.text.strip())


if __name__ == "__main__":
    main()

