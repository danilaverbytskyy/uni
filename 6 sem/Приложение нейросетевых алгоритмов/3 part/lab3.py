import random

students = [
    [1, 'Варданян', 1, 1, 60, 79, 60, 72, 63, 1.00],
    [2, 'Горбунов', 1, 0, 60, 61, 30, 5, 17, 0.00],
    [3, 'Гуменюк', 0, 0, 60, 61, 30, 66, 58, 0.00],
    [4, 'Егоров', 1, 1, 85, 78, 72, 70, 85, 1.25],
    [5, 'Захарова', 0, 1, 65, 78, 60, 67, 65, 1.00],
    [6, 'Иванова', 0, 1, 60, 78, 77, 81, 60, 1.25],
    [7, 'Ишонина', 0, 1, 55, 79, 56, 69, 72, 0.00],
    [8, 'Климчук', 1, 0, 55, 56, 50, 56, 60, 0.00],
    [9, 'Лисовский', 1, 0, 55, 60, 21, 64, 50, 0.00],
    [10, 'Негреба', 1, 0, 60, 56, 30, 16, 17, 0.00],
    [11, 'Остапова', 0, 1, 85, 89, 85, 92, 85, 1.75],
    [12, 'Пашкова', 0, 1, 60, 88, 76, 66, 60, 1.25],
    [13, 'Попов', 1, 0, 55, 64, 0, 9, 50, 0.00],
    [14, 'Сазон', 0, 1, 80, 83, 62, 72, 72, 1.25],
    [15, 'Степоненко', 1, 0, 55, 10, 3, 8, 50, 0.00],
    [16, 'Терентьева', 0, 1, 60, 67, 57, 64, 50, 0.00],
    [17, 'Титов', 1, 1, 75, 98, 86, 82, 85, 1.50],
    [18, 'Чернова', 0, 1, 85, 85, 81, 85, 72, 1.25],
    [19, 'Четкин', 1, 1, 80, 56, 50, 69, 50, 0.00],
    [20, 'Шевченко', 1, 0, 55, 60, 30, 8, 60, 0.00]
]

X = [[s[2], s[3], s[4], s[5], s[6], s[7], s[8]] for s in students]
y = [s[9] for s in students]
names = [s[1] for s in students]


def normalize_data(data):
    mins = [min(col) for col in zip(*data)]
    maxs = [max(col) for col in zip(*data)]
    normalized = []
    for row in data:
        norm_row = [(val - mins[i]) / (maxs[i] - mins[i]) if maxs[i] != mins[i] else 0.5
                    for i, val in enumerate(row)]
        normalized.append(norm_row)
    return normalized, mins, maxs


X_norm, mins, maxs = normalize_data(X)


class KohonenNetwork:
    def __init__(self, input_size, output_size):
        self.weights = [[random.random() for _ in range(input_size)]
                        for _ in range(output_size)]

    def train(self, data, epochs=6, initial_rate=0.3, decay=0.05):
        for epoch in range(epochs):
            learning_rate = initial_rate - epoch * decay
            if learning_rate < 0:
                learning_rate = 0
            for sample in data:
                winner = self.find_winner(sample)
                for i in range(len(self.weights[winner])):
                    self.weights[winner][i] += learning_rate * (sample[i] - self.weights[winner][i])

    def find_winner(self, sample):
        min_dist = float('inf')
        winner = 0
        for i, neuron in enumerate(self.weights):
            dist = sum((s - w) ** 2 for s, w in zip(sample, neuron)) ** 0.5
            if dist < min_dist:
                min_dist = dist
                winner = i
        return winner

    def predict(self, data):
        clusters = []
        for sample in data:
            clusters.append(self.find_winner(sample))
        return clusters


input_size = 7
output_size = 4
kohonen = KohonenNetwork(input_size, output_size)
kohonen.train(X_norm)

clusters = kohonen.predict(X_norm)

cluster_info = {i: {'students': [], 'scholarships': []} for i in range(output_size)}
for i, cluster in enumerate(clusters):
    cluster_info[cluster]['students'].append(names[i])
    cluster_info[cluster]['scholarships'].append(y[i])

print("Результаты кластеризации:")
for cluster in sorted(cluster_info.keys()):
    students = cluster_info[cluster]['students']
    scholarships = cluster_info[cluster]['scholarships']
    avg_scholarship = sum(scholarships) / len(scholarships) if scholarships else 0
    print(f"\nКластер {cluster + 1}:")
    print(f"Количество студентов: {len(students)}")
    print(f"Средняя стипендия: {avg_scholarship:.2f}")
    print(f"Студенты: {', '.join(students)}")

print("\nПодробное распределение студентов по кластерам:")
for i in range(len(students)):
    print(f"{names[i]:<12} -> Кластер {clusters[i] + 1}, Стипендия: {y[i]}")