Hola bienvenido a proyecto de redes de computadores de la universidad san sebastian , sede tres pascualas

bY: Zaku(Lucas Castro) , mariscalrommel(Benjamin Beltrán)

Este repositorio contiene un script en Python que permite conectar a una red WiFi y transmitir datos de forma broadcast usando el protocolo UDP. El código está diseñado para ejecutarse en un contenedor Docker con soporte para `NetworkManager`.

## Requisitos Previos

Asegúrate de cumplir con los siguientes requisitos antes de usar este proyecto:

- Docker instalado en tu sistema.
- La imagen base del contenedor debe incluir `NetworkManager` para la gestión de redes WiFi.
- Un adaptador WiFi compatible y accesible para el contenedor.
- Python 3.10 o superior configurado en el entorno del contenedor.

## Instalación

Clona este repositorio en tu máquina local:

```bash
git clone https://github.com/<tu-usuario>/<tu-repositorio>.git
cd <tu-repositorio>
```

## Configuración del Dockerfile

El `Dockerfile` debe incluir las dependencias necesarias, como se muestra a continuación:

```dockerfile
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    network-manager \
    dbus \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

CMD ["python", "script.py"]
```

## Uso

### 1. Construir la Imagen de Docker

Construye la imagen de Docker con el siguiente comando:

```bash
docker build -t wifi-data-sender .
```

### 2. Ejecutar el Contenedor

Ejecuta el contenedor con los permisos necesarios para acceder a las interfaces de red:

```bash
docker run --rm -d --network host --privileged \
    -v /var/run/dbus:/var/run/dbus \
    --device /dev/net/tun:/dev/net/tun \
    wifi-data-sender
```

### 3. Monitorizar la Transmisión de Datos

Utiliza herramientas como Wireshark en tu máquina anfitrión para monitorizar los paquetes UDP enviados por el contenedor. La dirección de broadcast y el puerto se pueden ajustar en el script de Python.

## Detalles del Código

El script realiza las siguientes tareas:

1. Conecta a la red WiFi especificada usando `nmcli`.
2. Genera datos aleatorios.
3. Transmite los datos en formato UDP broadcast.

Partes clave del código:

```python
def conectar_wifi(ssid, password):
    print(f"Intentando conectar a la red WiFi '{ssid}'...")
    resultado = os.system(f'nmcli dev wifi connect "{ssid}" password "{password}"')
    if resultado == 0:
        print(f"Conectado a la red WiFi '{ssid}'.")
    else:
        print(f"No se pudo conectar a la red WiFi '{ssid}'.")

def enviar_datos():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        while True:
            datos = generar_datos()
            client.sendto(datos.encode(), (BROADCAST_IP, UDP_PORT))
            print(f"Datos enviados: {datos}")
            time.sleep(1)
```

### Por qué se usó SQLite y no PostgreSQL

- **Simplicidad**: SQLite es liviano y no requiere configuración adicional para este tipo de pruebas.
- **Portabilidad**: Los archivos SQLite son fáciles de mover entre sistemas y no necesitan un servidor en ejecución.
- **Uso del Espacio**: Ideal para entornos donde no se necesita una base de datos robusta y persistente.

## Depuración

- Si encuentras el error `sh: 1: netsh: not found`, verifica que el contenedor esté usando `nmcli` en lugar de comandos específicos de Windows.
- Usa `docker logs <container_id>` para revisar los registros del script.
