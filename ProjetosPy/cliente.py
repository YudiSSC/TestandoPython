import socket
import numpy as np
import cv2
import struct


CLIENT_PORT = 9999
SERVER_IP = '127.0.0.1' 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP, CLIENT_PORT))

server_ip = client_socket.recv(1024).decode('utf-8')
print(f"Conectado ao servidor em {server_ip}:{CLIENT_PORT}")

while True:

    data = b''
    while len(data) < struct.calcsize("!I"):
        packet = client_socket.recv(4 * 1024) 
        if not packet: 
            break
        data += packet
    
    if not data:  
        break
    

    frame_size = struct.unpack("!I", data[:struct.calcsize("!I")])[0]
    

    data = b''
    while len(data) < frame_size:
        packet = client_socket.recv(4 * 1024)
        if not packet:
            break
        data += packet


    frame = np.frombuffer(data, dtype=np.uint8)
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)


    cv2.imshow("Transmissão ao Vivo", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

client_socket.close()
cv2.destroyAllWindows()
