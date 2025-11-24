#variant2 verbytskyy danila
import re


def is_valid_ipv4(ip):
    pattern = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?).){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    return re.match(pattern, ip) is not None


def get_ipv4(ip):
    if not isinstance(ip, str):
        raise ValueError("Аргумент должен быть строкой")

    if is_valid_ipv4(ip):
        return ip
    else:
        raise ValueError("Некорректный IP-адрес")


#192.168.1.1
#256.256.256.1
while True:
    try:
        s = input()
        print(get_ipv4(s))
    except ValueError as e:
        print(e)