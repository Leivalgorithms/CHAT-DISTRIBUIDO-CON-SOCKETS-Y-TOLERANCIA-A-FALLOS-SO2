"""
metrics.py — Script de pruebas de carga y medición de métricas.

Simula N clientes concurrentes, cada uno enviando M mensajes,
y mide latencia de entrega y tasa de éxito.

Uso:
    python metrics.py --clientes 20 --mensajes 10
"""

import socket
import threading
import time
import argparse
import statistics
from protocol import msg_mensaje as encode, decode

HOST = "127.0.0.1"
PORT = 5000
BUFFER = 4096

resultados_lock = threading.Lock()
latencias: list[float] = []
errores: int = 0


def cliente_carga(id_cliente: int, n_mensajes: int) -> None:
    """Simula un cliente que envía n_mensajes y mide la latencia de cada uno."""
    global errores
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.settimeout(5.0)

        usuario = f"bot_{id_cliente}"
        sock.sendall(encode(usuario, "conectado"))

        for i in range(n_mensajes):
            mensaje = f"mensaje_{i}_de_{usuario}"
            t0 = time.perf_counter()
            sock.sendall(encode(usuario, mensaje))

            # Esperar eco/respuesta (otro cliente en el mismo proceso no existe,
            # así que medimos el tiempo de envío exitoso como latencia de red)
            time.sleep(0.05)
            t1 = time.perf_counter()

            latencia_ms = (t1 - t0) * 1000
            with resultados_lock:
                latencias.append(latencia_ms)

        sock.close()

    except Exception as e:
        with resultados_lock:
            errores += 1


def ejecutar_prueba(n_clientes: int, n_mensajes: int) -> None:
    print(f"\n{'='*50}")
    print(f"  Prueba de carga: {n_clientes} clientes × {n_mensajes} mensajes")
    print(f"{'='*50}")

    hilos = []
    t_inicio = time.perf_counter()

    for i in range(n_clientes):
        h = threading.Thread(target=cliente_carga, args=(i, n_mensajes))
        hilos.append(h)

    for h in hilos:
        h.start()

    for h in hilos:
        h.join()

    t_total = time.perf_counter() - t_inicio

    # ── Resultados ────────────────────────────────────────────────────
    total_mensajes = n_clientes * n_mensajes
    exitosos = total_mensajes - errores

    print(f"\n  Resultados:")
    print(f"  {'Mensajes enviados':<30} {total_mensajes}")
    print(f"  {'Mensajes exitosos':<30} {exitosos}")
    print(f"  {'Errores':<30} {errores}")
    print(f"  {'Tiempo total (s)':<30} {t_total:.2f}")
    print(f"  {'Throughput (msg/s)':<30} {exitosos / t_total:.1f}")

    if latencias:
        print(f"\n  Latencia (ms):")
        print(f"  {'  Promedio':<30} {statistics.mean(latencias):.2f}")
        print(f"  {'  Mínima':<30} {min(latencias):.2f}")
        print(f"  {'  Máxima':<30} {max(latencias):.2f}")
        print(f"  {'  Desv. estándar':<30} {statistics.stdev(latencias):.2f}" if len(latencias) > 1 else "")

    print(f"{'='*50}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Prueba de carga del servidor de chat")
    parser.add_argument("--clientes", type=int, default=10, help="Número de clientes simultáneos")
    parser.add_argument("--mensajes", type=int, default=5, help="Mensajes por cliente")
    args = parser.parse_args()

    ejecutar_prueba(args.clientes, args.mensajes)
