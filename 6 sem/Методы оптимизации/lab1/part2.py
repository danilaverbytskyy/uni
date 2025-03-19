def f(arg):
    return arg ** 2 - 2 * arg + 5


def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def calculate_N(a, b, l):
    N = 0
    while True:
        fib = fibonacci(N)
        if fib >= abs(b - a) / l:
            return N
        N += 1


def fibonacci_search(a, b):
    eps = 0.2
    l = 0.5

    N = calculate_N(a, b, l)

    k = 0

    y = a + (fibonacci(N - 2) / fibonacci(N)) * (b - a)
    z = a + (fibonacci(N - 1) / fibonacci(N)) * (b - a)

    fy = f(y)
    fz = f(z)

    while k < N - 3:
        if fy <= fz:
            b = z
            z = y
            y = a + (fibonacci(N - k - 3) / fibonacci(N - k - 1)) * (b - a)
            fz = fy
            fy = f(y)
        else:
            a = y
            y = z
            z = a + (fibonacci(N - k - 2) / fibonacci(N - 1 - k)) * (b - a)
            fy = fz
            fz = f(z)
        k += 1

    y = (a + b) / 2
    z = y + eps

    if f(y) <= f(z):
        b = z
    else:
        a = y

    print(f"{a}, {b}")
    x_min = (a + b) / 2
    print(f"Минимум находится в точке {x_min} и равен {f(x_min)}")
    print(f"k = {k}, N = {N}")
    print(f"R(N) = {1 / fibonacci(N)}")


fibonacci_search(-2, 8)
