from random import *

def shuffle(mylist: list):
    for i in range(len(mylist)-1):
        mylist[i], mylist[i+1] = mylist[i+1], mylist[i]
    return mylist[::-1]

def shuffle2(mylist: list):
    used_indexes = []
    for i in range(len(mylist)):
        index = randint(0, len(mylist)-1)
        while index in used_indexes:
            index = randint(0, len(mylist)-1)
        used_indexes.append(index)
        mylist[i], mylist[index] = mylist[index], mylist[i]
    return mylist


print(shuffle2([1, 5, 7, 8, 10]))