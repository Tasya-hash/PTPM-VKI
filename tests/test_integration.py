import unittest
from unittest.mock import patch, MagicMock
from scr.calculator import TriangleCalculator
from scr.repository import TriangleRepository
from scr.ui import ConsoleUserInterface, UserInterface
from scr.notifier import Notifier
from scr.controller import Controller

class TestUserInterfaceInput(unittest.TestCase):
    def test_ui_returns_sides_from_mocked_input(self):
        with patch("builtins.input", side_effect=["3", "4", "5"]):
            ui = ConsoleUserInterface()
            self.assertEqual(ui.get_triangle_sides(), (3.0, 4.0, 5.0))

    def test_ui_raises_on_non_numeric_input(self):
        with patch("builtins.input", side_effect=["abc", "4", "5"]):
            ui = ConsoleUserInterface()
            with self.assertEqual(ValueError):
                ui.get_triangle_sides()
class TestRepositoryCRUD(unittest.TestCase):

    def setUp(self):
        self.repo = TriangleRepository(":memory:")

    def tearDown(self):
        self.repo.close()

    def test_repository_save_get_delete(self):
        self.repo.add(3, 4, 5, "разносторонний", "")
        self.assertEqual(self.repo.get(3, 4, 5), ("разносторонний", ""))
        self.assertTrue(self.repo.delete(3, 4, 5))
        self.assertIsNone(self.repo.get(3, 4, 5))

    def test_repository_returns_none_for_missing_record(self):
        self.assertIsNone(self.repo.get(9, 9, 9))


class TestCalculatorVertices(unittest.TestCase):

    def test_compute_vertices_returns_three_points(self):
        verts = compute_vertices(3, 4, 5)
        self.assertEqual(len(verts), 3)

    def test_compute_vertices_in_bounds(self):
        verts = compute_vertices(3, 4, 5)
        for (x, y) in verts:
            self.assertGreaterEqual(x, 0)
            self.assertLessEqual(x, 100)
            self.assertGreaterEqual(y, 0)
            self.assertLessEqual(y, 100)


class TestControllerIntegration(unittest.TestCase):

    def setUp(self):
        self.repo = TriangleRepository(":memory:")
        self.calculator = TriangleCalculator()
        self.ui = MagicMock(spec=UserInterface)
        self.notifier = MagicMock(spec=Notifier)
        self.notifier.send.return_value = True
        self.controller = Controller(
            self.ui, self.repo, self.calculator, self.notifier
        )

    def tearDown(self):
        self.repo.close()

    def test_controller_full_flow_new_triangle(self):
        self.ui.get_triangle_sides.return_value = (3.0, 4.0, 5.0)

        kind, error, from_cache = self.controller.process()

        self.assertEqual(kind, "разносторонний")
        self.assertEqual(error, "")
        self.assertFalse(from_cache)
        self.assertEqual(self.repo.get(3.0, 4.0, 5.0), ("разносторонний", ""))
        self.notifier.send.assert_called_once()

    def test_controller_uses_cache_on_second_call(self):
        self.ui.get_triangle_sides.return_value = (3.0, 4.0, 5.0)

        self.controller.process()
        self.controller.calculator = MagicMock()

        kind, error, from_cache = self.controller.process()

        self.assertTrue(from_cache)
        self.assertEqual(kind, "разносторонний")
        self.controller.calculator.calculate.assert_not_called()

    def test_controller_sends_notification_after_processing(self):
        self.ui.get_triangle_sides.return_value = (2.0, 2.0, 2.0)

        self.controller.process()

        self.notifier.send.assert_called_once()
        sent_message = self.notifier.send.call_args[0][0]
        self.assertIn("2.0x2.0x2.0", sent_message)
        self.assertIn("равносторонний", sent_message)

    def test_controller_error_path_notification(self):
        self.ui.get_triangle_sides.return_value = (1.0, 2.0, 10.0)

        kind, error, from_cache = self.controller.process()

        self.assertEqual(kind, "не треугольник")
        self.assertTrue(error)
        self.assertFalse(from_cache)
        self.assertEqual(self.repo.get(1.0, 2.0, 10.0), (kind, error))
        self.notifier.send.assert_called_once()


if __name__ == "__main__":
    unittest.main()