__author__ = 'mohammadreza'
import socket
import time

SERVERIP = ("127.0.0.1",8888)



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVERIP)

connect_r = s.recv(1024).decode(encoding="ASCII")
print(connect_r)
name = str(input("ENTER ID?"))
SENDREQ = bytes("REG#"+name,encoding="ASCII")
s.sendall(SENDREQ)


register_r = s.recv(1024).decode(encoding="ASCII")
print(register_r)


inp = str(input("1-STREAM A FILE  2-WAIT FOR STREAM"))

if inp == "1" :
    SENDREQ = bytes("PEERCHECK# "+str(input("enter stream name?")),encoding="ASCII")
    s.sendall(SENDREQ)
    check_r = s.recv(1024).decode(encoding="ASCII")
    print(check_r)
    SENDREQ = bytes("STREAM#START#",encoding="ASCII")
    s.sendall(SENDREQ)
    ip_r = s.recv(1024).decode(encoding="ASCII")
    cd = ip_r.split("#")
    totalByte = 0
    if cd[0] == "START":
        f = open("simul.png",'rb')
        input("Press any key to start the stream ...")
        # ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # while(1) :
            # data = f.read(1024)
            # ss.sendto(data, (cd[2], int(cd[1])))
            # totalByte += 1024
            # print(totalByte)
        data = f.read(1024)

        ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while (data):
            if( ss.sendto(data, (cd[2], int(cd[1]))) ):
                data = f.read(1024)
                totalByte += 1024
                print(totalByte)
        f.close()
        ss.close()


if inp == "2" :
    stream_r = s.recv(1024).decode(encoding="ASCII")
    if input(stream_r[6:]+" is available. download ? Y/N") == "y":
        inp2 = "PEER#YES"
    else:
        inp2 = "PEER#NO"

    s.sendall(bytes(inp2,encoding="ASCII"))

    ip_r = s.recv(1024).decode(encoding="ASCII")
    cd = ip_r.split("#")
    print(ip_r)

    if cd[0] == "FINISH":
        fs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        fs.bind(('', int(cd[1])))
        f = open("simul2.png",'wb')
        t = time.time()
        totalByte = 0
        while 1:
            totalByte += 1024
            fs.settimeout(5)
            data,addr = fs.recvfrom(1024)
            f.write(data)
            print(totalByte)
            print("AVG DOWNLOAD RATE = "+str(totalByte/t) , "TOTAL BYTES", totalByte)
        f.close()
        fs.close()

    elif cd[0] == "MID":
        #f = open(name+".frm",'wb')
        ms = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ms.bind(('', int(cd[1]) ))
        mt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        print(ms)
        totalByte = 0
        while 1:
            d = ms.recvfrom(1024)
            #f.write(d[0])
            totalByte += 1024
            print(totalByte)
            mt.sendto(d[0],( cd[3], int(cd[2])) )

        #f.close()
