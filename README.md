README

Sistema de monitoreo de sesión de cookies en Python. 
El objetivo de este programa es verificar periódicamente si una sesión de cookie está activa y válida, y enviar una notificación por SMS si se detecta algún compromiso.

Requisitos previos:

Antes de ejecutar este código, asegúrate de tener instaladas las siguientes dependencias:

    requests
    schedule
    twilio
    logging
    scapy

Puedes instalar estas dependencias ejecutando el siguiente comando:

```
pip install requests schedule twilio scapy
```

Además, necesitarás una cuenta en Twilio para enviar mensajes de texto. Obtén el ACCOUNT_SID y el AUTH_TOKEN de tu cuenta y reemplázalos en el código.

Configuración:

Antes de ejecutar el código, es necesario realizar algunas configuraciones:

Establece la URL del sitio web que deseas monitorear en la variable url dentro del bloque if __name__ == "__main__":.
Define el nombre de la cookie de sesión que deseas verificar en la variable cookie_name.
Modifica los números de teléfono de origen y destino en las variables from_phone y to_phone dentro de la función send_sms_notification().

Uso:

Una vez que hayas realizado la configuración adecuada, puedes ejecutar el programa ejecutando el archivo. Asegúrate de estar en el mismo directorio donde se encuentra el archivo y ejecuta el siguiente comando:

```
python CapCookie.py
```

El programa comenzará a capturar paquetes de red y verificará periódicamente la sesión de cookie. Si se detecta alguna irregularidad en la sesión de cookie, se enviará una notificación por SMS al número de destino especificado.

Registro:

El programa registra información relevante en el archivo app.log. Este archivo contiene registros detallados de la actividad del programa, incluyendo la captura de paquetes, errores de solicitud HTTP y envío de mensajes de texto.

Notas adicionales:

  El programa utiliza la biblioteca schedule para programar tareas periódicas de verificación de la sesión de cookie. Puedes modificar la frecuencia de las verificaciones ajustando el parámetro de la función schedule.every() dentro del bloque if __name__ == "__main__":.
  El programa utiliza la biblioteca scapy para la captura de paquetes de red. Puedes personalizar la función packet_callback() para realizar análisis adicional de los paquetes capturados.
