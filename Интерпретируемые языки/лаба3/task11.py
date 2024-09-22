def average_ascii_weight(triplet):
    """Вычисляет средний вес ASCII-кодов тройки символов."""
    return sum(ord(char) for char in triplet) / len(triplet)


def max_average_weight(s):
    """Вычисляет максимальный средний вес ASCII-кодов тройки символов в строке."""
    max_weight = 0
    for i in range(len(s) - 2):
        triplet = s[i:i + 3]
        weight = average_ascii_weight(triplet)
        max_weight = max(max_weight, weight)
    return max_weight


def f11(str_list):
    """Сортирует строки по квадратичному отклонению дисперсии от максимального среднего веса первой строки."""
    if not str_list:
        return []

    # Получаем максимальный средний вес первой строки
    first_max_weight = max_average_weight(str_list[0])

    # Функция для вычисления квадратичного отклонения
    def calculate_deviation(s):
        max_weight = max_average_weight(s)
        return (max_weight - first_max_weight) ** 2

    # Сортируем строки по квадратичному отклонению
    sorted_str_list = sorted(str_list, key=calculate_deviation)

    return sorted_str_list


# uw5uw hjweghfk 456 uwiuk992
str_list = list(map(str, input().split(' ')))
sorted_dict_items = f11(str_list)
for i in sorted_dict_items:
    print(i, end=' ')