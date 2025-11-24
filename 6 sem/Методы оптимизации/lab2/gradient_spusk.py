def f(x1, x2):
    return x1 ** 2 + 4 * x2 ** 2 - x1 * x2 + x1


def der_f(x1, x2):
    return 2 * x1 - x2 + 1, 8 * x2 - x1


def tk(x1, x2):
    p1 = der_f(x1, x2)[0]
    p2 = der_f(x1, x2)[1]
    t = (p1 ** 2 + p2 ** 2) / (2 * (p1 ** 2) + 8 * (p2 ** 2) - 2 * p1 * p2)
    return t


def norm_point(point1, point2):
    x11 = point1[0]
    x12 = point1[1]
    x21 = point2[0]
    x22 = point2[1]
    return ((x11 - x21) ** 2 + (x12 - x22) ** 2) ** 0.5


def norm_func(point1, point2):
    f1 = f(point1[0], point1[1])
    f2 = f(point2[0], point2[1])
    return abs(f1 - f2)


def Grad(point, M, e1, e2):
    k = -1
    last = False
    while True:
        k += 1
        grad_f = der_f(point[0], point[1])
        if ((grad_f[0] ** 2 + grad_f[1] ** 2) ** 0.5) < e1:
            print("Количество итераций: ", k + 1)
            print("Норма градиента меньше е1")
            return point[0], point[1]
        if k >= M:
            print("Количество итераций: ", k + 1)
            print("k стало больше M")
            return point[0], point[1]
        last_point = point
        t = tk(point[0], point[1])

        point = [point[0] - t * der_f(point[0], point[1])[0], point[1] - t * der_f(point[0], point[1])[1]]

        if (norm_point(point, last_point)) < e2 and (norm_func(point, last_point)) < e2 and last:
            print("Количество итераций: ", k + 1)
            print("Норма точек и модуль функций на шагах к и к-1 меньше е2")
            return point[0], point[1]
        elif (norm_point(point, last_point)) < e2 and norm_func(point, last_point) < e2:
            last = True


res = Grad([3, 1], 10, 0.1, 0.15)
print("x*= ", res)
print("f(x*)= ", f(res[0], res[1]))
