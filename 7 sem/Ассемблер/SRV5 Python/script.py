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

TH_T_C = 60.0
T1_PERIOD = 0.1
T2_PERIOD = 0.5
MUX_SWITCH = 0.02
DAC_CONV = 0.08
EM_PULSE = 0.08

TURN_VOLT = 11.3
RET_VOLT = -2.2
TURN_TIME = 36.0
RET_TIME = 36.0

BIT_SEL = 10
BIT_EM = 11
BIT_TURN = 12
BIT_RET = 13
BIT_SD = 14
BIT_SA = 15

BIT_DR1 = 12
BIT_DR2 = 13
BIT_GT = 15

MASK_ADC = (1 << ADC_N) - 1
MASK_DAC = (1 << DAC_M) - 1


def clamp(x, a, b):
    return max(a, min(b, x))


def adc_code_from_temp_c(t_c: float) -> int:
    u = 0.1 * t_c
    u = clamp(u, ADC_U1, ADC_U2)
    levels = 2 ** ADC_N
    code = int(round((u - ADC_U1) / (ADC_U2 - ADC_U1) * levels))
    return int(clamp(code, 0, levels - 1))


def dac_code_from_u(u: float) -> int:
    u = clamp(u, DAC_U1, DAC_U2)
    levels = 2 ** DAC_M
    code = int(round((u - DAC_U1) / (DAC_U2 - DAC_U1) * levels))
    return int(clamp(code, 0, levels - 1))


def dac_u_from_code(code: int) -> float:
    levels = 2 ** DAC_M
    code = int(clamp(code, 0, levels - 1))
    return DAC_U1 + (DAC_U2 - DAC_U1) * (code / levels)


def bit(val: int, n: int) -> int:
    return (val >> n) & 1


def set_bit(val: int, n: int, b: int) -> int:
    if b:
        return val | (1 << n)
    return val & ~(1 << n)


@dataclass
class Ports:
    port300: int = 0
    port301: int = 0


class Variant8SimulatorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("ЛР5 СРВ — Вариант 8 (имитационная модель)")

        self.ports = Ports()
        self.running = True

        self.time_scale = tk.DoubleVar(value=10.0)
        self.auto_heat = tk.BooleanVar(value=True)

        self.t1 = tk.DoubleVar(value=25.0)
        self.t2 = tk.DoubleVar(value=25.0)

        self.size_mode = tk.StringVar(value="normal")
        self.status = tk.StringVar(value="Ожидание…")

        self.process_thread = None
        self.lock = threading.Lock()

        self._build_ui()
        self.apply_size_bits()

        self.ui_updater()
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=12)
        main.grid(row=0, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=1)

        title = ttk.Label(main, text="Имитационная модель работы СРВ (вариант 8)", font=("Arial", 14, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        sensors = ttk.LabelFrame(main, text="Аналоговые датчики температуры", padding=10)
        sensors.grid(row=1, column=0, sticky="nsew", padx=(0, 8))

        ttk.Label(sensors, text="t1 (опрос 0.1с)").grid(row=0, column=0, sticky="w")
        ttk.Scale(sensors, from_=-40, to=240, variable=self.t1, orient="horizontal").grid(row=1, column=0, sticky="ew")
        self.lbl_t1 = ttk.Label(sensors, text="")
        self.lbl_t1.grid(row=2, column=0, sticky="w", pady=(0, 8))

        ttk.Label(sensors, text="t2 (опрос 0.5с)").grid(row=3, column=0, sticky="w")
        ttk.Scale(sensors, from_=-40, to=240, variable=self.t2, orient="horizontal").grid(row=4, column=0, sticky="ew")
        self.lbl_t2 = ttk.Label(sensors, text="")
        self.lbl_t2.grid(row=5, column=0, sticky="w")

        sensors.columnconfigure(0, weight=1)

        ttk.Checkbutton(sensors, text="Автонагрёв при обработке (для демонстрации)", variable=self.auto_heat)\
            .grid(row=6, column=0, sticky="w", pady=(8, 0))

        size = ttk.LabelFrame(main, text="Дискретные датчики размера (DR1/DR2)", padding=10)
        size.grid(row=2, column=0, sticky="nsew", padx=(0, 8), pady=(8, 0))

        ttk.Radiobutton(size, text="Норма (DR1=0, DR2=1)", value="normal", variable=self.size_mode,
                        command=self.apply_size_bits).grid(row=0, column=0, sticky="w")
        ttk.Radiobutton(size, text="Меньше нормы (DR1=1)", value="undersize", variable=self.size_mode,
                        command=self.apply_size_bits).grid(row=1, column=0, sticky="w")
        ttk.Radiobutton(size, text="Больше нормы (DR2 инверсный → 0)", value="oversize", variable=self.size_mode,
                        command=self.apply_size_bits).grid(row=2, column=0, sticky="w")

        ttk.Button(size, text="Смоделировать цикл (по текущим DR1/DR2)", command=self.start_cycle)\
            .grid(row=3, column=0, sticky="ew", pady=(8, 0))

        size.columnconfigure(0, weight=1)

        ports = ttk.LabelFrame(main, text="Порты и исполнительные устройства", padding=10)
        ports.grid(row=1, column=1, rowspan=2, sticky="nsew")

        self.lbl_port300 = ttk.Label(ports, text="", font=("Consolas", 10))
        self.lbl_port300.grid(row=0, column=0, sticky="w")

        self.lbl_port301 = ttk.Label(ports, text="", font=("Consolas", 10))
        self.lbl_port301.grid(row=1, column=0, sticky="w", pady=(6, 10))

        self.ind_em = ttk.Label(ports, text="Электромагнит заслонки: OFF")
        self.ind_em.grid(row=2, column=0, sticky="w")

        self.ind_turn = ttk.Label(ports, text="Поворот: OFF")
        self.ind_turn.grid(row=3, column=0, sticky="w")

        self.ind_ret = ttk.Label(ports, text="Возврат: OFF")
        self.ind_ret.grid(row=4, column=0, sticky="w")

        self.ind_dac = ttk.Label(ports, text="ЦАП: код=000h, U=0.0V")
        self.ind_dac.grid(row=5, column=0, sticky="w", pady=(6, 0))

        ttk.Label(ports, text="Масштаб времени (больше = быстрее):").grid(row=6, column=0, sticky="w", pady=(10, 0))
        ttk.Scale(ports, from_=1, to=50, variable=self.time_scale, orient="horizontal").grid(row=7, column=0, sticky="ew")
        ports.columnconfigure(0, weight=1)

        status_box = ttk.LabelFrame(main, text="Статус", padding=10)
        status_box.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        ttk.Label(status_box, textvariable=self.status, font=("Arial", 11)).grid(row=0, column=0, sticky="w")

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

    def _sleep(self, sec: float):
        scale = max(0.1, float(self.time_scale.get()))
        time.sleep(sec / scale)

    def _set_action_bits(self, em=0, turn=0, ret=0):
        with self.lock:
            p = self.ports.port301
            p = set_bit(p, BIT_EM, em)
            p = set_bit(p, BIT_TURN, turn)
            p = set_bit(p, BIT_RET, ret)
            self.ports.port301 = p

    def _set_sel(self, sel: int):
        with self.lock:
            p = self.ports.port301
            p = set_bit(p, BIT_SEL, 1 if sel else 0)
            self.ports.port301 = p

    def _pulse_sa(self):
        with self.lock:
            p = self.ports.port301
            p = set_bit(p, BIT_SA, 1)
            self.ports.port301 = p
        self._sleep(MUX_SWITCH)
        with self.lock:
            p = self.ports.port301
            p = set_bit(p, BIT_SA, 0)
            self.ports.port301 = p

    def _pulse_sd(self):
        with self.lock:
            p = self.ports.port301
            p = set_bit(p, BIT_SD, 1)
            self.ports.port301 = p
        self._sleep(DAC_CONV)
        with self.lock:
            p = self.ports.port301
            p = set_bit(p, BIT_SD, 0)
            self.ports.port301 = p

    def _write_dac_code(self, code: int):
        code = int(clamp(code, 0, MASK_DAC))
        with self.lock:
            p = self.ports.port301
            p = (p & ~MASK_DAC) | (code & MASK_DAC)
            self.ports.port301 = p

    def _adc_measure_selected(self) -> int:
        with self.lock:
            sel = bit(self.ports.port301, BIT_SEL)

        t = self.t2.get() if sel else self.t1.get()
        code = adc_code_from_temp_c(float(t))

        with self.lock:
            p = self.ports.port300
            p = (p & ~MASK_ADC) | code
            p = set_bit(p, BIT_GT, 1)
            self.ports.port300 = p

        self._sleep(0.02)

        with self.lock:
            p = self.ports.port300
            p = set_bit(p, BIT_GT, 0)
            self.ports.port300 = p

        return code

    def start_cycle(self):
        if self.process_thread and self.process_thread.is_alive():
            return
        self.process_thread = threading.Thread(target=self._cycle_logic, daemon=True)
        self.process_thread.start()

    def _cycle_logic(self):
        with self.lock:
            p300 = self.ports.port300

        dr1 = bit(p300, BIT_DR1)
        dr2 = bit(p300, BIT_DR2)

        if dr1 == 1:
            self.status.set("DR1=1 (меньше нормы) → брак → заслонка")
            self._set_action_bits(em=1, turn=0, ret=0)
            self._sleep(EM_PULSE)
            self._set_action_bits(em=0, turn=0, ret=0)
            self.status.set("Брак: заслонка отработала, режим ожидания.")
            return

        if dr2 == 0:
            self.status.set("DR2=0 (инверсный, больше нормы) → поворот 36с → возврат 36с → контроль Tср≥60°C")

            code_turn = dac_code_from_u(TURN_VOLT)
            self._write_dac_code(code_turn)
            self._set_action_bits(em=0, turn=1, ret=0)
            self._pulse_sd()
            self._sleep(TURN_TIME)

            code_ret = dac_code_from_u(RET_VOLT)
            self._write_dac_code(code_ret)
            self._set_action_bits(em=0, turn=0, ret=1)
            self._pulse_sd()
            self._sleep(RET_TIME)

            self._set_action_bits(em=0, turn=0, ret=0)

            t2_last_code = None
            cycles = 0

            while True:
                if self.auto_heat.get():
                    self.t1.set(clamp(self.t1.get() + 0.6, -40, 240))
                    self.t2.set(clamp(self.t2.get() + 0.2, -40, 240))

                self._set_sel(0)
                self._pulse_sa()
                t1_code = self._adc_measure_selected()

                if t2_last_code is None or cycles % 5 == 0:
                    self._set_sel(1)
                    self._pulse_sa()
                    t2_last_code = self._adc_measure_selected()

                avg_code = (t1_code + (t2_last_code if t2_last_code is not None else t1_code)) // 2

                t_avg = (self.t1.get() + self.t2.get()) / 2.0
                self.status.set(f"t1={self.t1.get():.1f}°C, t2={self.t2.get():.1f}°C → Tср={t_avg:.1f}°C, код ср={avg_code}")

                if t_avg >= TH_T_C:
                    self.status.set("Готово: Tср ≥ 60°C, цикл завершён.")
                    break

                cycles += 1
                self._sleep(T1_PERIOD)

            return

        self.status.set("DR1=0 и DR2=1 (норма) → управляющих действий нет.")

    def ui_updater(self):
        if not self.running:
            return

        with self.lock:
            p300 = self.ports.port300
            p301 = self.ports.port301

        t1_code = adc_code_from_temp_c(self.t1.get())
        t2_code = adc_code_from_temp_c(self.t2.get())

        self.lbl_t1.config(text=f"t1={self.t1.get():.1f}°C → U={0.1*self.t1.get():.2f}V → АЦП={t1_code} (0x{t1_code:03X})")
        self.lbl_t2.config(text=f"t2={self.t2.get():.1f}°C → U={0.1*self.t2.get():.2f}V → АЦП={t2_code} (0x{t2_code:03X})")

        p300_bits = (
            f"300h = 0x{p300:04X} | GT={bit(p300, BIT_GT)} "
            f"DR2(inv)={bit(p300, BIT_DR2)} DR1={bit(p300, BIT_DR1)} "
            f"ADC=0x{(p300 & MASK_ADC):03X}"
        )
        p301_bits = (
            f"301h = 0x{p301:04X} | SA={bit(p301, BIT_SA)} SD={bit(p301, BIT_SD)} "
            f"RET={bit(p301, BIT_RET)} TURN={bit(p301, BIT_TURN)} EM={bit(p301, BIT_EM)} "
            f"SEL={bit(p301, BIT_SEL)} DAC=0x{(p301 & MASK_DAC):03X}"
        )

        self.lbl_port300.config(text=p300_bits)
        self.lbl_port301.config(text=p301_bits)

        em = bit(p301, BIT_EM)
        turn = bit(p301, BIT_TURN)
        ret = bit(p301, BIT_RET)

        self.ind_em.config(text=f"Электромагнит заслонки: {'ON' if em else 'OFF'}")
        self.ind_turn.config(text=f"Поворот: {'ON' if turn else 'OFF'}")
        self.ind_ret.config(text=f"Возврат: {'ON' if ret else 'OFF'}")

        dac_code = (p301 & MASK_DAC)
        u = dac_u_from_code(dac_code)
        self.ind_dac.config(text=f"ЦАП: код=0x{dac_code:03X} ({dac_code}) → U≈{u:.2f} V")

        self.root.after(100, self.ui_updater)

    def on_close(self):
        self.running = False
        self.root.destroy()


def main():
    root = tk.Tk()
    app = Variant8SimulatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
