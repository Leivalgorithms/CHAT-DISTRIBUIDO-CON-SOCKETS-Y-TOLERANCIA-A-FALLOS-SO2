"""
client.py — Cliente de chat distribuido sobre TCP.

Dos hilos:
  - Principal: lee input del usuario y lo envía al servidor.
  - Receptor: escucha mensajes entrantes del servidor y los imprime.
"""

import socket
import threading
import sys
from protocol import encode, decode, format_display

# ── Configuración ─────────────────────────────────────────────────────────────
HOST = "127.0.0.1"   # Cambiar a la IP del servidor si es remoto
PORT = 5000
BUFFER = 4096


def recibir(sock: socket.socket, usuario: str) -> None:
    """Hilo receptor: imprime mensajes entrantes hasta que se cierre la conexión."""
    while True:
        try:
            data = sock.recv(BUFFER)
            if not data:
                print("\n[Desconectado del servidor]")
                break
            msg = decode(data)
            if msg:
                print(f"\r{format_display(msg)}\n{usuario} > ", end="", flush=True)
        except (ConnectionResetError, BrokenPipeError):
            print("\n[Conexión perdida con el servidor]")
            break
        except Exception as e:
            print(f"\n[Error al recibir: {e}]")
            break


def conectar() -> None:
    """Establece la conexión y corre el loop de envío."""
    usuario = input("Ingresá tu nombre de usuario: ").strip()
    if not usuario:
        usuario = "Anónimo"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except ConnectionRefusedError:
        print(f"[ERROR] No se pudo conectar al servidor en {HOST}:{PORT}")
        sys.exit(1)

    # Presentarse al servidor con el primer mensaje
    sock.sendall(encode(usuario, "se conectó"))

    # Iniciar hilo receptor en segundo plano
    hilo = threading.Thread(target=recibir, args=(sock, usuario), daemon=True)
    hilo.start()

    print(f"[Conectado al servidor {HOST}:{PORT}]")
    print("Escribí tu mensaje y presioná Enter. Ctrl+C para salir.\n")

    # Loop de envío (hilo principal)
    try:
        while True:
            texto = input(f"{usuario} > ").strip()
            if not texto:
                continue
            if texto.lower() in ("/salir", "/quit", "/exit"):
                break
            sock.sendall(encode(usuario, texto))
    except KeyboardInterrupt:
        pass
    finally:
        sock.close()
        print("\n[Desconectado]")


if __name__ == "__main__":
    conectar()
