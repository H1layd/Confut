import requests
import subprocess
import sys

def check_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"{url} доступен.")
        else:
            print(f"{url} недоступен. Статус код: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"{url} недоступен. Ошибка: {e} если вы проверяите после обхода то это нормально")

websites = {
    "YouTube": "https://www.youtube.com",
    "Discord": "https://discord.com",
}

for name, url in websites.items():
    print(f"Проверка {name}...")
    check_website(url)

input("Нажмите Enter, чтобы вернуться в другой файл...")

subprocess.run(["python", "main.py"])


sys.exit()