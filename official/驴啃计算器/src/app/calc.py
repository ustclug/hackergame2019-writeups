import math


allow_lists = ['sin', 'cos', 'tan',
               'asin', 'acos', 'atan',
               'sinh', 'cosh', 'tanh',
               'asinh', 'acosh', 'atanh',
               'exp', 'log', 'sqrt']


class CalculatorUnknownKey(Exception):
    pass


class Calculator:
    def __init__(self):
        self.v = 0.0
        self.logs = []

    def reset(self):
        self.v = 0.0
        self.logs = []

    def value(self):
        return self.v

    def equal(self, x):
        return abs(x - self.v) <= 1e-5

    def click(self, key):
        self.logs.append(key)
        if key in allow_lists:
            fn = getattr(math, key)
            self.v = fn(self.v)
        elif key == "ON":
            self.v = 0.0
        elif key == "x^2":
            self.v = math.pow(self.v, 2)
        elif key == "1/x":
            self.v = 1.0 / self.v
        elif key == "-x":
            self.v = -self.v
        elif key == "D2R":
            self.v = self.v * (math.pi / 180.0)
        elif key == "R2D":
            self.v = self.v * (180.0 / math.pi)
        else:
            raise CalculatorUnknownKey
        return self.v

