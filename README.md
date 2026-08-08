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

## 9. Marco Teórico

### 9.1 Sockets y el Modelo de Comunicación TCP

Un socket TCP es una abstracción del sistema operativo que representa un extremo de una conexión de red confiable. Desde la perspectiva del programador, un socket se comporta como un archivo: se puede leer y escribir en él, y el sistema operativo se encarga de fragmentar los datos en paquetes IP, transmitirlos por la red y reensamblarlos en el destino.

El modelo de comunicación para el servidor sigue el patrón: crear socket → asignar dirección y puerto (`bind`) → habilitar escucha (`listen`) → aceptar conexiones (`accept`). Cada llamada a `accept()` bloquea hasta que un cliente se conecta y retorna un nuevo socket dedicado a esa conexión. El socket original continúa aceptando nuevas conexiones, mientras que el nuevo socket se usa exclusivamente para comunicarse con ese cliente (Stevens y Rago, 2013).

### 9.2 Concurrencia Mediante Hilos

Un hilo (thread) es la unidad mínima de ejecución dentro de un proceso. A diferencia de los procesos, los hilos de un mismo proceso comparten el espacio de memoria, los descriptores de archivo y otros recursos del sistema operativo. Esta característica permite que múltiples hilos accedan y modifiquen estructuras de datos compartidas, lo que introduce la necesidad de sincronización (Tanenbaum y Bos, 2015).

En el servidor de chat, la estructura de datos compartida crítica es la lista de clientes conectados. El mecanismo estándar para prevenir condiciones de carrera es el mutex (mutual exclusion lock): solo un hilo puede adquirir el lock a la vez, garantizando acceso exclusivo a la sección crítica.

### 9.3 Arquitectura Cliente-Servidor

La arquitectura cliente-servidor es el patrón de diseño dominante en sistemas de comunicación en red. El servidor es pasivo (espera solicitudes) y los clientes son activos (inician la comunicación). En el contexto de sistemas de chat, el servidor actúa como intermediario (broker): recibe mensajes de un cliente y los redistribuye a los demás conectados — patrón conocido como publish-subscribe centralizado (Hohpe y Woolf, 2003).

### 9.4 Tolerancia a Fallos

La tolerancia a fallos se implementa a través de manejo de excepciones a nivel de socket. Cuando un cliente se desconecta abruptamente, las operaciones de lectura sobre ese socket lanzan una excepción (`ConnectionResetError`, `BrokenPipeError`). El servidor captura estas excepciones, remueve al cliente de la lista compartida y cierra el socket. El resto de los clientes no se ve afectado, ya que cada uno es atendido por su propio hilo independiente (Birman, 2012).

### 9.5 Protocolo de Mensajes

Para estructurar la comunicación se utiliza JSON como formato de serialización. Cada mensaje tiene la estructura:

```json
{ "usuario": "nombre", "mensaje": "texto", "timestamp": "HH:MM:SS" }
```

Este formato permite agregar campos adicionales en el futuro sin romper la compatibilidad con versiones anteriores del protocolo.

---

## 10. Referencias Bibliográficas

- Beazley, D. y Jones, B. K. (2013). *Python Cookbook* (3.ª ed.). O'Reilly Media.
- Birman, K. (2012). *Guide to Reliable Distributed Systems*. Springer.
- Coulouris, G., Dollimore, J., Kindberg, T. y Blair, G. (2012). *Distributed Systems: Concepts and Design* (5.ª ed.). Addison-Wesley.
- Forouzan, B. A. (2021). *Data Communications and Networking* (5.ª ed.). McGraw-Hill Education.
- Hohpe, G. y Woolf, B. (2003). *Enterprise Integration Patterns*. Addison-Wesley.
- Jain, R. (1991). *The Art of Computer Systems Performance Analysis*. Wiley.
- Kerrisk, M. (2010). *The Linux Programming Interface*. No Starch Press.
- Lamport, L. (1978). Time, clocks, and the ordering of events in a distributed system. *Communications of the ACM*, 21(7), 558–565.
- Python Software Foundation. (2024). *socket — Low-level networking interface*. https://docs.python.org/3/library/socket.html
- Python Software Foundation. (2024). *threading — Thread-based parallelism*. https://docs.python.org/3/library/threading.html
- Stevens, W. R. (2003). *UNIX Network Programming, Volume 1* (3.ª ed.). Addison-Wesley.
- Stevens, W. R. y Rago, S. A. (2013). *Advanced Programming in the UNIX Environment* (3.ª ed.). Addison-Wesley.
- Tanenbaum, A. S. y Bos, H. (2015). *Modern Operating Systems* (4.ª ed.). Pearson.
- Tanenbaum, A. S. y Van Steen, M. (2017). *Distributed Systems: Principles and Paradigms* (3.ª ed.). Pearson.

---

## 11. Identificación de Riesgos

| Riesgo | Probabilidad | Mitigación |
|---|---|---|
| Problemas de concurrencia (race conditions) | Media | Uso de locks y diseño cuidadoso de secciones críticas |
| Complejidad en tolerancia a fallos | Media | Implementar primero funcionalidad básica y agregar tolerancia como incremento |
| Configuración de Docker en Windows | Baja | Usar WSL2 o desarrollar directamente en Linux |
| Atraso en cronograma | Baja | Seguir el plan incremental; las características opcionales son prescindibles |
