from math import sqrt


def f(point: list | tuple) -> float:
    if len(point) != 2:
        raise Exception('Координаты точки не соответствуют x1 и x2')
    return point[0] ** 2 + 4 * point[1] ** 2 - point[0] * point[1] + point[0]


def getGradient(xk: list | tuple) -> list:
    return [
        2 * xk[0] - xk[1] + 1,
        -xk[0] + 8 * xk[1]
    ]


print(getGradient([0.66, 0.296]))
print(sqrt(2.024 ** 2 + 1.708 ** 2))
print(f([-8/15, -1/15]))