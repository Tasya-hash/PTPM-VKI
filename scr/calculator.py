import math

EPS = 1e-9
FIELD_SIZE = 100
MARGIN = 10

class TriangleCalculator:
    def calculate(self, a: float, b: float, c: float):
        if a<= 0 or b <= 0 or c <= 0:
            return "не треугольник", "стороны должны быть положительными"
        if not self._is_triangle(a, b, c):
            return "не треугольник", "нарушено неравенство треугольника"
        return self._classify(a, b, c), ""

    @staticmethod
    def _is_triangle(a, b, c):
        return (a + b > c + EPS) and (a + c > b + EPS) and (b + c > a + EPS)

    @staticmethod
    def _eq(x, y):
        return abs(x - y) < EPS

    def _classify(self, a, b, c):
        if self._eq(a, b) and self._eq(b, c):
            return "равносторонний"
        if self._eq(a, b) or self._eq(b, c) or self._eq(a, c):
            return "равносторонний"
        return "разносторонний"

    @staticmethod
    def compute_vertices(a, b, c):
        usable = FIELD_SIZE - 2 * MARGIN
        max_side = max(a, b, c)
        scale = usable / max_side if max_side > 0 else 1.0
        ax, ay = MARGIN, FIELD_SIZE - MARGIN
        bx, by = ax + a * scale, ay
        cos_a = (a * a + c * c - b * b) / (2 * a * c)
        cos_a = max(-1.0, min(1.0, cos_a))
        sin_a = math.sqrt(max(0.0, 1.0 - cos_a * cos_a))
        cx = ax + c * scale * cos_a
        cy = ay - c * scale * sin_a

        def clamp(v):
            return int(round(max(0, min(FIELD_SIZE, v))))

        return ([clamp(ax), clamp(ay)],
            [clamp(bx), clamp(by)],
            [clamp(cx), clamp(cy)])
