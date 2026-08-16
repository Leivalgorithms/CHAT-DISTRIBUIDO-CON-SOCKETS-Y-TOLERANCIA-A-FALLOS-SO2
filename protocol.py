"""
protocol.py — Serialización de mensajes del chat.

Tipos de mensaje (campo "tipo"):
  mensaje     — mensaje normal de chat
  sistema     — aviso del servidor (conexión, desconexión, etc.)
  historial   — bloque de mensajes anteriores enviado al conectarse
  usuarios    — lista de usuarios conectados
  escribiendo — indicador de "está escribiendo..."
  privado     — mensaje privado entre dos usuarios
"""

import json
from datetime import datetime


def _paquete(data: dict) -> bytes:
    return (json.dumps(data, ensure_ascii=False) + "\n").encode("utf-8")


def msg_mensaje(usuario: str, texto: str) -> bytes:
    return _paquete({
        "tipo": "mensaje",
        "usuario": usuario,
        "mensaje": texto,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
    })


def msg_sistema(texto: str) -> bytes:
    return _paquete({
        "tipo": "sistema",
        "mensaje": texto,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
    })


def msg_historial(mensajes: list) -> bytes:
    return _paquete({"tipo": "historial", "mensajes": mensajes})


def msg_usuarios(lista: list[str]) -> bytes:
    return _paquete({"tipo": "usuarios", "lista": lista})


def msg_escribiendo(usuario: str) -> bytes:
    return _paquete({"tipo": "escribiendo", "usuario": usuario})


def msg_privado(de: str, para: str, texto: str) -> bytes:
    return _paquete({
        "tipo": "privado",
        "de": de,
        "para": para,
        "mensaje": texto,
        "timestamp": datetime.now().strftime("%H:%M:%S"),
    })


def decode(data: bytes) -> dict | None:
    try:
        return json.loads(data.decode("utf-8").strip())
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None
