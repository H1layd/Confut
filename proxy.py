import socket
import threading
import requests
import logging
import subprocess
proxy_start = r"start_proxy.bat"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def proxyServer():
    port = 8080
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(5)

    logging.info(f"Proxy server started on port {port}")

    subprocess.run([proxy_start], shell=True)

    def handle_request(client_socket):
        try:
            request = client_socket.recv(4096)
            request = request.decode('utf-8', errors='replace')
        except Exception as e:
            logging.error(f"Error receiving request: {e}")
            client_socket.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
            client_socket.close()
            return

        if request:
            logging.debug(f"Request: {request}")

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
                    
                    response = requests.get(url, headers=headers, allow_redirects=True)
                    logging.info(f"Response status code: {response.status_code}")
                    client_socket.sendall(f"HTTP/1.1 {response.status_code} OK\r\nContent-Length: {len(response.content)}\r\nCache-Control: no-cache\r\n\r\n".encode('utf-8'))
                    client_socket.sendall(response.content)
                except Exception as e:
                    logging.error(f"Error fetching {url}: {e}")
                    client_socket.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
            else:
                client_socket.sendall(b"HTTP/1.1 403 Forbidden\r\n\r\n")
        client_socket.close()

    try:
        while True:
            client_socket, address = server_socket.accept()
            threading.Thread(target=handle_request, args=(client_socket,)).start()
    except KeyboardInterrupt:
        logging.info("Shutting down the proxy server...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    proxyServer()