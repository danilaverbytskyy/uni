def f(arg):
    return arg ** 2 - 2 * arg + 5


def fibonacci(n):
    if n<0:
        return
    if n==0 or n==1:
        return 1
    fib = [1, 1]
    for i in range(2, n+1):
        fib.append(fib[-2] + fib[-1])
    return fib[-1]


def calculate_N(a, b, l):
    N = 0
    right_part = abs(b - a) / l
    while fibonacci(N) < right_part:
        N += 1
    return N


def fibonacci_method(a, b):
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

    print('Числа Фибоначчи')
    for i in range(N+1):
        print(fibonacci(i), end=' ')
    print()
    print(f"{a}, {b}")
    x_min = (a + b) / 2
    print(f"Минимум находится в точке {x_min} и равен {f(x_min)}")
    print(f"k = {k}, N = {N}")
    print(f"R(N) = {1 / fibonacci(N)}")


a = -2
b = 8
fibonacci_method(a, b)
