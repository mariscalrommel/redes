import json
import psycopg2

#sudo apt update
#sudo apt install python3-psycopg2


# Conexión a la base de datos PostgreSQL
def conectar_postgres():
    try:
        # Cambia estos valores según tu configuración
        conexion = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="tu_contraseña"
        )
        conexion.autocommit = True
        return conexion
    except Exception as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return None

# Crear la base de datos
def crear_base_de_datos(cursor, nombre_bd):
    try:
        cursor.execute(f"CREATE DATABASE {nombre_bd}")
        print(f"Base de datos '{nombre_bd}' creada exitosamente.")
    except Exception as e:
        print(f"Error al crear la base de datos: {e}")

# Crear las tablas
def crear_tablas(cursor):
    try:
        # Tabla de alumnos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS alumnos (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100),
            matricula VARCHAR(20)
        )
        """)
        
        # Tabla de asignaturas
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS asignaturas (
            id SERIAL PRIMARY KEY,
            nombre_asignatura VARCHAR(100),
            nota DECIMAL(5, 2),
            alumno_id INTEGER REFERENCES alumnos(id)
        )
        """)
        
        print("Tablas creadas exitosamente.")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")

# Insertar datos desde el archivo JSON
def insertar_datos_desde_json(cursor, archivo_json):
    try:
        with open(archivo_json, 'r') as archivo:
            datos = json.load(archivo)
        
        # Insertar alumnos
        for alumno in datos['alumnos']:
            cursor.execute("""
            INSERT INTO alumnos (nombre, matricula) 
            VALUES (%s, %s) RETURNING id
            """, (alumno['nombre'], alumno['matricula']))
            
            alumno_id = cursor.fetchone()[0]

            # Insertar asignaturas asociadas al alumno
            for asignatura in alumno['asignaturas']:
                cursor.execute("""
                INSERT INTO asignaturas (nombre_asignatura, nota, alumno_id)
                VALUES (%s, %s, %s)
                """, (asignatura['nombre_asignatura'], asignatura['nota'], alumno_id))
        
        print("Datos insertados exitosamente desde el archivo JSON.")
    except Exception as e:
        print(f"Error al insertar datos desde JSON: {e}")

def main():
    conexion = conectar_postgres()
    
    if conexion:
        cursor = conexion.cursor()
        
        # Crear base de datos (cambiar "alumnos_bd" si es necesario)
        crear_base_de_datos(cursor, 'alumnos_bd')
        
        # Conectarse a la nueva base de datos
        cursor.close()
        conexion.close()
        
        conexion = psycopg2.connect(
            host="localhost",
            database="alumnos_bd",
            user="postgres",
            password="tu_contraseña"
        )
        conexion.autocommit = True
        cursor = conexion.cursor()
        
        # Crear tablas
        crear_tablas(cursor)

        # Insertar datos desde el archivo JSON
        insertar_datos_desde_json(cursor, 'ejdb.json')
        
        cursor.close()
        conexion.close()

if __name__ == "__main__":
    main()
