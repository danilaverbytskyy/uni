from math import sqrt


def f(point: list | tuple) -> float:
    if len(point) != 2:
        raise ValueError("Координаты точки должны быть двумерными.")
    x1, x2 = point
    return x1 ** 2 + 4 * x2 ** 2 - x1 * x2 + x1


def get_gradient(point: list | tuple) -> list:
    x1, x2 = point
    return [2 * x1 - x2 + 1, -x1 + 8 * x2]


def get_hessian() -> list[list]:
    return [
        [2, -1],
        [-1, 8]
    ]


def get_inverse_hessian() -> list[list]:
    hessian = get_hessian()
    det = hessian[0][0] * hessian[1][1] - hessian[0][1] * hessian[1][0]
    return [
        [hessian[1][1] / det, -hessian[0][1] / det],
        [-hessian[1][0] / det, hessian[0][0] / det]
    ]


def vector_norm(vector: list) -> float:
    return sqrt(sum(x ** 2 for x in vector))


def matrix_vector_mult(matrix: list[list], vector: list) -> list:
    return [sum(m * v for m, v in zip(row, vector)) for row in matrix]


def vector_add(v1: list, v2: list) -> list:
    return [x + y for x, y in zip(v1, v2)]


def scalar_mult(scalar: float, vector: list) -> list:
    return [scalar * x for x in vector]


def line_search(f, xk: list, dk: list, max_iter=100, tol=1e-6) -> float:
    """Метод золотого сечения для поиска оптимального шага t_k."""
    a, b = 0, 1
    phi = (1 + sqrt(5)) / 2
    c = b - (b - a) / phi
    d = a + (b - a) / phi

    for _ in range(max_iter):
        if abs(c - d) < tol:
            break
        if f(vector_add(xk, scalar_mult(c, dk))) < f(vector_add(xk, scalar_mult(d, dk))):
            b = d
        else:
            a = c
        c = b - (b - a) / phi
        d = a + (b - a) / phi

    return (a + b) / 2


def newton_raphson(f, x0: list, eps1=0.1, eps2=0.15, max_iter=10) -> list:
    xk = x0.copy()
    k = 0

    while k < max_iter:
        grad = get_gradient(xk)
        grad_norm = vector_norm(grad)

        if grad_norm <= eps1:
            print(f"Критерий остановки 1: ||∇f|| = {grad_norm:.4f} <= {eps1}")
            break

        H_inv = get_inverse_hessian()
        dk = scalar_mult(-1, matrix_vector_mult(H_inv, grad))

        tk = line_search(f, xk, dk)

        xk_new = vector_add(xk, scalar_mult(tk, dk))

        delta_x = vector_norm([xk_new[0] - xk[0], xk_new[1] - xk[1]])
        delta_f = abs(f(xk_new) - f(xk))

        if delta_x < eps2 and delta_f < eps2:
            print(f"Критерий остановки 2: Δx = {delta_x:.4f} < {eps2} и Δf = {delta_f:.4f} < {eps2}")
            break

        xk = xk_new
        k += 1
        print(f"Итерация {k}: x = {[round(val, 4) for val in xk]}, f(x) = {f(xk):.4f}, ||∇f|| = {grad_norm:.4f}")

    return xk


# Параметры
x0 = [3, 1]
eps1 = 0.1
eps2 = 0.15
max_iter = 10

# Запуск метода
result = newton_raphson(f, x0, eps1, eps2, max_iter)
print(f"\nРезультат: x* = {[round(val, 4) for val in result]}, f(x*) = {f(result):.4f}")