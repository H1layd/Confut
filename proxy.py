import http.server
import socketserver
import requests
import logging
import winreg as reg

# Настройки прокси
PORT = 8080
PROXY_HOST = "localhost:8080"

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def set_proxy(proxy_host):
    logging.info("Попытка установить прокси...")
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(key, "ProxyEnable", 0, reg.REG_DWORD, 1)
        reg.SetValueEx(key, "ProxyServer", 0, reg.REG_SZ, proxy_host)
        reg.CloseKey(key)
        logging.info(f"Настройки прокси обновлены: {proxy_host}")
    except Exception as e:
        logging.error(f"Ошибка при изменении настроек прокси: {e}")

class Proxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        logging.info(f"Получен GET-запрос: {self.path}")
        try:
            # Перенаправление запроса к YouTube
            if "youtube.com" in self.path:
                response = requests.get(self.path)
                self.send_response(response.status_code)
                self.send_header("Content-Type", response.headers['Content-Type'])
                self.end_headers()
                self.wfile.write(response.content)
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"404 Not Found")
        except Exception as e:
            logging.error(f"Ошибка при обработке запроса: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"500 Internal Server Error")

def run(server_class=http.server.HTTPServer, handler_class=Proxy):
    logging.info(f"Запуск прокси-сервера на порту {PORT}...")
    try:
        with server_class(("", PORT), handler_class) as httpd:
            logging.info("Прокси-сервер успешно запущен.")
            httpd.serve_forever()
    except Exception as e:
        logging.error(f"Ошибка при запуске сервера: {e}")

if __name__ == "__main__":
    logging.info("Настройка прокси...")
    set_proxy(PROXY_HOST)  # Установить прокси перед запуском сервера
    run()
