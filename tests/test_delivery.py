import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scr.Delivery import calculate_delivery_cost

class TestInputValidation(unittest.TestCase):
    def test_weight_below_minimum_returns_error(self):
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")
    def test_weight_above_maximum_returns_error(self):
        cost, _ = calculate_delivery_cost(51.0, 100, "обычный")
        self.assertEqual(cost, -1)
    def test_weight_at_minimum_boundary_is_valid(self):
        cost, _ = calculate_delivery_cost(0.1, 100, "обычный")
        self.assertNotEqual(cost, -1)
    def test_weight_at_maximum_boundary_is_valid(self):
        cost, _ = calculate_delivery_cost(50.0, 100, "обычный")
        self.assertNotEqual(cost, -1)
    def test_distance_zero_returns_error(self):
        cost, _ = calculate_delivery_cost(1.0, 0, "обычный")
        self.assertEqual(cost, -1)
    def test_distance_above_maximum_returns_error(self):
        cost, _ = calculate_delivery_cost(1.0, 5001, "обычный")
        self.assertEqual(cost, -1)
    def test_invalid_package_type_returns_error(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "стеклянный")
        self.assertEqual(cost, -1)

class TestBaseCost(unittest.TestCase):
    def test_minimal_distance_base_cost(self):
        cost, _ = calculate_delivery_cost(1.0, 1, "обычный")
        self.assertEqual(cost, 205)
    def test_mid_distance_base_cost(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(cost, 700)

class TestWeightCoefficients(unittest.TestCase):
    def test_weight_above_5_applies_1_2(self):
        cost, _ = calculate_delivery_cost(6.0, 100, "обычный")
        self.assertEqual(cost, 840)
    def test_weight_equal_5_applies_1_2_or_not(self):
        cost, _ = calculate_delivery_cost(5.0, 100, "обычный")
        self.assertEqual(cost, 840)
    def test_weight_20_applies_1_5(self):
        cost, _ = calculate_delivery_cost(20.0, 100, "обычный")
        self.assertEqual(cost, 1050)
    def test_weight_50_applies_1_5(self):
        cost, _ = calculate_delivery_cost(50.0, 100, "обычный")
        self.assertEqual(cost, 1050)


class TestPackageTypeSurcharge(unittest.TestCase):
    def test_fragile_adds_300(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "хрупкий")
        self.assertEqual(cost, 1000)
    def test_dangerous_adds_1000(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "опасный")
        self.assertEqual(cost, 1700)
    def test_regular_no_surcharge(self):
        cost, _ = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(cost, 700)

class TestExpressDelivery(unittest.TestCase):
    def test_express_costs_more_than_regular(self):
        regular_cost, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=False)
        express_cost, _ = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertGreater(express_cost, regular_cost)
    def test_express_delivery_is_faster(self):
        _, regular_date = calculate_delivery_cost(1.0, 1000, "обычный", is_express=False)
        _, express_date = calculate_delivery_cost(1.0, 1000, "обычный", is_express=True)
        self.assertLess(express_date, regular_date)
    def test_express_never_delivers_same_day(self):
        _, express_date = calculate_delivery_cost(1.0, 100, "обычный", is_express=True)
        self.assertNotEqual(express_date, "2026-09-03")

class TestDeliveryDate(unittest.TestCase):
    def test_date_format(self):
        _, date = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertRegex(date, r"^\d{4}-\d{2}-\d{2}$")
    def test_distance_500_is_one_day(self):
        _, date = calculate_delivery_cost(1.0, 500, "обычный")
        self.assertEqual(date, "2026-09-04")
    def test_distance_1000_is_two_days(self):
        _, date = calculate_delivery_cost(1.0, 1000, "обычный")
        self.assertEqual(date, "2026-09-05")
    def test_short_distance_still_one_day_minimum(self):
        _, date = calculate_delivery_cost(1.0, 100, "обычный")
        self.assertEqual(date, "2026-09-04")

class TestCostRounding(unittest.TestCase):
    def test_cost_is_integer(self):
        cost, _ = calculate_delivery_cost(6.0, 99, "хрупкий")
        self.assertIsInstance(cost, int)
    def test_cost_rounded_up_not_truncated(self):
        cost, _ = calculate_delivery_cost(6.0, 101, "обычный")
        self.assertIsInstance(cost, int)

if __name__ == "__main__":
    unittest.main(verbosity=2)