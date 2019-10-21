#!/usr/bin/python3

import find_flag

l = 65531
s = set(range(l))
i = iter(find_flag.random_iter(0))
a = open('might_be_flag.txt').read()

for n in range(l):
    s.discard(next(i))

for n in s:
    i = iter(find_flag.random_iter(n))
    l = [next(i)] + [next(i) for _ in range(17)]
    print('(%s) => flag{%s}' % ('0x%04X' % l[0], ''.join([a[n] for n in l])))

