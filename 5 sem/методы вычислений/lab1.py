import math
import time


def s(x, error=3e-8):
    sum_s = 0
    k = 1
    term = 1 / (k + x) ** (3 / 2) - 1 / (k - x) ** (3 / 2)
    while abs(term) > error:
        sum_s += term
        k += 1
        term = 1 / (k + x) ** (3 / 2) - 1 / (k - x) ** (3 / 2)

    return [sum_s, k - 1]


val1 = [0.5, 0.999999999]
for item in val1:
    print(f's({item}) = {s(item)[0]}')
    print(f'Б) {s(item)[1]}')
    # print(f'B) time = {500 * s(item)[1]} ms')
    print()

def s2(x, error=3e-8):
    sum_s = 0
    k = 1
    term = ((k - x) ** 3/2 + (k + x) ** 3/2) / ((k - x) ** 3/2 * (k + x) ** 3/2)
    while abs(term) > error:
        sum_s += term
        k += 1
        term = ((k - x) ** 3/2 + (k + x) ** 3/2) / ((k - x) ** 3/2 * (k + x) ** 3/2)

    return [sum_s, k - 1]

print(f'((k - x) ** 3/2 + (k + x) ** 3/2) / ((k - x) ** 3/2 * (k + x) ** 3/2)')  # для ускорения сходимости ряда
val1 = [0.5, 0.999999999]
# for item in val1:
    # print(f's({item}) = {s2(item)[0]}')
print({s2(val1[1])[1]})
print({s(val1[1])[1]})



# def row_four1(error=1e-10):
#     sum_row = 0
#     n = 1
#     row = 1 / (n ** 2 + 1)
#     while abs(row) > error:
#         sum_row += row
#         n += 1
#         row = 1 / (n ** 2 + 1)
#
#     return sum_row,n


# def row_four2(error=1e-10):
#     sum_row = math.pi ** 2 / 6 - math.pi ** 4 / 90
#     n = 1
#     row = 1 / (n ** 4 * (n ** 2 + 1))
#     while abs(row) > error:
#         sum_row += row
#         n += 1
#         row = 1 / (n ** 4 * (n ** 2 + 1))
#
#     return sum_row,n
#
#
# start1 = time.time()
# print(row_four1())
#
# start2 = time.time()
# print(row_four2())
# end2 = time.time()
# print(end2 - start2, end2, start2)