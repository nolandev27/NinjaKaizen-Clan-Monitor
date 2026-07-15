import requests
from bs4 import BeautifulSoup
import time
import sys
import sqlite3
from datetime import datetime 
import urllib3
import os
from dotenv import load_dotenv

# Cargo las variables del archivo .env en la memoria del script
load_dotenv() 
# Deshabilito las advertencias de seguridad de urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 

# Fuerzo la consola a usar UTF-8 nativo
sys.stdout.reconfigure(encoding='utf-8')

# Creamos el túnel de red global
objeto_red = requests.Session()

def inicializador_base_datos ():
    # Conecto con el archivo, (si no exite, python me lo crea en la carpeta)
    conexion_db = sqlite3.connect("clan_data.db")
    
    # Aqui creo el cursor para poder ejecutar el codigo sql
    cursor = conexion_db.cursor()
    
    # Le damos la orden en lenguaje SQL para creear la tabla si no exise
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS al_members (
            name TEXT PRIMARY KEY,
            level INTEGER,
            reputation INTEGER,
            last_update TEXT
        )
    """)
    
    # Guardamos los cambios y cerramos la conexión por seguridad
   
    print("✅ Base de datos inicializada correctamente.")
    
    # 📈 Tabla 2: Historial de ataques para las métricas de Power BI
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS guerra_eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            puntos_ganados INTEGER,
            timestamp TEXT
        )
    """)
    
    # Guardamos los cambios y cerramos la conexión por seguridad
    conexion_db.commit()
    conexion_db.close()
    print("✅ Base de datos inicializada correctamente con tabla de historial.")

# Forzamos la consola a usar UTF-8 nativo
sys.stdout.reconfigure(encoding='utf-8')

# 🌐 FUNCIÓN SECRETA PARA MANDAR ALERTAS A DISCORD
def enviar_alerta_discord(mensaje):
    url_webhook = os.getenv("DISCORD_WEBHOOK_URL")
    
    if not url_webhook:
        print("❌ Error: No se encontró la variable DISCORD_WEBHOOK_URL en el archivo .env")
        return
    
    # Preparamos el paquete de datos en el formato que Discord exige
    datos = {"content": mensaje}
    
    try:
        # Hacemos el envío en vivo
        objeto_red.post(url_webhook, json=datos)
        
    except Exception as e:
        print(f"❌ No se pudo enviar el reporte a Discord: {e}")


def monitorear_clan():
    url_clan = "https://ninjakaizen.com/clan/551"  # Link de mi clan
    
    print("🚀 Iniciando el Monitor en vivo de Alma Latina...")
    
    while True:
        print("\n🔄 Realizando llamado web para iniciar el monitoreo...")
        
        try:
            conexion = objeto_red.get(url_clan, timeout=10)
            
            if conexion.status_code == 200:
                print("✅ Conexión exitosa. Es hora de observar a estos lecheers...")
                
                conexion.encoding = 'utf-8'  # Forzamos la codificación correcta
                
                sopa = BeautifulSoup(conexion.text, "html.parser")
                
                print(f"Título detectado: '{sopa.title.string if sopa.title else 'Sin título'}'")
                print("--- LISTOS PARA EVALUAR ---")
                
                tabla = sopa.find("table")
                filas = sopa.find_all("tr")
                
                # Abrimos la conexión para esta vuelta de monitoreo
                conexion_db = sqlite3.connect("clan_data.db")
                cursor = conexion_db.cursor()
                
                # Capturamos la hora actual para registrar en la base de datos
                hora_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                print (f" Hemos encontrado {len(filas)} Ninjas en este legendario clan.")
                
                # Definimos los códigos de color ANSI
                VERDE = "\033[32m"
                ROJO = "\033[31m"
                RESET = "\033[0m"
                
                hora_exacta = datetime.now().strftime("%H:%M:%S")
                
                #Creamos la hoja en blanco para el reporte de esta vuelta
                reporte_vuelta = f"\n📊 **REPORTE DE ESTADO EN VIVO (GUERRA)** {hora_exacta}\n\n"
                
                for fila in filas[1:36]:  # Ignoramos la primera fila (encabezado)
                    celdas = fila.find_all("td")
                   
                   # Hacemos la extracción de datos de cada ninja 
                    name = celdas[1].text.strip()
                    level = int(celdas[2].text.strip())
                    reputation = int(celdas[3].text.strip())
                    
                    # Hacemos una consulta al pasado, pedimos la reputation previa del ninja en especifico
                    cursor.execute("SELECT reputation FROM al_members WHERE name = ?", (name,))
                    resultado = cursor.fetchone() # trae una sola fila de la base de datos 
                    
                    if resultado is not None:
                        reputation_anterior = resultado[0]
                        diferencia = reputation - reputation_anterior
                        
                        if diferencia > 0:
                            # 🟢 GANÓ PUNTOS
                            texto_ninja = f"🟢🔥 **{name}** ¡Está atacando! **+{diferencia}** de rep."
                            print(f"\033[32m{texto_ninja}\033[0m")
                    
                    # Lo acumulamos en nuestro reporte general
                            reporte_vuelta += f"{texto_ninja}\n"
                            
                            cursor.execute("""
                                INSERT INTO guerra_eventos (name, puntos_ganados, timestamp)
                                VALUES (?, ?, ?)
                            """, (name, diferencia, hora_actual))
                        else:
                    #  Mensaje de inactividad
                            texto_ninja = f"🔴🛡️ **{name}** ¡INACTIVO!"
                            print(f"\033[31m{texto_ninja}\033[0m")
                    
                    # También lo acumulamos en nuestro reporte general
                            reporte_vuelta += f"{texto_ninja}\n"
                            
                            # GUARDAMOS EL ATAQUE EN EL HISTORIAL DE GUERRA!
                            cursor.execute("""
                                INSERT INTO guerra_eventos (name, puntos_ganados, timestamp)
                                VALUES (?, ?, ?)
                            """, (name, diferencia, hora_actual))
                    
                    
                            

                    else:
                        #  Miembro nuevo en la base de datos
                        print(f"✨ ¡Nuevo miembro detectado! Bienvenido, [{name}].")
                    
                    # Ejecutamos la inserción o actualización en la base de datos
                    cursor.execute("""
                        INSERT OR REPLACE INTO al_members (name, level, reputation, last_update)
                        VALUES (?, ?, ?, ?)
                    """, (name, level, reputation, hora_actual))
                    
                    # Fuera del bucle 'for', cuando ya revisó todos los ninjas:
                print("📤 Enviando reporte consolidado a Discord...")
                enviar_alerta_discord(reporte_vuelta)
                    
                # Guardamos los cambios y cerramos la conexión por seguridad
                conexion_db.commit()    
                conexion_db.close()
                print("✅ Datos de los ninjas guardados correctamente.")
                    
                    
                    
               
        
            else:
                print("❌ Error en la conexión. Verificando estado...")
        except requests.exceptions.RequestException as e:
    # Este es el "escudo" que atrapa si no hay internet o si la página está caída
            print(f"No se pudo establecer contacto con el servidor. Motivo: {e}")
        
        print("😴 Esperando 6 segundos para la siguiente revisión...")
        
        time.sleep(6)

# Arrancamos la función principal de forma segura e independiente
if __name__ == "__main__":
    inicializador_base_datos()
    monitorear_clan()