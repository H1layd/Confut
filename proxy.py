import socket
import threading
import requests
import logging
import subprocess

proxy_host = 'localhost:8080' 
proxy_enabled = True  

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def set_proxy():

    if proxy_enabled:
        command_enable = f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f'
        result_enable = subprocess.run(command_enable, shell=True, capture_output=True)
        
        command_server = f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyServer /t REG_SZ /d {proxy_host} /f'
        result_server = subprocess.run(command_server, shell=True, capture_output=True)
        
        if result_enable.returncode == 0 and result_server.returncode == 0:
            logging.info(f"Настройки прокси обновлены: {proxy_host}")
        else:
            logging.error(f"Ошибка при обновлении настроек прокси: {result_enable.stderr.decode().strip()} {result_server.stderr.decode().strip()}")
    else:

        command_disable = f'reg add "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Internet Settings" /v ProxyEnable /t REG_DWORD /d 0 /f'
        result_disable = subprocess.run(command_disable, shell=True, capture_output=True)
        
        if result_disable.returncode == 0:
            logging.info("Настройки прокси отключены.")
        else:
            logging.error(f"Ошибка при отключении прокси: {result_disable.stderr.decode().strip()}")

def proxyServer():
    port = 8080
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(5)

    logging.info(f"Прокси-сервер запущен на порту {port}")

    def handle_request(client_socket):
        try:
            request = client_socket.recv(4096)
            request = request.decode('utf-8', errors='replace')
        except Exception as e:
            logging.error(f"Ошибка при получении запроса: {e}")
            client_socket.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            client_socket.close()
            return

        if request:
            logging.debug(f"Запрос: {request}")

        lines = request.splitlines()
        if len(lines) > 0:
            first_line = lines[0].split()
            if len(first_line) > 1:
                url = first_line[1]

                if not url.startswith(('http://', 'https://')):
                    url = 'http://' + url  

                try:
                    headers = {
                        'User -Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    }
                    
                    logging.info(f"Получение URL: {url}")
                    response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
                    logging.info(f"Код статуса ответа: {response.status_code}")
                    client_socket.sendall(f"HTTP/1.1 {response.status_code} OK\r\nContent-Length: {len(response.content)}\r\nCache-Control: no-cache\r\n\r\n".encode('utf-8'))
                    client_socket.sendall(response.content)
                except Exception as e:
                    logging.error(f"Ошибка при получении {url}: {e}")
                    client_socket.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
            else:
                client_socket.sendall(b"HTTP/1.1 403 Forbidden\r\n\r\n")
        client_socket.close()

    try:
        while True:
            client_socket, address = server_socket.accept()
            threading.Thread(target=handle_request, args=(client_socket,)).start()
    except KeyboardInterrupt:
        logging.info("Завершение работы прокси-сервера...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    set_proxy()
    proxyServer()
