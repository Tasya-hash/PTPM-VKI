import logging
from logging import error

from pyexpat.errors import messages

logger = logging.getLogger(__name__)

class Controller:
    def __init__(self, ui, repository, calculator, notifier):
        self.ui = ui
        self.repository = repository
        self.calculator = calculator
        self.notifier = notifier

    def process(self):
        logger.info("Старт обработки запроса")
        a, b, c = self.ui.get_triangle_sides()
        cached = self.repository.get(a, b, c)
        if cached is not None:
            kind, error = cached
            from_cache = True
            logger.info(f"Данные взяты из БД: {kind}, error='{error}'")
        else:
            kind, error = self.calculator.calculate(a, b, c)
            self.repository.add(a, b, c, kind, error)
            from_cache = False
            logger.info(f"Данные вычислены и сохранены: {kind}")

        message = f"Треугольник {a}x{b}x{c}: kind"
        if error:
            message += f" ({error})"
        self.notifier.send(message)

        logger.info("Завершение обработки запроса")
        return kind, error, from_cache