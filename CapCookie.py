import requests
import schedule
import time
from twilio.rest import Client
import logging
from multiprocessing import Process, Queue
from scapy.all import sniff, IP

# Configuración de registro
logging.basicConfig(level=logging.INFO, filename="app.log", filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s")

def packet_callback_wrapper(packet, queue):
    packet_callback(packet)
    # Aquí puedes realizar cualquier operación adicional que requiera el uso de 'queue'

def packet_callback(packet):
    # Aquí puedes realizar el análisis de los paquetes capturados
    # Puedes obtener información como las direcciones IP de origen y destino

    # Ejemplo: Obtener la IP de origen
    if packet.haslayer(IP):
        src_ip = packet[IP].src
        logging.info("Paquete capturado desde la IP: %s", src_ip)

def check_session_cookie(url, cookie_name, queue):
    try:
        session = requests.Session()
        response = session.get(url)
        response.raise_for_status()  # Lanza una excepción si hay un error en la respuesta
        cookies = response.cookies

        if cookie_name in cookies:
            authenticated_urls = [
                "https://www.example.com/protected_page1",
                "https://www.example.com/protected_page2",
                "https://www.example.com/protected_page3"
            ]
            compromised = False

            for authenticated_url in authenticated_urls:
                response = session.get(authenticated_url)
                response.raise_for_status()  # Lanza una excepción si hay un error en la respuesta

                if response.status_code != 200 or "Invalid session" in response.text:
                    compromised = True
                    break

            if compromised:
                queue.put("La sesión de cookie ha sido comprometida.")
            else:
                queue.put("La sesión de cookie está activa y válida.")
        else:
            queue.put("La sesión de cookie no está activa o ha sido comprometida.")

    except requests.exceptions.RequestException as e:
        logging.error("Error en la solicitud: %s", str(e))
        queue.put("Error en la solicitud. Verifica la conexión.")

    except requests.exceptions.HTTPError as e:
        logging.error("Error HTTP en la respuesta: %s", str(e))
        queue.put("Error en la respuesta HTTP.")

def send_sms_notification(message):
    try:
        account_sid = 'TU_ACCOUNT_SID'
        auth_token = 'TU_AUTH_TOKEN'
        from_phone = '+1234567890'
        to_phone = '+0987654321'

        client = Client(account_sid, auth_token)

        client.messages.create(
            body=message,
            from_=from_phone,
            to=to_phone
        )
        logging.info("Mensaje de texto enviado.")

    except Exception as e:
        logging.error("Error al enviar el mensaje de texto: %s", str(e))

def job(url, cookie_name, queue):
    try:
        check_session_cookie(url, cookie_name, queue)
        message = queue.get()
        if "comprometida" in message:
            send_sms_notification(message)
        logging.info(message)
    except Exception as e:
        logging.error("Error en el trabajo programado: %s", str(e))

if __name__ == "__main__":
    url = "https://www.example.com"
    cookie_name = "session_id"

    queue = Queue()

    schedule.every(1).hours.do(job, url=url, cookie_name=cookie_name, queue=queue)

    p = Process(target=schedule.run_continuously)
    p.start()

    sniff(prn=lambda packet: packet_callback_wrapper(packet, queue), store=0)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        p.terminate()
        p.join()
