import tkinter as tk
from tkinter import ttk, messagebox
import random
import math


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


class RussianAlphabet:
    """
    Русский алфавит:
    А=1, Б=2, ..., Я=33, _=34
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


class GMKP:
    """
    ГМВКР / GMKP — обобщённый мультипликативный рюкзак.

    Учебная схема:
    1) Выбирается секретная мультипликативно-сверхвозрастающая последовательность A
    2) Выбирается простое m > product(A)
    3) Шифрование: P = Π(a_i ^ e_i) mod m
    4) Дешифрование: по секретной последовательности восстанавливаются показатели e_i

    Здесь для наглядности:
    - base = 3, то есть коэффициенты e_i лежат в диапазоне 0..2
    - n = 4, этого хватает для кодирования русского алфавита:
      3^4 = 81 >= 34
    """

    def __init__(self, base: int = 3, n: int = 4):
        self.base = base
        self.n = n
        self.secret_sequence = None
        self.m = None
        self.keys_generated = False
        self.alphabet = RussianAlphabet()

    def generate_multiplicative_superincreasing(self):
        """
        Генерация мультипликативно-сверхвозрастающей последовательности:
        каждый следующий элемент больше произведения предыдущих.
        """
        seq = [2]
        current_product = 2

        while len(seq) < self.n:
            candidate = current_product + random.randint(1, 10)
            while not is_prime(candidate):
                candidate += 1
            seq.append(candidate)
            current_product *= candidate

        return seq

    def number_to_base_vector(self, num: int):
        """
        Число -> вектор коэффициентов по основанию base длины n.
        Младшие разряды идут первыми.
        """
        vec = [0] * self.n
        temp = num
        for i in range(self.n):
            vec[i] = temp % self.base
            temp //= self.base
        return vec

    def base_vector_to_number(self, vec):
        """
        Вектор коэффициентов -> число.
        Предполагается, что vec[0] — младший разряд.
        """
        num = 0
        power = 1
        for x in vec:
            num += x * power
            power *= self.base
        return num

    def generate_keys(self):
        self.secret_sequence = self.generate_multiplicative_superincreasing()

        product = 1
        for x in self.secret_sequence:
            product *= x

        self.m = product + 1
        while not is_prime(self.m):
            self.m += 1

        self.keys_generated = True

    def encrypt_char_num(self, num: int) -> int:
        """
        Шифрует номер символа через вектор показателей степени.
        P = Π(a_i ^ e_i) mod m
        """
        coeffs = self.number_to_base_vector(num)
        result = 1

        for i in range(self.n):
            if coeffs[i] > 0:
                result = (result * pow(self.secret_sequence[i], coeffs[i], self.m)) % self.m

        return result

    def decrypt_char_num(self, value: int) -> int:
        """
        Дешифрование:
        для учебной схемы раскладываем число по секретной последовательности.
        Так как последовательность мультипликативно-сверхвозрастающая,
        показатели e_i можно восстановить жадно.
        """
        coeffs = [0] * self.n
        remaining = value

        for i in range(self.n - 1, -1, -1):
            count = 0
            while remaining % self.secret_sequence[i] == 0 and count < self.base - 1:
                remaining //= self.secret_sequence[i]
                count += 1
            coeffs[i] = count

        return self.base_vector_to_number(coeffs)

    def encrypt(self, message: str):
        if not self.keys_generated:
            raise ValueError("Сначала сгенерируйте ключи.")

        numbers = self.alphabet.text_to_numbers(message)
        return [self.encrypt_char_num(num) for num in numbers]

    def decrypt(self, encrypted_blocks):
        if not self.keys_generated:
            raise ValueError("Сначала сгенерируйте ключи.")

        numbers = [self.decrypt_char_num(x) for x in encrypted_blocks]
        return self.alphabet.numbers_to_text(numbers)

    def get_info(self):
        if not self.keys_generated:
            return "Ключи не сгенерированы."

        product = 1
        for x in self.secret_sequence:
            product *= x

        return (
            f"ГМВКР / GMKP — обобщённый мультипликативный рюкзак\n\n"
            f"Основание p = {self.base}\n"
            f"Размерность n = {self.n}\n"
            f"Секретная мультипликативно-сверхвозрастающая последовательность A = {self.secret_sequence}\n"
            f"Произведение элементов A = {product}\n"
            f"Модуль m = {self.m}\n"
            f"Шифрование: P = Π(a_i ^ e_i) mod m"
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


class GMKPApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ГМВКР / GMKP — обобщённый мультипликативный рюкзак")
        self.geometry("980x650")

        self.crypto = GMKP(base=3, n=4)
        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 10, "pady": 6}

        top = ttk.Frame(self)
        top.pack(fill="x", **pad)

        ttk.Label(
            top,
            text="ГМВКР / GMKP — обобщённый мультипликативный рюкзак",
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
    app = GMKPApp()
    app.mainloop()