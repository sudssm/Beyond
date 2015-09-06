# Tcp Chat server
 
import socket, select, base64, hashlib

MAGIC = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
HSHAKE_RESP = "HTTP/1.1 101 Switching Protocols\r\n" + \
            "Upgrade: websocket\r\n" + \
            "Connection: Upgrade\r\n" + \
            "Sec-WebSocket-Accept: %s\r\n" + \
            "\r\n"


#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)
 
if __name__ == "__main__":
     
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 5000
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "Socket server started on port " + str(PORT)
 
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
                              
            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                #try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        print data
                        broadcast_data(sock, data)                
                 

                        #might be html
                        if "User-Agent:" in data:
                            headers = {}
                            lines = data.splitlines()
                            for l in lines:
                                parts = l.split(": ", 1)
                                if len(parts) == 2:
                                    headers[parts[0]] = parts[1]
                            headers['code'] = lines[len(lines) - 1]
                            key = headers['Sec-WebSocket-Key']
                            resp_data = HSHAKE_RESP % ((base64.b64encode(hashlib.sha1(key+MAGIC).digest()),))
                            sock.send(resp_data)

                #except:
                #    sock.close()
                #    CONNECTION_LIST.remove(sock)
                #    continue
     
    server_socket.close()