#!/usr/bin/env python3
import sympy
import random

if __name__ == "__main__":
    print(
        """
       the        answer
      toli      fetheuniv
     ersea     nde     ver
    ything     the     ans
   wer tol     ife     the
  uni  ver           sean
 dev   ery         thin
gth    ean       swer
tolifetheuni    ver
seandeveryth   ing
       the     ans      wer
       tol     ifetheuniver
       sea     ndeverything"""
    )
    print()
    print(
        "Do you know The Answer to the Ultimate Question of Life, The Universe, and Everything?"
    )
    print()
    print("Give me 3 integers, x, y, and z, such that")
    print("x^3 + y^3 + z^3 = 42")
    print()
    try:
        x = int(input("x = "))
        y = int(input("y = "))
        z = int(input("z = "))
    except ValueError:
        print("Invalid input!")
        exit()
    ans = x ** 3 + y ** 3 + z ** 3
    print(f"({x}) ^ 3 + ({y}) ^ 3 + ({z}) ^ 3 = {ans}")
    if ans == 42:
        print(open("flag1").read())
    else:
        print("Sorry, you are not Deep Thought.")
        exit()

    n = sympy.randprime(3, 2 ** 256) * sympy.randprime(3, 2 ** 256)
    print()
    print(
        "Since you already know the Answer to Everything, could you give me 8 integers, a, b, c, d, i, j, k and l, such that"
    )
    print(
        f"a^3 + b^3 + c^3 + d^3 = i^2 + j^2 + k^2 + l^2 = random_prime(2^256) * random_prime(2^256) = {n}"
    )
    print()
    try:
        a = int(input("a = "))
        b = int(input("b = "))
        c = int(input("c = "))
        d = int(input("d = "))
        i = int(input("i = "))
        j = int(input("j = "))
        k = int(input("k = "))
        l = int(input("l = "))
    except ValueError:
        print("Invalid input!")
        exit()
    print()
    if a ** 3 + b ** 3 + c ** 3 + d ** 3 == i ** 2 + j ** 2 + k ** 2 + l ** 2 == n:
        print(open("flag2").read())
    else:
        print("No, you don't know the answer to EVERYTHING.")
        exit()

    n = random.randint(0, 2 ** 256)
    print()
    print(
        "The last question is beyond Everything, but still you can try to solve it, by giving me 2 integers, p and q, such that"
    )
    print(f"p^2 + q^2 = randint(2^256) = {n}")
    try:
        p = int(input("p = "))
        q = int(input("q = "))
    except ValueError:
        print("Invalid input!")
        exit()
    print()
    if p ** 2 + q ** 2 == n:
        print(open("flag3").read())
    else:
        print("Nope, maybe Everything is Nothing.")
