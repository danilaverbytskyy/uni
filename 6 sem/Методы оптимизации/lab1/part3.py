PHI = 0.38196


def f(arg):
    return arg ** 2 - 2 * arg + 5


def golden_section(a, b):
    l = 0.5
    k = 0
    y = a + PHI * (b - a)
    z = a + b - y

    while abs(b - a) > l:
        if f(y) <= f(z):
            b = z
            z = y
            y = a + b - y
        else:
            a = y
            y = z
            z = a + b - z

        k += 1

    N = k + 1

    print(f"{a}, {b}")
    x_min = (a + b) / 2
    print(f"Минимум находится в точке {x_min} и равен {f(x_min)}")
    print(f"k = {k}, N = {N}")
    print(f"R(N) = {0.618 ** (N - 1)}")


golden_section(-2, 8)
