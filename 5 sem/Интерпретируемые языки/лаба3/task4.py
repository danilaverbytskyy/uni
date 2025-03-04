def f4(str_list):
    first_str = str_list[0]
    avg_first = sum(ord(char) for char in first_str) / len(first_str)

    def calc_variance(string):
        #avg = sum(ord(symbol) for symbol in string) / len(string)
        result = sum((ord(char) - avg_first) ** 2 for char in string)
        print(result)
        return result

    sorted_list = sorted(str_list, key=lambda s: calc_variance(s))
    return sorted_list

# uw5uw hjweghfk 456 uwiuk992
str_list = list(map(str, input().split(' ')))
sorted_items = f4(str_list)
for i in sorted_items:
    print(i, end=' ')
