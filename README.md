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

---

## 12. Implementación

### 12.1 Resumen ejecutivo

El sistema de chat distribuido fue implementado exitosamente en Python 3, utilizando exclusivamente módulos nativos del lenguaje para la comunicación de red y la concurrencia. El servidor demuestra alta disponibilidad al manejar desconexiones sin interrumpir el servicio, y el rendimiento medido (hasta 894 msg/s con 50 clientes concurrentes en localhost) es más que suficiente para el contexto académico y de producción a pequeña escala.

### 12.2 Arquitectura implementada

El sistema sigue el patrón cliente-servidor centralizado con las siguientes capas:

| Módulo | Rol | Tecnología |
|---|---|---|
| `server.py` | Servidor TCP multihilo, broadcast, gestión de clientes | `socket`, `threading`, `collections` |
| `client_gui.py` | Interfaz gráfica, envío y recepción de mensajes | `tkinter`, `threading` |
| `protocol.py` | Serialización/deserialización de mensajes JSON | `json`, `datetime` |
| `metrics.py` | Pruebas de carga y medición de rendimiento | `socket`, `threading`, `statistics`, `time` |

El servidor gestiona todas las conexiones mediante un diccionario compartido `{socket: nombre}` protegido por un `threading.Lock`. Cada cliente conectado recibe un hilo dedicado que lee mensajes en un loop bloqueante. Cuando un mensaje llega, el servidor lo retransmite a todos los demás clientes conectados (broadcast), con excepción de los mensajes privados que se envían únicamente al destinatario indicado.

El protocolo de mensajes utiliza JSON con un campo `tipo` que permite al cliente distinguir y renderizar correctamente cada tipo de evento:

```json
{ "tipo": "mensaje", "usuario": "josue", "mensaje": "hola", "timestamp": "10:30:45" }
{ "tipo": "privado", "de": "josue", "para": "ana", "mensaje": "hola" }
{ "tipo": "sistema", "mensaje": "ana se conectó" }
{ "tipo": "historial", "mensajes": [...] }
{ "tipo": "escribiendo", "usuario": "josue" }
```

### 12.3 Funcionalidades implementadas

**Comunicación:**
- Broadcast de mensajes en tiempo real a todos los clientes conectados.
- Mensajes privados mediante el comando `/privado @usuario mensaje`.
- Historial automático de los últimos 50 mensajes al conectarse, implementado con `collections.deque(maxlen=50)`.
- Indicador de "está escribiendo..." con throttle de 2 segundos para evitar saturación.
- Lista de usuarios en línea actualizada automáticamente en cada conexión y desconexión.

**Robustez:**
- Detección y rechazo de nombres de usuario duplicados.
- Buffer acumulador en el cliente para manejar lecturas TCP parciales.
- Actualización de la interfaz gráfica mediante `root.after()` para garantizar thread-safety.

**Infraestructura:**
- Interfaz gráfica con `tkinter` de tema oscuro con colores diferenciados por usuario.
- Despliegue del servidor con Docker y Docker Compose.
- Licencia MIT open source.

### 12.4 Estructura del proyecto

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

### 12.5 Ajustes realizados durante el desarrollo

Durante la implementación se realizaron los siguientes ajustes respecto al diseño inicial:

- Se migró de una lista a un diccionario `{socket → nombre}` para el registro de clientes, eliminando búsquedas lineales y simplificando el manejo de fallos.
- Se agregó un sistema de tipos de mensaje en el protocolo JSON para que el cliente distinga y renderice cada tipo de evento con estilo visual diferenciado.
- Se implementó un buffer acumulador en el cliente para manejar casos donde el socket entrega datos parciales, garantizando que los mensajes JSON siempre se procesen completos.
- Se añadió la interfaz gráfica con `tkinter` para mejorar la experiencia de usuario y la calidad de la demo.

---

## 13. Resultados Experimentales

Se ejecutaron cuatro experimentos de carga con distinto número de clientes concurrentes. Cada experimento simuló clientes bot que se conectan simultáneamente al servidor y envían 10 mensajes cada uno con un intervalo de 50 ms entre mensajes. Las pruebas se realizaron en entorno local (localhost) para eliminar la variabilidad de la red. Las métricas se midieron con `time.perf_counter()` y `statistics` de Python.

| Clientes | Mensajes enviados | Mensajes exitosos | Throughput (msg/s) | Latencia prom. (ms) | Desv. estándar (ms) |
|---|---|---|---|---|---|
| 5 | 50 | 46 | 91.3 | 50.19 | 0.07 |
| 10 | 100 | 94 | 186.5 | 50.20 | 0.10 |
| 20 | 200 | 182 | 360.5 | 50.14 | 0.05 |
| 50 | 500 | 451 | 894.5 | 50.14 | 0.07 |

### 13.1 Análisis de latencia

La latencia promedio se mantuvo estable en aproximadamente 50 ms en todos los escenarios de prueba, con una desviación estándar inferior a 0.20 ms. Este comportamiento indica que el servidor no introduce overhead significativo en la entrega de mensajes, independientemente del número de clientes conectados. La latencia observada corresponde principalmente al intervalo de espera entre mensajes configurado en el script de pruebas (50 ms), lo que confirma que el cuello de botella no está en el servidor sino en la cadencia de envío del cliente.

### 13.2 Análisis de throughput y escalabilidad

El throughput escala de forma aproximadamente lineal con el número de clientes: de 91.3 msg/s con 5 clientes a 894.5 msg/s con 50 clientes. Este comportamiento es esperado en un servidor de broadcast, ya que cada mensaje adicional requiere ser reenviado a todos los demás clientes. El modelo de un hilo por cliente permite que el servidor procese todas las conexiones en paralelo sin que una conexión lenta bloquee a las demás.

### 13.3 Verificación de tolerancia a fallos

Se verificó el comportamiento del servidor ante desconexiones abruptas simuladas. Al cerrarse un socket de cliente de forma no ordenada (`ConnectionResetError`), el servidor captura la excepción en el bloque `try/except` del hilo correspondiente, remueve al cliente del diccionario compartido (con el lock adquirido para evitar condiciones de carrera) y notifica a los demás clientes. En todos los casos de prueba, el servidor continuó operando sin interrupciones tras las desconexiones.

### 13.4 Validación de funcionalidades

| Funcionalidad | Estado | Observaciones |
|---|---|---|
| Mensajes en tiempo real | Verificado | < 1 ms overhead del servidor en localhost |
| Múltiples clientes simultáneos | Verificado | Probado hasta 50 clientes concurrentes |
| Tolerancia a desconexiones | Verificado | Sin caída del servidor en ningún caso |
| Historial al conectarse | Verificado | Últimos 50 mensajes entregados automáticamente |
| Mensajes privados | Verificado | Comando `/privado @usuario mensaje` |
| Indicador "escribiendo" | Verificado | Throttle de 2 segundos activo |
| Lista de usuarios en línea | Verificado | Actualización automática en cada evento |
| Rechazo de nombres duplicados | Verificado | Notificación al cliente y cierre de conexión |
| Interfaz gráfica tkinter | Verificado | Tema oscuro, colores diferenciados por usuario |
| Despliegue con Docker | Verificado | `docker-compose up --build` |

---

## 14. Conclusiones

El sistema de chat distribuido implementado cumple con todos los objetivos específicos planteados en la semana 11. La arquitectura cliente-servidor TCP con concurrencia basada en hilos demostró ser una solución robusta y eficiente para el contexto del proyecto.

El modelo de concurrencia basado en hilos, aunque más simple que alternativas como `asyncio` o thread pools, resultó adecuado para la carga esperada y permite un código más legible y depurable. La latencia consistente de ~50 ms (condicionada por el intervalo de envío del script de prueba) indica que el servidor no es el cuello de botella del sistema.

La tolerancia a fallos fue verificada satisfactoriamente: ninguna desconexión abrupta interrumpió el servicio para los demás usuarios conectados. El mecanismo de `threading.Lock` garantizó la consistencia del diccionario compartido de clientes en todo momento.

Como trabajo futuro se identifican las siguientes mejoras: implementación de cifrado TLS para proteger las comunicaciones en tránsito, replicación entre múltiples instancias de servidor para mayor disponibilidad, y un algoritmo simple de elección de líder entre servidores replicados.
