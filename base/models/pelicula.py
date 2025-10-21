from typing import Any, Dict, List, Optional

from ..config.mysqlconnection import query_db


class Pelicula:
	TABLE = "peliculas"

	@classmethod
	def create(cls, data: Dict[str, Any]) -> int:
		query = (
			"INSERT INTO peliculas (titulo, director, fecha_estreno, sinopsis, usuario_id, created_at, updated_at) "
			"VALUES (%(titulo)s, %(director)s, %(fecha_estreno)s, %(sinopsis)s, %(usuario_id)s, NOW(), NOW())"
		)
		return int(query_db(query, data))

	@classmethod
	def get_all(cls) -> List[Dict[str, Any]]:
		query = (
			"SELECT p.id, p.titulo, p.director, p.fecha_estreno, p.sinopsis, p.usuario_id, p.created_at, p.updated_at, "
			"u.nombre AS autor_nombre, u.apellido AS autor_apellido "
			"FROM peliculas p JOIN usuarios u ON u.id=p.usuario_id ORDER BY p.id DESC"
		)
		return list(query_db(query))

	@classmethod
	def get_by_id(cls, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
		query = (
			"SELECT p.*, u.nombre AS autor_nombre, u.apellido AS autor_apellido "
			"FROM peliculas p JOIN usuarios u ON u.id=p.usuario_id WHERE p.id=%(id)s"
		)
		return query_db(query, data, fetch="one")

	@classmethod
	def update(cls, data: Dict[str, Any]) -> int:
		query = (
			"UPDATE peliculas SET titulo=%(titulo)s, director=%(director)s, fecha_estreno=%(fecha_estreno)s, sinopsis=%(sinopsis)s, updated_at=NOW() "
			"WHERE id=%(id)s AND usuario_id=%(usuario_id)s"
		)
		return int(query_db(query, data))

	@classmethod
	def delete(cls, data: Dict[str, Any]) -> int:
		query = "DELETE FROM peliculas WHERE id=%(id)s AND usuario_id=%(usuario_id)s"
		return int(query_db(query, data))

	@classmethod
	def exists_title(cls, data: Dict[str, Any]) -> bool:
		query = "SELECT id FROM peliculas WHERE titulo=%(titulo)s"
		return query_db(query, data, fetch="one") is not None