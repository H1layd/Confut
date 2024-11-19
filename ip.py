import requests
import subprocess

def get_user_ip():
    try:
        response = requests.get('https://api.ipify.org?format=json')
        ip_info = response.json()
        print(f"Ваш IP-адрес: {ip_info['ip']}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


    input("\nНажмите Enter, чтобы вернутся...")


    subprocess.run(['python', 'main.py'])