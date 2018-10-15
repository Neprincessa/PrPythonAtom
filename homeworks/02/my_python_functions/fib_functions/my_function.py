from math import sqrt

def cache_decorator(func):
    memory = {}

    def cashFunc(argument):
        if argument in memory:
            return memory[argument]
        else:
            memory[argument] = func(argument)
            return memory[argument]

    return cashFunc

@cache_decorator
def fib(n):
     if n == 0 or n == 1:
        return 1
     else:
        return fib(n-1)+fib(n-2)

