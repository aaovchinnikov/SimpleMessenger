try:
    import tkinter as tk #python3
except ImportError:
    import Tkinter as tk #python2

def choose_chat(event=None):  # event is passed by binders.
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
login.set("")
entry_field = tk.Entry(registration, textvariable=login, width=45)
#entry_field.bind("<Return>", send_message)
entry_field.pack(side = tk.LEFT)
accept_button = tk.Button(registration, text="Accept", width=10, command=choose_chat)
accept_button.pack(side = tk.RIGHT)
registration.geometry("340x150")
registration.mainloop()
