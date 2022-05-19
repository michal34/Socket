import socket
from _thread import *
from common import *
import uuid

users = {'adam': 'tak', 'michal':'haslo'}

auth_users = []

messages = []
lista = []

def server_client(client):
    data = ''
    while 'QUIT' not in data:
        data = get_data(client)
        print(data,'\r\n')
        
        if 'LOGIN' in data:
            params = data.split("\r\n")
            
            if params[1] in users and users[params[1]] == params[2]:
                session_id = uuid.uuid4().hex
                auth_users.append(session_id)
                send_response(client, 200, session_id)
            else:
                send_response(client, 400, "User or pass is wrong!")
                
        elif 'rejestracja' in data:
            params = data.split("\r\n")
            if params[1] in users:
                send_data(client, 'nazwa uzytkowika jest juz zajeta')
            else:
                users[params[1]] = params[2]
                send_data(client, 'Udalo sie zarejestrowac')
            print(users)
            
        elif 'wiadomosc' in data:
            session_id = check_session_id(data)
            params = data.split("\r\n")
            
            if session_id == False or session_id not in auth_users:
                send_response(client, 500, "Please log in.")
            
            elif params[1] == params[2] == '' or params[1] not in users:
                    send_response(client, 400, "User doesnt exist")
            
            else:
                messages.append( ( params[1], params[2], params[4]) )
                send_response(client, 200, "Wysłane")
                print(messages)
                
        elif 'sprawdz odebrane' in data:
            
            if messages != []:
                tab = []
                login = data.split(', ')[1]
                for i in messages:
                    if i[0] == login:
                        tab.append(i[2] + " --> " + i[0] + ": " + i[1])
            
                if tab != []:
                    send_response(client, 200, "dziala")
                    tab_length = len(tab)
                    send_data(client, str(tab_length))
        
                    for i in range(0, tab_length):
                        send_data(client, tab[i])
                        print(tab[i])
                else:
                    send_response(client, 301, 'Nie masz zadnyh wiadomosci')
                    
            else:
                send_response(client, 301, 'Chat jest pusty')
                
        elif 'sprawdz wyslane' in data:
            if messages != []:
                tab = []
                login = data.split(', ')[1]
                for i in messages:
                    if i[2] == login:
                        tab.append(i[2] + " --> " + i[0] + ": " + i[1])
            
                if tab != []:
                    send_response(client, 200, "dziala")
                    tab_length = len(tab)
                    send_data(client, str(tab_length))
        
                    for i in range(0, tab_length):
                        send_data(client, tab[i])
                        print(tab[i])
                else:
                    send_response(client, 301, 'Nie wyslales jeszcze zadnych wiadmosci')
                    
            else:
                send_response(client, 301, 'Chat jest pusty')
                
        elif 'wyczysc chat' in data:
            print('czyszczenie chatu')
            if messages == []:
                send_data(client, 'chat jest wyczyszczony')
            else:
                send_data(client, 'z kim chcesz wyczyscic chat')
                data = get_data(client).split(',')
                do_kogo = data[0]
                od_kogo = data[1]
                cos = 0
                for i in messages:
                    if i[0] == do_kogo and i[2] == od_kogo:
                        del messages[cos]
                    cos += 1
                
                print(messages)
            
    client.close()

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(ip_connection)
    s.listen(5)
    try:
        while True:
            client, addr = s.accept()
            print("CONNECTED WITH ", addr[0])
            start_new_thread(server_client, (client, ))
    except KeyboardInterrupt:
        s.close()
