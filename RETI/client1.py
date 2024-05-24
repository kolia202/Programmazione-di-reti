#!/usr/bin/env python3

#NOME: NIKOLAI
#COGNOME: ZANNI
#MATRICOLA: 0001069041

"""Script relativa alla chat del client utilizzato per lanciare la GUI Tkinter, 
deve consentire agli utenti di connettersi al server, inviare messaggi alla chatroom 
e ricevere messaggi dagli altri utenti."""

from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt
from datetime import datetime

def receive():
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf8")
            msg_list.insert(tkt.END, msg)
            msg_list.see(tkt.END)
        except Exception as e:
            print("Errore durante la ricezione del messaggio: ", e)
            break

def close_connection():
    try:
        finestra.destroy()
    except tkt.TclError:
        pass
    try:
        client_socket.close()
    except:
        pass
    finally:
        finestra.quit()

def on_closing(event=None):
    my_msg.set("{quit}")
    send()

def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    try:
        if msg == "{quit}":
            client_socket.send(bytes(msg, "utf8"))
            close_connection()
        else:
            client_socket.send(bytes(msg, "utf8"))
    except ConnectionResetError:
        close_connection()

def start_chat():
    global client_socket, finestra, msg_list, my_msg
    default_host = 'localhost'
    HOST = input('Inserire il Server host (invio per host di default {default_host}): ') or default_host
    PORT = input('Inserire la porta del server host (invio per la porta di default [53000]): ')
    if not PORT: 
        PORT = 53000
    else:
        PORT = int(PORT)

    ADDR = (HOST, PORT)
    client_socket = socket(AF_INET, SOCK_STREAM)
    try:
        client_socket.connect(ADDR)
    except Exception as e:
        print("Errore durante la connessione al server: ", e)
        return
    
    finestra = tkt.Tk()
    finestra.title("Chatroom Condivisa")
    finestra.geometry("500x600")
    finestra.configure(bg="#ECE5DD")
    status_frame = tkt.Frame(finestra, bg="#075E54", height=50)
    status_frame.pack(fill=tkt.X)
    status_label = tkt.Label(status_frame, text="Online", bg="#075E54", fg="white", font=("Helvetica", 14, "bold"))
    status_label.pack(side=tkt.LEFT, padx=10)
    messages_frame = tkt.Frame(finestra, bg="#ECE5DD")
    my_msg = tkt.StringVar()
    my_msg.set("")
    scrollbar = tkt.Scrollbar(messages_frame)
    msg_list = tkt.Listbox(messages_frame, height=20, width=60, yscrollcommand=scrollbar.set, bg="#ECE5DD", fg="black", font=("Helvetica", 12), highlightthickness=0, bd=0, selectbackground="#34B7F1", selectforeground="white")
    scrollbar.pack(side=tkt.RIGHT, fill=tkt.Y)
    msg_list.pack(side=tkt.LEFT, fill=tkt.BOTH, expand=True)
    messages_frame.pack(padx=10, pady=10, expand=True, fill=tkt.BOTH)
    entry_frame = tkt.Frame(finestra, bg="#FFFFFF")
    entry_field = tkt.Entry(entry_frame, textvariable=my_msg, font=("Helvetica", 12), bd=0, bg="#F1F0F0", fg="black")
    entry_field.bind("<Return>", send)
    entry_field.pack(padx=10, pady=10, fill=tkt.X, side=tkt.LEFT, expand=True)
    send_button = tkt.Button(entry_frame, text="Invio", command=send, font=("Helvetica", 12, "bold"), bg="#34B7F1", fg="white", bd=0, activebackground="#34B7F1", activeforeground="white")
    send_button.pack(pady=10, side=tkt.RIGHT)
    entry_frame.pack(fill=tkt.X)
    finestra.protocol("WM_DELETE_WINDOW", on_closing)
    receive_thread = Thread(target=receive)
    receive_thread.start()
    tkt.mainloop()

if __name__ == "__main__":
    try:
        start_chat()
    except Exception as e:
        print("Errore durante l'esecuzione del client: ", e)
    finally:
        close_connection()