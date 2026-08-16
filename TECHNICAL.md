# Chat Distribuido con Sockets y Tolerancia a Fallos

Sistema de mensajería distribuida en tiempo real implementado en Python con arquitectura cliente-servidor TCP, concurrencia mediante hilos y tolerancia a fallos ante desconexiones abruptas.

> Proyecto de Investigación — Sistemas Operativos II · Universidad Latina de Costa Rica

---

## Características

- **Chat en tiempo real** — mensajes broadcast a todos los clientes conectados
- **Mensajes privados** — `/privado @usuario mensaje`
- **Historial automático** — al conectarte recibís los últimos 50 mensajes
- **"Está escribiendo..."** — indicador en tiempo real con throttle de 2 segundos
- **Lista de usuarios en línea** — panel lateral con ● verde por usuario conectado
- **Tolerancia a fallos** — desconexiones detectadas y limpiadas sin caer el servidor
- **Interfaz gráfica** — tema oscuro con colores por usuario (tkinter)
- **Despliegue con Docker** — `docker-compose up --build`

---

## Estructura del proyecto

```
chat/
├── server.py          # Servidor TCP multihilo
├── client_gui.py      # Cliente con interfaz gráfica tkinter
├── protocol.py        # Serialización de mensajes JSON
├── metrics.py         # Script de pruebas de carga
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── LICENSE
```

---

## Requisitos

- Python 3.11+
- `psutil` (solo para métricas): `pip install psutil`
- tkinter (incluido con Python en Windows/macOS; en Linux: `sudo apt install python3-tk`)

---

## Cómo ejecutar

### Local

```bash
# Terminal 1 — iniciar servidor
python server.py

# Terminal 2+ — un cliente por persona
python client_gui.py
```

### Con Docker

```bash
docker-compose up --build
```

---

## Comandos del chat

| Comando | Descripción |
|---|---|
| Escribir y Enter | Enviar mensaje a todos |
| `/privado @nombre mensaje` | Mensaje privado a un usuario específico |
| `/usuarios` | Refrescar lista de conectados |
| Ctrl+C o cerrar ventana | Desconectarse |

---

## Resultados experimentales

Pruebas ejecutadas en localhost con clientes simulados enviando 10 mensajes cada uno:

| Clientes | Throughput (msg/s) | Latencia prom. (ms) | Desv. estándar (ms) |
|---|---|---|---|
| 5 | 91.3 | 50.19 | 0.07 |
| 10 | 186.5 | 50.20 | 0.10 |
| 20 | 360.5 | 50.14 | 0.05 |
| 50 | 894.5 | 50.14 | 0.07 |

La latencia se mantuvo estable en ~50 ms independientemente de la carga. El servidor no presentó ninguna caída durante las pruebas.

---

## Arquitectura

```
Cliente A ──┐
Cliente B ──┤── TCP :5000 ──► Servidor (server.py)
Cliente C ──┘                  │
                               ├── Thread por cliente
                               ├── dict {socket: nombre} + Lock
                               ├── deque historial (50 msg)
                               └── Broadcast / mensajes privados
```

**Protocolo:** mensajes JSON con campo `tipo` (`mensaje`, `privado`, `sistema`, `historial`, `usuarios`, `escribiendo`) + `usuario`, `mensaje`, `timestamp`.

---

## Tolerancia a fallos

Cuando un cliente se desconecta abruptamente:
1. El socket lanza `ConnectionResetError` o `BrokenPipeError`
2. El hilo captura la excepción
3. Adquiere el `threading.Lock` y remueve al cliente del diccionario
4. Notifica al resto: "usuario abandonó el chat"
5. El hilo termina — el servidor sigue sin interrupciones

---

## Tecnologías

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.11+ |
| Comunicación | `socket` (TCP) |
| Concurrencia | `threading` |
| Protocolo | `json` |
| Interfaz gráfica | `tkinter` |
| Métricas | `psutil`, `time`, `statistics` |
| Contenerización | Docker + Docker Compose |
| Control de versiones | Git / GitHub |

---

## Referencias

- Stevens, W. R. (2003). *UNIX Network Programming, Volume 1* (3.ª ed.). Addison-Wesley.
- Tanenbaum, A. S. y Bos, H. (2015). *Modern Operating Systems* (4.ª ed.). Pearson.
- Tanenbaum, A. S. y Van Steen, M. (2017). *Distributed Systems: Principles and Paradigms* (3.ª ed.). Pearson.
- Python Software Foundation. (2024). *socket* — https://docs.python.org/3/library/socket.html
- Python Software Foundation. (2024). *threading* — https://docs.python.org/3/library/threading.html

---

## Licencia

MIT © 2026 Josue Leiva — ver [LICENSE](LICENSE)
