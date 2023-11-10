import os
try:
    import requests
except ImportError:
    os.system('pip install requests')

THREADS = 500
PORTS = [80, 443]

from threading import Thread, active_count
from concurrent import futures
from os import system, name
from requests import get, exceptions

def get_public_ip():
    try:
        return get('https://api.ipify.org').text
    except exceptions.RequestException:
        return 'Unable to retrieve the public IP.'

PUBLIC_IP = get_public_ip()

def check_target(ip_address, port):
    try:
        response = get(f'http://{ip_address}:{port}', timeout=5)
        if response.status_code == 200:
            print(f'[{PUBLIC_IP}] Target {ip_address}:{port} is accessible.')
    except exceptions.RequestException:
        pass

def scan_ports(targets, protocol):
    with futures.ThreadPoolExecutor(max_workers=THREADS) as executor:
        future_to_ip = {executor.submit(check_target, target, port): target for target in targets for port in PORTS}
        for future in futures.as_completed(future_to_ip):
            ip = future_to_ip[future]
            try:
                future.result()
            except exceptions.RequestException:
                pass

def main():
    targets = get('https://t.me/{@D_T_T_Bot}', params={'limit': 5, 'offset': 0}).json()['result']
    scan_ports(targets, 'http')

if __name__ == '__main__':
    main()
