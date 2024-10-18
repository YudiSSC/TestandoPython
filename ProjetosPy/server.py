import os
import subprocess
import sys
import socket
import cv2
import numpy as np
import pyautogui
import struct

# Função para instalar pacotes ausentes
def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# Verificar e instalar pacotes necessários
required_packages = ['opencv-python', 'numpy', 'pyautogui']
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        install(package)

# Obter o IP local da máquina
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # Conectar a um IP externo (Google DNS) para obter o IP local
        ip = s.getsockname()[0]      # Capturar o IP local
    finally:
        s.close()
    return ip

# Configuração do servidor
SERVER_IP = get_local_ip()
SERVER_PORT = 9999

print(f"Transmissão iniciada em {SERVER_IP}:{SERVER_PORT}")

# Configurar o socket do servidor
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, SERVER_PORT))
server_socket.listen(1)

print("Aguardando conexão...")

# Aceitar conexão de um cliente
conn, addr = server_socket.accept()
print(f"Conectado a: {addr}")

# Enviar IP ao cliente conectado
conn.sendall(SERVER_IP.encode('utf-8'))

try:
    while True:
        # Capturar a tela usando pyautogui
        screenshot = pyautogui.screenshot()
        
        # Converter a imagem PIL para um array NumPy
        frame = np.array(screenshot)
        
        # Convertendo o formato de cores RGB para BGR (compatível com OpenCV)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        # Codificar a imagem em formato JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        
        # Converter para bytes
        data = buffer.tobytes()
        
        # Enviar o tamanho do pacote e a imagem codificada
        conn.sendall(struct.pack("!I", len(data)) + data)
except Exception as e:
    print(f"Erro durante a transmissão: {e}")
finally:
    # Fechar conexões e liberar recursos
    conn.close()
    server_socket.close()
    print("Conexão fechada.")
