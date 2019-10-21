#!/usr/bin/env python3

import ast
import signal
import traceback
from copy import deepcopy

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
END = "\033[0m"


def timeout(*args, **kwargs):
    print("Timeout!")
    exit(-1)


class Challenges:
    def __init__(self):
        signal.signal(signal.SIGALRM, timeout)
        self.challenges = {}
        self.cleared = {}
        for method in dir(self):
            if method.startswith("challenge_"):
                n = int(method.split("_")[-1])
                self.challenges[n] = getattr(self, method)
                self.cleared[n] = False

    def do_challenge(self, n):
        while True:
            inp = input("Your answer: ")
            if len(inp) > 100:
                print("Input too long")
                continue
            try:
                answer = ast.literal_eval(inp)
                break
            except Exception:
                print("Invalid input!")
                continue

        signal.alarm(1)
        print(YELLOW, end="")
        try:
            if self.challenges[n](answer):
                print(f"Challenge {n:02d} cleared!")
                self.cleared[n] = True
            else:
                print(f"Challenge {n:02d} failed!")
        except Exception:
            print(traceback.format_exc(), end="")
        print(END, end="")
        signal.alarm(0)

    def show_status(self):
        print()
        print("------ Do you know Python? ------")
        for i, (challenge, cleared) in enumerate(sorted(self.cleared.items())):
            color = GREEN if cleared else RED
            text = "Y" if cleared else "N"
            print(color + f"{challenge:02d}: {text}" + END, end="  ")
            if i % 5 == 4:
                print()
        print()

    def cleared_count(self):
        return sum(self.cleared.values())

    def total_count(self):
        return len(self.challenges)

    def challenge_1(self, answer):
        if answer == "Hello":
            return True

    def challenge_2(self, answer):
        a, b, c, d = answer
        if a == b and a is b and c == d and c is not d:
            return True

    def challenge_3(self, answer):
        if answer in answer == answer:
            return True

    def challenge_4(self, answer):
        a1, b1 = answer
        a2, b2 = answer
        if a1 * 2 != a1 and b1 * 2 != b1:
            a1 *= 2
            b1 *= 2
            if a1 == a2 and b1 != b2:
                return True

    def challenge_5(self, answer):
        r = reversed([1, 2, 3])
        if list(r) == list(r) + answer:
            return True

    def challenge_6(self, answer):
        a, b = answer
        if max(a, b) != max(b, a):
            return True

    def challenge_7(self, answer):
        a, b, c = answer
        for x in a, b, c:
            if isinstance(x, float) or isinstance(x, complex):
                return False
        if a * (b + c) != a * b + a * c:
            return True

    def challenge_8(self, answer):
        a, b, c = answer
        for x in a, b, c:
            if isinstance(x, float) or isinstance(x, complex):
                return False
        if a * (b * c) != (a * b) * c:
            return True

    def challenge_9(self, answer):
        a, b = answer
        for x in a, b:
            if isinstance(x, float) or isinstance(x, complex):
                return False
        if type(a ** b) != type(b ** a):
            return True

    def challenge_10(self, answer):
        a, b = answer
        if a and a.count(b) > len(a):
            return True

    def challenge_11(self, answer):
        if max(answer) != max(*answer):
            return True

    def challenge_12(self, answer):
        a, b = answer
        if a < b and all(x > y for x, y in zip(a, b)):
            return True

    def challenge_13(self, answer):
        a, b = answer
        if b and not (a ^ b) - a:
            return True

    def challenge_14(self, answer):
        backup = deepcopy(answer)
        try:
            answer[0] += answer[1]
        except:
            if backup != answer:
                return True

    def challenge_15(self, answer):
        item, l = answer
        if item in l and not min(l) <= item <= max(l):
            return True

    def challenge_16(self, answer):
        item, l = answer
        if item == 233 and item in l and l in l:
            return True

    def challenge_17(self, answer):
        item, l = answer
        if l[0] == item and item not in l:
            return True

    def challenge_18(self, answer):
        a, b = answer
        if (a - b) != -(b - a):
            return True

    def challenge_19(self, answer):
        if answer.isdecimal():
            if len(answer) < 5:
                if sum(ord(c) - ord("0") for c in answer) == 23333:
                    return True

    def challenge_20(self, answer):
        if len(set(str(x) for x in answer)) == 7 and all(x == 0 for x in answer):
            return True


if __name__ == "__main__":
    c = Challenges()
    while True:
        c.show_status()
        inp = input("Which one do you want to play? ")
        try:
            n = int(inp)
        except ValueError:
            print("Invalid input!")
            continue
        if n not in c.challenges:
            print("Challenge not found!")
            continue
        c.do_challenge(n)
        print(f"Your progress: {c.cleared_count()}/{c.total_count()}")
        if c.cleared_count() == c.total_count():
            print("You are the master of Python.")
            print("Here is the final flag:")
            print(open("flag3").read().strip())
            break
        elif c.cleared_count() >= c.total_count() * 3 // 4:
            print(open("flag2").read().strip())
        elif c.cleared_count() >= c.total_count() // 2:
            print(open("flag1").read().strip())
        else:
            print("Go on to get your flags!")
