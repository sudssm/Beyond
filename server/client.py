# telnet program example
import socket, select, string, sys
 
#main function
if __name__ == "__main__":
     
    host = "45.79.152.183"
    port = 5000
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
     
    # connect to remote host
    try :
        s.connect((host, port))
    except :
        print 'Unable to connect'
        sys.exit()
     
    while 1:
        socket_list = [sys.stdin, s]
         
        # Get the list sockets which are readable
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
         
        for sock in read_sockets:
            #incoming message from remote server
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from server'
                    sys.exit()
                else :
                    #print data
                    sys.stdout.write(data + "\n")
                    sys.stdout.flush()
                