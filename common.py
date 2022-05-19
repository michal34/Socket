import socket

ip_connection = ('localhost', 3030)

def get_data(socket_connection):
    data = b''
    while not b'\r\n\r\n' in data:
        data += socket_connection.recv(10)
    
    data = data.decode('utf-8')
    data = str(data).split('\r\n\r\n')[0]
    return data

def send_data(socket_connection, data):
    socket_connection.sendall((data + '\r\n\r\n').encode('utf-8'))


def send_response(socket_connection, status_code, data):
    code_description = ''

    if status_code == 200:
        code_description = "OK"
    elif status_code == 300:
        code_description = "Wrong command"
    elif status_code == 400:
        code_description = "Wrong params for command"
    elif status_code == 500:
        code_description = "You are not authorised user."
    else:
        code_description = "Something went wrong! Unexpected error."

    socket_connection.sendall((str(status_code) + '\r\n' + code_description +'\r\n' + data + '\r\n\r\n').encode('utf-8'))


def get_split_response(data):
    params = data.split('\r\n')
    return int(params[0]), params[1], params[2]


def check_session_id(data):
    if 'session_id' in data:
        session_id = data.split('session_id:')[1].split('\r\n')[0]
        return session_id
    else:
        return False