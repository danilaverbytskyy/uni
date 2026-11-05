import tkinter as tk
from tkinter import ttk, messagebox
from math import gcd


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


def egcd(a: int, b: int):
    if b == 0:
        return (a, 1, 0)
    g, x1, y1 = egcd(b, a % b)
    return (g, y1, x1 - (a // b) * y1)


def modinv(a: int, m: int) -> int:
    g, x, _ = egcd(a, m)
    if g != 1:
        raise ValueError("Обратного элемента не существует (gcd != 1)")
    return x % m


def choose_e(phi: int) -> int:
    """
    Выбор e.
    Пытаемся 65537, иначе находим небольшое нечётное e, взаимно простое с phi.
    """
    preferred = 65537
    if preferred < phi and gcd(preferred, phi) == 1:
        return preferred
    e = 3
    while e < phi:
        if gcd(e, phi) == 1:
            return e
        e += 2
    raise ValueError("Не удалось подобрать e")


def generate_keys(p: int, q: int):
    """
    Генерация ключей RSA по двум простым числам p и q.

    Возвращает:
        (public_key, private_key, meta)
    где public_key=(e,n), private_key=(d,n), meta=dict(n=...,phi=...)
    """
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
    """Шифрование одного блока-числа."""
    if not (0 <= m < n):
        raise ValueError("Блок сообщения должен быть в диапазоне 0 <= m < n")
    return pow(m, e, n)


def rsa_decrypt_int(c: int, d: int, n: int) -> int:
    """Расшифрование одного блока-числа."""
    if not (0 <= c < n):
        raise ValueError("Блок шифртекста должен быть в диапазоне 0 <= c < n")
    return pow(c, d, n)


def encrypt_text_to_cipher_list(text: str, public_key):
    """
    Каждый символ шифруется отдельно как число ord(ch).
    Возвращает список целых чисел (cipher blocks).
    """
    e, n = public_key
    blocks = []
    for ch in text:
        m = ord(ch)
        if m >= n:
            raise ValueError(
                "n слишком маленькое для выбранной кодировки символов.\n"
                "Увеличьте p и q (чтобы n > 1114111 для Unicode),\n"
                "или используйте ASCII-текст и n > 127."
            )
        blocks.append(rsa_encrypt_int(m, e, n))
    return blocks


def decrypt_cipher_list_to_text(blocks, private_key):
    """Обратная операция: список чисел -> строка."""
    d, n = private_key
    chars = []
    for c in blocks:
        m = rsa_decrypt_int(c, d, n)
        chars.append(chr(m))
    return "".join(chars)


def parse_cipher_blocks(s: str):
    """
    Парсер списка блоков из строки.
    Ожидаем формат: числа, разделённые пробелами или запятыми.
    """
    s = s.strip()
    if not s:
        return []
    parts = [p for p in s.replace(",", " ").split() if p]
    blocks = []
    for p in parts:
        if not p.isdigit():
            raise ValueError(f"Некорректный блок: {p}")
        blocks.append(int(p))
    return blocks


class RSAApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("RSA")
        self.geometry("980x620")

        self.public_key = None
        self.private_key = None
        self.meta = None

        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 10, "pady": 6}

        top = ttk.Frame(self)
        top.pack(fill="x", **pad)

        ttk.Label(top, text="Введите два простых числа p и q:", font=("Segoe UI", 11, "bold")).pack(anchor="w")

        pq = ttk.Frame(top)
        pq.pack(fill="x", pady=4)

        ttk.Label(pq, text="p:").grid(row=0, column=0, sticky="w")
        self.p_var = tk.StringVar(value="61")
        ttk.Entry(pq, textvariable=self.p_var, width=18).grid(row=0, column=1, sticky="w", padx=(4, 16))

        ttk.Label(pq, text="q:").grid(row=0, column=2, sticky="w")
        self.q_var = tk.StringVar(value="53")
        ttk.Entry(pq, textvariable=self.q_var, width=18).grid(row=0, column=3, sticky="w", padx=(4, 16))

        ttk.Button(pq, text="Сгенерировать ключи", command=self.on_generate).grid(row=0, column=4, sticky="w")

        keys = ttk.LabelFrame(self, text="Ключи")
        keys.pack(fill="x", **pad)

        self.pub_text = tk.Text(keys, height=2, wrap="word")
        self.priv_text = tk.Text(keys, height=2, wrap="word")
        self.meta_text = tk.Text(keys, height=2, wrap="word")
        for t in (self.pub_text, self.priv_text, self.meta_text):
            t.configure(state="disabled")

        ttk.Label(keys, text="Public key (e, n):").pack(anchor="w", padx=10, pady=(8, 0))
        self.pub_text.pack(fill="x", padx=10)
        ttk.Label(keys, text="Private key (d, n):").pack(anchor="w", padx=10, pady=(8, 0))
        self.priv_text.pack(fill="x", padx=10)
        ttk.Label(keys, text="Доп. значения (n, φ(n))").pack(anchor="w", padx=10, pady=(8, 0))
        self.meta_text.pack(fill="x", padx=10, pady=(0, 10))

        body = ttk.Frame(self)
        body.pack(fill="both", expand=True, **pad)

        left = ttk.LabelFrame(body, text="Сообщение (ввод)")
        right = ttk.LabelFrame(body, text="Шифртекст и результат")

        left.pack(side="left", fill="both", expand=True, padx=(0, 6))
        right.pack(side="left", fill="both", expand=True, padx=(6, 0))

        self.msg_in = tk.Text(left, height=12, wrap="word")
        self.msg_in.pack(fill="both", expand=True, padx=10, pady=10)
        self.msg_in.insert("1.0", "Привет, RSA!")

        btns = ttk.Frame(left)
        btns.pack(fill="x", padx=10, pady=(0, 10))

        ttk.Button(btns, text="Зашифровать →", command=self.on_encrypt).pack(side="left")
        ttk.Button(btns, text="Очистить", command=lambda: self.msg_in.delete("1.0", "end")).pack(side="left", padx=8)

        ttk.Label(right, text="Шифртекст (блоки чисел):").pack(anchor="w", padx=10, pady=(10, 0))
        self.cipher_out = tk.Text(right, height=10, wrap="word")
        self.cipher_out.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        btns2 = ttk.Frame(right)
        btns2.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(btns2, text="Расшифровать ↓", command=self.on_decrypt).pack(side="left")
        ttk.Button(btns2, text="Копировать шифртекст", command=self.copy_cipher).pack(side="left", padx=8)

        ttk.Label(right, text="Расшифрованное сообщение:").pack(anchor="w", padx=10, pady=(2, 0))
        self.msg_out = tk.Text(right, height=8, wrap="word")
        self.msg_out.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _set_text(self, widget: tk.Text, value: str):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", value)
        widget.configure(state="disabled")

    def on_generate(self):
        try:
            p = int(self.p_var.get().strip())
            q = int(self.q_var.get().strip())
            pub, priv, meta = generate_keys(p, q)
            self.public_key, self.private_key, self.meta = pub, priv, meta

            self._set_text(self.pub_text, str(pub))
            self._set_text(self.priv_text, str(priv))
            self._set_text(self.meta_text, f"n={meta['n']}, φ(n)={meta['phi']}  (p={meta['p']}, q={meta['q']})")
            messagebox.showinfo("Готово", "Ключи сгенерированы.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def on_encrypt(self):
        if not self.public_key:
            self.on_generate()
            if not self.public_key:
                return
        try:
            text = self.msg_in.get("1.0", "end").rstrip("\n")
            blocks = encrypt_text_to_cipher_list(text, self.public_key)
            cipher_str = " ".join(str(b) for b in blocks)
            self.cipher_out.delete("1.0", "end")
            self.cipher_out.insert("1.0", cipher_str)
        except Exception as e:
            messagebox.showerror("Ошибка шифрования", str(e))

    def on_decrypt(self):
        if not self.private_key:
            messagebox.showerror("Ошибка", "Сначала сгенерируйте ключи.")
            return
        try:
            cipher_str = self.cipher_out.get("1.0", "end").strip()
            blocks = parse_cipher_blocks(cipher_str)
            text = decrypt_cipher_list_to_text(blocks, self.private_key)
            self.msg_out.delete("1.0", "end")
            self.msg_out.insert("1.0", text)
        except Exception as e:
            messagebox.showerror("Ошибка расшифрования", str(e))

    def copy_cipher(self):
        s = self.cipher_out.get("1.0", "end").strip()
        self.clipboard_clear()
        self.clipboard_append(s)
        self.update()
        messagebox.showinfo("Скопировано", "Шифртекст скопирован в буфер обмена.")


if __name__ == "__main__":
    app = RSAApp()
    app.mainloop()
