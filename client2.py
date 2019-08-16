from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
try:
    import tkinter as tk #python3
except ImportError:
    import Tkinter as tk #python2

def send_message(event=None):  # event is passed by binders.

    msg = txt.get()
    txt.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{quit}":
        client_socket.close()
        main.quit()


def receive_message():
    while True:
        try:
            msg = client_socket.recv(1024).decode("utf8")
            chat_list.insert(tk.END, msg+'\n')
        except OSError:  # Possibly client has left the chat.
            break    


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    #txt.set("{quit}")
    #send_message()
    msg = "{quit}"
    client_socket.send(bytes(msg, "utf8"))
    client_socket.close()
    main.quit()
    

def update_chat_list():
    while True:
        try:
            
            msg = client_socket.recv(1024).decode("utf8")
            chat_list.delete(0, tk.END)
            msg_buf=""
            for i in msg:
                if i != "*":
                    msg_buf = msg_buf + i
                else:
                    chat_list.insert(tk.END, msg_buf)
                    msg_buf=""
    
        except OSError:  # Possibly client has left the chat.
            break
    
 

def registration(event=None):  # event is passed by binders.
    """Function to introduce yourself"""
    name = txt.get()
    client_socket.send(bytes(name, "utf8"))
    label1.destroy()
    label2.destroy()
    entry_field.destroy()

def chatting(event=None):
    print("LOL")


main = tk.Tk() 
main.title("Simple Messenger")

label1 = tk.Label(main, text = "Welcome to Simple Messenger!         ",  bg = "lightgreen", font = 'arial 15')
label1.pack(side = tk.TOP, anchor = tk.W)

label2 = tk.Label(main, text = "Please introduce yourself ", bg = "white", width = 300, height = 7, font='arial 12')
label2.pack()

txt = tk.StringVar()
entry_field = tk.Entry(main, textvariable=txt, width=56)

entry_field.bind("<Return>", registration)
entry_field.pack(side = tk.LEFT)
main.geometry("340x210")


label3 = tk.Label(main, text = " Please choose somebody to chat        ",  bg = "lightgreen", font = 'arial 15')
label3.pack(anchor = tk.NW)
chat_frame = tk.Frame(main)
scrollbar = tk.Scrollbar(chat_frame)
chat_list = tk.Listbox(chat_frame, height=10, width=50, yscrollcommand=scrollbar.set)
chat_list.pack(side=tk.LEFT, fill=tk.BOTH)
chat_list.pack()
chat_list.bind('<Double-Button-1>', chatting)
chat_frame.pack()
scrollbar.pack(side=tk.RIGHT, fill=tk.Y) 

#update_chat_list()

main.protocol("WM_DELETE_WINDOW", on_closing) 

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('localhost', 80))

receive_thread = Thread(target=update_chat_list)
receive_thread.start()
main.mainloop()