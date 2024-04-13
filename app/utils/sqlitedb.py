"""Module with a Class to connect to a SQLite database."""

import sqlite3

from typing import Any


class SQLiteDB:
    """Class to connect to a SQLite database."""

    def __init__(self, file) -> None:
        self.file = file

    def execute_query(self, query) -> None:
        """Execute a SQL statment without parameters."""

        def body(cursor, conn):
            cursor.execute(query)
            conn.commit()

        self._execute(body)

    def execute_update(self, query, params) -> int:
        """Execute a Update SQL query and return the row ID."""
        return self.execute_insert(query, params)

    def execute_insert(self, query, params) -> int:
        """Execute a Insert SQL query and return the row ID."""

        def body(cursor, conn):
            cursor.execute(query, params)
            conn.commit()
            return cursor.lastrowid

        return self._execute(body)

    def execute_select(self, query, params=()) -> Any:
        """Execute a Select SQL query and return the result."""

        def body(cursor, conn):
            cursor.execute(query, params)
            return cursor.fetchall()

        return self._execute(body)

    def _execute(self, body) -> Any:
        conn = sqlite3.connect(self.file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        result = body(cursor, conn)

        cursor.close()
        conn.close()

        return result
