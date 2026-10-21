import unittest
import os
import sys

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scr'))
)
from scr.lab_1 import (
parse_sides,
is_triangle,
classify_triangle,
compute_vertices,
process_request,
FIELD_SIZE
)

class TestParseSides(unittest.TestCase):
    def test_parse_sides_returns_floats_for_valid_input(self):
        a, b, c = parse_sides("3", "4", "5")
        self.assertIsInstance(a, float)
        self.assertIsInstance(b, float)
        self.assertIsInstance(c, float)
        self.assertEqual((a, b, c), (3.0, 4.0, 5.0))

    def test_sides_accepts_float_string(self):
        a, b, c = parse_sides("2.5", "3.5", "4.5")
        self.assertIsInstance(a, 2.5)
        self.assertIsInstance(b, 3.5)
        self.assertIsInstance(c, 4.5)

    def test_parse_sides_raises_valueerror_for_non_numeric(self):
        with self.assertRaises(ValueError) as ctx:
            parse_sides("abs", "4", "5")
        self.assertEqual(str(ctx.exception), "non-numeric input")

    def test_parse_sides_raises_valueerror_for_zero_side(self):
        with self.assertRaises(ValueError) as ctx:
            parse_sides("0", "4", "5")
        self.assertEqual(str(ctx.exception), "non-positive input")

    def test_parse_sides_raises_valueerror_for_negative_side(self):
        with self.assertRaises(ValueError) as ctx:
            parse_sides("-1", "4", "5")
        self.assertEqual(str(ctx.exception), "non-positive input")

class TestIsTriangle(unittest.TestCase):
    def test_is_triangle_returns_true_for_classic_345(self):
        self.assertTrue(is_triangle(3, 4, 5))
    def test_is_triangle_returns_false_for_degenerate_line(self):
        self.assertFalse(is_triangle(1, 2, 3))
    def test_is_triangle_returns_true_for_long_side(self):
        self.assertTrue(is_triangle(3, 3, 7))
    def test_is_triangle_returns_true_for_tiny_sides(self):
        self.assertTrue(is_triangle(0.001, 0.001, 0.001))

class TestClassifyTriangle(unittest.TestCase):
    def test_classify_returns_equilateral_for_equal_sides(self):
        self.assertEqual(classify_triangle(3, 3, 3), "равносторонний")
    def test_classify_returns_isosceles_for_two_equal_sides(self):
        self.assertEqual(classify_triangle(3, 3, 5), "равнобедренный")
    def test_classify_returns_scalene_for_three_different_sides(self):
        self.assertEqual(classify_triangle(3, 4, 5), "разносторонний")
    def test_classify_returns_not_triangle_for_inequality_violation(self):
        self.assertEqual(classify_triangle(1, 2, 100), "не треугольник")
    def test_classify_handles_float_with_precision(self):
        self.assertEqual(classify_triangle(0.1 + 0.2, 0.3, 0.3), "равносторонний")

class TestComputeVertices(unittest.TestCase):
    def test_compute_vertices_returns_three_points(self):
        v = compute_vertices(3, 4, 5)
        self.assertEqual(len(v), 3)
    def test_compute_vertices_returns_integer_tuples(self):
        for x, y in compute_vertices(3, 4, 5):
            self.assertIsInstance(x, int)
            self.assertIsInstance(y, int)
    def test_compute_vertices_points_within_field_bouns(self):
        cases = [(3, 4, 5), (2, 2, 2), (100, 100, 100), (0.1, 0.1, 0.1)]
        for sides in cases:
            v = compute_vertices(*sides)
            for x, y in v:
                self.assertGreaterEqual(x, 0, f"x<0 для сторон {sides}")
                self.assertLessEqual(x, FIELD_SIZE, f"x>{FIELD_SIZE} для {sides}")
                self.assertGreaterEqual(y, 0, f"y<0 для сторон {sides}")
                self.assertLessEqual(y, FIELD_SIZE, f"y>{FIELD_SIZE} для {sides}")
    def test_compute_vertices_differ_for_different_shapes(self):
        v1 = compute_vertices(3, 3, 3)
        v2 = compute_vertices(3, 4, 5)
        self.assertNotEqual(v1, v2)

class TestProcessRequest(unittest.TestCase):
    def test_process_request_returns_scalene_with_vertices(self):
        kind, v = process_request("3", "4", "5")
        self.assertEqual(kind, "разносторонний")
        self.assertEqual(len(v), 3)
    def test_process_request_returns_equilateral(self):
        kind, v = process_request("2", "2", "2")
        self.assertEqual(kind, "равносторонний")
        self.assertEqual(len(v), 3)
    def test_process_request_returns_isosceles(self):
        kind, v = process_request("3", "3", "4")
        self.assertEqual(kind, "равнобедренный")
        self.assertEqual(len(v), 3)
    def test_process_request_returns_not_triangle_not_triangle_for_bad_inequality(self):
        kind, v = process_request("1", "2", "10")
        self.assertEqual(kind, "не треугольник")
        self.assertEqual(v, [(-1, -1)] * 3)
    def test_process_request_returns_empty_for_non_numeric(self):
        kind, v = process_request("abc", "4", "5")
        self.assertEqual(kind, "")
        self.assertEqual(v, [(-2, -2)] * 3)
    def test_process_request_returns_minus_two_for_non_numeric(self):
        kind, v = process_request("3", "hello", "5")
        self.assertEqual(v, [(-2, -2)] * 3)
    def test_process_request_returns_minus_one_for_negative_side(self):
        kind, v = process_request("-1", "4", "5")
        self.assertEqual(kind, "не треугольник")
        self.assertEqual(v, [(-1, -1)] * 3)
    def test_process_request_returns_minus_one_for_zero_side(self):
        kind, v = process_request("0", "4", "5")
        self.assertEqual(kind, "не треугольник")
        self.assertEqual(v, [(-1, -1)] * 3)

if __name__ == "__main__":
    unittest.main(verbosity=2)
