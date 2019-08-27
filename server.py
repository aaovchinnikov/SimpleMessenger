from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()
        



def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(1024).decode("utf8")
    if name == "{quit}":
        client.close()
    else:
        clients[client] = name

        while True:
            
            for c in clients:
                if len(clients) == 1:
                    c.send(bytes("Nobody is now available. Please wait...*", "utf8"))
                    break
                msg = ""
                
            
                for i in clients:
                    if clients[c] != clients[i] or clients[c] == clients[i] and c != i:
                        cl = '%s' % clients[i]
                        msg = msg + cl + "*"
                c.send(bytes(msg, "utf8"))
            
            
            msg = client.recv(1024).decode("utf8")
            print(msg, name, sep=" ")
            msg_buf='%s' % msg
            if msg == "{quit}":
                client.close()
                del clients[client]
                for c in clients:
                    if len(clients) == 1:
                        c.send(bytes("Nobody is now available. Please wait...*", "utf8"))
                        break
                    msg = ""                           
                    for i in clients:
                        if clients[c] != clients[i]:
                            cl = '%s' % clients[i]
                            msg = msg + cl + "*"
                    c.send(bytes(msg, "utf8"))
                break

            else:
                r = ""
                for i in msg_buf:
                    if i != "$":
                        r = r+i
                    else:
                        break
                for c in clients:
                    if clients[c] == r:
                        c.send(bytes("$"+ name + "$" + msg_buf, "utf8"))



clients = {}
addresses = {}


SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(('localhost', 80))

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
