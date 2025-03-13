def f(arg):
    return arg * arg - 2 * arg + 5


epsilon = 0.005
l = 0.02
a = -2
b = 8

while b - a > l:
    y = (a + b - epsilon) / 2
    z = (a + b + epsilon) / 2
    if f(y) <= f(z):
        b = z
    else:
        a = y

x = (a + b) / 2
print(f"Минимум находится в точке {x} и равен {f(x)}")
