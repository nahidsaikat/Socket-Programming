import socket 
import select 
import sys 
from thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 

IP_address = '127.0.0.1'

Port = 65432 

server.bind((IP_address, Port)) 

server.listen(100) 

list_of_clients = [] 
dict_of_clients = {}

def clientthread(name, conn, addr): 

    conn.send("Welcome to this chatroom! @" + name) 

    while True: 
            try: 
                message = conn.recv(2048) 
                if message: 
                    _from = ''
                    for name, client in dict_of_clients.iteritems():
						if client == conn:
							_from = name
                    print( "<" + addr[0] + "> " + message )
                    if message == 'quit':
                        remove(conn)

                    splited = message.split('@')
                    if len(splited) > 1:
                        name = splited[0]
                        message = splited[1]
                        unicast(_from or addr[0], message, dict_of_clients[name])
                    else:
                        message_to_send = "<" + str(_from or addr[0]) + "> " + message 
                        broadcast(message_to_send, conn) 

                else: 
                    remove(conn) 

            except: 
                continue

def unicast(name, message, conn):
    try:
        conn.send("<" + name + "> " + message)
    except:
        clients.close() 
        remove(clients) 

def broadcast(message, connection): 
	for clients in list_of_clients: 
		if clients!=connection: 
			try: 
				clients.send(message) 
			except: 
				clients.close() 
				remove(clients) 

def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 
    for name, conn in dict_of_clients.iteritems():
        if conn == connection:
            del dict_of_clients[name]
            break

total_clients = 0
while True: 
	conn, addr = server.accept() 
	list_of_clients.append(conn) 
	print(addr[0] + " connected")
	name = conn.recv(2048) 
	dict_of_clients[name.strip()] = conn
	start_new_thread(clientthread,(name, conn,addr))	 

conn.close() 
server.close() 
