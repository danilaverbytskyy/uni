import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
from math import gcd


# =========================
# Общие вспомогательные функции
# =========================

def egcd(a: int, b: int):
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y


def modinv(a: int, m: int) -> int:
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("Обратный элемент не существует")
    return x % m


def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def parse_int_blocks(s: str):
    s = s.strip()
    if not s:
        return []
    parts = [p for p in s.replace(",", " ").split() if p]
    result = []
    for p in parts:
        try:
            result.append(int(p))
        except ValueError:
            raise ValueError(f"Некорректный блок: {p}")
    return result


# =========================
# Алфавиты
# =========================

class LatinAlphabet:
    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"
        self.char_to_num = {}
        self.num_to_char = {}
        for i, ch in enumerate(self.alphabet, start=1):
            self.char_to_num[ch] = i
            self.num_to_char[i] = ch

    def text_to_numbers(self, text):
        nums = []
        for ch in text.upper():
            if ch in self.char_to_num:
                nums.append(self.char_to_num[ch])
            elif ch == " ":
                nums.append(27)
            else:
                nums.append(27)
        return nums

    def numbers_to_text(self, numbers):
        return "".join(self.num_to_char.get(n, "?") for n in numbers)


class RussianAlphabet:
    def __init__(self):
        self.alphabet = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ_"
        self.char_to_num = {}
        self.num_to_char = {}
        for i, ch in enumerate(self.alphabet, start=1):
            self.char_to_num[ch] = i
            self.num_to_char[i] = ch

    def normalize_text(self, text: str) -> str:
        result = []
        for ch in text.upper():
            if ch == " ":
                result.append("_")
            elif ch in self.char_to_num:
                result.append(ch)
            else:
                result.append("_")
        return "".join(result)

    def text_to_numbers(self, text: str):
        text = self.normalize_text(text)
        return [self.char_to_num[ch] for ch in text]

    def numbers_to_text(self, numbers):
        return "".join(self.num_to_char.get(n, "?") for n in numbers)


RUS_TO_LAT = {
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E',
    'Ё': 'E', 'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K',
    'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
    'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'KH', 'Ц': 'TS',
    'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH', 'Ъ': '', 'Ы': 'Y',
    'Ь': '', 'Э': 'E', 'Ю': 'YU', 'Я': 'YA', ' ': '_', '_': '_'
}


def translit_to_latin(text: str) -> str:
    result = ""
    for ch in text.upper():
        result += RUS_TO_LAT.get(ch, ch)
    return result


# =========================
# RSA
# =========================

def choose_e(phi: int) -> int:
    preferred = 65537
    if preferred < phi and gcd(preferred, phi) == 1:
        return preferred
    e = 3
    while e < phi:
        if gcd(e, phi) == 1:
            return e
        e += 2
    raise ValueError("Не удалось подобрать e")


def rsa_generate_keys(p: int, q: int):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("p и q должны быть простыми числами")
    if p == q:
        raise ValueError("p и q должны быть разными простыми числами")

    n = p * q
    phi = (p - 1) * (q - 1)
    e = choose_e(phi)
    d = modinv(e, phi)
    return (e, n), (d, n), {"n": n, "phi": phi, "p": p, "q": q}


def rsa_encrypt_int(m: int, e: int, n: int) -> int:
    if not (0 <= m < n):
        raise ValueError("Блок сообщения должен быть в диапазоне 0 <= m < n")
    return pow(m, e, n)


def rsa_decrypt_int(c: int, d: int, n: int) -> int:
    if not (0 <= c < n):
        raise ValueError("Блок шифртекста должен быть в диапазоне 0 <= c < n")
    return pow(c, d, n)


def rsa_encrypt_text(text: str, public_key):
    e, n = public_key
    blocks = []
    for ch in text:
        m = ord(ch)
        if m >= n:
            raise ValueError(
                "n слишком маленькое для кодировки символов.\n"
                "Увеличьте p и q."
            )
        blocks.append(rsa_encrypt_int(m, e, n))
    return blocks


def rsa_decrypt_blocks(blocks, private_key):
    d, n = private_key
    chars = []
    for c in blocks:
        chars.append(chr(rsa_decrypt_int(c, d, n)))
    return "".join(chars)


# =========================
# АВКР
# =========================

class AdditiveKnapsack:
    def __init__(self):
        self.n = 8
        self.superincreasing = None
        self.m = None
        self.w = None
        self.w_inv = None
        self.public_key = None
        self.keys_generated = False
        self.alphabet = LatinAlphabet()

    def generate_superincreasing(self):
        vector = [random.randint(1, 5)]
        for _ in range(1, self.n):
            vector.append(sum(vector) + random.randint(1, 10))
        return vector

    def generate_keys(self):
        self.superincreasing = self.generate_superincreasing()
        self.m = sum(self.superincreasing) + random.randint(50, 200)

        self.w = random.randint(2, self.m - 1)
        while math.gcd(self.w, self.m) != 1:
            self.w = random.randint(2, self.m - 1)

        self.w_inv = modinv(self.w, self.m)
        self.public_key = [(self.w * a) % self.m for a in self.superincreasing]
        self.keys_generated = True

    def number_to_bits(self, num):
        bits = [0] * self.n
        for i in range(self.n):
            bits[i] = (num >> i) & 1
        return bits

    def bits_to_number(self, bits):
        num = 0
        for i in range(self.n):
            if bits[i]:
                num |= (1 << i)
        return num

    def encrypt_char(self, ch):
        num = self.alphabet.char_to_num.get(ch, 27)
        bits = self.number_to_bits(num)
        s = 0
        for i in range(self.n):
            if bits[i]:
                s += self.public_key[i]
        return s

    def decrypt_char(self, value):
        v_prime = (value * self.w_inv) % self.m
        bits = [0] * self.n
        remaining = v_prime

        for i in range(self.n - 1, -1, -1):
            if remaining >= self.superincreasing[i]:
                bits[i] = 1
                remaining -= self.superincreasing[i]

        num = self.bits_to_number(bits)
        if 1 <= num <= 27:
            return self.alphabet.num_to_char.get(num, "_")
        return "?"

    def encrypt(self, message):
        if not self.keys_generated:
            raise ValueError("Сначала сгенерируйте ключи")
        latin_text = translit_to_latin(message)
        return [self.encrypt_char(ch) for ch in latin_text]

    def decrypt(self, encrypted):
        if not self.keys_generated:
            raise ValueError("Сначала сгенерируйте ключи")
        return "".join(self.decrypt_char(x) for x in encrypted)

    def get_info(self):
        if not self.keys_generated:
            return "Ключи не сгенерированы"
        return (
            f"АВКР — классический аддитивный рюкзак\n\n"
            f"Размерность n = {self.n}\n"
            f"Секретный сверхрастущий вектор A' = {self.superincreasing}\n"
            f"Модуль m = {self.m}\n"
            f"Множитель w = {self.w}\n"
            f"Обратный элемент w^(-1) mod m = {self.w_inv}\n"
            f"Открытый ключ A = {self.public_key}"
        )


# =========================
# МВКР
# =========================

class MultiplicativeKnapsack:
    def __init__(self):
        self.n = 5
        self.primes = None
        self.m = None
        self.w = None
        self.w_inv = None
        self.public_key = None
        self.keys_generated = False
        self.alphabet = LatinAlphabet()

    def generate_prime_vector(self):
        primes = []
        candidate = 2
        while len(primes) < self.n:
            if is_prime(candidate):
                primes.append(candidate)
            candidate += 1
        return primes

    def number_to_bits(self, num: int):
        bits = [0] * self.n
        for i in range(self.n):
            bits[i] = (num >> i) & 1
        return bits

    def bits_to_number(self, bits):
        num = 0
        for i in range(self.n):
            if bits[i]:
                num |= (1 << i)
        return num

    def generate_keys(self):
        self.primes = self.generate_prime_vector()
        product = 1
        for p in self.primes:
            product *= p

        self.m = product + 1
        while not is_prime(self.m):
            self.m += 1

        self.w = random.randint(2, self.m - 2)
        while math.gcd(self.w, self.m - 1) != 1:
            self.w = random.randint(2, self.m - 2)

        self.w_inv = modinv(self.w, self.m - 1)
        self.public_key = [pow(p, self.w, self.m) for p in self.primes]
        self.keys_generated = True

    def encrypt_char(self, ch: str) -> int:
        num = self.alphabet.char_to_num.get(ch, 27)
        bits = self.number_to_bits(num)

        result = 1
        for i in range(self.n):
            if bits[i]:
                result = (result * self.public_key[i]) % self.m
        return result

    def decrypt_char(self, value: int) -> str:
        v_prime = pow(value, self.w_inv, self.m)

        bits = [0] * self.n
        remaining = v_prime

        for i in range(self.n - 1, -1, -1):
            if remaining % self.primes[i] == 0:
                bits[i] = 1
                remaining //= self.primes[i]

        num = self.bits_to_number(bits)

        if 1 <= num <= 27:
            return self.alphabet.num_to_char.get(num, "_")
        return "?"

    def encrypt(self, message: str):
        if not self.keys_generated:
            raise ValueError("Сначала сгенерируйте ключи")
        latin_text = translit_to_latin(message)
        return [self.encrypt_char(ch) for ch in latin_text]

    def decrypt(self, encrypted):
        if not self.keys_generated:
            raise ValueError("Сначала сгенерируйте ключи")
        return "".join(self.decrypt_char(x) for x in encrypted)

    def get_info(self):
        if not self.keys_generated:
            return "Ключи не сгенерированы"
        return (
            f"МВКР — классический мультипликативный рюкзак\n\n"
            f"Размерность n = {self.n}\n"
            f"Секретные простые числа P = {self.primes}\n"
            f"Секретный модуль m = {self.m}\n"
            f"Секретный множитель w = {self.w}\n"
            f"Обратный элемент w^(-1) mod (m-1) = {self.w_inv}\n"
            f"Открытый ключ A = {self.public_key}"
        )


# =========================
# ГАВКР
# =========================

class GeneralizedAdditiveKnapsack:
    def __init__(self, base: int = 3):
        self.base = base
        self.n = 4
        self.superincreasing = None
        self.m = None
        self.w = None
        self.w_inv = None
        self.public_key = None
        self.keys_generated = False
        self.alphabet = RussianAlphabet()

    def generate_superincreasing(self):
        vector = [random.randint(1, 5)]
        for _ in range(1, self.n):
            min_val = (self.base - 1) * sum(vector) + 1
            vector.append(min_val + random.randint(0, 5))
        return vector

    def number_to_base_vector(self, num: int):
        vector = [0] * self.n
        temp = num
        for i in range(self.n):
            vector[i] = temp % self.base
            temp //= self.base
        return vector

    def base_vector_to_number(self, vector):
        num = 0
        power = 1
        for digit in vector:
            num += digit * power
            power *= self.base
        return num

    def generate_keys(self):
        self.superincreasing = self.generate_superincreasing()

        min_m = (self.base - 1) * sum(self.superincreasing) + 1
        self.m = random.randint(min_m, min_m * 2)

        self.w = random.randint(2, self.m - 1)
        while math.gcd(self.w, self.m) != 1:
            self.w = random.randint(2, self.m - 1)

        self.w_inv = modinv(self.w, self.m)
        self.public_key = [(self.w * a) % self.m for a in self.superincreasing]
        self.keys_generated = True

    def encrypt_char_num(self, num: int) -> int:
        digits = self.number_to_base_vector(num)
        result = 0
        for i in range(self.n):
            result += digits[i] * self.public_key[i]
        return result

    def decrypt_char_num(self, value: int) -> int:
        v_prime = (value * self.w_inv) % self.m
        digits = [0] * self.n
        remaining = v_prime

        for i in range(self.n - 1, -1, -1):
            coeff = min(self.base - 1, remaining // self.superincreasing[i])
            digits[i] = coeff
            remaining -= coeff * self.superincreasing[i]

        return self.base_vector_to_number(digits)

    def encrypt(self, message: str):
        if not self.keys_generated:
            raise ValueError("Сначала сгенерируйте ключи")
        numbers = self.alphabet.text_to_numbers(message)
        return [self.encrypt_char_num(num) for num in numbers]

    def decrypt(self, encrypted):
        if not self.keys_generated:
            raise ValueError("Сначала сгенерируйте ключи")
        result_numbers = [self.decrypt_char_num(x) for x in encrypted]
        return self.alphabet.numbers_to_text(result_numbers)

    def get_info(self):
        if not self.keys_generated:
            return "Ключи не сгенерированы"
        return (
            f"ГАВКР — обобщённый аддитивный рюкзак\n\n"
            f"Основание p = {self.base}\n"
            f"Размерность n = {self.n}\n"
            f"Секретный обобщённо-сверхрастущий вектор A' = {self.superincreasing}\n"
            f"Секретный модуль m = {self.m}\n"
            f"Секретный множитель w = {self.w}\n"
            f"Обратный элемент w^(-1) mod m = {self.w_inv}\n"
            f"Открытый ключ A = {self.public_key}"
        )


# =========================
# ГМВКР
# =========================

class GeneralizedMultiplicativeKnapsack:
    def __init__(self, base: int = 5, n: int = 3):
        self.base = base
        self.n = n
        self.primes = None
        self.m = None
        self.w = None
        self.w_inv = None
        self.public_key = None
        self.keys_generated = False
        self.alphabet = RussianAlphabet()

    def generate_prime_vector(self):
        primes = []
        candidate = 2
        while len(primes) < self.n:
            if is_prime(candidate):
                primes.append(candidate)
            candidate += 1
        return primes

    def number_to_base_vector(self, num: int):
        vec = [0] * self.n
        temp = num
        for i in range(self.n):
            vec[i] = temp % self.base
            temp //= self.base
        return vec

    def base_vector_to_number(self, vec):
        num = 0
        power = 1
        for x in vec:
            num += x * power
            power *= self.base
        return num

    def generate_keys(self):
        self.primes = self.generate_prime_vector()

        product = 1
        for p in self.primes:
            product *= p

        self.m = product + 1
        while not is_prime(self.m):
            self.m += 1

        self.w = random.randint(2, self.m - 2)
        while math.gcd(self.w, self.m - 1) != 1:
            self.w = random.randint(2, self.m - 2)

        self.w_inv = modinv(self.w, self.m - 1)
        self.public_key = [pow(p, self.w, self.m) for p in self.primes]
        self.keys_generated = True

    def encrypt_char_num(self, num: int) -> int:
        coeffs = self.number_to_base_vector(num)
        result = 1
        for i in range(self.n):
            if coeffs[i] > 0:
                result = (result * pow(self.public_key[i], coeffs[i], self.m)) % self.m
        return result

    def decrypt_char_num(self, value: int) -> int:
        v_prime = pow(value, self.w_inv, self.m)
        coeffs = [0] * self.n
        remaining = v_prime

        for i in range(self.n - 1, -1, -1):
            count = 0
            while remaining % self.primes[i] == 0 and count < self.base - 1:
                remaining //= self.primes[i]
                count += 1
            coeffs[i] = count

        return self.base_vector_to_number(coeffs)

    def encrypt(self, message: str):
        if not self.keys_generated:
            raise ValueError("Сначала сгенерируйте ключи")
        numbers = self.alphabet.text_to_numbers(message)
        return [self.encrypt_char_num(num) for num in numbers]

    def decrypt(self, encrypted):
        if not self.keys_generated:
            raise ValueError("Сначала сгенерируйте ключи")
        nums = [self.decrypt_char_num(x) for x in encrypted]
        return self.alphabet.numbers_to_text(nums)

    def get_info(self):
        if not self.keys_generated:
            return "Ключи не сгенерированы"
        return (
            f"ГМВКР — обобщённый мультипликативный рюкзак\n\n"
            f"Основание p = {self.base}\n"
            f"Размерность n = {self.n}\n"
            f"Секретные простые числа = {self.primes}\n"
            f"Секретный модуль m = {self.m}\n"
            f"Секретный множитель w = {self.w}\n"
            f"w^(-1) mod (m-1) = {self.w_inv}\n"
            f"Открытый ключ = {self.public_key}"
        )


# =========================
# Код Хэмминга
# =========================

def hamming_encode_8bits(data_bits: str) -> str:
    if len(data_bits) != 8 or any(b not in "01" for b in data_bits):
        raise ValueError("Нужно ровно 8 бит данных.")

    code = ['0'] * 13
    data_positions = [3, 5, 6, 7, 9, 10, 11, 12]

    for bit, pos in zip(data_bits, data_positions):
        code[pos] = bit

    parity_positions = [1, 2, 4, 8]
    for p in parity_positions:
        parity = 0
        for i in range(1, 13):
            if i & p and i != p:
                parity ^= int(code[i])
        code[p] = str(parity)

    return ''.join(code[1:])


def hamming_check_and_correct_12bits(codeword: str):
    if len(codeword) != 12 or any(b not in "01" for b in codeword):
        raise ValueError("Нужно ровно 12 бит кодового слова.")

    code = ['0'] + list(codeword)
    parity_positions = [1, 2, 4, 8]

    error_position = 0
    for p in parity_positions:
        parity = 0
        for i in range(1, 13):
            if i & p:
                parity ^= int(code[i])
        if parity != 0:
            error_position += p

    if 1 <= error_position <= 12:
        code[error_position] = '1' if code[error_position] == '0' else '0'

    return ''.join(code[1:]), error_position


def hamming_decode_12bits(codeword: str):
    corrected, error_position = hamming_check_and_correct_12bits(codeword)
    c = ['0'] + list(corrected)
    data_positions = [3, 5, 6, 7, 9, 10, 11, 12]
    data_bits = ''.join(c[pos] for pos in data_positions)
    return data_bits, corrected, error_position


def encode_text_hamming(text: str):
    blocks = []
    for ch in text:
        bits = format(ord(ch), '08b')
        if len(bits) > 8:
            raise ValueError("Используйте символы с кодом до 255 (обычный текст).")
        blocks.append(hamming_encode_8bits(bits.zfill(8)))
    return blocks


def decode_hamming_blocks(blocks):
    decoded_bits = []
    corrected_blocks = []
    errors = []

    for block in blocks:
        data_bits, corrected, err = hamming_decode_12bits(block)
        decoded_bits.append(data_bits)
        corrected_blocks.append(corrected)
        errors.append(err)

    text = ''.join(chr(int(bits, 2)) for bits in decoded_bits)
    return text, corrected_blocks, errors


def parse_hamming_blocks(s: str):
    s = s.strip()
    if not s:
        return []

    parts = s.replace(',', ' ').split()
    blocks = []
    for part in parts:
        if len(part) != 12 or any(ch not in '01' for ch in part):
            raise ValueError(f"Некорректный блок: {part}. Ожидается 12 бит.")
        blocks.append(part)
    return blocks


# =========================
# Базовые UI-компоненты
# =========================

class BaseMethodFrame(ttk.Frame):
    def __init__(self, parent, title_text, hint_text, input_default="ПРИВЕТ"):
        super().__init__(parent)
        self._build_base_ui(title_text, hint_text, input_default)

    def _build_base_ui(self, title_text, hint_text, input_default):
        pad = {"padx": 10, "pady": 6}

        top = ttk.Frame(self)
        top.pack(fill="x", **pad)

        ttk.Label(top, text=title_text, font=("Segoe UI", 12, "bold")).pack(anchor="w")
        ttk.Label(top, text=hint_text).pack(anchor="w", pady=(4, 0))

        self.top_extra = ttk.Frame(self)
        self.top_extra.pack(fill="x", **pad)

        self.keys_frame = ttk.LabelFrame(self, text="Информация / ключи")
        self.keys_frame.pack(fill="x", **pad)

        self.keys_text = tk.Text(self.keys_frame, height=9, wrap="word")
        self.keys_text.pack(fill="x", padx=10, pady=10)

        body = ttk.Frame(self)
        body.pack(fill="both", expand=True, **pad)

        left = ttk.LabelFrame(body, text="Исходные данные")
        right = ttk.LabelFrame(body, text="Результат")

        left.pack(side="left", fill="both", expand=True, padx=(0, 6))
        right.pack(side="left", fill="both", expand=True, padx=(6, 0))

        self.input_text = tk.Text(left, height=14, wrap="word")
        self.input_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.input_text.insert("1.0", input_default)

        self.left_btns = ttk.Frame(left)
        self.left_btns.pack(fill="x", padx=10, pady=(0, 10))

        self.right_top_label = ttk.Label(right, text="Шифртекст / код:")
        self.right_top_label.pack(anchor="w", padx=10, pady=(10, 0))

        self.cipher_text = tk.Text(right, height=10, wrap="word")
        self.cipher_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.right_btns = ttk.Frame(right)
        self.right_btns.pack(fill="x", padx=10, pady=(0, 10))

        ttk.Label(right, text="Расшифрованный / декодированный текст:").pack(anchor="w", padx=10)
        self.output_text = tk.Text(right, height=8, wrap="word")
        self.output_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def clear_input(self):
        self.input_text.delete("1.0", "end")

    def copy_cipher(self):
        try:
            text = self.cipher_text.get("1.0", "end").strip()
            if not text:
                raise ValueError("Нет данных для копирования.")
            self.clipboard_clear()
            self.clipboard_append(text)
            self.update()
            messagebox.showinfo("Скопировано", "Данные скопированы в буфер обмена.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))


# =========================
# Вкладки / панели методов
# =========================

class RSAFrame(BaseMethodFrame):
    def __init__(self, parent):
        self.public_key = None
        self.private_key = None
        self.meta = None
        super().__init__(parent, "RSA", "Введите p и q, затем выполните шифрование и расшифрование.",
                         "Привет, RSA!")

        pq = ttk.Frame(self.top_extra)
        pq.pack(fill="x")

        ttk.Label(pq, text="p:").grid(row=0, column=0, sticky="w")
        self.p_var = tk.StringVar(value="3557")
        ttk.Entry(pq, textvariable=self.p_var, width=18).grid(row=0, column=1, sticky="w", padx=(4, 16))

        ttk.Label(pq, text="q:").grid(row=0, column=2, sticky="w")
        self.q_var = tk.StringVar(value="2579")
        ttk.Entry(pq, textvariable=self.q_var, width=18).grid(row=0, column=3, sticky="w", padx=(4, 16))

        ttk.Button(pq, text="Сгенерировать ключи", command=self.on_generate).grid(row=0, column=4, sticky="w")

        ttk.Button(self.left_btns, text="Зашифровать →", command=self.on_encrypt).pack(side="left")
        ttk.Button(self.left_btns, text="Очистить", command=self.clear_input).pack(side="left", padx=8)

        ttk.Button(self.right_btns, text="Расшифровать ↓", command=self.on_decrypt).pack(side="left")
        ttk.Button(self.right_btns, text="Копировать", command=self.copy_cipher).pack(side="left", padx=8)

    def on_generate(self):
        try:
            p = int(self.p_var.get().strip())
            q = int(self.q_var.get().strip())
            pub, priv, meta = rsa_generate_keys(p, q)
            self.public_key, self.private_key, self.meta = pub, priv, meta

            self.keys_text.delete("1.0", "end")
            self.keys_text.insert(
                "1.0",
                f"Public key (e, n): {pub}\n"
                f"Private key (d, n): {priv}\n"
                f"n = {meta['n']}\n"
                f"φ(n) = {meta['phi']}\n"
                f"p = {meta['p']}, q = {meta['q']}"
            )
            messagebox.showinfo("Готово", "Ключи сгенерированы.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def on_encrypt(self):
        try:
            if not self.public_key:
                self.on_generate()
                if not self.public_key:
                    return
            text = self.input_text.get("1.0", "end").rstrip("\n")
            blocks = rsa_encrypt_text(text, self.public_key)
            self.cipher_text.delete("1.0", "end")
            self.cipher_text.insert("1.0", " ".join(str(x) for x in blocks))
        except Exception as e:
            messagebox.showerror("Ошибка шифрования", str(e))

    def on_decrypt(self):
        try:
            if not self.private_key:
                raise ValueError("Сначала сгенерируйте ключи.")
            blocks = parse_int_blocks(self.cipher_text.get("1.0", "end"))
            text = rsa_decrypt_blocks(blocks, self.private_key)
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", text)
        except Exception as e:
            messagebox.showerror("Ошибка расшифрования", str(e))


class AVKRFrame(BaseMethodFrame):
    def __init__(self, parent):
        self.crypto = AdditiveKnapsack()
        super().__init__(parent, "АВКР", "Русский текст транслитерируется в латиницу.",
                         "ПРИВЕТ")

        ttk.Button(self.top_extra, text="Сгенерировать ключи", command=self.on_generate_keys).pack(anchor="w")

        ttk.Button(self.left_btns, text="Зашифровать →", command=self.on_encrypt).pack(side="left")
        ttk.Button(self.left_btns, text="Очистить", command=self.clear_input).pack(side="left", padx=8)

        ttk.Button(self.right_btns, text="Расшифровать ↓", command=self.on_decrypt).pack(side="left")
        ttk.Button(self.right_btns, text="Копировать", command=self.copy_cipher).pack(side="left", padx=8)

    def on_generate_keys(self):
        try:
            self.crypto.generate_keys()
            self.keys_text.delete("1.0", "end")
            self.keys_text.insert("1.0", self.crypto.get_info())
            messagebox.showinfo("Готово", "Ключи успешно сгенерированы.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def on_encrypt(self):
        try:
            if not self.crypto.keys_generated:
                self.on_generate_keys()
            text = self.input_text.get("1.0", "end").strip()
            encrypted = self.crypto.encrypt(text)
            self.cipher_text.delete("1.0", "end")
            self.cipher_text.insert("1.0", " ".join(str(x) for x in encrypted))
        except Exception as e:
            messagebox.showerror("Ошибка шифрования", str(e))

    def on_decrypt(self):
        try:
            if not self.crypto.keys_generated:
                raise ValueError("Сначала сгенерируйте ключи.")
            encrypted = parse_int_blocks(self.cipher_text.get("1.0", "end"))
            decrypted = self.crypto.decrypt(encrypted)
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", decrypted)
        except Exception as e:
            messagebox.showerror("Ошибка дешифрования", str(e))


class MVKRFrame(BaseMethodFrame):
    def __init__(self, parent):
        self.crypto = MultiplicativeKnapsack()
        super().__init__(parent, "МВКР", "Русский текст транслитерируется в латиницу.",
                         "ПРИВЕТ")

        ttk.Button(self.top_extra, text="Сгенерировать ключи", command=self.on_generate_keys).pack(anchor="w")

        ttk.Button(self.left_btns, text="Зашифровать →", command=self.on_encrypt).pack(side="left")
        ttk.Button(self.left_btns, text="Очистить", command=self.clear_input).pack(side="left", padx=8)

        ttk.Button(self.right_btns, text="Расшифровать ↓", command=self.on_decrypt).pack(side="left")
        ttk.Button(self.right_btns, text="Копировать", command=self.copy_cipher).pack(side="left", padx=8)

    def on_generate_keys(self):
        try:
            self.crypto.generate_keys()
            self.keys_text.delete("1.0", "end")
            self.keys_text.insert("1.0", self.crypto.get_info())
            messagebox.showinfo("Готово", "Ключи успешно сгенерированы.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def on_encrypt(self):
        try:
            if not self.crypto.keys_generated:
                self.on_generate_keys()
            text = self.input_text.get("1.0", "end").strip()
            encrypted = self.crypto.encrypt(text)
            self.cipher_text.delete("1.0", "end")
            self.cipher_text.insert("1.0", " ".join(str(x) for x in encrypted))
        except Exception as e:
            messagebox.showerror("Ошибка шифрования", str(e))

    def on_decrypt(self):
        try:
            if not self.crypto.keys_generated:
                raise ValueError("Сначала сгенерируйте ключи.")
            encrypted = parse_int_blocks(self.cipher_text.get("1.0", "end"))
            decrypted = self.crypto.decrypt(encrypted)
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", decrypted)
        except Exception as e:
            messagebox.showerror("Ошибка дешифрования", str(e))


class GAVKRFrame(BaseMethodFrame):
    def __init__(self, parent):
        self.crypto = GeneralizedAdditiveKnapsack(base=3)
        super().__init__(parent, "ГАВКР", "Русский алфавит, троичное кодирование.",
                         "ПРИВЕТ")

        ttk.Button(self.top_extra, text="Сгенерировать ключи", command=self.on_generate_keys).pack(anchor="w")

        ttk.Button(self.left_btns, text="Зашифровать →", command=self.on_encrypt).pack(side="left")
        ttk.Button(self.left_btns, text="Очистить", command=self.clear_input).pack(side="left", padx=8)

        ttk.Button(self.right_btns, text="Расшифровать ↓", command=self.on_decrypt).pack(side="left")
        ttk.Button(self.right_btns, text="Копировать", command=self.copy_cipher).pack(side="left", padx=8)

    def on_generate_keys(self):
        try:
            self.crypto.generate_keys()
            self.keys_text.delete("1.0", "end")
            self.keys_text.insert("1.0", self.crypto.get_info())
            messagebox.showinfo("Готово", "Ключи успешно сгенерированы.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def on_encrypt(self):
        try:
            if not self.crypto.keys_generated:
                self.on_generate_keys()
            text = self.input_text.get("1.0", "end").strip()
            encrypted = self.crypto.encrypt(text)
            self.cipher_text.delete("1.0", "end")
            self.cipher_text.insert("1.0", " ".join(str(x) for x in encrypted))
        except Exception as e:
            messagebox.showerror("Ошибка шифрования", str(e))

    def on_decrypt(self):
        try:
            if not self.crypto.keys_generated:
                raise ValueError("Сначала сгенерируйте ключи.")
            encrypted = parse_int_blocks(self.cipher_text.get("1.0", "end"))
            decrypted = self.crypto.decrypt(encrypted)
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", decrypted)
        except Exception as e:
            messagebox.showerror("Ошибка дешифрования", str(e))


class GMVKRFrame(BaseMethodFrame):
    def __init__(self, parent):
        self.crypto = GeneralizedMultiplicativeKnapsack(base=5, n=3)
        super().__init__(parent, "ГМВКР", "Русский алфавит, p = 5, n = 3.",
                         "ПРИВЕТ")

        ttk.Button(self.top_extra, text="Сгенерировать ключи", command=self.on_generate_keys).pack(anchor="w")

        ttk.Button(self.left_btns, text="Зашифровать →", command=self.on_encrypt).pack(side="left")
        ttk.Button(self.left_btns, text="Очистить", command=self.clear_input).pack(side="left", padx=8)

        ttk.Button(self.right_btns, text="Расшифровать ↓", command=self.on_decrypt).pack(side="left")
        ttk.Button(self.right_btns, text="Копировать", command=self.copy_cipher).pack(side="left", padx=8)

    def on_generate_keys(self):
        try:
            self.crypto.generate_keys()
            self.keys_text.delete("1.0", "end")
            self.keys_text.insert("1.0", self.crypto.get_info())
            messagebox.showinfo("Готово", "Ключи успешно сгенерированы.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def on_encrypt(self):
        try:
            if not self.crypto.keys_generated:
                self.on_generate_keys()
            text = self.input_text.get("1.0", "end").strip()
            encrypted = self.crypto.encrypt(text)
            self.cipher_text.delete("1.0", "end")
            self.cipher_text.insert("1.0", " ".join(str(x) for x in encrypted))
        except Exception as e:
            messagebox.showerror("Ошибка шифрования", str(e))

    def on_decrypt(self):
        try:
            if not self.crypto.keys_generated:
                raise ValueError("Сначала сгенерируйте ключи.")
            encrypted = parse_int_blocks(self.cipher_text.get("1.0", "end"))
            decrypted = self.crypto.decrypt(encrypted)
            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", decrypted)
        except Exception as e:
            messagebox.showerror("Ошибка дешифрования", str(e))


class HammingFrame(BaseMethodFrame):
    def __init__(self, parent):
        super().__init__(parent, "Код Хэмминга", "Реализация Hamming (12,8) с исправлением одной ошибки.",
                         "HELLO")

        self.keys_text.delete("1.0", "end")
        self.keys_text.insert(
            "1.0",
            "Код Хэмминга (12,8):\n"
            "Каждый символ представляется 8 битами и кодируется в 12-битное слово.\n"
            "Программа умеет обнаруживать и исправлять одну ошибку в каждом блоке."
        )

        ttk.Button(self.left_btns, text="Закодировать →", command=self.on_encode).pack(side="left")
        ttk.Button(self.left_btns, text="Очистить", command=self.clear_input).pack(side="left", padx=8)

        ttk.Button(self.right_btns, text="Декодировать ↓", command=self.on_decode).pack(side="left")
        ttk.Button(self.right_btns, text="Копировать", command=self.copy_cipher).pack(side="left", padx=8)

        self.extra_label = ttk.Label(self, text="Информация об ошибках:")
        self.extra_label.pack(anchor="w", padx=20, pady=(0, 0))

        self.error_info = tk.Text(self, height=6, wrap="word")
        self.error_info.pack(fill="x", padx=20, pady=(0, 10))

    def on_encode(self):
        try:
            text = self.input_text.get("1.0", "end").rstrip("\n")
            if not text:
                raise ValueError("Введите текст для кодирования.")
            blocks = encode_text_hamming(text)
            self.cipher_text.delete("1.0", "end")
            self.cipher_text.insert("1.0", " ".join(blocks))
            self.output_text.delete("1.0", "end")
            self.error_info.delete("1.0", "end")
        except Exception as e:
            messagebox.showerror("Ошибка кодирования", str(e))

    def on_decode(self):
        try:
            raw = self.cipher_text.get("1.0", "end").strip()
            blocks = parse_hamming_blocks(raw)
            text, corrected_blocks, errors = decode_hamming_blocks(blocks)

            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", text)

            lines = []
            for i, err in enumerate(errors, start=1):
                if err == 0:
                    lines.append(f"Блок {i}: ошибок не обнаружено")
                else:
                    lines.append(f"Блок {i}: исправлена ошибка в позиции {err}")

            self.error_info.delete("1.0", "end")
            self.error_info.insert(
                "1.0",
                "Исправленные блоки:\n"
                + " ".join(corrected_blocks)
                + "\n\n"
                + "\n".join(lines)
            )
        except Exception as e:
            messagebox.showerror("Ошибка декодирования", str(e))


# =========================
# Главное приложение
# =========================

class CryptoSuiteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Криптографические алгоритмы — единое приложение")
        self.geometry("1180x780")
        self.minsize(1050, 720)

        self.frames = {}
        self.buttons = {}

        self._build_ui()

    def _build_ui(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)

        ttk.Label(
            top,
            text="Единое приложение для лабораторных работ по защите информации",
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w")

        ttk.Label(
            top,
            text="Выберите алгоритм кнопкой сверху."
        ).pack(anchor="w", pady=(3, 8))

        self.nav = ttk.Frame(self)
        self.nav.pack(fill="x", padx=10, pady=(0, 10))

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        methods = [
            ("RSA", RSAFrame),
            ("АВКР", AVKRFrame),
            ("МВКР", MVKRFrame),
            ("ГАВКР", GAVKRFrame),
            ("ГМВКР", GMVKRFrame),
            ("Код Хэмминга", HammingFrame),
        ]

        for name, frame_cls in methods:
            btn = ttk.Button(self.nav, text=name, command=lambda n=name: self.show_frame(n))
            btn.pack(side="left", padx=4)
            self.buttons[name] = btn

            frame = frame_cls(container)
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.frames[name] = frame

        self.show_frame("RSA")

    def show_frame(self, name: str):
        frame = self.frames[name]
        frame.tkraise()


if __name__ == "__main__":
    app = CryptoSuiteApp()
    app.mainloop()