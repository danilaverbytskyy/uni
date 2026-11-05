import tkinter as tk
from tkinter import ttk, messagebox
import random
import math


def egcd(a: int, b: int):
    """Расширенный алгоритм Евклида."""
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y


def modinv(a: int, m: int) -> int:
    """Обратный элемент a по модулю m."""
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("Обратный элемент не существует")
    return x % m


def is_prime(n: int) -> bool:
    """Проверка числа на простоту."""
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


class LatinAlphabet:
    """
    Латинский алфавит для рюкзачных шифров:
    A=1, B=2, ..., Z=26, _=27
    """
    def __init__(self):
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"
        self.char_to_num = {}
        self.num_to_char = {}

        for i, ch in enumerate(self.alphabet, start=1):
            self.char_to_num[ch] = i
            self.num_to_char[i] = ch


class MultiplicativeKnapsack:
    """
    МВКР — классический мультипликативный рюкзак

    Схема:
    1) Выбирается секретный вектор простых чисел P = (p1, ..., pn)
    2) Выбирается простое m > произведения всех pi
    3) Выбирается w, взаимно простое с (m - 1)
    4) Строится открытый ключ A: ai = pi^w mod m
    5) Шифрование: произведение элементов открытого ключа по битам
    6) Дешифрование: c' = c^(w^(-1)) mod m, затем факторизация по секретным pi
    """

    def __init__(self):
        self.n = 5
        self.primes = None
        self.m = None
        self.w = None
        self.w_inv = None
        self.public_key = None
        self.keys_generated = False

        self.alphabet = LatinAlphabet()
        self.rus_to_lat = {
            'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E',
            'Ё': 'E', 'Ж': 'ZH', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K',
            'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
            'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'KH', 'Ц': 'TS',
            'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH', 'Ъ': '', 'Ы': 'Y',
            'Ь': '', 'Э': 'E', 'Ю': 'YU', 'Я': 'YA', ' ': '_', '_': '_'
        }

    def translit(self, text: str) -> str:
        """Транслитерация русского текста в латиницу."""
        result = ""
        for ch in text.upper():
            result += self.rus_to_lat.get(ch, ch)
        return result

    def generate_prime_vector(self):
        """Генерация 5 простых чисел для секретного вектора."""
        primes = []
        candidate = 2
        while len(primes) < self.n:
            if is_prime(candidate):
                primes.append(candidate)
            candidate += 1
        return primes

    def number_to_bits(self, num: int):
        """Число -> 5-битный массив."""
        bits = [0] * self.n
        for i in range(self.n):
            bits[i] = (num >> i) & 1
        return bits

    def bits_to_number(self, bits):
        """5-битный массив -> число."""
        num = 0
        for i in range(self.n):
            if bits[i]:
                num |= (1 << i)
        return num

    def generate_keys(self):
        """
        Генерация ключей МВКР.
        """
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
        """
        Шифрование одного символа.
        """
        num = self.alphabet.char_to_num.get(ch, 27)
        bits = self.number_to_bits(num)

        result = 1
        for i in range(self.n):
            if bits[i]:
                result = (result * self.public_key[i]) % self.m
        return result

    def decrypt_char(self, value: int) -> str:
        """
        Дешифрование одного числа.
        """
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
        """Шифрует сообщение."""
        if not self.keys_generated:
            raise ValueError("Сначала сгенерируйте ключи")

        latin_text = self.translit(message)
        return [self.encrypt_char(ch) for ch in latin_text]

    def decrypt(self, encrypted):
        """Дешифрует сообщение."""
        if not self.keys_generated:
            raise ValueError("Сначала сгенерируйте ключи")

        return "".join(self.decrypt_char(x) for x in encrypted)

    def get_info(self):
        if not self.keys_generated:
            return "Ключи не сгенерированы"

        return (
            f"МВКР — мультипликативный рюкзак\n\n"
            f"Размерность n = {self.n}\n"
            f"Секретные простые числа P = {self.primes}\n"
            f"Секретный модуль m = {self.m}\n"
            f"Секретный множитель w = {self.w}\n"
            f"Обратный элемент w^(-1) mod (m-1) = {self.w_inv}\n"
            f"Открытый ключ A = {self.public_key}"
        )


class MVKRApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("МВКР — классический мультипликативный рюкзак")
        self.geometry("980x650")

        self.crypto = MultiplicativeKnapsack()
        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 10, "pady": 6}

        top = ttk.Frame(self)
        top.pack(fill="x", **pad)

        ttk.Label(
            top,
            text="МВКР — классический мультипликативный рюкзак",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        ttk.Label(
            top,
            text="Русский текст автоматически транслитерируется в латиницу перед шифрованием."
        ).pack(anchor="w", pady=(4, 0))

        ttk.Button(
            top,
            text="Сгенерировать ключи",
            command=self.on_generate_keys
        ).pack(anchor="w", pady=(8, 0))

        keys_frame = ttk.LabelFrame(self, text="Информация о ключах")
        keys_frame.pack(fill="x", **pad)

        self.keys_text = tk.Text(keys_frame, height=10, wrap="word")
        self.keys_text.pack(fill="x", padx=10, pady=10)

        body = ttk.Frame(self)
        body.pack(fill="both", expand=True, **pad)

        left = ttk.LabelFrame(body, text="Исходное сообщение")
        right = ttk.LabelFrame(body, text="Шифртекст и дешифрование")

        left.pack(side="left", fill="both", expand=True, padx=(0, 6))
        right.pack(side="left", fill="both", expand=True, padx=(6, 0))

        self.input_text = tk.Text(left, height=14, wrap="word")
        self.input_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.input_text.insert("1.0", "ПРИВЕТ")

        left_btns = ttk.Frame(left)
        left_btns.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(left_btns, text="Зашифровать →", command=self.on_encrypt).pack(side="left")
        ttk.Button(left_btns, text="Очистить", command=self.clear_input).pack(side="left", padx=8)

        ttk.Label(right, text="Шифртекст (последовательность чисел):").pack(anchor="w", padx=10, pady=(10, 0))
        self.cipher_text = tk.Text(right, height=10, wrap="word")
        self.cipher_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        right_btns = ttk.Frame(right)
        right_btns.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(right_btns, text="Расшифровать ↓", command=self.on_decrypt).pack(side="left")
        ttk.Button(right_btns, text="Копировать", command=self.copy_cipher).pack(side="left", padx=8)

        ttk.Label(right, text="Расшифрованный текст:").pack(anchor="w", padx=10, pady=(0, 0))
        self.output_text = tk.Text(right, height=10, wrap="word")
        self.output_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

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
            if not text:
                raise ValueError("Введите текст для шифрования.")

            encrypted = self.crypto.encrypt(text)
            cipher_str = " ".join(str(x) for x in encrypted)

            self.cipher_text.delete("1.0", "end")
            self.cipher_text.insert("1.0", cipher_str)
        except Exception as e:
            messagebox.showerror("Ошибка шифрования", str(e))

    def on_decrypt(self):
        try:
            if not self.crypto.keys_generated:
                raise ValueError("Сначала сгенерируйте ключи.")

            raw = self.cipher_text.get("1.0", "end").strip()
            if not raw:
                raise ValueError("Введите или получите шифртекст.")

            encrypted = [int(x) for x in raw.replace(",", " ").split()]
            decrypted = self.crypto.decrypt(encrypted)

            self.output_text.delete("1.0", "end")
            self.output_text.insert("1.0", decrypted)
        except Exception as e:
            messagebox.showerror("Ошибка дешифрования", str(e))

    def copy_cipher(self):
        try:
            text = self.cipher_text.get("1.0", "end").strip()
            if not text:
                raise ValueError("Нет шифртекста для копирования.")

            self.clipboard_clear()
            self.clipboard_append(text)
            self.update()
            messagebox.showinfo("Скопировано", "Шифртекст скопирован в буфер обмена.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def clear_input(self):
        self.input_text.delete("1.0", "end")


if __name__ == "__main__":
    app = MVKRApp()
    app.mainloop()