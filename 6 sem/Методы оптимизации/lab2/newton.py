def f(x1, x2):
    return x1 ** 2 + 4 * x2 ** 2 - x1 * x2 + x1


def H():
    return [[2, -1], [-1, 8]]


def reverse_H(m):
    d = m[0][0] * m[1][1] - m[0][1] * m[1][0]
    rev_m = [[0, 0], [0, 0]]
    for i in range(2):
        for j in range(2):
            rev_m[i][j] = m[2 - i - 1][2 - j - 1] * (-1) ** (i + 1 + j + 1)
            rev_m[i][j] /= d
    return rev_m


def m_def_true(m):
    a11 = m[0][0]
    d = m[0][0] * m[1][1] - m[0][1] * m[1][0]
    return a11 > 0 and d > 0


reverse_H(H())


def der_f(x1, x2):
    return 2 * x1 - x2 + 1, 8 * x2 - x1


def mult(m1, m2):
    o1 = -(m1[0][0] * m2[0] + m1[0][1] * m2[1])
    o2 = -(m1[1][0] * m2[0] + m1[1][1] * m2[1])
    return o1, o2


def tk(x1, x2):
    p1 = der_f(x1, x2)[0]
    p2 = der_f(x1, x2)[1]
    t = (p1 ** 2 + p2 ** 2) / (4 * (p1 ** 2) + 6 * (p2 ** 2) - 2 * p1 * p2)
    return t


def norm_point(point1, point2):
    x11 = point1[0]
    x12 = point1[1]
    x21 = point2[0]
    x22 = point2[1]
    return ((x11 - x21) ** 2 + (x12 - x22) ** 2) ** 0.5


def norm_func(point1, point2):
    def f(x1, x2):
        return 2 * x1 ** 2 + 3 * x2 ** 2 - x1 * x2 + x1

    f1 = f(point1[0], point1[1])
    f2 = f(point2[0], point2[1])
    return abs(f1 - f2)


def Newton(point, maxiter, e1, e2):
    k = -1
    last = False
    while True:
        k += 1
        grad_f = der_f(point[0], point[1])
        if ((grad_f[0] ** 2 + grad_f[1] ** 2) ** 0.5) < e1:
            print("Количество итераций: ", k + 1)
            print("Норма градиента меньше е1")
            return point[0], point[1]
        if k >= maxiter:
            print("Количество итераций: ", k + 1)
            print("Превышено количество итераций")
            return point[0], point[1]
        last_point = point
        if m_def_true(H()):
            d = mult(reverse_H(H()), grad_f)
            point = [point[0] + d[0], point[1] + d[1]]
        else:
            d = [-grad_f[0], -grad_f[1]]
            t = tk(point[0], point[1])
            point = [point[0] + t * d[0], point[1] + t * d[1]]

        if (norm_point(point, last_point)) < e2 and (norm_func(point, last_point)) < e2 and last:
            print("Количество итераций: ", k + 1)
            print("Норма точек и модуль функций на шагах к и к-1 меньше е2")
            return point[0], point[1]
        elif (norm_point(point, last_point)) < e2 and norm_func(point, last_point) < e2:
            last = True


res = Newton([3, 1], 10, 0.1, 0.15)
print("x*= ", res)
print("f(x*)= ", f(res[0], res[1]))
