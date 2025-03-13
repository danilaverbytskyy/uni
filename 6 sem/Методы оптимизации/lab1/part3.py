PHI = 0.38196

def f(arg):
    return arg * arg - 2 * arg + 5

def gold_search(a, b, epsilon):
    y = a + PHI * (b - a)
    z = a + b - y
    fy = f(y)
    fz = f(z)

    while abs(b - a) > epsilon:
        if fy <= fz:
            b = z
            z = y
            fz = fy
            y = a + PHI * (b - a)
            fy = f(y)
        else:
            a = y
            y = z
            fy = fz
            z = a + b - y
            fz = f(z)

    x_min = (a + b) / 2
    return x_min, f(x_min)

a = -2
b = 8
epsilon = 0.2

x_min, f_min = gold_search(a, b, epsilon)

print(f"Минимум функции находится в точке x = {x_min}, f(x) = {f_min}")
