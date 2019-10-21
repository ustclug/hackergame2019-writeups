#!/usr/bin/python3

from time import sleep
from signal import signal, SIGINT

def random_iter(value):
    while True:
        yield value
        value *= 0x7603
        value += 0x980B
        value %= 0xFFFB

def print_flags():
    a = open('might_be_flag.txt').read()
    i = iter(random_iter(0x0000))
    l = [next(i)]
    while True:
        l = [l[-1]] + [next(i) for _ in range(0x0011)]
        s = (l[0], ''.join([a[n] for n in l]))
        print('(0x%04X) => flag{%s}' % s)
        # sleep(0.05)

if __name__ == '__main__':
    signal(SIGINT, lambda a, b: exit())
    print_flags()

