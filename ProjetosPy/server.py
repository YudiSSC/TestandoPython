import os
import subprocess
import sys
import socket
import cv2
import numpy as np
import pyautogui
import struct

def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

required_packages = ['opencv-python', 'numpy', 'pyautogui']
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        install(package)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  
        ip = s.getsockname()[0]      
    finally:
        s.close()
    return ip

SERVER_IP = get_local_ip()
SERVER_PORT = 9999

print(f"Transmissão iniciada em {SERVER_IP}:{SERVER_PORT}")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)

print("Aguardando conexão...")

conn, addr = server_socket.accept()
print(f"Conectado a: {addr}")

conn.sendall(SERVER_IP.encode('utf-8'))

try:
    while True:

        screenshot = pyautogui.screenshot()

        frame = np.array(screenshot)
        

        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        _, buffer = cv2.imencode('.jpg', frame)

        data = buffer.tobytes()

        conn.sendall(struct.pack("!I", len(data)) + data)
except Exception as e:
    print(f"Erro durante a transmissão: {e}")
finally:
    conn.close()
    server_socket.close()
    print("Conexão fechada.")
