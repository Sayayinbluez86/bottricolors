import tkinter as tk
from tkinter import ttk
from datetime import datetime
import threading
import os
from modulos.login_bot import procesar_csv, procesar_rango, set_proxy_global
from proxy_handler import obtener_proxies_gratis, obtener_proxy_pago

def iniciar():
    tipo = tipo_opcion.get()
    sub = subopcion.get()
    modo = modo_opcion.get()

    if usar_proxy_pago.get():
        proxy = obtener_proxy_pago(usuario_proxy.get(), clave_proxy.get(), url_proxy.get(), log_text)
        if proxy:
            set_proxy_global(proxy)
    elif usar_proxy_gratis.get():
        proxy = obtener_proxies_gratis(log_text)
        if proxy:
            set_proxy_global(proxy)

    if modo == "CSV":
        threading.Thread(target=procesar_csv, args=(tipo, sub, log_text)).start()
    elif modo == "Rango":
        try:
            i = int(entry_inicio.get())
            f = int(entry_fin.get())
            nombre = entry_nombre.get().strip().upper()
            threading.Thread(target=procesar_rango, args=(i, f, nombre, tipo, sub, log_text)).start()
        except ValueError:
            log_text.insert(tk.END, "⚠️ Error: inicio/fin inválido\n")

app = tk.Tk()
app.title("BOT TRICOLOR DV")
app.geometry("600x600")

tk.Label(app, text="BOT TRICOLOR DV", font=("Helvetica", 16, "bold")).pack(pady=10)

tk.Label(app, text="Modo de ejecución", font=("Helvetica", 10, "bold")).pack()
modo_opcion = tk.StringVar(value="CSV")
tk.Radiobutton(app, text="Generar por Archivo CSV", variable=modo_opcion, value="CSV").pack()
tk.Radiobutton(app, text="Generar por Rango", variable=modo_opcion, value="Rango").pack()

tk.Label(app, text="Tipo de logo (1=4Díg, 2=2Díg)", font=("Helvetica", 10, "bold")).pack(pady=5)
tipo_opcion = ttk.Combobox(app, values=["1", "2"])
tipo_opcion.pack()

tk.Label(app, text="Tipo de recorrido", font=("Helvetica", 10, "bold")).pack(pady=5)
subopcion = ttk.Combobox(app, values=["Normal", "Alante", "Repetitiva", "Inversa"])
subopcion.pack()

tk.Label(app, text="Inicio del rango").pack()
entry_inicio = tk.Entry(app)
entry_inicio.pack()

tk.Label(app, text="Fin del rango").pack()
entry_fin = tk.Entry(app)
entry_fin.pack()

tk.Label(app, text="Nombre base del usuario").pack()
entry_nombre = tk.Entry(app)
entry_nombre.pack()

usar_proxy_pago = tk.BooleanVar()
tk.Checkbutton(app, text="Activar Proxy Pagos", variable=usar_proxy_pago).pack(pady=5)

tk.Label(app, text="Usuario Proxy").pack()
usuario_proxy = tk.Entry(app)
usuario_proxy.pack()

tk.Label(app, text="Clave Proxy").pack()
clave_proxy = tk.Entry(app, show="*")
clave_proxy.pack()

tk.Label(app, text="URL Proxy (http://...)").pack()
url_proxy = tk.Entry(app)
url_proxy.pack()

usar_proxy_gratis = tk.BooleanVar()
tk.Checkbutton(app, text="Usar Proxy Gratuito", variable=usar_proxy_gratis).pack()

tk.Button(app, text="Iniciar", command=iniciar).pack(pady=10)

log_text = tk.Text(app, height=15)
log_text.pack()

app.mainloop()