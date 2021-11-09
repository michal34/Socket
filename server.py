import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 7321))
server.listen(5)

commands =  ['Login', 'End_connection', 'Help']
data = {'michal' :'haslo123', 'adam': 'tak12'}

while True:
    client, address = server.accept()
    client.send('Connected\r\n'.encode())
    client.send(f'Avaible commands: {commands}'.encode())
    
    while True:
        message = client.recv(2048).decode()
        print(message)
        
        if not message:
            break
    
        if message not in commands:
            client.send(b"Wrong command, type: 'Help'")
    
        if message == 'Help':
            client.send(f'Avaible commands: {commands}'.encode())
            
        if message == 'End_connection':
            client.send(b'End_connection')

        if message == 'Login':
            client.send(b'Enter login: ')
            login = client.recv(2048).decode()
            client.send(b'Enter password: ')
            password = client.recv(2048).decode()

            if login in data:
                if data[f'{login}'] == f'{password}':
                    client.send(f'Hello {login}\r\nYou logged in\r\n'.encode('utf-8'))
                    
                else:
                    client.send(b'Invalid login or password\r\n')
                    
            else:
                    client.send(b'Invalid login or password\r\n')
