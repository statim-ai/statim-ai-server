import sqlite3


class SQLiteDB:
    def __init__(self, file) -> None:
        self.file = file

    def execute_query(self, query) -> None:
        def body(cursor, conn):
            cursor.execute(query)
            conn.commit()

        self._execute(body)

    def execute_update(self, query, params) -> int:
        return self.execute_insert(query, params)

    def execute_insert(self, query, params) -> int:
        def body(cursor, conn):
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid

        return self._execute(body)

    def execute_select(self, query, params=()) -> list[any]:
        def body(cursor, conn):
            cursor.execute(query, params)
            return cursor.fetchall()

        return self._execute(body)

    def _execute(self, body):
        conn = sqlite3.connect(
            self.file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        result = body(cursor, conn)

        cursor.close()
        conn.close()

        return result
