from tabulate import tabulate

import numpy as np


def gradi(F, x0=None, epsilon=1e-6, max_iter=1000):
    """
    Метод наискорейшего градиентного спуска для минимизации функции F(x1, x2)

    Параметры:
    F - функция двух переменных для минимизации
    x0 - начальное приближение (по умолчанию [0, 0])
    epsilon - точность для остановки
    max_iter - максимальное число итераций

    Возвращает:
    Найденную точку минимума [x1, x2]
    """
    if x0 is None:
        x0 = [0, 0]

    x = np.array(x0, dtype=float)
    h = 1e-6  # шаг для численного дифференцирования

    for _ in range(max_iter):
        # Численное вычисление градиента
        grad = np.zeros(2)
        # Производная по x1
        f1 = F(x[0] + h, x[1])
        f2 = F(x[0] - h, x[1])
        grad[0] = (f1 - f2) / (2 * h)

        # Производная по x2
        f1 = F(x[0], x[1] + h)
        f2 = F(x[0], x[1] - h)
        grad[1] = (f1 - f2) / (2 * h)

        # Критерий остановки
        if np.linalg.norm(grad) < epsilon:
            break

        # Линейный поиск для определения оптимального шага
        alpha = 1.0
        c = 0.5  # коэффициент уменьшения шага
        tau = 0.5  # параметр условия Армихо

        # Условие Армихо для выбора шага
        while True:
            new_x = x - alpha * grad
            if F(*new_x) <= F(*x) - tau * alpha * np.dot(grad, grad):
                break
            alpha *= c

        x = x - alpha * grad

    return x

def f(x1,x2):
    return x1**2+4*x2**2-x1*x2+x1

def g(x1,x2):
    return 2*x1+x2-1

r = 1
c = 10
eps = 0.0001
n = 50

res = []

for i in range(50):
    def F(x1, x2):
        return f(x1,x2) + r/2 * g(x1,x2) ** 2
    x = gradi(F) # метод наиск. градиентного спуска из 2-го отчета
    p = r/2 * g(x[0],x[1])**2
    xr = r * g(x[0],x[1])
    res.append([i, r, round(x[0], 4), round(x[1], 4), round(F(x[0],x[1]), 4), round(xr, 4)])
    if (p < eps):
        break
    r *= c

headers = ["i", "r", "x1", "x2", "F(x)", "r·g(x)"]
print(tabulate(res, headers=headers, tablefmt="grid"))

print("x_min: ", x)
print("f_min: ", round(f(x[0],x[1]), 4))