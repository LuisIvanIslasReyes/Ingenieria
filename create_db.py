import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

try:
    # Conexión a la base de datos postgres (default)
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password='123456789'
    )
    
    # Establecer autocommit para poder crear la base de datos
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    
    # Crear cursor
    cursor = conn.cursor()
    
    # Verificar si la base de datos ya existe
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'Parrasdev'")
    exists = cursor.fetchone()
    
    if exists:
        print("La base de datos 'Parrasdev' ya existe.")
    else:
        # Crear la base de datos
        cursor.execute('CREATE DATABASE "Parrasdev"')
        print("Base de datos 'Parrasdev' creada exitosamente.")
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f"Error: {e}")
