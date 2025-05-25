def f(x1, x2):
    return x1 ** 2 + 4 * x2 ** 2 - x1 * x2 + x1


def p(x1, x2, rk):
    return rk / 2 * ((2 * x1 + x2 - 1) ** 2)


def x1(rk):
    return (-16+36*rk)/(30+76*rk)


def x2(rk):
    return (-94+68*rk)/((30+76*rk)*17)


rk = 1000
x1 = x1(rk)
x2 = x2(rk)
print(f'x1 = {x1}')
print(f'x2 = {x2}')
print(f'p = {p(x1, x2, rk)}')
