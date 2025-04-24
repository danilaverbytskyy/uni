from math import sqrt


def f(point: list | tuple) -> float:
    if len(point) != 2:
        raise ValueError('Координаты точки не соответствуют x1 и x2')
    return point[0] ** 2 + 4 * point[1] ** 2 - point[0] * point[1] + point[0]


def get_gradient(xk: list | tuple) -> list:
    return [
        2 * xk[0] - xk[1] + 1,
        -xk[0] + 8 * xk[1]
    ]


def get_norm(vector: list) -> float:
    """Вычисление евклидовой нормы вектора"""
    return sqrt(sum(x ** 2 for x in vector))


def scalar_mult(scalar: float, vector: list) -> list:
    return [scalar * x for x in vector]


def vector_sub(v1: list, v2: list) -> list:
    return [x - y for x, y in zip(v1, v2)]


def optimize(x0: list, eps1: float = 0.1, eps2: float = 0.15, max_iter: int = 100) -> list:
    xk = x0.copy()
    k = 0
    prev_f = f(xk)

    while k < max_iter:
        grad = get_gradient(xk)
        grad_norm = get_norm(grad)

        # Критерий остановки по норме градиента
        if grad_norm < eps1:
            print(f'Остановка: норма градиента {grad_norm:.4f} < {eps1}')
            break

        # Вычисляем t_k = (g^T g) / (g^T Q g), где Q - матрица Гессе
        Qg = [
            2 * grad[0] - grad[1],  # Q[0][0]*g[0] + Q[0][1]*g[1]
            -grad[0] + 8 * grad[1]  # Q[1][0]*g[0] + Q[1][1]*g[1]
        ]
        numerator = sum(g ** 2 for g in grad)
        denominator = sum(g * qg for g, qg in zip(grad, Qg))
        t_k = numerator / denominator

        xk_new = vector_sub(xk, scalar_mult(t_k, grad))
        current_f = f(xk_new)

        delta_x = get_norm(vector_sub(xk_new, xk))
        delta_f = abs(current_f - prev_f)

        if delta_x < eps2 and delta_f < eps2:
            print(f"k={k}")
            print(f'Остановка: изменения стали меньше eps2')
            break
        print(
            f'Итерация {k}: x = {[round(val, 4) for val in xk]}, f(x) = {current_f:.4f}, ||∇f|| = {grad_norm:.4f}')

        xk = xk_new
        prev_f = current_f
        k += 1

    return xk


eps1 = 0.1
eps2 = 0.15
max_iter = 100
x0 = [3, 1]

result = optimize(x0, eps1, eps2, max_iter)
print(f'\nРезультат: x* = {[round(val, 4) for val in result]}, f(x*) = {f(result):.4f}')