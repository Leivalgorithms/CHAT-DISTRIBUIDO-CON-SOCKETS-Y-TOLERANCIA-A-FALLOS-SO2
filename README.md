# Chat Distribuido con Sockets y Tolerancia a Fallos

## 1. Definición del Tema

El proyecto consiste en el diseño e implementación de un sistema de mensajería distribuida basado en el protocolo TCP, capaz de gestionar múltiples clientes de forma concurrente. El sistema incorporará mecanismos de tolerancia a fallos para garantizar la continuidad del servicio ante desconexiones o errores de red.

La implementación se realizará en Python, aprovechando sus módulos nativos de comunicación de red (`socket`) y concurrencia (`threading`), así como contenedores Docker para facilitar el despliegue y la demostración del sistema.

---

## 2. Justificación

Los sistemas de comunicación distribuida son fundamentales en la infraestructura tecnológica moderna. Comprender su funcionamiento a bajo nivel —desde la apertura de sockets hasta el manejo de hilos concurrentes— proporciona una base sólida para el análisis de plataformas como sistemas de mensajería, microservicios y aplicaciones en la nube.

Este tema permite aplicar directamente los conceptos centrales del curso: sockets TCP, concurrencia mediante hilos, sistemas distribuidos y análisis de métricas de rendimiento como latencia y disponibilidad del servidor.

---

## 3. Objetivo General

Implementar un sistema de chat distribuido sobre sockets TCP con soporte para múltiples clientes concurrentes y mecanismos de tolerancia a fallos, evaluando su comportamiento bajo métricas de alta disponibilidad, rendimiento y escalabilidad.

---

## 4. Objetivos Específicos

- Diseñar la arquitectura cliente-servidor del sistema de chat utilizando sockets TCP en Python, definiendo los protocolos de comunicación y el formato de los mensajes intercambiados.
- Implementar un servidor de chat capaz de gestionar múltiples conexiones simultáneas mediante hilos (threading), garantizando la consistencia en la difusión de mensajes a todos los clientes conectados.
- Incorporar mecanismos de tolerancia a fallos en el servidor para detectar y manejar desconexiones inesperadas de clientes sin interrumpir el servicio para los demás usuarios activos.
- Medir y analizar métricas de rendimiento del sistema, incluyendo latencia de entrega de mensajes, número máximo de clientes concurrentes soportados y tiempo de recuperación ante fallos.
- Contenerizar la aplicación mediante Docker para facilitar su despliegue reproducible, documentar el proceso en este README y publicar el código fuente en GitHub con licencia open source.

---

## 5. Alcance del Proyecto

El proyecto contempla las siguientes características:

- Servidor central TCP que acepta conexiones de múltiples clientes simultáneamente.
- Clientes capaces de enviar y recibir mensajes en tiempo real.
- Manejo de concurrencia mediante hilos por cliente en el servidor.
- Detección de clientes desconectados y limpieza de recursos asociados.
- Registro de eventos del servidor (logs) para monitoreo básico.
- Despliegue completo con Docker Compose (servidor + múltiples clientes simulados).

**Características opcionales (a implementar si el tiempo lo permite):**

- Replicación entre dos instancias de servidor para mayor disponibilidad.
- Algoritmo simple de elección de líder entre servidores replicados.

---

## 6. Tecnologías y Herramientas

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.11+ |
| Módulos principales | `socket`, `threading`, `logging`, `json` |
| Contenerización | Docker y Docker Compose |
| Control de versiones | Git / GitHub |
| Medición de métricas | Scripts Python con `time` y `psutil` |
