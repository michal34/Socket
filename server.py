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
        
        message = b''
        message = client.recv(2048)
        while b'END_LINE' not in message:
            message += client.recv(100)
            
        message = message.decode()
        message = message.split('END_LINE')
        message = message[0]
        print(message)
        
        if not message:
            break
    
        if message not in commands:
            client.send(b"Wrong command, type: 'Help' END_LINE")
    
        if message == 'Help':
            client.send(f'Avaible commands: {commands} END_LINE'.encode())
            
        if message == 'End_connection':
            client.send(b'End_connection END_LINE')

        if message == 'Login':
            client.send(b'Enter login:  END_LINE')
            login = b''
            login = client.recv(2048)
            while b'END_LINE' not in login:
                login += client.recv(100)
            login = login.decode()
            login = login.split('END_LINE')
            login = login[0]
            
            client.send(b'Enter password:  END_LINE')
            password = b''
            password = client.recv(2048)
            while b'END_LINE' not in password:
                password += client.recv(100)
            password = password.decode()
            password = password.split('END_LINE')
            password = password[0]

            if login in data:
                if data[f'{login}'] == f'{password}':
                    client.send(f'Hello {login}\r\nYou logged in\r\n END_LINE'.encode('utf-8'))
                    
                else:
                    client.send(b'Invalid login or password\r\n END_LINE')
                    
            else:
                    client.send(b'Invalid login or password\r\n END_LINE')
    server.close()
