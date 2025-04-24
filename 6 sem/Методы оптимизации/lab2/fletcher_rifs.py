from math import sqrt


def f(point: list | tuple) -> float:
    if len(point) != 2:
        raise Exception('Координаты точки не соответствуют x1 и x2')
    return point[0]**2 + 4 * point[1]**2 - point[0] * point[1] + point[0]


def getGradient(xk: list | tuple) -> list:
    return [
        2 * xk[0] - xk[1] + 1,
        -xk[0] + 8 * xk[1]
    ]


def getNorma(vector: list) -> float:
    return sqrt(sum(x ** 2 for x in vector))


def scalar_mult(scalar: float, vector: list) -> list:
    return [scalar * x for x in vector]


def vector_add(v1: list, v2: list) -> list:
    return [x + y for x, y in zip(v1, v2)]


def vector_sub(v1: list, v2: list) -> list:
    return [x - y for x, y in zip(v1, v2)]


def dot_product(v1: list, v2: list) -> float:
    return sum(x * y for x, y in zip(v1, v2))


def line_search(f, xk, dk, max_iter=100, tol=1e-6):
    """Метод золотого сечения для поиска оптимального шага"""
    a, b = 0, 1
    gr = (sqrt(5) + 1) / 2

    c = b - (b - a) / gr
    d = a + (b - a) / gr

    for _ in range(max_iter):
        if f(vector_add(xk, scalar_mult(c, dk))) < f(vector_add(xk, scalar_mult(d, dk))):
            b = d
        else:
            a = c

        c = b - (b - a) / gr
        d = a + (b - a) / gr

        if abs(b - a) < tol:
            break

    return (a + b) / 2


def fletcher_reeves(f, x0, eps1=0.1, eps2=0.15, M=10):
    xk = x0.copy()
    k = 0
    grad_prev = None
    dk_prev = None

    while True:
        # Вычислить градиент
        grad = getGradient(xk)

        # Проверить критерий окончания по градиенту
        if getNorma(grad) < eps1:
            print(f'Критерий остановки 1: ∇f = {getNorma(grad):.4f} < {eps1}')
            return xk

        # Проверить максимальное число итераций
        if k >= M:
            print(f'Критерий остановки 2: достигнут максимум итераций {M}')
            return xk

        # Первая итерация - метод наискорейшего спуска
        if k == 0:
            dk = scalar_mult(-1, grad)
        else:
            # Вычислить β по Флетчеру-Ривсу
            beta = dot_product(grad, grad) / dot_product(grad_prev, grad_prev)

            # Новое направление
            dk = vector_add(scalar_mult(-1, grad), scalar_mult(beta, dk_prev))

        # Найти оптимальный шаг
        tk = line_search(f, xk, dk)

        # Сохранить предыдущие значения
        xk_prev = xk.copy()
        grad_prev = grad.copy()
        dk_prev = dk.copy()

        # Обновить точку
        xk = vector_add(xk, scalar_mult(tk, dk))

        # Проверить дополнительные критерии остановки
        delta_x = vector_sub(xk, xk_prev)
        delta_f = abs(f(xk) - f(xk_prev))

        if getNorma(delta_x) < eps2 and delta_f < eps2:
            print(f'Критерий остановки 3: изменения стали меньше {eps2}')
            return xk

        print(
            f'Итерация {k}: x = {[round(val, 4) for val in xk]}, f(x) = {round(f(xk), 4)}, ∇f = {round(getNorma(grad), 4)}')
        k += 1


# Параметры
eps1 = 0.1
eps2 = 0.15
M = 10
x0 = [3, 1]

# Запуск метода
print("Метод Флетчера-Ривса:")
result = fletcher_reeves(f, x0, eps1, eps2, M)
print(f'\nРезультат: x* = {[round(val, 4) for val in result]}, f(x*) = {round(f(result), 4)}')