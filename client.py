import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 7321))

connected = client.recv(2048).decode()
print(connected)
first = client.recv(2048).decode()
print(first)

while True:
    
    message = input('Send message: ')
    client.send(message.encode())
    server_message = client.recv(4096).decode()
    print(server_message)
    
    if server_message == 'End_connection':
        break
        
client.close()
