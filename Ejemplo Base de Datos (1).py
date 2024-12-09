<<<<<<< HEAD
import socket
import sqlite3
import time

#SQLite
DB_NAME = "red_logs.db"
RASPBERRY_IP = "0.0.0.0"  
RASPBERRY_PORT = 12345


def conectar_db():
    try:
        conexion = sqlite3.connect(DB_NAME)
        conexion.row_factory = sqlite3.Row 
        return conexion
    except Exception as e:
        print(f"Error al conectar a SQLite: {e}")
        return None

def crear_tablas(cursor):
    try:
        # tabla de logs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datos TEXT,
            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        # tabla Data_2
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Data_2 (
            Id_device INT,
            Racc_x FLOAT,
            Racc_y FLOAT,
            Racc_z FLOAT,
            Rgyr_x FLOAT,
            Rgyr_y FLOAT,
            Rgyr_z FLOAT,
            Time_client DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)

        #  tabla configuration
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS configuration (
            Id_device INT PRIMARY KEY,
            TCP_PORT INT,
            UDP_port INT,
            Host_ip_addr TEXT,
            Ssid VARCHAR(45),
            Pass VARCHAR(45)
        )
        """)

        print("Tablas creadas exitosamente.")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")

#  insertar los datos del paquete en la base de datos
def insertar_log(cursor, datos):
    try:
        cursor.execute("INSERT INTO logs (datos) VALUES (?)", (datos,))
        print(f"Datos guardados en la base de datos: {datos}")
    except Exception as e:
        print(f"Error al insertar datos en la base de datos: {e}")

def servidor_udp():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server:
        server.bind((RASPBERRY_IP, RASPBERRY_PORT))
        print(f"Escuchando en {RASPBERRY_IP}:{RASPBERRY_PORT}...")
        conexion = conectar_db()
        if conexion:
            cursor = conexion.cursor()
            crear_tablas(cursor)

            while True:
                datos, direccion = server.recvfrom(1024)
                datos = datos.decode() 
                print(f"Paquete recibido de {direccion}: {datos}")
                if "error" in datos: 
                    print("Datos corruptos detectados. Bloqueando la conexión...")
                    server.sendto(b"dispositivo bloqueado", direccion)
                    break 
                else:
                    insertar_log(cursor, datos)
                    
                time.sleep(0.1)

            cursor.close()
            conexion.close()

if __name__ == "__main__":
    servidor_udp()
=======
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
>>>>>>> 4e1897ef260d11a1c49226c1e3bb65a91abd704d
