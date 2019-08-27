from socket import socket, AF_INET, SOCK_STREAM 
from threading import Thread 
import tkinter as tk 

def send_message(event=None): # event is passed by binders. 
    msg = my_msg.get() 
    my_msg.set("") # Clears input field. 
    client_socket.send(bytes(msg, "utf8")) 
    if msg == "{quit}": 
        client_socket.close() 
        main.quit() 


def receive_message(): 
    while True: 
        try: 
            msg = client_socket.recv(1024).decode("utf8") 
            msg_list.insert(tk.END, msg) 
        except OSError: # Possibly client has left the chat. 
            break 


def on_closing(event=None): 
    """This function is to be called when the window is closed.""" 
    my_msg.set("{quit}") 
    send_message() 


main = tk.Tk() 
main.title("Messenger") 

tk.Label(main, text="select") 

messages_frame = tk.Frame(main) 
my_msg = tk.StringVar() # For the messages to be sent. 
my_msg.set("Type your messages here.") 
scrollbar = tk.Scrollbar(messages_frame) # To navigate through past messages. 
# Following will contain the messages. 
msg_list = tk.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set) 
scrollbar.pack(side=tk.RIGHT, fill=tk.Y) 
msg_list.pack(side=tk.LEFT, fill=tk.BOTH) 
msg_list.pack() 
messages_frame.pack() 

entry_field = tk.Entry(main, textvariable=my_msg) 
entry_field.bind("<Return>", send_message) 
entry_field.pack() 
send_button = tk.Button(main, text="Send", command=send_message) 
send_button.pack() 

main.protocol("WM_DELETE_WINDOW", on_closing) 

client_socket = socket(AF_INET, SOCK_STREAM) 
client_socket.connect(('localhost', 80)) 

receive_thread = Thread(target=receive_message) 
receive_thread.start() 
tk.mainloop()
