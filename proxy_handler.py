
import requests
import random

proxy_global = None

def set_proxy_global(proxy):
    global proxy_global
    proxy_global = proxy

def obtener_proxy_pago(usuario, clave, url, log_widget=None):
    try:
        proxies = {
            "http": f"http://{usuario}:{clave}@{url.replace('http://', '')}",
            "https": f"http://{usuario}:{clave}@{url.replace('http://', '')}",
        }
        r = requests.get("http://httpbin.io/ip", proxies=proxies, timeout=10)
        if r.status_code == 200:
            if log_widget:
                log_widget.insert("end", f"✅ Proxy pago activo: {r.json()}\n")
            return proxies
        else:
            if log_widget:
                log_widget.insert("end", f"❌ Proxy pago fallido: código {r.status_code}\n")
    except Exception as e:
        if log_widget:
            log_widget.insert("end", f"❌ Error con proxy pago: {e}\n")
    return None

def obtener_proxies_gratis(log_widget=None):
    try:
        url = "https://www.proxy-list.download/api/v1/get?type=https"
        response = requests.get(url)
        proxy_list = response.text.strip().split("\n")
        random.shuffle(proxy_list)
        for proxy in proxy_list:
            proxies = {
                "http": f"http://{proxy}",
                "https": f"http://{proxy}",
            }
            try:
                r = requests.get("http://httpbin.io/ip", proxies=proxies, timeout=5)
                if r.status_code == 200:
                    if log_widget:
                        log_widget.insert("end", f"✅ Proxy gratis activo: {proxy}\n")
                    return proxies
            except:
                if log_widget:
                    log_widget.insert("end", f"❌ Proxy gratis fallido: {proxy}\n")
    except Exception as e:
        if log_widget:
            log_widget.insert("end", f"❌ Error al obtener proxies gratuitos: {e}\n")
    return None
