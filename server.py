"""
server.py — Servidor de chat distribuido sobre TCP.

Características:
  - Un hilo por cliente.
  - Lista de clientes protegida con Lock.
  - Historial de los últimos 50 mensajes enviado al conectarse.
  - Comando /usuarios para ver quién está conectado.
  - Mensajes privados: /privado @usuario mensaje
  - Reenvío de indicadores "escribiendo...".
  - Tolerancia a fallos: limpieza garantizada ante desconexiones abruptas.
"""

import socket
import threading
import logging
import sys
from collections import deque
from protocol import (
    decode, msg_mensaje, msg_sistema, msg_historial,
    msg_usuarios, msg_escribiendo, msg_privado
)

HOST = "0.0.0.0"
PORT = 5000
BUFFER = 4096
MAX_HISTORIAL = 50

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [SERVER] %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("server.log"),
    ],
)
log = logging.getLogger(__name__)

# ── Estado compartido ─────────────────────────────────────────────────────────
clientes: dict[socket.socket, str] = {}   # socket → nombre
historial: deque = deque(maxlen=MAX_HISTORIAL)
lock = threading.Lock()


def usuarios_conectados() -> list[str]:
    with lock:
        return list(clientes.values())


def broadcast(data: bytes, excluir: socket.socket | None = None) -> None:
    """Envía a todos los clientes excepto al excluido."""
    with lock:
        destinos = [(s, u) for s, u in clientes.items() if s != excluir]
    for sock, usuario in destinos:
        try:
            sock.sendall(data)
        except Exception as e:
            log.warning(f"Error al enviar a {usuario}: {e}")


def enviar_a(sock: socket.socket, data: bytes) -> bool:
    """Envía datos a un socket específico. Retorna False si falla."""
    try:
        sock.sendall(data)
        return True
    except Exception:
        return False


def manejar_cliente(conn: socket.socket, addr: tuple) -> None:
    usuario = "desconocido"
    try:
        # ── Handshake: primer mensaje es la presentación ──────────────────
        data = conn.recv(BUFFER)
        msg = decode(data)
        if not msg or msg.get("tipo") != "mensaje":
            conn.close()
            return

        usuario = msg["usuario"].strip()

        # Verificar nombre duplicado
        with lock:
            if usuario in clientes.values():
                conn.sendall(msg_sistema(f'El nombre "{usuario}" ya está en uso. Reconectate con otro nombre.'))
                conn.close()
                return
            clientes[conn] = usuario

        log.info(f"Conectado: {usuario} desde {addr}")

        # Enviar historial al nuevo cliente
        with lock:
            hist = list(historial)
        if hist:
            enviar_a(conn, msg_historial(hist))

        # Notificar a todos
        aviso = msg_sistema(f"{usuario} se unió al chat. 👋")
        broadcast(aviso, excluir=conn)

        # Actualizar lista de usuarios para todos
        broadcast(msg_usuarios(usuarios_conectados()))

        # ── Loop principal ────────────────────────────────────────────────
        while True:
            data = conn.recv(BUFFER)
            if not data:
                break

            msg = decode(data)
            if not msg:
                continue

            tipo = msg.get("tipo")

            if tipo == "mensaje":
                texto = msg.get("mensaje", "").strip()
                if not texto:
                    continue

                # Comando /usuarios
                if texto == "/usuarios":
                    lista = usuarios_conectados()
                    enviar_a(conn, msg_usuarios(lista))
                    continue

                # Comando /privado @destinatario mensaje
                if texto.startswith("/privado "):
                    partes = texto.split(" ", 2)
                    if len(partes) < 3 or not partes[1].startswith("@"):
                        enviar_a(conn, msg_sistema("Uso: /privado @usuario mensaje"))
                        continue
                    dest_nombre = partes[1][1:]
                    mensaje_priv = partes[2]
                    with lock:
                        dest_sock = next((s for s, u in clientes.items() if u == dest_nombre), None)
                    if dest_sock:
                        paquete = msg_privado(usuario, dest_nombre, mensaje_priv)
                        enviar_a(dest_sock, paquete)
                        enviar_a(conn, paquete)  # eco al remitente
                    else:
                        enviar_a(conn, msg_sistema(f'Usuario "{dest_nombre}" no encontrado.'))
                    continue

                # Mensaje normal — guardar en historial y broadcast
                paquete = msg_mensaje(usuario, texto)
                with lock:
                    historial.append({
                        "tipo": "mensaje",
                        "usuario": usuario,
                        "mensaje": texto,
                        "timestamp": msg.get("timestamp", ""),
                    })
                broadcast(paquete, excluir=conn)
                log.info(f"[{usuario}]: {texto}")

            elif tipo == "escribiendo":
                # Reenviar indicador a todos menos al remitente
                broadcast(msg_escribiendo(usuario), excluir=conn)

    except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError) as e:
        log.warning(f"Desconexión abrupta de {usuario}: {e}")
    except Exception as e:
        log.error(f"Error con {usuario}: {e}")
    finally:
        with lock:
            clientes.pop(conn, None)
        try:
            conn.close()
        except Exception:
            pass
        log.info(f"Desconectado: {usuario}. Activos: {len(clientes)}")
        aviso = msg_sistema(f"{usuario} abandonó el chat.")
        broadcast(aviso)
        broadcast(msg_usuarios(usuarios_conectados()))


def iniciar() -> None:
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind((HOST, PORT))
    servidor.listen()
    log.info(f"Servidor escuchando en {HOST}:{PORT}")

    try:
        while True:
            conn, addr = servidor.accept()
            hilo = threading.Thread(target=manejar_cliente, args=(conn, addr), daemon=True)
            hilo.start()
    except KeyboardInterrupt:
        log.info("Servidor detenido.")
    finally:
        servidor.close()


if __name__ == "__main__":
    iniciar()
