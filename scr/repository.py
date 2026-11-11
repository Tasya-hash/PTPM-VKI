import logging
import sqlite3

logger = logging.getLogger(__name__)

class TriangleRepository:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._init_db()

        def _init_db(self):
            self.conn = sqlite3.connect(self.db_path)
            self.conn.execute()
            self.conn.commit()
            logger.debug(f"БД инициализирована: {self.db_path}")

        def add(self, a: float, b: float, c:float, kind: str, error: str = ""):
            logger.debug(f"add({a}, {b}, {c}, kind = {kind})")
            cur = self.conn.execute(
                "INSERT OR REPLACE INTO triangles ",
                "(side1, side2, side3, kind, error) VALUES (?, ?, ?, ?, ?)",
                (a, b, c, kind, error)
            )
            self.conn.commit()

        def get(self, a: float, b: float, c: float):
            cur = self.conn.execute(
                "SELECT kinf, error FROM triangles "
                "WHERE side1 = ? AND side2 = ? AND side3 = ?",
                (a, b, c)
            )
            row = cur.fetchone()
            if row is None:
                logger.debug(f"get({a}, {b}, {c}) -> None")
                return None
            logger.debug(f"get({a}, {b}, {c}) -> {row}")
            return (row[0], row[1])

        def delete(self, a: float, b: float, c: float) -> bool:
            cur = self.conn.execute(
                "DELETE FROM triangles "
                "WHERE side1 = ? AND side2 = ? AND side3 = ?",
                (a, b, c)
            )
            self.conn.commit()
            deleted = cur.rowcount > 0
            logger.debug(f"delete({a}, {b}, {c}) -> {deleted}")
            return deleted
        def close(self):
            self.conn.close()
            logger.debug("БД закрыта")