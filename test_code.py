import math
import os


def big_function(a, b, c, d, e, f):
    x = a + b
    y = c + d
    z = e + f

    print("debug1")
    print("debug2")
    print("debug3")
    print("debug4")
    print("debug5")
    print("debug6")

    for i in range(5):
        print(i)

    for j in range(5):
        print(j)

    for k in range(5):
        print(k)

    for m in range(5):
        print(m)

    for n in range(5):
        print(n)

    for p in range(5):
        print(p)

    for q in range(5):
        print(q)

    return x + y + z


class TestClass:

    def method1(self):
        a = 10
        b = 20
        c = a + b
        return c


def unused_var_function():
    x = 10
    y = 20
    z = 30
    return x
