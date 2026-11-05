import tkinter as tk
from tkinter import ttk, messagebox


def text_to_binary(text: str) -> str:
    """Преобразует строку в двоичную последовательность (по 8 бит на символ)."""
    return ''.join(format(ord(ch), '08b') for ch in text)


def binary_to_text(binary: str) -> str:
    """Преобразует двоичную строку обратно в текст."""
    if len(binary) % 8 != 0:
        raise ValueError("Длина двоичной строки должна быть кратна 8.")
    chars = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i + 8]
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)


def hamming_encode_8bits(data_bits: str) -> str:
    """
    Кодирование 8 бит данных в Hamming (12,8).
    Позиции битов (1-based):
    1,2,4,8 — проверочные
    3,5,6,7,9,10,11,12 — информационные
    """
    if len(data_bits) != 8 or any(b not in "01" for b in data_bits):
        raise ValueError("Нужно ровно 8 бит данных.")

    code = ['0'] * 13  # индекс 0 не используем

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
    """
    Проверка и исправление 1 ошибки в Hamming (12,8).
    Возвращает:
      corrected_codeword, error_position
    где error_position = 0, если ошибки нет.
    """
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
    """
    Декодирование Hamming (12,8) с исправлением 1 ошибки.
    Возвращает:
      data_bits, corrected_codeword, error_position
    """
    corrected, error_position = hamming_check_and_correct_12bits(codeword)
    c = ['0'] + list(corrected)

    data_positions = [3, 5, 6, 7, 9, 10, 11, 12]
    data_bits = ''.join(c[pos] for pos in data_positions)

    return data_bits, corrected, error_position


def encode_text_hamming(text: str):
    """
    Кодирует весь текст.
    Каждый символ -> 8 бит -> Hamming(12,8)
    Возвращает список кодовых слов по 12 бит.
    """
    blocks = []
    for ch in text:
        bits = format(ord(ch), '08b')
        blocks.append(hamming_encode_8bits(bits))
    return blocks


def decode_hamming_blocks(blocks):
    """
    Декодирует список 12-битных блоков.
    Возвращает:
      decoded_text, corrected_blocks, errors
    где errors — список позиций ошибок по каждому блоку.
    """
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


def parse_blocks(s: str):
    """
    Разбор блоков из строки.
    Разрешены разделители: пробелы, запятые, переносы строк.
    Каждый блок должен содержать 12 бит.
    """
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


class HammingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Код Хэмминга")
        self.geometry("1000x700")
        self._build_ui()

    def _build_ui(self):
        pad = {"padx": 10, "pady": 6}

        top = ttk.Frame(self)
        top.pack(fill="x", **pad)

        ttk.Label(
            top,
            text="Код Хэмминга Hamming (12,8)",
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        ttk.Label(
            top,
            text="Каждый символ кодируется в 8 бит и затем преобразуется в 12-битный код Хэмминга."
        ).pack(anchor="w", pady=(4, 0))

        info = ttk.LabelFrame(self, text="Описание")
        info.pack(fill="x", **pad)

        self.info_text = tk.Text(info, height=7, wrap="word")
        self.info_text.pack(fill="x", padx=10, pady=10)
        self.info_text.insert(
            "1.0",
            "Программа выполняет:\n"
            "1) Кодирование текста с помощью кода Хэмминга (12,8)\n"
            "2) Декодирование закодированных блоков\n"
            "3) Обнаружение и исправление одной ошибки в каждом 12-битном блоке\n\n"
            "Формат кодовых блоков: двоичные слова по 12 бит, разделённые пробелами."
        )
        self.info_text.configure(state="disabled")

        body = ttk.Frame(self)
        body.pack(fill="both", expand=True, **pad)

        left = ttk.LabelFrame(body, text="Исходное сообщение")
        right = ttk.LabelFrame(body, text="Код Хэмминга и декодирование")

        left.pack(side="left", fill="both", expand=True, padx=(0, 6))
        right.pack(side="left", fill="both", expand=True, padx=(6, 0))

        self.input_text = tk.Text(left, height=14, wrap="word")
        self.input_text.pack(fill="both", expand=True, padx=10, pady=10)
        self.input_text.insert("1.0", "Привет")

        left_btns = ttk.Frame(left)
        left_btns.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(left_btns, text="Закодировать →", command=self.on_encode).pack(side="left")
        ttk.Button(left_btns, text="Очистить", command=self.clear_input).pack(side="left", padx=8)

        ttk.Label(right, text="Закодированные блоки (по 12 бит):").pack(anchor="w", padx=10, pady=(10, 0))
        self.encoded_text = tk.Text(right, height=10, wrap="word")
        self.encoded_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        right_btns = ttk.Frame(right)
        right_btns.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(right_btns, text="Декодировать ↓", command=self.on_decode).pack(side="left")
        ttk.Button(right_btns, text="Копировать", command=self.copy_encoded).pack(side="left", padx=8)

        ttk.Label(right, text="Декодированный текст:").pack(anchor="w", padx=10)
        self.decoded_text = tk.Text(right, height=6, wrap="word")
        self.decoded_text.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        ttk.Label(right, text="Информация об ошибках:").pack(anchor="w", padx=10)
        self.error_info = tk.Text(right, height=6, wrap="word")
        self.error_info.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def on_encode(self):
        try:
            text = self.input_text.get("1.0", "end").rstrip("\n")
            if not text:
                raise ValueError("Введите текст для кодирования.")

            blocks = encode_text_hamming(text)
            result = " ".join(blocks)

            self.encoded_text.delete("1.0", "end")
            self.encoded_text.insert("1.0", result)

            self.decoded_text.delete("1.0", "end")
            self.error_info.delete("1.0", "end")
        except Exception as e:
            messagebox.showerror("Ошибка кодирования", str(e))

    def on_decode(self):
        try:
            raw = self.encoded_text.get("1.0", "end").strip()
            if not raw:
                raise ValueError("Введите или получите закодированные блоки.")

            blocks = parse_blocks(raw)
            text, corrected_blocks, errors = decode_hamming_blocks(blocks)

            self.decoded_text.delete("1.0", "end")
            self.decoded_text.insert("1.0", text)

            report_lines = []
            for i, err in enumerate(errors, start=1):
                if err == 0:
                    report_lines.append(f"Блок {i}: ошибок не обнаружено")
                else:
                    report_lines.append(f"Блок {i}: исправлена ошибка в позиции {err}")

            self.error_info.delete("1.0", "end")
            self.error_info.insert(
                "1.0",
                "Исправленные блоки:\n"
                + " ".join(corrected_blocks)
                + "\n\n"
                + "\n".join(report_lines)
            )
        except Exception as e:
            messagebox.showerror("Ошибка декодирования", str(e))

    def copy_encoded(self):
        try:
            text = self.encoded_text.get("1.0", "end").strip()
            if not text:
                raise ValueError("Нет данных для копирования.")

            self.clipboard_clear()
            self.clipboard_append(text)
            self.update()
            messagebox.showinfo("Скопировано", "Закодированные блоки скопированы в буфер обмена.")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def clear_input(self):
        self.input_text.delete("1.0", "end")


if __name__ == "__main__":
    app = HammingApp()
    app.mainloop()