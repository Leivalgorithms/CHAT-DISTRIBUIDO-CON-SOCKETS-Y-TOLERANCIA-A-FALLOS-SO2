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

---
 
## 7. Plan de Trabajo
 
| Semana | Fase | Actividades | Entregable |
|---|---|---|---|
| 12 | Planificación | Definir arquitectura. Configurar entorno (Python, Docker). Crear repositorio con estructura inicial. | Repo GitHub + diagrama de arquitectura |
| 13 | Revisión Bibliográfica | Investigar literatura sobre sockets TCP, concurrencia y tolerancia a fallos. Elaborar marco teórico. | Marco teórico |
| 14 | Implementación y Pruebas | Implementar servidor TCP multihilo y cliente. Agregar tolerancia a fallos. Pruebas y métricas. | Código funcional + resultados |
| 15 | Cierre y Entrega | Redactar informe final. Preparar presentación. Publicar Docker Compose y README. Exposición. | Informe + presentación + demo |
 
---
 
## 8. Metodología de Investigación
 
### Enfoque Iterativo-Incremental
 
El desarrollo se divide en incrementos funcionales: servidor básico de un cliente → múltiples clientes concurrentes → mecanismos de tolerancia a fallos. Esto permite validar cada componente de forma aislada antes de integrarlo al sistema completo.
 
### Método Experimental
 
Para evaluar el rendimiento se ejecutarán experimentos controlados con distintas cargas de clientes simultáneos. Las variables medidas serán:
 
- Latencia promedio de entrega de mensajes (ms).
- Número máximo de clientes concurrentes sin degradación del servicio.
- Tiempo de detección y recuperación ante desconexiones inesperadas (ms).
- Uso de CPU y memoria del proceso servidor bajo carga.
Cada experimento se repetirá al menos 5 veces para obtener promedios estadísticamente representativos.
 
### Revisión Bibliográfica
 
Se consultarán las siguientes fuentes:
 
- Stevens, W. R. & Rago, S. A. – *Unix Network Programming* (Vol. 1).
- Tanenbaum, A. S. & Van Steen, M. – *Distributed Systems: Principles and Paradigms*.
- Documentación oficial de Python 3 – módulos `socket` y `threading` (docs.python.org).
- Documentación oficial de Docker y Docker Compose (docs.docker.com).
- Repositorios de referencia en GitHub sobre implementaciones de chat TCP en Python.
---
 
## 9. Identificación de Riesgos
 
| Riesgo | Probabilidad | Mitigación |
|---|---|---|
| Problemas de concurrencia (race conditions) | Media | Uso de locks y diseño cuidadoso de secciones críticas |
| Complejidad en tolerancia a fallos | Media | Implementar primero funcionalidad básica y agregar tolerancia como incremento |
| Configuración de Docker en Windows | Baja | Usar WSL2 o desarrollar directamente en Linux |
| Atraso en cronograma | Baja | Seguir el plan incremental; las características opcionales son prescindibles |


