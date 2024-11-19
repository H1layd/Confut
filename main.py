from banner import banner
from pystyle import *
import os


COLOR_CODE = {
    "RESET": "\033[0m",  
    "UNDERLINE": "\033[04m", 
    "GREEN": "\033[32m",     
    "YELLOW": "\033[93m",    
    "RED": "\033[31m",       
    "CYAN": "\033[36m",     
    "BOLD": "\033[01m",        
    "PINK": "\033[95m",
    "URL_L": "\033[36m",       
    "LI_G": "\033[92m",      
    "F_CL": "\033[0m",
    "DARK": "\033[90m",     
}

print(Colorate.Horizontal(Colors.black_to_white, Center.XCenter(banner)))
select = input(f'{COLOR_CODE["DARK"]}[+]{COLOR_CODE["BOLD"]} Выбрать >{COLOR_CODE["GREEN"]} ')
if select == '1':
    from vpnc import check_vpn 
    check_vpn()  
elif select == '2':
    from url import check_website, url
    check_website(url)
elif select == '3':
    from ip import get_user_ip
    get_user_ip()
elif select == '4':
    from proxy import proxyServer
    proxyServer()
elif select == '5':
    exit    