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
            msg_list.insert(tk.END, msg)
        except OSError:  # Possibly client has left the chat.
            break


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    login.set("{quit}")
    send_message()


def choose_chat(event=None):  # event is passed by binders.
    send_message()
    registration.destroy()
    sel = tk.Tk() #selection
    sel.title("Simple Messenger")
    sel.geometry("340x150")
    label3 = tk.Label(sel, text = " Please choose somebody to chat        ",  bg = "lightgreen", font = 'arial 15')
    label3.pack( anchor = tk.NW)
    chat_frame = tk.Frame(sel)
    chat_list = tk.Listbox(chat_frame, height=6, width=50, selectmode=SINGLE)
    chat_list.pack(side=tk.LEFT, fill=tk.BOTH)
    chat_frame.pack()

    chat_list.bind('<<ListboxSelect>>', chatting)
    sel.mainloop()

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



'''

main = tk.Tk()
main.title("Messenger")

tk.Label(main, text="select")

messages_frame = tk.Frame(main)
login = tk.StringVar()  # For the messages to be sent.
login.set("Type your messages here.")
scrollbar = tk.Scrollbar(messages_frame)  # To navigate through past messages.
# Following will contain the messages.
msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
msg_list.pack()
messages_frame.pack()

entry_field = tk.Entry(main, textvariable=login)
entry_field.bind("<Return>", send_message)
entry_field.pack()
send_button = tk.Button(main, text="Send", command=send_message)
send_button.pack()

main.protocol("WM_DELETE_WINDOW", on_closing)
tk.mainloop()
'''
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('localhost', 80))

receive_thread = Thread(target=receive_message)
receive_thread.start()
