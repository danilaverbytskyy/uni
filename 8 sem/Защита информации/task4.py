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


class RussianAlphabet:
    """
    Русский алфавит:
    А=1, Б=2, ..., Я=33
    Пробел заменяем на '_' и тоже кодируем как 33.
    """
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


class GeneralizedAdditiveKnapsack:
    """
    ГАВКР — обобщённый аддитивный рюкзак (p = 3)

    Схема:
    1) Генерируем обобщённо-сверхрастущий вектор A'
    2) Выбираем m > (p-1) * sum(A')
    3) Выбираем w, взаимно простое с m
    4) Строим открытый ключ A: a_i = (w * a'_i) mod m
    5) Буква -> число -> троичный вектор длины 4
    6) Шифрование: V = Σ(alpha_i * a_i)
    7) Дешифрование: V' = (V * w^(-1)) mod m, затем жадное восстановление троичного кода
    """

    def __init__(self, base: int = 3):
        self.base = base
        self.n = 4  # 3^4 = 81 >= 34
        self.superincreasing = None
        self.m = None
        self.w = None
        self.w_inv = None
        self.public_key = None
        self.keys_generated = False
        self.alphabet = RussianAlphabet()

    def generate_superincreasing(self):
        """
        Генерация обобщённо-сверхрастущего вектора.
        Условие:
            a_j > (p - 1) * (a_1 + ... + a_{j-1})
        """
        vector = [random.randint(1, 5)]
        for _ in range(1, self.n):
            min_val = (self.base - 1) * sum(vector) + 1
            vector.append(min_val + random.randint(0, 5))
        return vector

    def number_to_base_vector(self, num: int):
        """
        Число -> троичный вектор длины 4.
        Младшие разряды идут первыми.
        """
        if num < 0:
            raise ValueError("Число должно быть неотрицательным")

        vector = [0] * self.n
        temp = num
        for i in range(self.n):
            vector[i] = temp % self.base
            temp //= self.base
        return vector

    def base_vector_to_number(self, vector):
        """
        Троичный вектор длины 4 -> число.
        Предполагается, что vector[0] — младший разряд.
        """
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
        """Шифрование одного числового символа."""
        digits = self.number_to_base_vector(num)
        result = 0
        for i in range(self.n):
            result += digits[i] * self.public_key[i]
        return result

    def decrypt_char_num(self, value: int) -> int:
        """Дешифрование одного числа в номер символа."""
        v_prime = (value * self.w_inv) % self.m

        digits = [0] * self.n
        remaining = v_prime

        for i in range(self.n - 1, -1, -1):
            coeff = min(self.base - 1, remaining // self.superincreasing[i])
            digits[i] = coeff
            remaining -= coeff * self.superincreasing[i]

        num = self.base_vector_to_number(digits)
        return num

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


def parse_cipher_blocks(s: str):
    s = s.strip()
    if not s:
        return []
    parts = [p for p in s.replace(",", " ").split() if p]
    blocks = []
    for p in parts:
        try:
            blocks.append(int(p))
        except ValueError:
            raise ValueError(f"Некорректный блок: {p}")
    return blocks


class GAVKRApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ГАВКР — обобщённый аддитивный рюкзак")
        self.geometry("980x650")

        self.crypto = GeneralizedAdditiveKnapsack(base=3)
        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 10, "pady": 6}

        top = ttk.Frame(self)
        top.pack(fill="x", **pad)

        ttk.Label(
            top,
            text="ГАВКР — обобщённый аддитивный рюкзак (p = 3)",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        ttk.Label(
            top,
            text="Используется русский алфавит. Пробелы автоматически заменяются на '_'."
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

            encrypted = parse_cipher_blocks(raw)
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
    app = GAVKRApp()
    app.mainloop()