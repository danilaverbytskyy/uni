import math


class Figure:
    def __init__(self, ident: str, points=None):
        if points is None:
            points = [[]]
        self.ident = ident
        self.points = points

    def get_name(self):
        return self.ident

    def set_points(self, points: list):
        self.points = points

    def get_points(self):
        print(f'Координаты {self.ident}: ', self.points)

    def move(self, coordinates_shift):
        if len(coordinates_shift) != 2:
            raise Exception('Изменение координат должно быть из 2 чисел')
        for point in self.points:
            point[0] += coordinates_shift[0]
            point[1] += coordinates_shift[1]


class Pentagon(Figure):
    def __init__(self, ident, points):
        super().__init__(ident)
        if len(points) != 5:
            raise Exception("У квадрата должно быть 4 точки")
        self.points = points


class Quad(Figure):
    def __init__(self, ident, points):
        super().__init__(ident)
        if len(points) != 4:
            raise Exception("У квадрата должно быть 4 точки")
        self.points = points

    def is_intersect(self, pentagon: Pentagon):
        def segments_intersect(a, b, c, d):
            """Проверяет, пересекается ли АВ с СD"""
            def ccw(p1, p2, p3):
                return (p3[1] - p1[1]) * (p2[0] - p1[0]) > (p2[1] - p1[1]) * (p3[0] - p1[0])
            return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)

        # получает стороны фигур
        quad_edges = [(self.points[i], self.points[(i + 1) % 4]) for i in range(4)]
        pentagon_edges = [(pentagon.points[i], pentagon.points[(i + 1) % 5]) for i in range(5)]

        # проходим по всем возможным комбинациям сторон квадрата и пятиугольника
        for quad_edge in quad_edges:
            for pent_edge in pentagon_edges:
                if segments_intersect(quad_edge[0], quad_edge[1], pent_edge[0], pent_edge[1]):
                    return True

        return False


try:
    q1 = Quad('q1', [[0, 0], [0, 4], [4, 4], [4, 0]])
    q1.get_points()
    q1.move([1, 1])
    q1.get_points()

    p1 = Pentagon('p1', [[0, 0], [0, 4], [4, 4], [4, 0], [2, 6]])
    p1.get_points()
    print('Figures intersect' if q1.is_intersect(p1) else 'Figures dont intersect')
except ValueError as e:
    print(e)
