import numpy as np
import matplotlib.pyplot as plt

def f(arg):
    return arg * arg - 2 * arg + 5

x = np.linspace(-2, 8, 400)
y = f(x)

plt.plot(x, y, label="f(x) = x^2 - 2x + 5")
plt.title("График функции f(x) = x^2 - 2x + 5")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.grid(True)
plt.legend()
plt.show()
