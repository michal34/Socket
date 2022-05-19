import socket
from common import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ip_connection)

login = None
password = None

while True:
    isAccount = input('Czy masz konto? tak/nie\r\n')
    if isAccount == "tak":
        login = input("Podaj login\n")
        password = input("Podaj haslo\n")
        send_data(s, f"LOGIN\r\n{login}\r\n{password}\r\n\r\n")
        break
    elif isAccount == "nie":
        new_login = input('Musisz się zarejestrować\r\n' + 'Podaj nowy login\r\n')
        new_password = input('Podaj nowe haslo\r\n')
        new_password1 = input('Powtorz nowe haslo\r\n')
        if new_password == new_password1:
            send_data(s, f"rejestracja\r\n{new_login}\r\n{new_password}\r\n\r\n")
            print(get_data(s))
        else:
            print('Hasla roznia sie od siebie')
    else:
        print('Niepoprawnaa odpowiedź')

data = get_data(s)
status_code, status_message, data = get_split_response(data)

session_id = ''
if status_code == 200:
    session_id = data
    print("Zalogowano")

    command = ''
    while command != 'quit':
        command = input("Dostepne komendy: wiadomosc, sprawdz odebrane, sprawdzy wyslane, wyczysc chat, wyjscie - quit\r\n")
        
        if command == "wiadomosc":
            
            send_to = input("Do kogo wyslac wiadomosc\n")
            if send_to != login: 
                message = input("Podaj wiadomosc\n")
                send_data(s, f"wiadomosc\r\n{send_to}\r\n{message}\r\nsession_id:{session_id}\r\n{login}\r\n\r\n")
                data = get_data(s)
                
                status_code, status_message, data = get_split_response(data)
                if status_code != 200:
                    print(status_message, data)
                else:
                    print("Wysłano\r\n")
            else:
                print('Nie mozesz wyslac sobie wiadomosci')
            
        elif command == 'sprawdz odebrane':
            send_data(s, f"{command}, {login}")
            data = get_data(s)
            status_code, status_message, data = get_split_response(data)
            
            if status_code == 200:
                tab = get_data(s)
                tab = float(tab)
                tab = int(tab)
                if "dziala" in data:
                    for i in range(0, tab):
                        tak = get_data(s)
                        print(tak)
            else:
                print(data)
        elif command == 'sprawdz wyslane':
            send_data(s, f'{command}, {login}')
            data = get_data(s)
            status_code, status_message, data = get_split_response(data)
            
            if status_code == 200:
                tab = get_data(s)
                tab = float(tab)
                tab = int(tab)
                if "dziala" in data:
                    for i in range(0, tab):
                        tak = get_data(s)
                        print(tak)
            else:
                print(data)
                
        elif command == "wyczysc chat":
            send_data(s, 'wyczysc chat')
            data = get_data(s)
            if data != 'chat jest wyczyszczony':
                name = input(data + '\r\n')
                send_data(s, name + ',' + login)
            else:
                print(data)
            
        elif command == "quit":
            print('Zamykam połączenie')
            
        else:
            print('Zla komenda')
    send_data(s, 'QUIT')
    
else:
    print("Bład!",status_message, data)

s.close()
