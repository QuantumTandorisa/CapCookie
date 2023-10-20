# -*- coding: utf-8 -*-
'''
   ______            ______            __   _    
  / ____/___ _____  / ____/___  ____  / /__(_)__ 
 / /   / __ `/ __ \/ /   / __ \/ __ \/ //_/ / _ \
/ /___/ /_/ / /_/ / /___/ /_/ / /_/ / ,< / /  __/
\____/\__,_/ .___/\____/\____/\____/_/|_/_/\___/ 
          /_/                                    
'''
#######################################################
#    CapCookie.py
#
# CapCookie is a tool that allows you to capture and 
# monitor cookies on different websites and check 
# their validity using NTLM authentication. It can 
# be useful to make sure that authentication cookies 
# in your web applications are still valid.
#
#
# 10/18/23 - Changed to Python3 (finally)
#
# Author: Facundo Fernandez 
#
#
#######################################################

import json
import requests
from requests_ntlm import HttpNtlmAuth

# Estructura para almacenar cookies y URLs
sitios = {}

# Cargar cookies y URLs desde el archivo JSON
def cargar_sitios_desde_archivo():
    try:
        with open("sitios.json", "r") as archivo:
            data = json.load(archivo)
            sitios.update(data)
    except FileNotFoundError:
        print("El archivo 'sitios.json' no se encontró.")

# Función para verificar una cookie
def verificar_cookie(url, cookie):
    try:
        # Crear una sesión de requests
        session = requests.Session()

        # Cargar la cookie en la sesión
        session.cookies.set(cookie["cookie_name"], cookie["cookie_value"])

        # Verificar si la cookie contiene la clave "username" y "password"
        if "username" in cookie and "password" in cookie:
            username = cookie["username"]
            password = cookie["password"]

            # Realizar la autenticación utilizando la biblioteca de autenticación de terceros
            auth = HttpNtlmAuth(username, password)

            # Realizar una solicitud a la URL con autenticación NTLM
            response = session.get(url, auth=auth)

            # Verificar el estado de inicio de sesión
            if response.status_code == 200:
                print(f"La cookie {cookie['cookie_name']} en {url} está en uso.")
            else:
                print(f"La cookie {cookie['cookie_name']} en {url} no está en uso. Realizando notificación.")
                # Puedes agregar aquí tu lógica de notificación (por correo, mensaje de texto, etc.)
        else:
            print(f"La cookie {cookie['cookie_name']} en {url} no contiene información de usuario.")

    except requests.exceptions.RequestException as e:
        print(f"Error al verificar la cookie: {e}")

# Cargar sitios y cookies desde el archivo JSON
cargar_sitios_desde_archivo()

for sitio, data in sitios.items():
    if "url" in data and "cookies" in data:
        url = data["url"]
        cookies_list = data["cookies"]
        print(f"Verificando cookies en {sitio} ({url}):")
        for cookie in cookies_list:
            if "cookie_name" in cookie and "cookie_value" in cookie:
                verificar_cookie(url, cookie)
    else:
        print(f"No se encontró la información completa para {sitio} en el archivo 'sitios.json'.")
