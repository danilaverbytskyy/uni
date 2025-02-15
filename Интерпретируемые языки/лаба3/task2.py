# verbytskyy danila variant2
# tasks 2 4 7 11

def get_weight(s):
    weight = 0
    c = 0
    for c1 in s:
        for c2 in c1:
            weight += ord(c2)
            c += 1
    return weight / c


def f2(str_list):
    mydict = dict()
    for i in str_list:
        mydict[i] = get_weight(i)
    print(mydict)
    sorted_dict = {k: v for k, v in sorted(mydict.items(), key=lambda item: item[1])}
    return sorted_dict.items()


# hjweghfkik 456 uwiu992
str_list = list(map(str, input().split(' ')))
sorted_dict_items = f2(str_list)
for i in sorted_dict_items:
    print(i[0], end=' ')
