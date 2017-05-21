from bs4 import BeautifulSoup
import requests
import sys
import itertools


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def main():
    problem = sys.argv[1]
    r = requests.get(f'https://open.kattis.com/problems/{problem}')
    if r.status_code != 200:
        print(f"Error: Kattis request for problem '{problem}' unsuccessful with error code: {r.status_code}")
        return
    html = r.text
    soup = BeautifulSoup(html, "lxml")
    samples = soup.select('.sample pre')
    for inp, outp in pairwise(samples):
        print(inp.text.strip())
        print(outp.text.strip())


if __name__ == "__main__":
    main()

