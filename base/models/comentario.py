from typing import Any, Dict, List

from ..config.mysqlconnection import query_db


class Comentario:
	TABLE = "comentarios"

	@classmethod
	def create(cls, data: Dict[str, Any]) -> int:
		query = (
			"INSERT INTO comentarios (contenido, usuario_id, pelicula_id, created_at, updated_at) "
			"VALUES (%(contenido)s, %(usuario_id)s, %(pelicula_id)s, NOW(), NOW())"
		)
		return int(query_db(query, data))

	@classmethod
	def list_for_movie(cls, data: Dict[str, Any]) -> List[Dict[str, Any]]:
		query = (
			"SELECT c.id, c.contenido, c.usuario_id, c.pelicula_id, c.created_at, "
			"u.nombre FROM comentarios c JOIN usuarios u ON u.id=c.usuario_id "
			"WHERE c.pelicula_id=%(pelicula_id)s ORDER BY c.id DESC"
		)
		return list(query_db(query, data))

	@classmethod
	def delete(cls, data: Dict[str, Any]) -> int:
		query = "DELETE FROM comentarios WHERE id=%(id)s AND usuario_id=%(usuario_id)s"
		return int(query_db(query, data))