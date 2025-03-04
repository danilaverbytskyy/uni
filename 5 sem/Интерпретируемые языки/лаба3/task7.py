def get_difference(s):
    ENG_GL = 'auioeAUIOE'
    RU_GL = 'уеыаоэяиюёУЕЫАОЭЯИЮЁ'
    gl_sogl = 0
    sogl_gl = 0
    for i in range(len(s)-1):
        if s[i].isnumeric() or s[i+1].isnumeric():
            continue
        if s[i] in ENG_GL or s[i] in RU_GL:
            if not(s[i+1] in ENG_GL) and not(s[i+1] in RU_GL):
                gl_sogl+=1
        if not(s[i] in ENG_GL) and not(s[i] in RU_GL):
            if s[i+1] in ENG_GL or s[i+1] in RU_GL:
                sogl_gl+=1
    return gl_sogl - sogl_gl


def f7(str_list):
    mydict = dict()
    for i in str_list:
        mydict[i] = get_difference(i)
    print(mydict)
    sorted_dict = {k: v for k, v in sorted(mydict.items(), key=lambda item: item[1])}
    return sorted_dict.keys()

# uw5uw hjweghfk 456 uwiuk992
str_list = list(map(str, input().split(' ')))
print('\nAnswer')
print(*f7(str_list))