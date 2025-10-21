#!/usr/bin/env python3
"""
Script para configurar la base de datos de CinePedia
"""

import pymysql
import os

def create_database():
    """Crear la base de datos y las tablas"""
    
    # Configuración de conexión (sin especificar base de datos)
    config = {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "user": os.getenv("MYSQL_USER", "root"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "charset": "utf8mb4",
    }
    
    # Agregar contraseña (por defecto "root")
    password = os.getenv("MYSQL_PASSWORD", "root")
    config["password"] = password
    
    try:
        # Conectar sin especificar base de datos
        print("Conectando a MySQL...")
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        
        # Crear base de datos
        db_name = os.getenv("MYSQL_DB", "cine_db")
        print(f"Creando base de datos '{db_name}'...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute(f"USE {db_name}")
        
        # Leer y ejecutar el script SQL
        print("Creando tablas...")
        with open("scripts.sql", "r", encoding="utf-8") as f:
            sql_script = f.read()
        
        # Dividir el script en comandos individuales
        commands = [cmd.strip() for cmd in sql_script.split(';') if cmd.strip()]
        
        for command in commands:
            if command.upper().startswith(('CREATE', 'INSERT', 'ALTER')):
                cursor.execute(command)
        
        conn.commit()
        print("✅ Base de datos configurada correctamente!")
        
    except pymysql.Error as e:
        print(f"❌ Error de MySQL: {e}")
        return False
    except FileNotFoundError:
        print("❌ No se encontró el archivo scripts.sql")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()
    
    return True

def test_connection():
    """Probar la conexión a la base de datos"""
    try:
        from flask_app.config.mysqlconnection import query_db
        result = query_db("SELECT 1 as test")
        print("✅ Conexión a la base de datos exitosa!")
        return True
    except Exception as e:
        print(f"❌ Error al conectar: {e}")
        return False

if __name__ == "__main__":
    print("=== Configuración de Base de Datos CinePedia ===\n")
    
    # Verificar si MySQL está disponible
    try:
        import pymysql
        print("✅ PyMySQL disponible")
    except ImportError:
        print("❌ PyMySQL no está instalado. Ejecuta: pip install PyMySQL")
        exit(1)
    
    # Crear base de datos
    if create_database():
        # Probar conexión
        test_connection()
    else:
        print("\n💡 Sugerencias:")
        print("1. Asegúrate de que MySQL esté ejecutándose")
        print("2. Verifica las credenciales de MySQL")
        print("3. Si MySQL requiere contraseña, configura la variable MYSQL_PASSWORD")
        print("   Ejemplo: set MYSQL_PASSWORD=tu_contraseña")