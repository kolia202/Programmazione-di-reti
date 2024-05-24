#!/usr/bin/env python3

#NOME: NIKOLAI
#COGNOME: ZANNI
#MATRICOLA: 0001069041

"""Script Python per la realizzazione di un Server multithread
per connessioni CHAT asincrone, deve essere in grado di gestire più 
client contemporaneamente e deve consentire agli utenti di inviare 
e ricevere messaggi in una chatroom condivisa"""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import sys
import signal

def add(connections_count, MAX_CONNECTIONS):
    if connections_count == MAX_CONNECTIONS:
        choice = input("Hai raggiunto il numero massimo di connessioni. Vuoi aggiungerne altre? (s/n): ")
        if choice.lower() == 's':
            additional_connections = int(input("Quante connessioni aggiuntive vuoi aprire? "))
            MAX_CONNECTIONS += additional_connections
            SERVER.listen(MAX_CONNECTIONS) 
            print("Numero nuovo di client in attesa massimo: ", MAX_CONNECTIONS)
            while connections_count < MAX_CONNECTIONS:
                try:
                    client, client_address = SERVER.accept()
                    print(f"{client_address[0]}:{client_address[1]} si è collegato.")
                    client.send(bytes("Digita il tuo Nome seguito dal tasto invio per iniziare!", "utf8"))
                    addresses[client] = client_address
                    Thread(target=handle_client, args=(client,)).start()
                    connections_count += 1
                    print("puoi aprire massimo altri", MAX_CONNECTIONS - connections_count, "client")
                except Exception as e:
                    print("Errore durante l'accettazione di una connessione: ", e)
                    break
            else:
                add(connections_count, MAX_CONNECTIONS)
        else:
            print("Numero massimo di connessioni raggiunto")
            print("Chiusura del server...")
            SERVER.close()
            sys.exit(0)

def accept_incoming_connections():
    connections_count = 0
    max_connections_input = input("Inserisci il numero massimo di connessioni da gestire in contemporanea (premi Invio per default 5): ")
    MAX_CONNECTIONS = int(max_connections_input) if max_connections_input else 5
    SERVER.listen(MAX_CONNECTIONS) 
    print("Numero di client in attesa massimo: ", MAX_CONNECTIONS)
    print("In attesa di connessioni...")
    while connections_count < MAX_CONNECTIONS:
        try:
            client, client_address = SERVER.accept()
            print(f"{client_address[0]}:{client_address[1]} si è collegato.")
            client.send(bytes("Digita il tuo Nome seguito dal tasto invio per iniziare!", "utf8"))
            addresses[client] = client_address
            Thread(target=handle_client, args=(client,)).start()
            connections_count += 1
            print("puoi aprire massimo altri", MAX_CONNECTIONS - connections_count, "client")
        except Exception as e:
            print("Errore durante l'accettazione di una connessione: ", e)
            break
    else:
        print("Numero massimo di connessioni raggiunto")
        add(connections_count, MAX_CONNECTIONS)


def handle_client(client):
    name = client.recv(1024).decode("utf8")
    welcome = f"Benvenuto {name}! Se vuoi lasciare la chat, scrivi {{quit}} per uscire."
    client.send(bytes(welcome, "utf8"))
    msg = f"{name} si è unito alla chat!"
    broadcast(bytes(msg, "utf8"))
    clients[client] = name
    while True:
        try:
            msg = client.recv(1024)
            if msg == bytes("{quit}", "utf8"):
                del clients[client]
                broadcast(bytes(f"{name} ha abbandonato la chat!", "utf8"))
                client.close()
                break
            else:
                broadcast(msg, name+": ")
        except ConnectionResetError:
            del clients[client]
            broadcast(bytes(f"{name} ha abbandonato la chat!", "utf8"))
            client.close()
            break

def broadcast(msg, prefix=""):
    for client in clients:
        client.send(bytes(prefix, "utf8")+msg)

clients = {}
addresses = {}
HOST = ''
PORT = 53000
ADDR = (HOST, PORT)
SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

def sigint_handler(sig, frame):
    print('Chiusura del server...')
    SERVER.close()
    sys.exit(0)

if __name__ == "__main__":
    try:
        signal.signal(signal.SIGINT, sigint_handler)
        SERVER.listen(5) 
        print("avvio server sulla porta di default 53000")
        accept_incoming_connections()
    except Exception as e:
        print("Errore durante l'avvio del server: ", e)
    finally:
        SERVER.close()