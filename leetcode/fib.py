# import fibo
from fibo import fib1, fib2


def foo(value):
    while True:
        value = yield value


if __name__ == "__main__":
    # f = fib(10)
    # fibo.fib1(10)
    # fib1(10)
    # # f = fibo.fib2(100)
    # f = fib2(100)
    # print(f)

    bar = foo(1)
    print(next(bar))
    print(next(bar))
    print(bar.send(2))


def fib(n):
    """print fibobacci func"""
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        print(a, end=" ")
        a, b = b, a + b
    return result
