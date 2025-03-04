#variant2 verbytskyy danila
from random import randint


def count_pairs(filename):
    with open(filename) as f:
        n, k = map(int, f.readline().split())
        ratings = [int(f.readline()) for _ in range(n)]
    ratings.sort()

    count = 0
    i, j = 0, n - 1

    while i < j:
        if ratings[i] + ratings[j] >= k:
            # Все пары (ratings[i], ratings[k]) для k от i до j допустимы
            count += j - i
            j -= 1
        else:
            i += 1

    return count

print(count_pairs('test.txt'))
print(count_pairs('27-169a.txt'))
print(count_pairs('27-169b.txt'))

numbers = [randint(1,100) for _ in range(100)]
with open('file7.1.txt','w') as f:
    for i in numbers:
        f.writelines(str(i)+'\n')

with open('file7.1.txt','r') as f1:
    last = 1
    with open('file7.2.txt','w') as f2:
        for i in range(len(numbers)):
            n = int(f1.readline())
            last *= n
            f2.writelines(str(last)+'\n')
