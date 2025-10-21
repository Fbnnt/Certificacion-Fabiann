from flask import Blueprint, render_template, request, redirect, flash, url_for, session

from ..models.pelicula import Pelicula
from ..models.comentario import Comentario


peliculas_bp = Blueprint("peliculas", __name__)


@peliculas_bp.get("/cine")
def listar_peliculas():
	if "user_id" not in session:
		flash("Debes iniciar sesión", "error")
		return redirect("/")
	peliculas = Pelicula.get_all()
	return render_template("dashboard.html", peliculas=peliculas, user_name=session.get("user_name"))


@peliculas_bp.get("/cine/nueva")
def nueva_pelicula():
	if "user_id" not in session:
		return redirect("/")
	form_data = session.pop("form_data", {})
	return render_template("nueva.html", form_data=form_data)


@peliculas_bp.post("/cine/nueva")
def crear_pelicula():
	if "user_id" not in session:
		return redirect("/")
	data = {
		"titulo": request.form.get("titulo", "").strip(),
		"director": request.form.get("director", "").strip(),
		"fecha_estreno": request.form.get("fecha_estreno", "").strip(),
		"sinopsis": request.form.get("sinopsis", "").strip(),
		"usuario_id": session["user_id"],
	}
	# Validaciones
	errors = []
	if not data["titulo"] or len(data["titulo"]) < 3:
		errors.append("El nombre de la película debe tener al menos 3 caracteres")
	if Pelicula.exists_title({"titulo": data["titulo"]}):
		errors.append("El nombre de la película debe ser único")
	for field in ("director", "fecha_estreno", "sinopsis"):
		if not data[field]:
			errors.append("Todos los campos son obligatorios")
	if errors:
		for e in errors:
			flash(e, "error")
		# Mantener campos en sesión para el bonus
		session["form_data"] = data
		return redirect("/cine/nueva")
	Pelicula.create(data)
	flash("Película creada", "success")
	return redirect("/cine")


@peliculas_bp.get("/cine/<int:pelicula_id>")
def ver_pelicula(pelicula_id: int):
	pelicula = Pelicula.get_by_id({"id": pelicula_id})
	if not pelicula:
		flash("Película no encontrada", "error")
		return redirect("/cine")
	comentarios = Comentario.list_for_movie({"pelicula_id": pelicula_id})
	return render_template("ver.html", pelicula=pelicula, comentarios=comentarios)


@peliculas_bp.get("/cine/editar/<int:pelicula_id>")
def editar_pelicula(pelicula_id: int):
	if "user_id" not in session:
		return redirect("/")
	pelicula = Pelicula.get_by_id({"id": pelicula_id})
	if not pelicula:
		flash("Película no encontrada", "error")
		return redirect("/cine")
	if pelicula["usuario_id"] != session["user_id"]:
		flash("Solo el autor puede editar", "error")
		return redirect("/cine")
	form_data = session.pop("form_data", {})
	return render_template("editar.html", pelicula=pelicula, form_data=form_data)


@peliculas_bp.post("/cine/editar/<int:pelicula_id>")
def actualizar_pelicula(pelicula_id: int):
	if "user_id" not in session:
		return redirect("/")
	data = {
		"id": pelicula_id,
		"titulo": request.form.get("titulo", "").strip(),
		"director": request.form.get("director", "").strip(),
		"fecha_estreno": request.form.get("fecha_estreno", "").strip(),
		"sinopsis": request.form.get("sinopsis", "").strip(),
		"usuario_id": session["user_id"],
	}
	# Validaciones
	errors = []
	if not data["titulo"] or len(data["titulo"]) < 3:
		errors.append("El nombre de la película debe tener al menos 3 caracteres")
	# Verificar si el título es único (excepto para la misma película)
	existing = Pelicula.get_by_id({"id": pelicula_id})
	if existing and existing["titulo"] != data["titulo"] and Pelicula.exists_title({"titulo": data["titulo"]}):
		errors.append("El nombre de la película debe ser único")
	for field in ("director", "fecha_estreno", "sinopsis"):
		if not data[field]:
			errors.append("Todos los campos son obligatorios")
	if errors:
		for e in errors:
			flash(e, "error")
		# Mantener campos en sesión para el bonus
		session["form_data"] = data
		return redirect(f"/cine/editar/{pelicula_id}")
	Pelicula.update(data)
	flash("Película actualizada", "success")
	return redirect("/cine")


@peliculas_bp.post("/cine/<int:pelicula_id>/eliminar")
def eliminar_pelicula(pelicula_id: int):
	if "user_id" not in session:
		return redirect("/")
	Pelicula.delete({"id": pelicula_id, "usuario_id": session["user_id"]})
	flash("Película eliminada", "success")
	return redirect("/cine")


@peliculas_bp.post("/cine/<int:pelicula_id>/comentarios")
def crear_comentario(pelicula_id: int):
	if "user_id" not in session:
		return redirect("/")
	contenido = request.form.get("contenido", "").strip()
	if not contenido:
		flash("El comentario no puede estar vacío", "error")
		return redirect(f"/cine/{pelicula_id}")
	pelicula = Pelicula.get_by_id({"id": pelicula_id})
	if pelicula and pelicula["usuario_id"] == session["user_id"]:
		flash("No puedes comentar tu propia película", "error")
		return redirect(f"/cine/{pelicula_id}")
	Comentario.create({
		"contenido": contenido,
		"usuario_id": session["user_id"],
		"pelicula_id": pelicula_id,
	})
	return redirect(f"/cine/{pelicula_id}")


@peliculas_bp.post("/cine/<int:pelicula_id>/comentarios/<int:comentario_id>/eliminar")
def eliminar_comentario(pelicula_id: int, comentario_id: int):
	if "user_id" not in session:
		return redirect("/")
	Comentario.delete({"id": comentario_id, "usuario_id": session["user_id"]})
	return redirect(f"/cine/{pelicula_id}")