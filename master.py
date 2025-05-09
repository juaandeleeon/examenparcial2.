from multiprocessing.connection import Listener
from datetime import datetime
import os

ADDRESS = ("localhost", 6000)
AUTHKEY = b"noticias"

os.makedirs("noticias_recibidas", exist_ok=True)

print("[FRANKFURT] Servidor iniciado y esperando noticias...")
with Listener(ADDRESS, authkey=AUTHKEY) as listener:
    while True:
        with listener.accept() as conn:
            try:
                data = conn.recv()
                if isinstance(data, dict):
                    equipo = data.get("equipo", "EquipoDesconocido")
                    print(f"\n[FRANKFURT] === Evento Recibido ===")
                    print(f"Equipo   : {equipo}")
                    print(f"Origen   : {data.get('origen')}")
                    print(f"Fecha    : {data.get('fecha')}")
                    print(f"Evento   : {data.get('titulo')}")
                    print(f"Contenido: {data.get('contenido')}")
                    print(f"===============================\n")

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"noticias_recibidas/{equipo}_{timestamp}.txt"
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(f"Equipo: {equipo}\n")
                        f.write(f"Evento: {data.get('titulo')}\n")
                        f.write(f"Fecha: {data.get('fecha')}\n")
                        f.write(f"Contenido: {data.get('contenido')}\n")
                else:
                    print("[FRANKFURT] Mensaje recibido no válido")
            except Exception as e:
                print(f"[FRANKFURT] Error al procesar mensaje: {e}")
