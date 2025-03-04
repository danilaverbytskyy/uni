def average_weight(triplet):
    return sum(ord(char) for char in triplet) / len(triplet)


def max_average_weight(s):
    max_weight = 0
    for i in range(len(s) - 2):
        triplet = s[i:i + 3]
        weight = average_weight(triplet)
        max_weight = max(max_weight, weight)
    return max_weight


def f11(str_list):
    first_max_weight = max_average_weight(str_list[0])

    def calculate_deviation(s):
        max_weight = max_average_weight(s)
        print((max_weight - first_max_weight) ** 2)
        return (max_weight - first_max_weight) ** 2

    sorted_str_list = sorted(str_list, key=calculate_deviation)

    return sorted_str_list


# uw5uw hjweghfk 456 uwiuk992
str_list = list(map(str, input().split(' ')))
sorted_dict_items = f11(str_list)
for i in sorted_dict_items:
    print(i, end=' ')