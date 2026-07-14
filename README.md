# Monitor de Clan - Ninja Kaizen

Este es un bot en Python desarrollado para rastrear y auditar en tiempo real la actividad, ataques y estadísticas de todos los miembros de mi clan en **Ninja Kaizen**. El sistema automatiza el raspado de datos de la web del juego, guarda el historial de forma local y reporta todo de manera organizada a nuestro servidor de Discord.

---

# ¿Por qué creé este proyecto?

Gestionar un clan competitivo de forma manual es un dolor de cabeza. Necesitaba automatizar el control de las batallas y el estado diario de cada miembro sin tener que revisar la web del juego a cada rato. 

Este monitor hace el trabajo pesado por mí cada 6 segundos, asegurando que ningún dato se pierda y que todo el equipo esté alineado a través de alertas automatizadas.

---

# Lo que hace este sistema

- **Scraping automatizado:** Conecta con la web oficial de Ninja Kaizen y extrae los datos limpios de los jugadores en cada ciclo.
- **Base de datos local (SQLite):** Guarda el estado de los miembros para llevar un registro histórico confiable. Uso **DB Browser por SQLite** para verificar la estructura y las consultas de la base de datos.
- **Alertas en Discord:** Envía reportes formateados directamente a los canales del clan usando Webhooks.
- **Seguridad en las credenciales:** Las URLs secretas de Discord y los datos sensibles no están expuestos en el código; se manejan de forma oculta en un archivo `.env` local por ciberseguridad.

---

# Desafíos Técnicos y Solución (Estabilidad de Red)

Durante las primeras pruebas, el script abría y cerraba conexiones de red individuales en cada vuelta. Esto saturaba los sockets de Windows y provocaba caídas constantes por bloqueos del servidor remoto (como el Error 10054).

**La Solución:** Refactoricé la conexión para implementar un **Túnel de Red Permanente (`requests.Session()`)**. Al mantener la tubería de comunicación abierta (Keep-Alive), el bot ya no fuerza la red en cada ciclo. Esto eliminó por completo los errores de desconexión, bajó el uso de CPU en mi computadora local y estabilizó los reportes masivos hacia Discord.

---

# Archivos del Proyecto

- `monitor_clan.py`: Código principal con la lógica del bot, las peticiones de red y el guardado en la base de datos.
- `clan_data.sqbpro`: Configuración de DB Browser para el manejo de las tablas SQLite.
- `.gitignore`: Filtro esencial para que Git no suba a GitHub mi base de datos real (`.db`) ni mis contraseñas privadas (`.env`).

---
Desarrollado por **nolandev** 