#!/usr/bin/env python3
import sympy
import signal
import random


def generate(bits):
    p = sympy.randprime(3, 2 ** bits)
    q = sympy.randprime(3, 2 ** bits)
    return p, q, p * q


def help():
    print("When the numbers are sufficiently large, no efficient,")
    print("non-quantum integer factorization algorithm is known.")
    print("An effort by several researchers, concluded in 2009, to")
    print("factor a 232-digit number (RSA-768) utilizing hundreds")
    print("of machines took two years and the researchers estimated")
    print("that a 1024-bit RSA modulus would take about a thousand")
    print("times as long.")
    print("                                            -- Wikipedia")
    print()
    print("Factoring big numbers is extremely hard.")
    print("However, I believe you can do it well.")
    print()
    print("Example:")
    print("I will send you a challenge like this:")
    bits = random.randrange(10, 1024)
    p, q, n = generate(bits)
    print("n =", n)
    print("You should send me your answer in two lines like this:")
    print("p =", p)
    print("q =", q)
    print("In this case, p and q are random primes under %s bits." % bits)
    print("[p * q = n] must be true for your answer.")
    print("p and q can be in any order.")
    print()
    print("If you can solve all my challenges up to 2048 bits,")
    print("I will give your my flag. :)")
    print()
    print("Now it's your show time!")


def readnumber():
    line = input()
    line = line.strip().strip("pq= ")
    try:
        return int(line)
    except:
        print("Invalid input!")
        exit()


def begin():
    for i in range(10, 1024, 32):
        p, q, n = generate(i)
        print("n =", n)
        input_p = readnumber()
        input_q = readnumber()
        if sorted([p, q]) != sorted([input_p, input_q]):
            print("Wrong answer!")
            exit()
        print("Good job!")
    print(open("flag").read())


if __name__ == "__main__":
    signal.alarm(60)
    print("Welcome to the Integer Factorization Competition!")
    while True:
        print()
        inp = input("[H]elp or [B]egin or [E]xit? ")
        print()
        if inp == "H":
            help()
        elif inp == "B":
            begin()
            exit()
        elif inp == "E":
            exit()
