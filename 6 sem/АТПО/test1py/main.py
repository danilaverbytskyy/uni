def get_number(input_text):
    n = 1
    while True:
        try:
            n = int(input(input_text))
            return n
        except ValueError:
            print("Ошибка значения. Введите число")
        except n == 0:
            print('Сторона не может быть <= 0')


def define_triangle(n1, n2, n3):
    if (n1 == n2 == n3):
        return "Равносторонний"
    elif (n1 == n2 or n1 == n3 or n2 == n3):
        return "Равнобедренный"
    elif ((n1 * n1 + n2 * n2) == n3 * n3):
        return "Прямоугольный"
    return "Обычный"


n1, n2, n3 = 1, 1, 1
try:
    n1 = get_number("Введите первое число: ")
    n2 = get_number("Введите второе число: ")
    n3 = get_number("Введите третье число: ")
    numbers = [n1, n2, n3].sort()
except numbers[0] + numbers[1] <= numbers[2]:
    print("Это не треугольник")
finally:
    print(define_triangle(n1, n2, n3))

