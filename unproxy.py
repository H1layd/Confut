import logging
import winreg as reg

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def disable_proxy():
    logging.info("Попытка отключить прокси...")
    try:
        key = reg.OpenKey(reg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Internet Settings", 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(key, "ProxyEnable", 0, reg.REG_DWORD, 0)  
        reg.SetValueEx(key, "ProxyServer", 0, reg.REG_SZ, "")  
        reg.CloseKey(key)
        logging.info("Прокси отключен и настройки восстановлены.")
    except Exception as e:
        logging.error(f"Ошибка при отключении прокси: {e}")

if __name__ == "__main__":
    disable_proxy()