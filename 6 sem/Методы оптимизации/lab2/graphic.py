import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def f(x1, x2):
    return x1**2 + 4 * x2**2 - x1 * x2 + x1

# сетка значений x1 и x2
x1 = np.linspace(-5, 5, 100)
x2 = np.linspace(-5, 5, 100)
X1, X2 = np.meshgrid(x1, x2)
Z = f(X1, X2)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
surf = ax.plot_surface(X1, X2, Z, cmap='viridis', alpha=0.8)

x0 = (3, 1)
ax.scatter(x0[0], x0[1], f(x0[0], x0[1]), color='red', s=100, label=f'x0 = {x0}')

ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('f(x)')
ax.set_title('График функции f(x) = x1² + 4x2² - x1x2 + x1')
ax.legend()

plt.show()