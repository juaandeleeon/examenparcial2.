
import asyncio
import random
from datetime import datetime
from multiprocessing.connection import Client
import socket

ADDRESS = ("localhost", 6000)
AUTHKEY = b"noticias"
ORIGEN = random.choice(["Madrid", "Londres", "SaoPaulo"])

EQUIPOS = ["Real Madrid", "FC Barcelona", "Liverpool", "Manchester City", "PSG", "Boca Juniors", "Flamengo"]
EVENTOS = ["Gol", "Falta", "Amarilla", "Roja", "Corner"]

descripciones = {
    "Gol": "Golazo impresionante desde fuera del área.",
    "Falta": "Entrada fuerte sancionada con falta.",
    "Amarilla": "Tarjeta amarilla por protestar al árbitro.",
    "Roja": "Expulsión directa tras una entrada violenta.",
    "Corner": "Córner a favor tras un despeje rival."
}

async def enviar_evento():
    await asyncio.sleep(random.randint(2, 8))
    equipo = random.choice(EQUIPOS)
    tipo = random.choice(EVENTOS)
    contenido = descripciones[tipo]

    evento = {
        "equipo": equipo,
        "origen": ORIGEN,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "titulo": tipo,
        "contenido": contenido
    }

    try:
        with Client(ADDRESS, authkey=AUTHKEY) as conn:
            conn.send(evento)
            print(f"[{ORIGEN}] {equipo} - Enviado: {tipo} → {contenido}")
    except (ConnectionRefusedError, socket.error) as e:
        print(f"[{ORIGEN}] Error al conectar con Frankfurt: {e}")

async def main():
    print(f"[{ORIGEN}] Nodo activo. Enviando eventos futbolísticos...")
    while True:
        await enviar_evento()

if __name__ == "__main__":
    asyncio.run(main())