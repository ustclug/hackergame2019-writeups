#!/usr/bin/env python3

import signal
import re


def flag(*args, **kwargs):
    print(open("flag").read())
    exit()


def main():
    print("Welcome to the free online Regular Expression Verifier")
    print("Please enter your RegEx and string and I will match them for you\n")

    r = input("RegEx: ")
    if len(r) > 6:
        print("Sorry your regex is too long.")
        exit()
    s = input("String: ")
    if len(s) > 24:
        print("Sorry your string is too long.")
        exit()

    r = re.compile(r)
    signal.signal(signal.SIGALRM, flag)
    signal.alarm(1)
    m = r.search(s)
    signal.alarm(0)
    if m:
        print("Your regex matches the string!")
    else:
        print("Your regex doesn't match the string!")


if __name__ == "__main__":
    signal.alarm(30)
    main()
