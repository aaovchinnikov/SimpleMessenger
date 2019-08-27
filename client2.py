from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread
try:
    import tkinter as tk #python3
except ImportError:
    import Tkinter as tk #python2

def send_message(event=None):  # event is passed by binders.

    msg = txt1.get()
    msg1 = name + ": " + msg
    chat_field.insert(tk.END, msg1)
    msg = friend + "$" + msg
    txt1.set("")  # Clears input field.
    client_socket.send(bytes(msg, "utf8"))


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    msg = "{quit}"
    client_socket.send(bytes(msg, "utf8"))
    client_socket.close()
    main.quit()
    
def on_closing_chat(event=None):
    global dialog
    chat.withdraw()
    dialog=0    

def receive_message():
    global dialog
    global friend
    global name
    while True:
        try:
            
            msg = client_socket.recv(1024).decode("utf8")
            if msg[0]=="$": #message for chatting
                friend1 = friend
                magia=msg[1:].split("$")
                msg=magia[2]
                if magia[0]==name:
                    friend = magia[1]
                else:
                    friend = magia[0]           
                msg = friend + ": " + msg    
                

                if dialog == 0: 
                    chat.deiconify()
                    label4['text'] = friend
                    dialog = 1
                if friend1 != friend:
                    label4['text'] = friend
                    chat_field.delete(0, tk.END)

                chat_field.insert(tk.END, msg)
            else: #updating chat list
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
    global name
    name = txt.get()

    if name != "":
        client_socket.send(bytes(name, "utf8"))
        label1.destroy()
        label2.destroy()
        entry_field.destroy()
    else:
        label2['text'] = "Name is null, enter your name"



def chatting(event=None):
    global friend
    friend1 = friend
    w = event.widget
    i = int(w.curselection()[0])
    friend = w.get(i)
    global dialog
    
    dialog = 1
    chat.deiconify()
    label4['text'] = friend
    if friend1 != friend:
        chat_field.delete(0, tk.END)
    
name=""
main = tk.Tk() 
main.title("Simple Messenger")

label1 = tk.Label(main, text = "Welcome to Simple Messenger!", bg = "lightgreen", font = 'arial 15', width = 340, anchor = tk.W)
label1.pack(side = tk.TOP)

label2 = tk.Label(main, text = "Please introduce yourself ", bg = "white", width = 300, height = 7, font='arial 12')
label2.pack()

txt = tk.StringVar()
entry_field = tk.Entry(main, textvariable=txt, width=56)

entry_field.bind("<Return>", registration)
entry_field.pack(side = tk.LEFT)
main.geometry("340x210")


label3 = tk.Label(main, text = "Please choose somebody to chat",  bg = "lightgreen", font = 'arial 15', width = 340, anchor = tk.W)
label3.pack(anchor = tk.NW)
chat_frame = tk.Frame(main)
scrollbar = tk.Scrollbar(chat_frame)
chat_list = tk.Listbox(chat_frame, height=10, width=50, yscrollcommand=scrollbar.set)
chat_list.pack(side=tk.LEFT, fill=tk.BOTH)
chat_list.pack()

txt1 = tk.StringVar()
dialog = 0 # flag 
friend = ""
chat_list.bind('<Double-Button-1>', chatting)
chat_frame.pack()
scrollbar.pack(side=tk.RIGHT, fill=tk.Y) 

#dialog
chat = tk.Toplevel(main)
label4 = tk.Label(chat, text = friend, bg = "lightgreen", font = 'arial 14', width = 340)
label4.pack(side = tk.TOP)
chat_frame1 = tk.Frame(chat)
chat_frame1.pack()
chat.geometry("340x220")
scrollbar1 = tk.Scrollbar(chat_frame1)

chat_field = tk.Listbox(chat_frame1, height=10, width=50, yscrollcommand=scrollbar1.set)
chat_field.pack(side=tk.LEFT, fill=tk.BOTH)
chat_field.pack()
scrollbar1.pack(side=tk.RIGHT, fill=tk.Y) 
entry_field1 = tk.Entry(chat, textvariable=txt1, width=56)

entry_field1.bind("<Return>", send_message)
entry_field1.pack(side = tk.BOTTOM)

chat.withdraw()

chat.protocol("WM_DELETE_WINDOW", on_closing_chat)
main.protocol("WM_DELETE_WINDOW", on_closing) 

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('localhost', 80))

receive_thread = Thread(target=receive_message)
receive_thread.start()
main.mainloop()
