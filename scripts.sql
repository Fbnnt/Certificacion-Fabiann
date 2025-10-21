-- Create database
CREATE DATABASE IF NOT EXISTS cine_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE cine_db;

-- Usuarios table
CREATE TABLE IF NOT EXISTS usuarios (
	id INT PRIMARY KEY AUTO_INCREMENT,
	nombre VARCHAR(100) NOT NULL,
	apellido VARCHAR(100) NOT NULL,
	email VARCHAR(150) NOT NULL UNIQUE,
	password_hash VARCHAR(255) NOT NULL,
	created_at DATETIME NOT NULL,
	updated_at DATETIME NOT NULL
);

-- Peliculas table
CREATE TABLE IF NOT EXISTS peliculas (
	id INT PRIMARY KEY AUTO_INCREMENT,
	titulo VARCHAR(200) NOT NULL UNIQUE,
	director VARCHAR(150) NOT NULL,
	fecha_estreno DATE NOT NULL,
	sinopsis TEXT NOT NULL,
	usuario_id INT NOT NULL,
	created_at DATETIME NOT NULL,
	updated_at DATETIME NOT NULL,
	CONSTRAINT fk_peliculas_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Comentarios table
CREATE TABLE IF NOT EXISTS comentarios (
	id INT PRIMARY KEY AUTO_INCREMENT,
	contenido TEXT NOT NULL,
	usuario_id INT NOT NULL,
	pelicula_id INT NOT NULL,
	created_at DATETIME NOT NULL,
	updated_at DATETIME NOT NULL,
	CONSTRAINT fk_comentarios_usuario FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
	CONSTRAINT fk_comentarios_pelicula FOREIGN KEY (pelicula_id) REFERENCES peliculas(id) ON DELETE CASCADE
);