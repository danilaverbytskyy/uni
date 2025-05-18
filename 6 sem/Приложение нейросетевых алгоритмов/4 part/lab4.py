import random


class HopfieldNetwork:
    def __init__(self, size):
        self.size = size
        self.weights = [[0.0 for _ in range(size)] for _ in range(size)]

    def train(self, patterns):
        """Обучение сети по правилу Хебба"""
        for pattern in patterns:
            for i in range(self.size):
                for j in range(self.size):
                    if i != j:
                        self.weights[i][j] += pattern[i] * pattern[j]

        # Нормализация весов
        num_patterns = len(patterns)
        for i in range(self.size):
            for j in range(self.size):
                self.weights[i][j] /= num_patterns

    def predict(self, input_pattern, max_iter=100):
        """Распознавание образа"""
        current_state = [x for x in input_pattern]
        previous_state = [0 for _ in range(self.size)]

        for _ in range(max_iter):
            for i in range(self.size):
                activation = 0.0
                for j in range(self.size):
                    activation += self.weights[i][j] * current_state[j]

                current_state[i] = 1 if activation >= 0 else -1

            # Проверка на сходимость
            converged = True
            for i in range(self.size):
                if current_state[i] != previous_state[i]:
                    converged = False
                    break

            if converged:
                break

            previous_state = [x for x in current_state]

        return current_state

    def add_noise(self, pattern, noise_level):
        """Добавление шума к образцу"""
        noisy = [x for x in pattern]
        for i in range(len(noisy)):
            if random.random() < noise_level:
                noisy[i] *= -1
        return noisy

    def test_noise_tolerance(self, patterns, noise_levels, num_tests=10):
        """Тестирование устойчивости к шуму"""
        results = {}

        for pattern in patterns:
            pattern_key = tuple(pattern)
            results[pattern_key] = {}

            for noise in noise_levels:
                correct = 0

                for _ in range(num_tests):
                    noisy = self.add_noise(pattern, noise)
                    result = self.predict(noisy)

                    # Проверяем, совпадает ли результат с оригиналом
                    match = True
                    for i in range(self.size):
                        if result[i] != pattern[i]:
                            match = False
                            break

                    if match:
                        correct += 1

                results[pattern_key][noise] = correct / num_tests

        return results


class HammingNetwork:
    def __init__(self, num_classes, input_size):
        self.num_classes = num_classes
        self.input_size = input_size
        self.first_layer_weights = [[0.0 for _ in range(input_size)] for _ in range(num_classes)]
        self.second_layer_weights = [[0.0 for _ in range(num_classes)] for _ in range(num_classes)]

    def train(self, patterns):
        """Обучение сети Хэмминга"""
        # Первый слой - запоминаем эталоны
        for i in range(self.num_classes):
            for j in range(self.input_size):
                self.first_layer_weights[i][j] = patterns[i][j]

        # Второй слой - устанавливаем веса
        for i in range(self.num_classes):
            for j in range(self.num_classes):
                if i == j:
                    self.second_layer_weights[i][j] = 1.0
                else:
                    self.second_layer_weights[i][j] = -1.0 / (self.num_classes - 1) + random.uniform(-0.1, 0.1)

    def hamming_distance(self, x, y):
        """Вычисление расстояния Хэмминга между двумя векторами"""
        distance = 0
        for xi, yi in zip(x, y):
            if xi != yi:
                distance += 1
        return distance

    def predict(self, input_pattern, max_iter=100, epsilon=0.1):
        """Распознавание образа"""
        # Первый слой - вычисляем выходы
        y = [0.0 for _ in range(self.num_classes)]
        for i in range(self.num_classes):
            r_h = 0.5 * (self.input_size - sum(
                self.first_layer_weights[i][j] * input_pattern[j]
                for j in range(self.input_size)
            ))
            y[i] = max(0.0, 1.0 - r_h / self.input_size)

        # Второй слой - итеративный процесс
        prev_y = [0.0 for _ in range(self.num_classes)]
        for _ in range(max_iter):
            new_y = [0.0 for _ in range(self.num_classes)]

            for i in range(self.num_classes):
                activation = sum(
                    self.second_layer_weights[i][j] * y[j]
                    for j in range(self.num_classes)
                )
                new_y[i] = max(0.0, activation)

            # Проверка на сходимость
            diff = sum(abs(new_y[i] - y[i]) for i in range(self.num_classes))
            if diff < epsilon:
                break

            y = new_y

        # Находим наиболее активный нейрон
        max_val = max(y)
        if max_val <= 0:
            return None

        return y.index(max_val)

    def add_noise(self, pattern, noise_level):
        """Добавление шума к образцу"""
        noisy = [x for x in pattern]
        for i in range(len(noisy)):
            if random.random() < noise_level:
                noisy[i] *= -1
        return noisy

    def test_accuracy(self, patterns, test_patterns, labels):
        """Тестирование точности сети"""
        correct = 0
        for test_pattern, true_label in zip(test_patterns, labels):
            predicted = self.predict(test_pattern)
            if predicted == true_label:
                correct += 1
        return correct / len(test_patterns)


def test_hopfield_10x10():
    """Тестирование сети Хопфилда для изображений 10x10"""
    print("\nТестирование сети Хопфилда для изображений 10x10")

    # Создаем два образца 10x10 (100 элементов)
    pattern1 = [1] * 100  # Полностью белое изображение
    for i in range(45, 55):  # Добавляем черную полосу
        pattern1[i] = -1

    pattern2 = [-1] * 100  # Полностью черное изображение
    for i in range(0, 100, 11):  # Добавляем белую диагональ
        pattern2[i] = 1

    # Создаем и обучаем сеть
    hn = HopfieldNetwork(100)
    hn.train([pattern1, pattern2])

    # Тестируем с разным уровнем шума
    noise_levels = [0.1, 0.2, 0.3, 0.4, 0.5]
    results = hn.test_noise_tolerance([pattern1, pattern2], noise_levels)

    # Выводим результаты
    for pattern, noise_results in results.items():
        print(f"\nДля образца:")
        for noise, accuracy in noise_results.items():
            print(f"Уровень шума {noise:.0%}: точность {accuracy:.1%}")


def test_hamming_7x7_digits():
    """Тестирование сети Хэмминга для цифр 7x7"""
    print("\nТестирование сети Хэмминга для цифр 7x7")

    # Упрощенные представления цифр 0-9 (7x7 = 49 элементов)
    digits = [
        # Цифра 0
        [
            1, 1, 1, 1, 1, 1, 1,
            1, -1, -1, -1, -1, -1, 1,
            1, -1, -1, -1, -1, -1, 1,
            1, -1, -1, -1, -1, -1, 1,
            1, -1, -1, -1, -1, -1, 1,
            1, -1, -1, -1, -1, -1, 1,
            1, 1, 1, 1, 1, 1, 1
        ],
        # Цифра 1
        [
            -1, -1, -1, 1, -1, -1, -1,
            -1, -1, 1, 1, -1, -1, -1,
            -1, 1, -1, 1, -1, -1, -1,
            -1, -1, -1, 1, -1, -1, -1,
            -1, -1, -1, 1, -1, -1, -1,
            -1, -1, -1, 1, -1, -1, -1,
            -1, -1, -1, 1, -1, -1, -1
        ],
        # Остальные цифры 2-9 (упрощенные представления)
        # Цифра 2
        [
            1, 1, 1, 1, 1, 1, 1,
            -1, -1, -1, -1, -1, -1, 1,
            -1, -1, -1, -1, -1, -1, 1,
            1, 1, 1, 1, 1, 1, 1,
            1, -1, -1, -1, -1, -1, -1,
            1, -1, -1, -1, -1, -1, -1,
            1, 1, 1, 1, 1, 1, 1
        ],
        # Цифра 3
        [
            1, 1, 1, 1, 1, 1, 1,
            -1, -1, -1, -1, -1, -1, 1,
            -1, -1, -1, -1, -1, -1, 1,
            1, 1, 1, 1, 1, 1, 1,
            -1, -1, -1, -1, -1, -1, 1,
            -1, -1, -1, -1, -1, -1, 1,
            1, 1, 1, 1, 1, 1, 1
        ],
        # Цифра 4
        [
            1, -1, -1, -1, -1, -1, 1,
            1, -1, -1, -1, -1, -1, 1,
            1, -1, -1, -1, -1, -1, 1,
            1, 1, 1, 1, 1, 1, 1,
            -1, -1, -1, -1, -1, -1, 1,
            -1, -1, -1, -1, -1, -1, 1,
            -1, -1, -1, -1, -1, -1, 1
        ],
        # Остальные цифры 5-9 заполним случайно для примера
        *[[random.choice([-1, 1]) for _ in range(49)] for _ in range(5)]
    ]

    # Создаем тестовые данные с шумом
    test_digits = []
    labels = []
    for i in range(10):
        for noise in [0.1, 0.2, 0.3]:
            noisy_digit = [x * (-1 if random.random() < noise else 1) for x in digits[i]]
            test_digits.append(noisy_digit)
            labels.append(i)

    # Создаем и обучаем сеть
    hn = HammingNetwork(10, 49)
    hn.train(digits)

    # Тестируем
    accuracy = hn.test_accuracy(digits, test_digits, labels)
    print(f"\nТочность распознавания цифр: {accuracy:.1%}")


def compare_networks():
    """Сравнение производительности сетей Хопфилда и Хэмминга"""
    print("\nСравнение сетей Хопфилда и Хэмминга")

    # Создаем тестовые данные - цифры 7x7 (49 элементов)
    digits = [
        [random.choice([-1, 1]) for _ in range(49)] for _ in range(10)
    ]

    # Создаем тестовые образцы с шумом
    test_data = []
    for i in range(10):
        for noise in [0.1, 0.2, 0.3]:
            noisy = [x * (-1 if random.random() < noise else 1) for x in digits[i]]
            test_data.append((noisy, i))

    hopfield = HopfieldNetwork(49)
    hopfield.train(digits)

    hamming = HammingNetwork(10, 49)
    hamming.train(digits)

    # Тестируем
    hopfield_correct = 0
    hamming_correct = 0

    for pattern, true_label in test_data:
        # Тестируем Хопфилда
        result = hopfield.predict(pattern)
        # Находим ближайший эталон
        min_dist = float('inf')
        predicted_label = -1
        for i, digit in enumerate(digits):
            dist = sum(1 for a, b in zip(result, digit) if a != b)
            if dist < min_dist:
                min_dist = dist
                predicted_label = i

        if predicted_label == true_label:
            hopfield_correct += 1

        # Тестируем Хэмминга
        predicted = hamming.predict(pattern)
        if predicted == true_label:
            hamming_correct += 1

    total_tests = len(test_data)
    print("\nРезультаты сравнения:")
    print(f"Сеть Хопфилда: {hopfield_correct}/{total_tests} ({hopfield_correct / total_tests:.1%})")
    print(f"Сеть Хэмминга: {hamming_correct}/{total_tests} ({hamming_correct / total_tests:.1%})")


if __name__ == "__main__":
    print("Лабораторная работа №4: Рекуррентные нейронные сети")

    # Тестирование сети Хопфилда
    test_hopfield_10x10()

    # Тестирование сети Хэмминга
    test_hamming_7x7_digits()

    # Сравнение двух сетей
    compare_networks()