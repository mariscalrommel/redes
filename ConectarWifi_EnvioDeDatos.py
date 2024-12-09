import os
import time
import socket
import random

# Configuración de la red WiFi y del servidor
SSID = "redesbeltran"  # Nombre de la red WiFi
PASSWORD = "benjamin555"  # Contraseña de la red WiFi
BROADCAST_IP = "10.42.0.255"  # Dirección de broadcast típica
UDP_PORT = 25555 # Puerto de comunicación UDPp

def conectar_wifi(ssid, password):
    """Conecta al WiFi especificado."""
    print(f"Intentando conectar a la red WiFi '{ssid}'...")
    os.system(f'netsh wlan connect name="{ssid}"')  # Comando para Windows
    time.sleep(10)  # Esperar a que se establezca la conexión

def verificar_conexion():
    """Verifica si está conectado a la red deseada."""
    ssid_actual = os.popen('netsh wlan show interfaces | findstr SSID').read()
    if SSID in ssid_actual:
        print(f"Conectado a la red WiFi '{SSID}'.")
        return True
    else:
        print(f"No estás conectado a la red WiFi '{SSID}'.")
        return False

def generar_datos():
    """Genera datos aleatorios para enviar."""
    acc_x = random.uniform(-16.0, 16.0)
    acc_y = random.uniform(-16.0, 16.0)
    acc_z = random.uniform(-16.0, 16.0)
    gyr_x = random.uniform(-1000.0, 1000.0)
    gyr_y = random.uniform(-1000.0, 1000.0)
    gyr_z = random.uniform(-1000.0, 1000.0)
    return f"{acc_x},{acc_y},{acc_z},{gyr_x},{gyr_y},{gyr_z}"

def enviar_datos():
    """Envía datos a través de UDP a la red WiFi."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # Activar el modo broadcast
        while True:
            datos = generar_datos()
            client.sendto(datos.encode(), (BROADCAST_IP, UDP_PORT))
            print(f"Datos enviados: {datos}")

            # Esperar un tiempo antes de enviar el siguiente paquete
            time.sleep(1)

if __name__ == "__main__":
    conectar_wifi(SSID, PASSWORD)
    if verificar_conexion():
        enviar_datos()
    else:
        print("No se puede enviar datos porque no estás conectado a la red correcta.")
