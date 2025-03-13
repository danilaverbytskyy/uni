def f(arg):
    return arg * arg - 2 * arg + 5

def fibonacci_method(a, b, epsilon):
    def get_fib(n):
        fib = [1, 1]
        while fib[-1] < n:
            fib.append(fib[-1] + fib[-2])
        return fib

    n = (b - a) / epsilon
    fib = get_fib(n)
    k = len(fib) - 1

    for i in range(1, k):
        y = a + (fib[k - i - 1] / fib[k - i + 1]) * (b - a)
        z = a + (fib[k - i] / fib[k - i + 1]) * (b - a)

        if f(y) < f(z):
            b = z
        else:
            a = y
    x = (a + b) / 2
    return x, f(x)

a = -2
b = 8
epsilon = 0.2

x_min, f_min = fibonacci_method(a, b, epsilon)
print(f"Минимум находится в точке {x_min}, f(x) = {f_min}")