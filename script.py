import os
import json
import socket
import psutil
import urllib.request
import requests
import paramiko


hostname = socket.gethostname()

def obtener_ip_publica():
    try:
        response = requests.get('https://ifconfig.me/ip')
        ip = response.text.strip()
        return ip
    except Exception as e:
        return "Error al obtener la IP pública: " + str(e)

def obtener_informacion_ip(ip):
    url = f"https://ipinfo.io/{ip}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            "IPv4": data.get("ip", "Not found"),
            "IPv6": data.get("ipv6", "Not found"),
            "Country": data.get("country", "Not found"),
            "Region": data.get("region", "Not found"),
            "City": data.get("city", "Not found"),
            "ZIP": data.get("postal", "Not found"),
            "ISP": data.get("org", "Not found"),
            "ASN": data.get("asn", "Not found"),
            "Timezone": data.get("timezone", "Not found"),
            "User Agent": data.get("user_agent", "Not found")
        }
    else:
        return "Error al obtener la información de la IP"

def obtener_informacion_pc():
    private_ip = socket.gethostbyname(hostname)
    public_ip = obtener_ip_publica()
    info_ip = obtener_informacion_ip(public_ip)
    return {
        "HOSTNAME": hostname,
        "Direccion IP": {
            "Privada": private_ip,
            "Publica": info_ip
        }
    }

def obtener_informacion_almacenamiento():
    volumenes = psutil.disk_partitions()
    info_volumenes = []
    for volumen in volumenes:
        tipo = os.name
        capacidad_bytes = psutil.disk_usage(volumen.mountpoint).total
        capacidad_gb = capacidad_bytes / (1024**3)
        info_volumenes.append({
            "Volumen": volumen.mountpoint,
            "Tipo": tipo,
            "Capacidad": capacidad_gb
        })
    return info_volumenes

data = {
    "Info PC": obtener_informacion_pc(),
    "Almacenamiento": obtener_informacion_almacenamiento()
}

json_data = json.dumps(data, indent=4)

# Aqui introducid vuestros datos
hostname_ssh = 'direccion_ip_servidor'
username_ssh = 'nombre_usuario'
password_ssh = 'contraseña'
ruta_destino_ssh = '/ruta/en/el/servidor'


with paramiko.SSHClient() as ssh:
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname_ssh, username=username_ssh, password=password_ssh)

  
    with ssh.open_sftp() as sftp:
       
        nombre_archivo_ssh = f"{hostname}.json"
        
        with sftp.file(os.path.join(ruta_destino_ssh, nombre_archivo_ssh), 'w') as file:
            file.write(json_data)

print("Los datos se han enviado correctamente al servidor.")
