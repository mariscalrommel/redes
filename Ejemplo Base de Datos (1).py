import json
import psycopg2

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
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Log (
            Id_device INT PRIMARY KEY,
            Status_report INT,
            Time_server TIMESTAMP
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Data_2 (
            Id_device INT,
            Racc_x FLOAT,
            Racc_y FLOAT,
            Racc_z FLOAT,
            Rgyr_x FLOAT,
            Rgyr_y FLOAT,
            Rgyr_z FLOAT,
            Time_client TIMESTAMP,
            PRIMARY KEY (Id_device),
            FOREIGN KEY (Id_device) REFERENCES Log(Id_device)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuration (
            Id_device INT PRIMARY KEY,
            TCP_PORT INT,
            UDP_port INT,
            Host_ip_addr INT,
            Ssid VARCHAR(45),
            Pass VARCHAR(45),
            FOREIGN KEY (Id_device) REFERENCES Log(Id_device)
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

        # Insertar datos en Log
        for log in datos['Log']:
            cursor.execute("""
            INSERT INTO Log (Id_device, Status_report, Time_server)
            VALUES (%s, %s, %s)
            """, (log['Id_device'], log['Status_report'], log['Time_server']))

        # Insertar datos en Data_2
        for data in datos['Data_2']:
            cursor.execute("""
            INSERT INTO Data_2 (Id_device, Racc_x, Racc_y, Racc_z, Rgyr_x, Rgyr_y, Rgyr_z, Time_client)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (data['Id_device'], data['Racc_x'], data['Racc_y'], data['Racc_z'], 
                  data['Rgyr_x'], data['Rgyr_y'], data['Rgyr_z'], data['Time_client']))

        # Insertar datos en configuration
        for config in datos['configuration']:
            cursor.execute("""
            INSERT INTO configuration (Id_device, TCP_PORT, UDP_port, Host_ip_addr, Ssid, Pass)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (config['Id_device'], config['TCP_PORT'], config['UDP_port'], 
                  config['Host_ip_addr'], config['Ssid'], config['Pass']))

        print("Datos insertados exitosamente desde el archivo JSON.")
    except Exception as e:
        print(f"Error al insertar datos desde JSON: {e}")

def main():
    conexion = conectar_postgres()
    
    if conexion:
        cursor = conexion.cursor()
        
        # Crear base de datos (cambiar "dispositivos_bd" si es necesario)
        crear_base_de_datos(cursor, 'dispositivos_bd')
        cursor.close()
        conexion.close()
        
        conexion = psycopg2.connect(
            host="localhost",
            database="dispositivos_bd",
            user="postgres",
            password="tu_contraseña"
        )
        conexion.autocommit = True
        cursor = conexion.cursor()
        crear_tablas(cursor)
        insertar_datos_desde_json(cursor, 'dispositivos.json')
        
        cursor.close()
        conexion.close()

if __name__ == "__main__":
    main()
