def f(x1, x2):
    return x1 ** 2 + 4 * x2 ** 2 - x1 * x2 + x1


def der_f(x1, x2):
    return 2 * x1 - x2 + 1, 8 * x2 - x1


def Dihotomia(a0, b0, eps, l, x, d):
    def f(t):
        x1 = x[0] + t * d[0]
        x2 = x[1] + t * d[1]
        return x1 ** 2 + 4 * x2 ** 2 - x1 * x2 + x1

    k = 0
    a = a0
    b = b0
    y0 = (a + b - eps) / 2
    z0 = (a + b + eps) / 2
    while (True):
        if (f(y0) <= f(z0)):
            b = z0
        else:
            a = y0
        if (abs(a - b) < l):
            return [round(a, 5), round(b, 5)]
        else:
            y0 = (a + b - eps) / 2
            z0 = (a + b + eps) / 2
            k = k + 1


def mult(m1, m2):
    o1 = -(m1[0][0] * m2[0] + m1[0][1] * m2[1])
    o2 = -(m1[1][0] * m2[0] + m1[1][1] * m2[1])
    return o1, o2


def norm_point(point1, point2):
    x11 = point1[0]
    x12 = point1[1]
    x21 = point2[0]
    x22 = point2[1]
    return ((x11 - x21) ** 2 + (x12 - x22) ** 2) ** 0.5


def norm_func(point1, point2):
    def f(x1, x2):
        return x1 ** 2 + 4 * x2 ** 2 - x1 * x2 + x1

    f1 = f(point1[0], point1[1])
    f2 = f(point2[0], point2[1])
    return abs(f1 - f2)


def flr(point, maxiter, e1, e2):
    k = -1
    last = False
    d = [0, 0]
    last_d = d
    last_point = point
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
        if k == 0:
            d = [-grad_f[0], -grad_f[1]]
        else:
            grad_min_1 = der_f(last_point[0], last_point[1])
            beta = (grad_f[0] ** 2 + grad_f[1] ** 2) / (grad_min_1[0] ** 2 + grad_min_1[1] ** 2)
            last_d = d
            d = [-grad_f[0] + beta * last_d[0], -grad_f[1] + beta * last_d[1]]
        answer = Dihotomia(0, 10, 0.2, 0.5, point, d)
        result = (answer[0] + answer[1]) / 2
        t = result
        last_point = point
        point = [point[0] + t * d[0], point[1] + t * d[1]]

        if (norm_point(point, last_point)) < e2 and (norm_func(point, last_point)) < e2 and last:
            print("Количество итераций: ", k + 1)
            print("Норма точек и модуль функций на шагах к и к-1 меньше е2")
            return point[0], point[1]
        elif (norm_point(point, last_point)) < e2 and norm_func(point, last_point) < e2:
            last = True


res = flr([3,1], 10, 0.1, 0.15)
print("x*= ", res)
print("f(x*)= ", f(res[0], res[1]))
