import socket
import sqlite3
import time

#SQLite
DB_NAME = "redes.db"
RASPBERRY_IP = "10.42.0.255"  
RASPBERRY_PORT = 25555


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