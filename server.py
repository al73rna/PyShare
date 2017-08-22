__author__ = 'mohammadreza'
import socket
import threading

L = threading.Lock()
L2 = threading.Lock()
CLIENTS = {}
HOST = ''

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST,8888))
s.listen(10)
COUNT = 0
chain = []
def clientThread(c,a):
    c.sendall(b"CONNECTED !")
    global COUNT
    while True :
        # try:
        d = c.recv(1024)
        print(d)
        request = d.decode(encoding="ASCII")
        if(request.startswith("REG#")):
            this = request[4:]
            CLIENTS[request[4:]] = [a[0],c]
            replay = b"REG#OK"
            c.sendall(replay)

        elif(request=="BYE"):
            replay = b"BYE#OK"
            c.sendall(replay)
            c.close()
        elif(request.startswith("PEERCHECK#")):
            streamName = request[10:]
            permission = False
            # noTransmit = []
            # chain = []
            sender_name = None
            for name in CLIENTS.keys() :
                if CLIENTS[name][1] == c :
                    permission = True
                    sender_name = name
            if permission :
                chain.append(sender_name)
                for name in CLIENTS.keys():
                    if CLIENTS[name][1] != c :
                        ask_ready = bytes("WANT?#" + streamName , encoding="ASCII")
                        CLIENTS[name][1].sendall(ask_ready)
            else:
                replay = b"STREAMREG#NOK#You are not registered !"
                c.sendall(replay)

        elif(request.startswith("PEER#YES")):
            L.acquire()
            for name in CLIENTS.keys():
                if CLIENTS[name][1] == c :
                    chain.append(name)
                    COUNT = COUNT + 1
                    print(name,len(chain),COUNT )
                    if COUNT == len(CLIENTS)-1:
                        replay = b"PEERS#READY#"
                        CLIENTS[chain[0]][1].sendall(replay)
            L.release()
        elif(request.startswith("PEER#NO")):
            L.acquire()
            for name in CLIENTS.keys():
                if CLIENTS[name][1] == c :
                    COUNT = COUNT + 1
                    print(name,len(chain),COUNT )
                    if COUNT == len(CLIENTS)-1:
                        replay = b"PEERS#READY#"
                        CLIENTS[chain[0]][1].sendall(replay)
            L.release()
        elif(request.startswith("STREAM#START#")):
            L2.acquire()
            port = 31750
            for i in range(0,len(chain)-1):
                FROM = CLIENTS[chain[i]]
                TO = CLIENTS[chain[i+1]]
                if i == 0 :
                    msg = bytes("START#"+str(port)+"#",encoding="ASCII")+bytes(CLIENTS[chain[1]][0],encoding="ASCII")
                    FROM[1].sendall(msg)
                elif i == len(chain)-2 :
                    msg = bytes("MID#"+str(port-1)+"#"+str(port)+"#",encoding="ASCII")+bytes(TO[0],encoding="ASCII")
                    FROM[1].sendall(msg)
                    port += 1
                    msg = bytes("FINISH#"+str(port-1),encoding="ASCII")
                    CLIENTS[chain[-1]][1].sendall(msg)

                else:

                    msg = bytes("MID#"+str(port-1)+"#"+str(port)+"#",encoding="ASCII")+bytes(TO[0],encoding="ASCII")
                    FROM[1].sendall(msg)

                port += 1
            L2.release()
            print(chain,"THE CHAIN ...")

        else:
            break
        # except:
        #     print("err")
        #     break


while 1 :

    conn,adr = s.accept()

    threading._start_new_thread(clientThread,(conn,adr,))
    #print(CLIENTS)


