import os
import platform
import subprocess
import threading
import time
import sys

def loading_animation(stop_event):
    animation = ['|', '/', '-', '\\']
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f'\rПроверка VPN... {animation[idx]}')
        sys.stdout.flush()
        idx = (idx + 1) % len(animation)
        time.sleep(0.1)

def check_vpn():
    os_type = platform.system()
    stop_event = threading.Event()  # Событие для остановки анимации
    loading_thread = threading.Thread(target=loading_animation, args=(stop_event,))
    
    loading_thread.start()  # Запускаем анимацию загрузки

    try:
        # Проверяем VPN в течение 5 секунд
        start_time = time.time()
        while time.time() - start_time < 5:
            if os_type == "Linux" or os_type == "Darwin":  
                result = subprocess.run(['ifconfig'], stdout=subprocess.PIPE, text=True)
                if 'tun' in result.stdout or 'ppp' in result.stdout:
                    print("\nVPN подключен, выключите его")
                    break
                else:
                    print("\nVPN не подключен")
                    break
            elif os_type == "Windows":
                result = subprocess.run(['powershell', '-Command', 'Get-VpnConnection'], stdout=subprocess.PIPE, text=True)
                if result.stdout.strip():
                    print("\nVPN подключен, выключите его")
                    break
                else:
                    print("\nVPN не подключен")
                    break
            else:
                print("\nНеизвестная операционная система")
                break
            
            time.sleep(1)  # Задержка перед следующей проверкой
    except Exception as e:
        print(f"\nОшибка при выполнении команды: {e}")
    finally:
        stop_event.set()  # Останавливаем анимацию
        loading_thread.join()  # Ждем завершения потока анимации

    input("\nНажмите Enter, чтобы вернутся...")

    # Открываем другой Python файл
    subprocess.run(['python', 'main.py'])

