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


def getH() -> list[list]:
    return [
        [2, -1],
        [-1, 8]
    ]


def getInverseH() -> list[list]:
    a, b = 2, -1
    c, d = -1, 8
    det = a * d - b * c
    return [
        [d / det, -b / det],
        [-c / det, a / det]
    ]


def getNorma(vector: list) -> float:
    return sqrt(sum(x ** 2 for x in vector))


def matrix_vector_mult(matrix: list[list], vector: list) -> list:
    return [
        sum(m * v for m, v in zip(row, vector))
        for row in matrix
    ]


def vector_sub(v1: list, v2: list) -> list:
    return [x - y for x, y in zip(v1, v2)]


def vector_add(v1: list, v2: list) -> list:
    return [x + y for x, y in zip(v1, v2)]


def scalar_mult(scalar: float, vector: list) -> list:
    return [scalar * x for x in vector]



eps1 = 0.1
eps2 = 0.15
M = 10
xk = [3, 1]
k = 0

while True:
    # Шаг 3
    grad = getGradient(xk)

    # Шаг 4
    if getNorma(grad) <= eps1:
        print(f'Расчет окончен: норма градиента {getNorma(grad):.4f} <= {eps1}')
        print(f'x* = {xk}, f(x*) = {f(xk):.4f}')
        break

    # Шаг 5
    if k >= M:
        print(f'Расчет окончен: достигнуто максимальное число итераций {M}')
        print(f'x* = {xk}, f(x*) = {f(xk):.4f}')
        break

    H_inv = getInverseH()

    dk = scalar_mult(-1, matrix_vector_mult(H_inv, grad))

    # Шаг 10
    xk_prev = xk.copy()
    xk = vector_add(xk, dk)

    # Шаг 11
    delta_x = vector_sub(xk, xk_prev)
    delta_f = f(xk) - f(xk_prev)

    if getNorma(delta_x) < eps2 and abs(delta_f) < eps2:
        print(f'Расчет окончен: изменения стали меньше {eps2}')
        print(f'x* = {xk}, f(x*) = {f(xk):.4f}')
        break

    k += 1
    print(f'Итерация {k}: x = {[round(val, 4) for val in xk]}, f(x) = {f(xk):.4f}, ||∇f|| = {getNorma(grad):.4f}')
