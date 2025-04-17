import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Определение функции
def f(x1, x2):
    return x1**2 + 4*x2**2 - x1*x2 + x1

# Создание сетки для построения
x1 = np.linspace(-2, 4, 100)
x2 = np.linspace(-2, 2, 100)
X1, X2 = np.meshgrid(x1, x2)
Z = f(X1, X2)

# Точка минимума (из решения)
x_min = np.array([-8/15, -1/15])
f_min = f(x_min[0], x_min[1])

# Построение 3D-графика
fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(121, projection='3d')
surf = ax1.plot_surface(X1, X2, Z, cmap='viridis', alpha=0.8)
ax1.scatter(x_min[0], x_min[1], f_min, color='red', s=100, label=f'Минимум: ({x_min[0]:.2f}, {x_min[1]:.2f})')
ax1.set_xlabel('x1')
ax1.set_ylabel('x2')
ax1.set_zlabel('f(x1, x2)')
ax1.set_title('3D-график функции')
ax1.legend()

# Построение линий уровня
ax2 = fig.add_subplot(122)
contour = ax2.contour(X1, X2, Z, levels=20, cmap='viridis')
ax2.scatter(x_min[0], x_min[1], color='red', s=100, label=f'Минимум: ({x_min[0]:.2f}, {x_min[1]:.2f})')
ax2.set_xlabel('x1')
ax2.set_ylabel('x2')
ax2.set_title('Линии уровня функции')
ax2.legend()
plt.colorbar(contour, ax=ax2)

plt.tight_layout()
plt.show()