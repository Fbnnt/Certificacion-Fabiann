import os
from contextlib import contextmanager
from typing import Any, Dict, List, Optional

import pymysql.cursors


DB_NAME = os.getenv("MYSQL_DB", "cine_db")
DB_CONFIG = {
	"host": os.getenv("MYSQL_HOST", "localhost"),
	"user": os.getenv("MYSQL_USER", "root"),
	"password": os.getenv("MYSQL_PASSWORD", "root"),  # Contraseña por defecto
	"database": DB_NAME,
	"port": int(os.getenv("MYSQL_PORT", "3306")),
	"charset": "utf8mb4",
	"cursorclass": pymysql.cursors.DictCursor,
	"autocommit": False,
}


@contextmanager
def get_connection():
	"""Get a database connection."""
	conn = pymysql.connect(**DB_CONFIG)
	try:
		yield conn
	finally:
		conn.close()


def query_db(query: str, data: Optional[Dict[str, Any]] = None, fetch: str = "all") -> Any:
	"""Run a query and return results.

	- fetch="one" | "all" | "none"
	"""
	with get_connection() as conn:
		cursor = conn.cursor()
		try:
			cursor.execute(query, data or {})
			if query.strip().lower().startswith(("insert", "update", "delete")):
				conn.commit()
				return cursor.lastrowid if query.strip().lower().startswith("insert") else cursor.rowcount
			if fetch == "one":
				return cursor.fetchone()
			if fetch == "none":
				return None
			return cursor.fetchall()
		finally:
			cursor.close()