from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
try:
    import tkinter as tk #python3
except ImportError:
    import Tkinter as tk #python2

def send_message(event=None):  # event is passed by binders.

    msg = login.get()
    login.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        sel.quit()


def receive_message():
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf8")
            chat_list.insert(tk.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    login.set("{quit}")
    send_message()


def choose_chat(event=None):  # event is passed by binders.
    send_message()
    registration.destroy()
    

def chatting(event=None):  # event is passed by binders.
    receive_message()
    #name = client_socket.recv(1024).decode("utf8")
    #chat_list.insert(tk.END, name)


client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('localhost', 80))



registration = tk.Tk() 
registration.title("Simple Messenger")
label1 = tk.Label(registration, text = "Welcome to Simple Messenger!         ",  bg = "lightgreen", font = 'arial 15')
label1.pack(side = tk.TOP, anchor = tk.W)
label2 = tk.Label(registration, text = "Please introduce yourself ", bg = "white", width = 300, height = 4, font='arial 12')
label2.pack()
login = tk.StringVar()
entry_field = tk.Entry(registration, textvariable=login, width=56)
entry_field.pack(side = tk.LEFT)
entry_field.bind("<Return>", choose_chat)
registration.geometry("340x150")
registration.mainloop()
sel = tk.Tk() #selection
sel.title("Simple Messenger")
sel.geometry("340x150")
label3 = tk.Label(sel, text = " Please choose somebody to chat        ",  bg = "lightgreen", font = 'arial 15')
label3.pack( anchor = tk.NW)
chat_frame = tk.Frame(sel)
chat_list = tk.Listbox(chat_frame, height=6, width=50)


#chat_list.bind('<<ListboxSelect>>', chatting)
chat_list.pack(side=tk.LEFT, fill=tk.BOTH)
chat_list.pack()
chat_frame.pack()
sel.mainloop()

sel.protocol("WM_DELETE_WINDOW", on_closing) 

receive_thread = Thread(target=receive_message)
receive_thread.start()
