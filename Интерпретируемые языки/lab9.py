import math


class Shape:
    def __init__(self, identifier, x, y):
        """Инициализация фигуры с идентификатором и координатами центра (x, y)."""
        if not isinstance(identifier, str) or not identifier:
            raise ShapeError("Идентификатор должен быть непустой строкой.")

        self.identifier = identifier
        self.x = x
        self.y = y

    def move(self, dx, dy):
        """Метод для перемещения фигуры на плоскости."""
        self.x += dx
        self.y += dy
        print(f"{self.identifier} перемещен на ({self.x}, {self.y}).")


class Quad(Shape):
    def __init__(self, identifier, x, y, side_length):
        """Инициализация квадрата с заданной длиной стороны."""
        super().__init__(identifier, x, y)
        if side_length <= 0:
            raise ShapeError("Длина стороны квадрата должна быть положительной.")
        self.side_length = side_length

    @property
    def radius(self):
        """Радиус описанной окружности квадрата."""
        return math.sqrt(2) * self.side_length / 2


class Pentagon(Shape):
    def __init__(self, identifier, x, y, side_length):
        """Инициализация пятиугольника с заданной длиной стороны."""
        super().__init__(identifier, x, y)
        if side_length <= 0:
            raise ShapeError("Длина стороны пятиугольника должна быть положительной.")
        self.side_length = side_length

    @property
    def radius(self):
        """Радиус описанной окружности пятиугольника."""
        return self.side_length / (2 * math.sin(math.pi / 5))


def is_intersect(shape1, shape2):
    """Определяет факт пересечения двух фигур."""
    if not isinstance(shape1, Shape) or not isinstance(shape2, Shape):
        raise ShapeError("Оба объекта должны быть экземплярами класса Shape.")

    # Расстояние между центрами объектов
    distance = math.sqrt((shape1.x - shape2.x) ** 2 + (shape1.y - shape2.y) ** 2)

    # Проверка пересечения
    if distance <= shape1.radius + shape2.radius:
        print(f"Фигуры {shape1.identifier} и {shape2.identifier} пересекаются.")
        return True
    else:
        print(f"Фигуры {shape1.identifier} и {shape2.identifier} не пересекаются.")
        return False


# Пример использования
try:
    quad = Quad("Квадрат_1", 0, 0, 4)
    pentagon = Pentagon("Пятиугольник_1", 5, 5, 3)

    quad.move(2, 3)
    pentagon.move(-1, -1)

    # Проверка пересечения
    is_intersect(quad, pentagon)

except ShapeError as e:
    print(f"Ошибка: {e}")
