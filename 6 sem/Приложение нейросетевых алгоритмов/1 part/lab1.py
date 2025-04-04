import math
import random


# Функция нормализации вектора
def normalize(vec):
    norm = math.sqrt(sum(x * x for x in vec))
    return [x / norm for x in vec] if norm != 0 else vec


# скалярное произведения двух векторов
def dot(v1, v2):
    return sum(a * b for a, b in zip(v1, v2))


# Задача 1
# Инициализация нейрона
def init_wta_neuron(dim):
    weights = [random.random() for _ in range(dim)]
    return normalize(weights)


# Вычисление активации нейрона
def wta_activation(weights, x):
    return dot(weights, x)


# Обновление весов нейрона
def update_wta(weights, x, eta):
    new_weights = [w + eta * (xi - w) for w, xi in zip(weights, x)]
    return normalize(new_weights)


def task1_WTA(train_data, eta=0.5):
    neurons = [init_wta_neuron(2) for _ in range(4)]

    for x in train_data:
        activations = [wta_activation(weights, x) for weights in neurons]
        winner_index = activations.index(max(activations))
        neurons[winner_index] = update_wta(neurons[winner_index], x, eta)

    print("Задача 1")
    for i, weights in enumerate(neurons):
        print(f"Нейрон {i + 1}: {weights}")
    print()


# Задача 2
def init_modified_wta_neuron(dim):
    return {"weights": normalize([random.random() for _ in range(dim)]),
            "win_count": 0}


# Активация с учетом штрафа
def modified_wta_activation(neuron, x, penalty=0.1):
    raw = dot(neuron["weights"], x)
    return raw - penalty * neuron["win_count"]


# Обновление весов по правилу Гроссберга
def update_modified_wta(neuron, x, eta):
    new_weights = [w + eta * (xi - w) for w, xi in zip(neuron["weights"], x)]
    neuron["weights"] = normalize(new_weights)
    neuron["win_count"] += 1


def task2_ModifiedWTA(train_data, eta=0.5, penalty=0.1):
    neurons = [init_modified_wta_neuron(2) for _ in range(4)]

    for x in train_data:
        activations = [modified_wta_activation(neuron, x, penalty) for neuron in neurons]
        winner_index = activations.index(max(activations))
        update_modified_wta(neurons[winner_index], x, eta)

    print("Задача 2")
    for i, neuron in enumerate(neurons):
        print(f"Нейрон {i + 1}: веса = {neuron['weights']}, число побед = {neuron['win_count']}")
    print()


# Задача 3
# Инициализация нейрона Хебба
def init_hebb_neuron(dim):
    return [random.random() for _ in range(dim)]


# Вычисление выхода нейрона
def hebb_output(weights, x):
    return dot(weights, x)


# Обновление весов по правилу Хебба
def update_hebb(weights, x, eta):
    y = hebb_output(weights, x)
    new_weights = [w + eta * y * xi for w, xi in zip(weights, x)]
    return new_weights


def task3_Hebb(train_data, eta=0.5):
    neurons = [init_hebb_neuron(2) for _ in range(2)]

    for x in train_data:
        for i in range(len(neurons)):
            neurons[i] = update_hebb(neurons[i], x, eta)

    print("Задача 3")
    for i, weights in enumerate(neurons):
        print(f"Нейрон {i + 1}: {weights}")
    print()


if __name__ == '__main__':
    train_data = [
        [0.97, 0.20],
        [1.00, 0.00],
        [-0.72, -0.70],
        [-0.67, -0.74],
        [-0.80, -0.60],
        [0.00, -1.00],
        [-0.20, -0.97],
        [-0.30, -0.95]
    ]

    task1_WTA(train_data, eta=0.5)
    task2_ModifiedWTA(train_data, eta=0.5, penalty=0.1)
    task3_Hebb(train_data, eta=0.5)
