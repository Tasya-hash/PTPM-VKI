import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class UserInterface(ABC):
    @abstractmethod
    def get_triangle_sides(self):
        ...

class ConsoleUserInterface(UserInterface):
    def get_triangle_sides(self):
        raw_a = input("Введите сторону А: ").strip()
        raw_b = input("Введите сторону B: ").strip()
        raw_c = input("Введите сторону C: ").strip()

        logger.debug(f"Ввод: A='{raw_a}', B='{raw_b}', C='{raw_c}'")
        try:
            a = float(raw_a)
            b = float(raw_b)
            c = float(raw_c)
        except (TypeError, ValueError) as ex:
            logger.error("Не удалось преобразовать входные данные во float")
            raise ValueError("non-numeric input") from ex
        return a, b, c