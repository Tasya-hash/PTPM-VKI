import logging
import sys
import math
import os
from datetime import datetime

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
        #logging.FileHandler(os.path.join(LOG_DIR, "logs/file_txt.log"), encoding="utf-8")
        logging.FileHandler("logs/file_txt")
    ]
)

logging.info("Логгер успешно сконфигурирован")
logging.info("Приложение запущено")

EPS = 1e-9
FIELD_SIZE = 100
MARGIN = 10

def parse_sides(raw_a: str, raw_b: str, raw_c: str):
    try:
        a = float(raw_a)
        b = float(raw_b)
        c = float(raw_c)
    except (TypeError, ValueError) as ex:
        logging.error("Не удалось преобразовать входные данные во float.")
        logging.exception("Трассировка ошибки парсинга: ")
        raise ValueError("non-numeric input") from ex

    if a<=0 or b<=0 or c<=0:
        logging.warning(f"Обнаружены неположительные стороны.")
        raise ValueError("non-positive sides")
    return a, b, c

def is_triangle(a: float, b: float, c: float) -> bool:
    return (a + b > c + EPS) and (a + c > b + EPS) and (b + c > a + EPS)

def classify_triangle(a: float, b: float, c: float) -> str:
    if not is_triangle(a, b, c):
        return "не треугольник"

    def eq(x, y):
        return abs(x - y) < EPS

    if eq(a, b) and eq(b, c):
        return "равносторонний"
    if eq(a, b) or eq(b, c) or eq(a, c):
        return "равнобедренный"
    return "разносторонний"

def compute_vertices(a: float, b: float, c: float):
    usable = FIELD_SIZE - 2 * MARGIN
    max_side = max(a, b, c)
    scale = usable / max_side if max_side > 0 else 1.0

    ax = MARGIN
    ay = FIELD_SIZE - MARGIN

    bx = ax + a * scale
    by = ay

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

def process_request(raw_a: str, raw_b: str, raw_c: str):
    logging.info(f"Запрос A='{raw_a}', B='{raw_b}', C='{raw_c}'")
    #тут нечисловые данные
    try:
        a, b, c = parse_sides(raw_a, raw_b, raw_c)
    except ValueError as ex:
        if str(ex) == "non-numeric input":
            logging.error("Нечисловые данные")
            return "", [(-2, -2), (-2, -2), (-2, -2)]
        else:
            logging.error("Ошибочные числовые данные (не положительные)")
            return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]
    #классификация
    try:
        kind = classify_triangle(a, b, c)
        logging.debug(f"Вид треугольника: {kind}")
    except Exception:
        logging.exception("Ошибка при классификации треугольника:")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    # если не треугольник - вернуть (-1, -1)
    if kind == "не треугольник":
        logging.warning("Стороны не образуются")
        return kind, [(-1, -1), (-1, -1), (-1, -1)]

    #координаты
    try:
        vertices = compute_vertices(a, b, c)
    except Exception:
        logging.exception("Ошибка при расчете координат:")
        return kind, vertices


def Main():
    logging.info("Старт обработки запроса")
    try:
        raw_a = input("Введите сторону А: ").strip()
        raw_b = input("Введите сторону B: ").strip()
        raw_c = input("Введите сторону C: ").strip()
    except Exception:
        logging.exception("Ошибка чтения входных данных")
        return

    try:
        kind, vertices = process_request(raw_a, raw_b, raw_c)
        print(f"\nВид треугольника: {kind}")
        print(f"\nКоординаты вершин {vertices}")
    except Exception:
        logging.critical("Критическая ошибка обработки запроса", exc_info=True)
        print("Критическая ошибка")
    finally:
        logging.info("Завершение обработки")

if __name__ == "__main__":
    Main()