import logging
import os
import sys
import unittest

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join(LOG_DIR, "test_report.log"), encoding="utf-8"),
    ],
)

logging.info("Логгер успешно сконфигурирован")
logging.info("Приложение запущено")


class LoggingTestResult(unittest.TextTestResult):

    def startTest(self, test):
        super().startTest(test)
        logging.info(f"СТАРТ : {test.id()}")

    def addSuccess(self, test):
        super().addSuccess(test)
        logging.info(f"OK : {test.id()}")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        logging.error(f"FAIL : {test.id()}")
        logging.error(self._exc_info_to_string(err, test))

    def addError(self, test, err):
        super().addError(test, err)
        logging.error(f"ERROR : {test.id()}")
        logging.error(self._exc_info_to_string(err, test))

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        logging.warning(f"SKIP : {test.id()} — {reason}")


class LoggingTestRunner(unittest.TextTestRunner):
    resultclass = LoggingTestResult

def Main():
    logging.info("=" * 70)
    logging.info("ЗАПУСК ТЕСТОВ")
    logging.info("=" * 70)

    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests", pattern="test_*.py")

    runner = LoggingTestRunner(verbosity=2)
    result = runner.run(suite)

    total = result.testsRun
    failed = len(result.failures)
    errored = len(result.errors)
    skipped = len(result.skipped)
    passed = total - failed - errored - skipped

    logging.info("=" * 70)
    logging.info("ИТОГОВАЯ СТАТИСТИКА")
    logging.info("=" * 70)
    logging.info(f"Всего тестов: {total}")
    logging.info(f"Прошло успешно: {passed}")
    logging.info(f"Упало (assert): {failed}")
    logging.info(f"Завершилось ошибкой: {errored}")
    logging.info(f"Пропущено: {skipped}")

    if result.failures:
        logging.error("-" * 70)
        logging.error("СПИСОК УПАВШИХ ТЕСТОВ (для пункта В отчёта):")
        logging.error("-" * 70)
        for test, traceback_text in result.failures:
            logging.error(f" • {test.id()}")
            for line in traceback_text.strip().split("\n")[-3:]:
                logging.error(f" {line}")

    if result.errors:
        logging.error("-" * 70)
        logging.error("СПИСОК ТЕСТОВ С ОШИБКАМИ (исключения в коде):")
        logging.error("-" * 70)
        for test, _ in result.errors:
            logging.error(f" • {test.id()}")

    logging.info("=" * 70)
    logging.info("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    logging.info("=" * 70)


if __name__ == "__main__":
    Main()