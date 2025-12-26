import tkinter as tk
from tkinter import ttk
import time
import threading
from dataclasses import dataclass

ADC_N = 12
ADC_U1 = -10.0
ADC_U2 = 10.0

DAC_M = 10
DAC_U1 = -6.4
DAC_U2 = 12.8

PORT300 = 0x300
PORT301 = 0x301

MASK_ADC = (1 << ADC_N) - 1
MASK_DAC = (1 << DAC_M) - 1

BIT_GT = 15
BIT_DR1 = 12
BIT_DR2 = 13

BIT_SEL = 10
BIT_EM = 11
BIT_TURN = 12
BIT_RET = 13
BIT_SD = 14
BIT_SA = 15

MUX_SWITCH = 0.02
DAC_CONV = 0.08
EM_PULSE = 0.08
T1_PERIOD = 0.1
T2_PERIOD = 0.5

TURN_TIME = 36.0
RET_TIME = 36.0

CODE_TURN = 0x3B0
CODE_RET = 0x0E0
TH_T60 = 0x0CCD


def clamp(x, a, b):
    return max(a, min(b, x))


def bit(val: int, n: int) -> int:
    return (val >> n) & 1


def set_bit(val: int, n: int, b: int) -> int:
    if b:
        return val | (1 << n)
    return val & ~(1 << n)


def adc_u_from_temp(t_c: float) -> float:
    return 0.1 * t_c


def adc_code_from_temp(t_c: float) -> int:
    u = adc_u_from_temp(t_c)
    u = clamp(u, ADC_U1, ADC_U2)
    levels = 2 ** ADC_N
    code = int(round((u - ADC_U1) / (ADC_U2 - ADC_U1) * levels))
    return int(clamp(code, 0, levels - 1))


def dac_u_from_code(code: int) -> float:
    levels = 2 ** DAC_M
    code = int(clamp(code, 0, levels - 1))
    return DAC_U1 + (DAC_U2 - DAC_U1) * (code / levels)


@dataclass
class Ports:
    port300: int = 0
    port301: int = 0


class Variant8Sim:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("ЛР5 СРВ — Вариант 8 (Пункт 9: имитационная модель)")

        self.ports = Ports()
        self.lock = threading.Lock()
        self.running = True

        self.time_scale = tk.DoubleVar(value=10.0)
        self.auto_heat = tk.BooleanVar(value=False)

        self.t1 = tk.DoubleVar(value=25.0)
        self.t2 = tk.DoubleVar(value=25.0)

        self.size_mode = tk.StringVar(value="normal")
        self.status = tk.StringVar(value="Ожидание…")

        self.thread = None

        self._ui()

        self.apply_size_bits()
        self.ui_update()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _ui(self):
        main = ttk.Frame(self.root, padding=12)
        main.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)


        lf_s = ttk.LabelFrame(main, text="Аналоговые датчики температуры", padding=10)
        lf_s.grid(row=1, column=0, sticky="nsew", padx=(0, 8))

        ttk.Label(lf_s, text="t1 (опрос 0.1с)").grid(row=0, column=0, sticky="w")
        ttk.Scale(lf_s, from_=-40, to=240, variable=self.t1, orient="horizontal").grid(row=1, column=0, sticky="ew")
        self.lbl_t1 = ttk.Label(lf_s, text="")
        self.lbl_t1.grid(row=2, column=0, sticky="w", pady=(0, 8))

        ttk.Label(lf_s, text="t2 (опрос 0.5с)").grid(row=3, column=0, sticky="w")
        ttk.Scale(lf_s, from_=-40, to=240, variable=self.t2, orient="horizontal").grid(row=4, column=0, sticky="ew")
        self.lbl_t2 = ttk.Label(lf_s, text="")
        self.lbl_t2.grid(row=5, column=0, sticky="w")

        ttk.Checkbutton(lf_s, text="Автоизменение t1/t2 в цикле (демо)", variable=self.auto_heat)\
            .grid(row=6, column=0, sticky="w", pady=(8, 0))

        lf_s.columnconfigure(0, weight=1)

        lf_d = ttk.LabelFrame(main, text="Дискретные датчики размера (сидят в 300h)", padding=10)
        lf_d.grid(row=2, column=0, sticky="nsew", padx=(0, 8), pady=(8, 0))

        ttk.Radiobutton(lf_d, text="Норма: DR1=0, DR2=1", value="normal", variable=self.size_mode,
                        command=self.apply_size_bits).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(lf_d, text="Меньше нормы: DR1=1", value="undersize", variable=self.size_mode,
                        command=self.apply_size_bits).grid(row=1, column=0, sticky="w")
        ttk.Radiobutton(lf_d, text="Больше нормы: DR2 инверсный → 0", value="oversize", variable=self.size_mode,
                        command=self.apply_size_bits).grid(row=2, column=0, sticky="w")

        ttk.Button(lf_d, text="Запустить цикл (как в драйвере)", command=self.start_cycle)\
            .grid(row=3, column=0, sticky="ew", pady=(8, 0))
        lf_d.columnconfigure(0, weight=1)

        lf_p = ttk.LabelFrame(main, text="Порты 300h/301h и индикация", padding=10)
        lf_p.grid(row=1, column=1, rowspan=2, sticky="nsew")

        self.lbl_300 = ttk.Label(lf_p, text="", font=("Consolas", 10))
        self.lbl_300.grid(row=0, column=0, sticky="w")

        self.lbl_301 = ttk.Label(lf_p, text="", font=("Consolas", 10))
        self.lbl_301.grid(row=1, column=0, sticky="w", pady=(6, 10))

        self.ind_sel = ttk.Label(lf_p, text="SEL: 0 (t1)")
        self.ind_sel.grid(row=2, column=0, sticky="w")
        self.ind_gt = ttk.Label(lf_p, text="GT: 0")
        self.ind_gt.grid(row=3, column=0, sticky="w")

        self.ind_em = ttk.Label(lf_p, text="EM (заслонка): OFF")
        self.ind_em.grid(row=4, column=0, sticky="w", pady=(6, 0))

        self.ind_turn = ttk.Label(lf_p, text="TURN (поворот): OFF")
        self.ind_turn.grid(row=5, column=0, sticky="w")

        self.ind_ret = ttk.Label(lf_p, text="RET (возврат): OFF")
        self.ind_ret.grid(row=6, column=0, sticky="w")

        self.ind_dac = ttk.Label(lf_p, text="DAC: code=000h, U=0.00V")
        self.ind_dac.grid(row=7, column=0, sticky="w", pady=(6, 0))

        ttk.Label(lf_p, text="Масштаб времени (больше = быстрее):").grid(row=8, column=0, sticky="w", pady=(10, 0))
        ttk.Scale(lf_p, from_=1, to=50, variable=self.time_scale, orient="horizontal").grid(row=9, column=0, sticky="ew")
        lf_p.columnconfigure(0, weight=1)

        lf_st = ttk.LabelFrame(main, text="Статус", padding=10)
        lf_st.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        ttk.Label(lf_st, textvariable=self.status, font=("Arial", 11)).grid(row=0, column=0, sticky="w")

    def _sleep(self, sec: float):
        scale = max(0.1, float(self.time_scale.get()))
        time.sleep(sec / scale)

    def apply_size_bits(self):
        with self.lock:
            p = self.ports.port300
            p = set_bit(p, BIT_DR1, 0)
            p = set_bit(p, BIT_DR2, 0)

            if self.size_mode.get() == "undersize":
                p = set_bit(p, BIT_DR1, 1)
                p = set_bit(p, BIT_DR2, 1)
            elif self.size_mode.get() == "oversize":
                p = set_bit(p, BIT_DR1, 0)
                p = set_bit(p, BIT_DR2, 0)
            else:
                p = set_bit(p, BIT_DR1, 0)
                p = set_bit(p, BIT_DR2, 1)

            self.ports.port300 = p

    def _write_301(self, new301: int):
        with self.lock:
            self.ports.port301 = new301 & 0xFFFF

    def _read_300(self) -> int:
        with self.lock:
            return self.ports.port300 & 0xFFFF

    def _set_300(self, new300: int):
        with self.lock:
            self.ports.port300 = new300 & 0xFFFF

    def _set_gt(self, v: int):
        with self.lock:
            p = self.ports.port300
            p = set_bit(p, BIT_GT, 1 if v else 0)
            self.ports.port300 = p

    def _set_301_bit(self, n: int, v: int):
        with self.lock:
            p = self.ports.port301
            p = set_bit(p, n, 1 if v else 0)
            self.ports.port301 = p

    def _set_301_dac(self, code: int):
        code &= MASK_DAC
        with self.lock:
            p = self.ports.port301
            p = (p & ~MASK_DAC) | code
            self.ports.port301 = p

    def read_adc_mux(self, sel: int) -> int:
        self._set_301_bit(BIT_SEL, 1 if sel else 0)
        self._sleep(MUX_SWITCH)

        self._set_301_bit(BIT_SA, 1)
        self._sleep(0.001)
        self._set_301_bit(BIT_SA, 0)

        t = float(self.t2.get()) if sel else float(self.t1.get())
        code = adc_code_from_temp(t) & MASK_ADC

        p300 = self._read_300()
        p300 = (p300 & ~MASK_ADC) | code
        self._set_300(p300)

        self._set_gt(1)
        self._sleep(0.02)
        self._set_gt(0)

        return code

    def write_dac_cmd(self, code: int, turn: int, ret: int, em: int):
        with self.lock:
            p = self.ports.port301
            sel = bit(p, BIT_SEL)
            p = 0
            p = set_bit(p, BIT_SEL, sel)
            p = set_bit(p, BIT_EM, 1 if em else 0)
            p = set_bit(p, BIT_TURN, 1 if turn else 0)
            p = set_bit(p, BIT_RET, 1 if ret else 0)
            p = (p & ~MASK_DAC) | (code & MASK_DAC)
            self.ports.port301 = p

        self._set_301_bit(BIT_SD, 1)
        self._sleep(DAC_CONV)
        self._set_301_bit(BIT_SD, 0)

    def pulse_em(self):
        self.write_dac_cmd(self.ports.port301 & MASK_DAC, 0, 0, 1)
        self._sleep(EM_PULSE)
        self.write_dac_cmd(self.ports.port301 & MASK_DAC, 0, 0, 0)

    def start_cycle(self):
        if self.thread and self.thread.is_alive():
            return
        self.thread = threading.Thread(target=self._cycle, daemon=True)
        self.thread.start()

    def _cycle(self):
        p300 = self._read_300()
        dr1 = bit(p300, BIT_DR1)
        dr2 = bit(p300, BIT_DR2)

        if dr1 == 1:
            self.status.set("DR1=1 → меньше нормы → брак → импульс электромагнита заслонки (80мс)")
            self.pulse_em()
            self.status.set("Готово: брак отброшен, ожидание.")
            return

        if dr2 == 0:
            self.status.set("DR2=0 (инверсный) → больше нормы → поворот 36с (+11.3В) → возврат 36с (-2.2В)")
            self.write_dac_cmd(CODE_TURN, 1, 0, 0)
            self._sleep(TURN_TIME)
            self.write_dac_cmd(CODE_TURN, 0, 0, 0)

            self.write_dac_cmd(CODE_RET, 0, 1, 0)
            self._sleep(RET_TIME)
            self.write_dac_cmd(CODE_RET, 0, 0, 0)

            cnt = 0
            t2_last = 0

            self.status.set("Температурный цикл: t1 каждые 0.1с, t2 раз в 0.5с, сравнение среднего кода с TH_T60")

            while True:
                if self.auto_heat.get():
                    self.t1.set(clamp(self.t1.get() + 0.6, -40, 240))
                    self.t2.set(clamp(self.t2.get() + 0.2, -40, 240))

                t1_code = self.read_adc_mux(0)

                if cnt % 5 == 0:
                    t2_last = self.read_adc_mux(1)

                avg = (t1_code + t2_last) // 2
                self.status.set(f"t1_code=0x{t1_code:03X}, t2_code=0x{t2_last:03X}, avg=0x{avg:03X} ; порог TH=0x{TH_T60:03X}")

                if avg >= TH_T60:
                    self.status.set("Условие выполнено: avg_code >= TH_T60. Цикл завершён.")
                    break

                cnt += 1
                self._sleep(T1_PERIOD)

            return

        self.status.set("Норма: DR1=0 и DR2=1 → управляющих воздействий нет.")

    def ui_update(self):
        if not self.running:
            return

        with self.lock:
            p300 = self.ports.port300 & 0xFFFF
            p301 = self.ports.port301 & 0xFFFF

        t1 = float(self.t1.get())
        t2 = float(self.t2.get())
        c1 = adc_code_from_temp(t1)
        c2 = adc_code_from_temp(t2)

        self.lbl_t1.config(text=f"t1={t1:.1f}°C → U={adc_u_from_temp(t1):.2f}V → АЦП≈0x{c1:03X}")
        self.lbl_t2.config(text=f"t2={t2:.1f}°C → U={adc_u_from_temp(t2):.2f}V → АЦП≈0x{c2:03X}")

        self.lbl_300.config(text=f"300h=0x{p300:04X}  GT={bit(p300,BIT_GT)} DR2(inv)={bit(p300,BIT_DR2)} DR1={bit(p300,BIT_DR1)}  ADC=0x{(p300 & MASK_ADC):03X}")
        self.lbl_301.config(text=f"301h=0x{p301:04X}  SA={bit(p301,BIT_SA)} SD={bit(p301,BIT_SD)} RET={bit(p301,BIT_RET)} TURN={bit(p301,BIT_TURN)} EM={bit(p301,BIT_EM)} SEL={bit(p301,BIT_SEL)}  DAC=0x{(p301 & MASK_DAC):03X}")

        self.ind_sel.config(text=f"SEL: {bit(p301, BIT_SEL)} ({'t2' if bit(p301, BIT_SEL) else 't1'})")
        self.ind_gt.config(text=f"GT: {bit(p300, BIT_GT)}")

        self.ind_em.config(text=f"EM (заслонка): {'ON' if bit(p301, BIT_EM) else 'OFF'}")
        self.ind_turn.config(text=f"TURN (поворот): {'ON' if bit(p301, BIT_TURN) else 'OFF'}")
        self.ind_ret.config(text=f"RET (возврат): {'ON' if bit(p301, BIT_RET) else 'OFF'}")

        dac_code = p301 & MASK_DAC
        u = dac_u_from_code(dac_code)
        self.ind_dac.config(text=f"DAC: code=0x{dac_code:03X} ({dac_code}) → U≈{u:.2f}V")

        self.root.after(100, self.ui_update)

    def on_close(self):
        self.running = False
        self.root.destroy()


def main():
    root = tk.Tk()
    Variant8Sim(root)
    root.mainloop()


if __name__ == "__main__":
    main()
