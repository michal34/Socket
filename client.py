import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 7321))

connected = client.recv(2048).decode()
print(connected)
first = client.recv(2048).decode()
print(first)

while True:
    
    message = str(input('Send message: '))
    message += 'END_LINE'
    client.send(message.encode())
    
    data = b''
    data += client.recv(4096)
    while b'END_LINE' not in data:
        data += client.recv(100)
        
    data = data.decode()
    data = data.split(' END_LINE')
    data = data[0]
    print(data)
    
    if data == 'End_connection':
        break
        
client.close()
