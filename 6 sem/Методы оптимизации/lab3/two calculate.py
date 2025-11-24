lam = -0.937186
rk = 100

def f(x1, x2):
    return x1 ** 2 + 4 * x2 ** 2 - x1 * x2 + x1


def p(x1, x2, rk):
    return lam*(2 * x1 + x2 - 1) + rk / 2 * ((2 * x1 + x2 - 1) ** 2)


def x1(rk):
    return (-18+36*rk-34*lam)/(30+76*rk)


def x2(rk):
    return (4*rk - 6 - 8 * lam)/(30+76*rk)


x1 = x1(rk)
x2 = x2(rk)
print(f'x1 = {x1}')
print(f'x2 = {x2}')
print(f'p = {p(x1, x2, rk)}')
print(lam+rk*(2*x1+x2-1))