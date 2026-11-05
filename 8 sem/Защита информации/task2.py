import tkinter as tk
from tkinter import ttk, messagebox
import random
import math


def egcd(a, b):
    """Расширенный алгоритм Евклида"""
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y


def modinv(a, m):
    """Обратный элемент a по модулю m"""
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("Обратный элемент не существует")
    return x % m


class LatinAlphabet:
    """
    Латинский алфавит для АВКР:
    A=1, B=2, ..., Z=26, _=27
    """
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
        result = ""
        for n in numbers:
            result += self.num_to_char.get(n, "?")
        return result


class AdditiveKnapsack:
    """
    Классический аддитивный рюкзак (АВКР)

    Схема:
    1) Генерируем сверхрастущий секретный вектор A'
    2) Выбираем m > sum(A')
    3) Выбираем w, взаимно простое с m
    4) Строим открытый ключ A: a_i = (w * a'_i) mod m
    5) Шифрование: сумма по открытому ключу
    6) Дешифрование: умножаем на w^(-1) mod m и применяем жадный алгоритм
    """

    def __init__(self):
        self.n = 8
        self.superincreasing = None
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
            'Ь': '', 'Э': 'E', 'Ю': 'YU', 'Я': 'YA', ' ': '_'
        }

    def translit(self, text):
        """
        Перевод русского текста в латиницу,
        потому что в учебном варианте АВКР используется латинский алфавит.
        """
        result = ""
        for ch in text.upper():
            result += self.rus_to_lat.get(ch, ch)
        return result

    def generate_superincreasing(self):
        """Генерация сверхрастущего вектора длины 8"""
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
        """Число -> 8-битный вектор"""
        bits = [0] * self.n
        for i in range(self.n):
            bits[i] = (num >> i) & 1
        return bits

    def bits_to_number(self, bits):
        """8-битный вектор -> число"""
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

        latin_text = self.translit(message)
        return [self.encrypt_char(ch) for ch in latin_text]

    def decrypt(self, encrypted):
        if not self.keys_generated:
            raise ValueError("Сначала сгенерируйте ключи")

        return "".join(self.decrypt_char(x) for x in encrypted)

    def get_info(self):
        if not self.keys_generated:
            return "Ключи не сгенерированы"

        return (
            f"АВКР - Классический аддитивный рюкзак\n\n"
            f"Размерность n = {self.n}\n"
            f"Секретный сверхрастущий вектор A' = {self.superincreasing}\n"
            f"Модуль m = {self.m}\n"
            f"Множитель w = {self.w}\n"
            f"Обратный элемент w^(-1) mod m = {self.w_inv}\n"
            f"Открытый ключ A = {self.public_key}"
        )


class AVKRApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("АВКР — классический аддитивный рюкзак")
        self.geometry("980x650")

        self.crypto = AdditiveKnapsack()
        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 10, "pady": 6}

        top = ttk.Frame(self)
        top.pack(fill="x", **pad)

        ttk.Label(
            top,
            text="АВКР — классический аддитивный рюкзак",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        ttk.Label(
            top,
            text="Поддерживается ввод русского текста; перед шифрованием он транслитерируется в латиницу."
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
        left.pack(side="left", fill="both", expand=True, padx=(0, 6))

        self.input_text = tk.Text(left, height=14, wrap="word")
        self.input_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.input_text.insert("1.0", "ПРИВЕТ")

        left_btns = ttk.Frame(left)
        left_btns.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(left_btns, text="Зашифровать →", command=self.on_encrypt).pack(side="left")
        ttk.Button(left_btns, text="Очистить", command=self.clear_input).pack(side="left", padx=8)

        right = ttk.LabelFrame(body, text="Шифртекст и дешифрование")
        right.pack(side="left", fill="both", expand=True, padx=(6, 0))

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
    app = AVKRApp()
    app.mainloop()