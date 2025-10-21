from flask import Blueprint, render_template, request, redirect, flash, url_for, session

from ..models.usuario import Usuario
from ..models.pelicula import Pelicula


usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.post("/registro")
def registro_submit():
	nombre = request.form.get("nombre", "").strip()
	apellido = request.form.get("apellido", "").strip()
	email = request.form.get("email", "").strip().lower()
	password = request.form.get("password", "")
	confirm = request.form.get("confirm", "")

	# Validaciones registro
	errors = []
	if len(nombre) < 2 or len(apellido) < 2:
		errors.append("Nombre y Apellido deben tener al menos 2 caracteres")
	if "@" not in email:
		errors.append("Email inválido")
	if password != confirm or len(password) < 8:
		errors.append("La contraseña debe coincidir y tener 8+ caracteres")
	if Usuario.get_by_email({"email": email}):
		errors.append("El email ya está registrado")
	if errors:
		for e in errors:
			flash(e, "error")
		return redirect("/")

	user_id = Usuario.create({
		"nombre": nombre,
		"apellido": apellido,
		"email": email,
		"password": password,
	})
	session["user_id"] = user_id
	session["user_name"] = nombre
	return redirect("/cine")


@usuarios_bp.post("/login")
def login_submit():
	email = request.form.get("email", "").strip().lower()
	password = request.form.get("password", "")
	user = Usuario.get_by_email({"email": email})
	if not user:
		flash("Email no encontrado", "error")
		return redirect("/")
	if not Usuario.check_password(user, password):
		flash("Contraseña incorrecta", "error")
		return redirect("/")
	session["user_id"] = user["id"]
	session["user_name"] = user["nombre"]
	return redirect("/cine")


@usuarios_bp.get("/logout")
def logout():
	session.clear()
	return redirect("/")