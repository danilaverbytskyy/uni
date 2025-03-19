def get_fib(n):
    fib = [1, 1]
    while fib[-1] < n:
        fib.append(fib[-1] + fib[-2])
    return fib

def calculate_N(a, b, epsilon):
    right_part = abs(b - a) / epsilon
    N = 0
    while get_fib(N)[-1]<right_part:
        N+=1
    return len(get_fib(N)) - 1

a = -2
b = 8
epsilon = 0.2
N = calculate_N(a, b, epsilon)
print(N)

def f(arg):
    return arg * arg - 2 * arg + 5


def fibonacci_method(a, b, epsilon):
    n = (b - a) / epsilon
    fib = get_fib(n)
    k = 0

    while k != N - 3:
        y = a + (fib[N - 2] / fib[N]) * (b - a)
        z = a + (fib[N-1] / fib[N]) * (b - a)

        if f(y) < f(z):
            b = z
        else:
            a = y
        k+=1
    x = (a + b) / 2
    return x, f(x)


x_min, f_min = fibonacci_method(a, b, epsilon)
print(f"Минимум находится в точке {x_min}, f(x) = {f_min}")
