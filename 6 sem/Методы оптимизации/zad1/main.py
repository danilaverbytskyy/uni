def func(x):
    return x ** 2 - 2 * x + 5


eps = 0.005
l = 0.01
a = -2
b = 8

N = 0
while b - a > l:
    y = (a + b - eps) / 2
    z = (a + b + eps) / 2
    f1 = func(y)
    f2 = func(z)
    if f1 <= f2:
        b = z
    else:
        a = y
    N += 1
x = (a + b) / 2
print(x, N)