from flask import Flask
from flask import render_template


def create_app():
	app = Flask(__name__)
	app.secret_key = "super_secret_key_change_me"

	# Register blueprints lazily to avoid circular imports
	from .controllers.usuarios import usuarios_bp
	from .controllers.peliculas import peliculas_bp
	app.register_blueprint(usuarios_bp)
	app.register_blueprint(peliculas_bp)

	# Root route - Login/Registro page
	@app.route("/")
	def index():
		return render_template("index.html")

	return app