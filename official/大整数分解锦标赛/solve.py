#!/usr/bin/env python3


class UncertainBit:
    def __init__(self, value):
        if value == 0 or value == 1 or value == None:
            self.value = value
        elif value == "0" or value == "1":
            self.value = int(value)
        elif value == "X":
            self.value = None
        elif isinstance(value, UncertainBit):
            self.value = value.value
        else:
            raise TypeError()

    def __and__(self, other):
        if self.value != None and other.value != None:
            return UncertainBit(self.value & other.value)
        if self.value == 0 or other.value == 0:
            return UncertainBit(0)
        return UncertainBit(None)

    def __or__(self, other):
        if self.value != None and other.value != None:
            return UncertainBit(self.value | other.value)
        if self.value == 1 or other.value == 1:
            return UncertainBit(1)
        return UncertainBit(None)

    def __xor__(self, other):
        if self.value != None and other.value != None:
            return UncertainBit(self.value ^ other.value)
        return UncertainBit(None)

    def __invert__(self):
        if self.value is None:
            return UncertainBit(None)
        else:
            return UncertainBit(1 - self.value)

    def __repr__(self):
        if self.value is None:
            return "X"
        else:
            return str(self.value)

    def combine(self, other):
        if self.value != None and other.value != None:
            if self.value != other.value:
                raise ValueError()
        if self.value != None:
            return UncertainBit(self.value)
        return UncertainBit(other.value)

    def repeat(self, n):
        return UncertainBitVector(n, [self for _ in range(n)])


class UncertainBitVector:
    def __init__(self, bits, value=None):
        self.bits = bits
        self.vec = [UncertainBit(0) for _ in range(len(self))]
        if value is None:
            for i in range(len(self)):
                self[i] = None
        elif isinstance(value, int):
            if value.bit_length() > len(self):
                raise ValueError()
            for i in range(value.bit_length()):
                self[i] = (value >> i) & 1
        else:
            if len(value) > len(self):
                raise ValueError()
            for i in range(len(value)):
                self[i] = value[i]

    def __len__(self):
        return self.bits

    def __getitem__(self, key):
        if isinstance(key, int):
            if key >= len(self):
                return UncertainBit(0)
            return self.vec[key]
        elif isinstance(key, slice):
            bv = self.vec[key]
            return UncertainBitVector(len(bv), bv)
        else:
            raise TypeError()

    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.vec[key] = UncertainBit(value)
        elif isinstance(key, slice):
            raise NotImplementedError()
        else:
            raise TypeError()

    def __and__(self, other):
        if isinstance(other, int):
            other = UncertainBitVector(other.bit_length(), other)
        bits = min(len(self), len(other))
        return UncertainBitVector(bits, [self[i] & other[i] for i in range(bits)])

    def __rand__(self, other):
        return self & other

    def __or__(self, other):
        if isinstance(other, int):
            other = UncertainBitVector(other.bit_length(), other)
        bits = max(len(self), len(other))
        return UncertainBitVector(bits, [self[i] | other[i] for i in range(bits)])

    def __ror__(self, other):
        return self & other

    def __xor__(self, other):
        if isinstance(other, int):
            other = UncertainBitVector(other.bit_length(), other)
        bits = max(len(self), len(other))
        return UncertainBitVector(bits, [self[i] ^ other[i] for i in range(bits)])

    def __rxor__(self, other):
        return self & other

    def __lshift__(self, other):
        bits = len(self) + other
        return UncertainBitVector(bits, [0] * other + self.vec)

    def __rshift__(self, other):
        bits = max(len(self) - other, 0)
        return UncertainBitVector(bits, self.vec[other:])

    def __sub__(self, other):
        if isinstance(other, int):
            other = UncertainBitVector(other.bit_length(), other)
        r = []
        carry = UncertainBit(0)
        for i in range(len(self)):
            r.append(self[i] ^ other[i] ^ carry)
            carry = ~((self[i] & ~other[i]) | (self[i] & ~carry) | (~other[i] & ~carry))
        if carry.value != 0:
            raise OverflowError()
        return UncertainBitVector(len(self), r)

    def __repr__(self):
        return "".join([str(b) for b in reversed(self.vec)])

    def sign_ext(self, bits):
        if bits < len(self):
            raise ValueError()
        return UncertainBitVector(bits, self.vec + [self[-1]] * (bits - len(self)))

    def combine(self, other):
        if len(self) != len(other):
            raise ValueError()
        else:
            return UncertainBitVector(
                len(self), [self[i].combine(other[i]) for i in range(len(self))]
            )

    def all_known(self):
        return all(self[i].value is not None for i in range(len(self)))

    def int_value(self):
        if not self.all_known():
            raise ValueError()
        v = 0
        for i in range(len(self)):
            v |= self[i].value << i
        return v


class MTSolver:
    N = 624

    def __init__(self):
        self.length = self.N * 6
        self.mt = [UncertainBitVector(32) for _ in range(self.length)]
        self.pos = 0

    def known_raw(self, pos, value):
        self.mt[pos] = self.mt[pos].combine(value)

    def known_32bit(self, value):
        if len(value) != 32:
            raise ValueError()
        self.known_raw(self.pos, self.untempering(value))
        self.pos += 1

    def known_prime(self, begin, end, p):
        self.known_range(begin - 1, end + 1, self.prime_to_bv(p))

    def known_range(self, begin, end, n):
        bits = (end - begin).bit_length()
        try:
            rnd = UncertainBitVector(bits, n - begin)
        except OverflowError:
            rnd = UncertainBit("X").repeat(bits)
        for i in range(bits // 32):
            self.known_32bit(rnd[i * 32 : i * 32 + 32])
        extra = bits % 32
        if extra:
            bv = UncertainBitVector(
                32,
                (rnd[bits // 32 * 32 :] << (32 - extra))
                ^ UncertainBit("X").repeat(32 - extra),
            )
            self.known_32bit(bv)

    def untempering(self, y):
        y ^= y >> 18
        y ^= (y << 15) & 0xEFC60000
        y ^= (
            ((y << 7) & 0x9D2C5680)
            ^ ((y << 14) & 0x94284000)
            ^ ((y << 21) & 0x14200000)
            ^ ((y << 28) & 0x10000000)
        )
        y ^= (y >> 11) ^ (y >> 22)
        return y

    def generate(self, i):
        y = (self.mt[i - self.N] & 0x80000000) | (self.mt[i - self.N + 1] & 0x7FFFFFFF)
        return (
            self.mt[i + 397 - self.N] ^ (y >> 1) ^ (0x9908B0DF & (y & 1).sign_ext(32))
        )

    def do_predit(self):
        for i in range(self.N, self.pos - 397 + self.N):
            self.known_raw(i, self.generate(i))

    def prime_to_bv(self, p):
        import sympy

        pp = sympy.prevprime(p)
        end = p - 1
        start = pp
        bv = UncertainBitVector(p.bit_length(), start)
        bv = bv ^ UncertainBit("X").repeat((start ^ end).bit_length())
        return bv

    def __str__(self):
        s = []
        for i, bv in enumerate(self.mt):
            s.append("%s: %s %s" % (i, bv, "<<X>>" if "X" in str(bv) else ""))
        return "\n".join(s)

    def get_mt_window(self):
        return self.mt[max(self.pos - self.N, 0) : self.pos]

    def ready(self):
        return self.pos >= self.N and all(bv.all_known() for bv in self.get_mt_window())

    def get_progress(self):
        return sum(int(bv.all_known()) for bv in self.get_mt_window())

    def get_random(self):
        if not self.ready():
            raise ValueError()
        import random

        rnd = random.Random()
        rnd.setstate(
            (3, tuple(bv.int_value() for bv in self.get_mt_window()) + (self.N,), None)
        )
        return rnd


if __name__ == "__main__":
    from pwn import * # pip3 install --upgrade git+https://github.com/arthaud/python3-pwntools.git
    import random
    import sympy

    # context.log_level = 'debug'

    r = remote("127.0.0.1", 10010)
    r.sendline("your token")
    r.recvuntil("Welcome")
    s = MTSolver()
    for i in range(10):
        for j in range(10):
            r.sendline("H")
        for j in range(10):
            print(i * 10 + j)
            r.recvuntil("p = ")
            p = int(r.recvline().strip())
            r.recvuntil("q = ")
            q = int(r.recvline().strip())
            r.recvuntil("under ")
            b = int(r.recvline().split(b" ")[0])

            s.known_range(10, 1024, b)
            bound = 2 ** b
            s.known_prime(3, bound, p)
            s.known_prime(3, bound, q)
        s.do_predit()
        print(s.get_progress(), "/ 624")
        if s.ready():
            break
    random.setstate(s.get_random().getstate())

    r.sendline("B")
    for i in range(10, 1024, 32):
        print(i)
        p = sympy.randprime(3, 2 ** i)
        q = sympy.randprime(3, 2 ** i)
        r.sendline("p = " + str(p))
        r.sendline("q = " + str(q))
    r.interactive()
