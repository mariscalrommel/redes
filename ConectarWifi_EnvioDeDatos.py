import os
import time
import socket
import random

# Configuración de la red WiFi y del servidor
SSID = "NombreDeTuRedWiFi"  #  WiFi
PASSWORD = "TuContraseñaWiFi"  #  contraseña  wifi
RASPBERRY_IP = "192.168.1.100"  #  raspberry
RASPBERRY_PORT = 12345

def conectar_wifi(ssid, password):
    print(f"Intentando conectar a la red WiFi '{ssid}'...")
    os.system(f'netsh wlan connect name="{ssid}"') 
    time.sleep(10)  

def generar_datos():
    acc_x = random.uniform(-16.0, 16.0)
    acc_y = random.uniform(-16.0, 16.0)
    acc_z = random.uniform(-16.0, 16.0)
    gyr_x = random.uniform(-1000.0, 1000.0)
    gyr_y = random.uniform(-1000.0, 1000.0)
    gyr_z = random.uniform(-1000.0, 1000.0)
    return f"{acc_x},{acc_y},{acc_z},{gyr_x},{gyr_y},{gyr_z}"

def enviar_datos():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        while True:
    
            datos = generar_datos()
            client.sendto(datos.encode(), (RASPBERRY_IP, RASPBERRY_PORT))
            print(f"Enviado: {datos}")

            try:
                client.settimeout(1) 
                respuesta, _ = client.recvfrom(1024)
                respuesta = respuesta.decode()
                if respuesta == "dispositivo bloqueado":
                    print("Dispositivo bloqueado por el servidor. Finalizando...")
                    break
            except socket.timeout:
                print("Sin respuesta del servidor.")
            
            time.sleep(0.1) 

if __name__ == "__main__":
    conectar_wifi(SSID, PASSWORD)
    enviar_datos()
