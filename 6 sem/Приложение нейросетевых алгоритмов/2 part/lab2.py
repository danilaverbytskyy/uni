import numpy as np

def task1():
    print("\n=== Задача 1: Решение XOR с ReLU ===")
    X = np.array([[0, 0], [1, 1], [1, 0], [0, 1]])
    W1 = np.array([[1, 1], [-1, -1]])
    b1 = np.array([-1, 1])
    W2 = np.array([1, -1])
    hidden = np.maximum(0, X.dot(W1) + b1)
    output = np.sign(hidden.dot(W2))
    print("Входные данные:\n", X)
    print("Предсказанные классы:", output)

class Perceptron:
    def __init__(self):
        self.weights = None
        self.bias = 0
    def train(self, X, y, lr=0.1, epochs=100):
        self.weights = np.zeros(X.shape[1])
        for _ in range(epochs):
            for i in range(len(X)):
                pred = np.sign(np.dot(self.weights, X[i]) + self.bias)
                if pred != y[i]:
                    self.weights += lr * (y[i] - pred) * X[i]
                    self.bias += lr * (y[i] - pred)
    def predict(self, X):
        return np.sign(X.dot(self.weights) + self.bias)

class Adaline:
    def __init__(self):
        self.weights = None
        self.bias = 0
    def train(self, X, y, lr=0.01, epochs=100):
        self.weights = np.zeros(X.shape[1])
        for _ in range(epochs):
            for i in range(len(X)):
                output = np.dot(self.weights, X[i]) + self.bias
                error = y[i] - output
                self.weights += lr * error * X[i]
                self.bias += lr * error
    def predict(self, X):
        return np.sign(X.dot(self.weights) + self.bias)

def task2():
    print("\n=== Задача 2: Перцептрон vs Адалайн ===")
    np.random.seed(42)
    X_train = np.random.rand(20, 2)
    y_train = np.where(X_train[:, 0] > X_train[:, 1], 1, -1)
    p = Perceptron()
    p.train(X_train, y_train)
    a = Adaline()
    a.train(X_train, y_train)
    X_test = np.random.rand(1000, 2)
    y_test = np.where(X_test[:, 0] > X_test[:, 1], 1, -1)
    acc_p = np.mean(p.predict(X_test) == y_test)
    acc_a = np.mean(a.predict(X_test) == y_test)
    print(f"Точность перцептрона: {acc_p:.2%}")
    print(f"Точность адалайна: {acc_a:.2%}")

class NeuralNetwork:
    def __init__(self):
        self.W1 = np.random.randn(9, 4)
        self.W2 = np.random.randn(4, 4)
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    def forward(self, x):
        self.hidden = self.sigmoid(x.dot(self.W1))
        self.output = self.sigmoid(self.hidden.dot(self.W2))
        return self.output
    def train(self, X, y, lr=0.1, epochs=10000):
        for _ in range(epochs):
            for i in range(len(X)):
                output = self.forward(X[i])
                error = y[i] - output
                delta_out = error * output * (1 - output)
                delta_hidden = delta_out.dot(self.W2.T) * self.hidden * (1 - self.hidden)
                self.W2 += lr * np.outer(self.hidden, delta_out)
                self.W1 += lr * np.outer(X[i], delta_hidden)

def task3():
    print("\n=== Задача 3: Распознавание символов ===")
    X_data = np.array([
        [1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 0, 1, 0],
        [0, 1, 0, 0, 1, 0, 0, 1, 0],
        [1, 0, 0, 1, 0, 0, 1, 1, 1]
    ])
    y_data = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    nn = NeuralNetwork()
    nn.train(X_data, y_data, lr=0.1, epochs=10000)
    I_noisy = np.array([0, 1, 0, 1, 1, 0, 0, 1, 0])
    pred = nn.forward(I_noisy)
    print("Предсказание для искаженной I:", np.argmax(pred) + 1)

if __name__ == "__main__":
    task1()
    task2()
    task3()