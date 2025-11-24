N = 0
k = -1


def f(arg):
    global N
    N = 2 * (k + 1)
    return arg * arg - 2 * arg + 5


epsilon = 0.1
l = 0.2
a = -2
b = 8

while b - a > l:
    k += 1
    y = (a + b - epsilon) / 2
    z = (a + b + epsilon) / 2
    if f(y) <= f(z):
        b = z
    else:
        a = y

x = (a + b) / 2
print(f"Минимум находится в точке {x} и равен {f(x)}")
print(f"k = {k}")
print(f"N = {N}")
print(f"R(N) = {1 / (2 ** (N / 2))}")
print(a, ' ', b)
