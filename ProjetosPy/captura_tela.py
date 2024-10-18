import socket
import cv2
import numpy as np
import pyautogui


hostname = socket.gethostname()
server_ip = socket.gethostbyname(hostname)
port = 12345


print(f"Servidor rodando no IP: {server_ip}")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_ip, port))
server_socket.listen(1)

print("Aguardando conexão...")
client_socket, addr = server_socket.accept()
print(f"Conexão estabelecida com {addr}")

try:
    while True:

        screenshot = pyautogui.screenshot()

    
        frame = np.array(screenshot)

      
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

      
        _, encoded_frame = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

        frame_size = len(encoded_frame)
        client_socket.sendall(frame_size.to_bytes(4, byteorder='big'))  
        client_socket.sendall(encoded_frame) 

except Exception as e:
    print(f"Erro: {e}")

finally:
    client_socket.close()
    server_socket.close()
