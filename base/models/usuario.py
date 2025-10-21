from typing import Any, Dict, List, Optional

from ..config.mysqlconnection import query_db
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario:
	TABLE = "usuarios"

	@classmethod
	def create(cls, data: Dict[str, Any]) -> int:
		data = data.copy()
		data["password_hash"] = generate_password_hash(data.pop("password"))
		query = (
			"INSERT INTO usuarios (nombre, apellido, email, password_hash, created_at, updated_at) "
			"VALUES (%(nombre)s, %(apellido)s, %(email)s, %(password_hash)s, NOW(), NOW())"
		)
		return int(query_db(query, data))

	@classmethod
	def get_all(cls) -> List[Dict[str, Any]]:
		query = "SELECT id, nombre, apellido, email, created_at, updated_at FROM usuarios ORDER BY id DESC"
		return list(query_db(query))

	@classmethod
	def get_by_id(cls, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		query = "SELECT id, nombre, apellido, email, created_at, updated_at FROM usuarios WHERE id=%(id)s"
		return query_db(query, data, fetch="one")

	@classmethod
	def update(cls, data: Dict[str, Any]) -> int:
		query = (
			"UPDATE usuarios SET nombre=%(nombre)s, apellido=%(apellido)s, email=%(email)s, updated_at=NOW() "
			"WHERE id=%(id)s"
		)
		return int(query_db(query, data))

	@classmethod
	def get_by_email(cls, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		query = "SELECT * FROM usuarios WHERE email=%(email)s"
		return query_db(query, data, fetch="one")

	@classmethod
	def check_password(cls, user: Dict[str, Any], password: str) -> bool:
		return check_password_hash(user["password_hash"], password)

	@classmethod
	def delete(cls, data: Dict[str, Any]) -> int:
		query = "DELETE FROM usuarios WHERE id=%(id)s"
		return int(query_db(query, data))