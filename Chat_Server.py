import sys
import socket
import select
from threading import *
import threading

active_users = []
delim = '/*/*/'

lock = threading.Lock()

def sendmsg(sender, receiver, data): #to be implemented
    for i in active_users:
        if(i[0] == receiver):
            conn = i[1]
            msg = createmsg(type=1,action=0,sender=sender,receiver=receiver,data=data)
            try:
                conn.send(msg.encode())
            except:
                pass
    

def createmsg(type=0,action=0,sender='',receiver='',data=''):
    msg = str(str(type)+'\n'+str(action)+'\n'+sender+'\n'+receiver+'\n'+data)
    return msg

def remove(sender): #to be implemented
    for i in active_users:
        if(i[0] == sender):
            active_users.remove((sender, i[1]))

def senduserlist():
    msg = ''
    for ele in active_users:
        msg = msg + (ele[0]) + '/*/*/'
        
    for ele in active_users:
        data = createmsg(type=0, action=2, sender='server', receiver=ele[0], data=msg)
        try:
            ele[1].send(data.encode())
        except:
            pass

def clientthread(client_port, client_ip, client):
    global lock
    clientserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clientserver.bind((client_ip,client_port))
    clientserver.listen(5)
    (conn, (ip,port)) = clientserver.accept()
        
    lock.acquire()
    try:
        active_users.append((client,conn))
        senduserlist()
    finally:
        lock.release()
    
    
    while True:
        print('success')
        try:
            msg = conn.recv(2048).decode()
            msg_str = msg.split('\n')
            print(msg_str)
            if(msg_str[0] == '0' and msg_str[1] == '1'):
              break
            elif(msg_str[0] == '0' and msg_str[1] == '2'):
                data = ''
                for ele in active_users:
                    data += ele[0]
                    data += '/*/*/'
                data = createmsg(type=1,action=0,sender='server',receiver=client,data=data)
                conn.send(data.encode())
                

            elif(msg_str[0] == '1' and msg_str[1] == '0'):
                sendmsg(sender = client, receiver = msg_str[3], data = msg_str[4])
    
        except socket.error as msg:
            print(msg)
            break
    try:
        conn.close()
    except:
        pass
    remove(client)
    
def parse(data):
    msg_str = data.split("\n")
    return msg_str

def checkuser(msg_str, conn, userdata, client_port, client_ip):

    if(msg_str[0] == '0' and msg_str[1] == '0'):
        sender = msg_str[2]
        if sender in userdata:
            msg = createmsg(type=0,action=0,sender='server',receiver=sender,data=(str(client_port) + '/*/*/' +  str(client_ip)))
            conn.send(msg.encode())
            #t = Thread(target=clientthread, args=(client_port, client_ip, sender))
            #t.start()
            clientthread(client_port, client_ip, sender)
        else:
            msg = createmsg(type=0,action=1,sender='server',receiver=sender,data='')
            conn.send(msg.encode())
    conn.close()

def newuser():
    new_IP = socket.gethostbyname(socket.gethostname())
    new_PORT = 2018
    buffer_size = 2048
    
    tcpnserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpnserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpnserver.bind((new_IP,new_PORT))
    
    while True:
        try:
            tcpnserver.listen(1)
            print('waiting for clients')
            #print(active_users)
            (newcliconn, (ip,port)) = tcpnserver.accept()
            data = newcliconn.recv(2048).decode()
            fh = open('D:\p.txt', 'a')
            userdata = fh.write(data)
            fh.close()
        except:
            try:
                newcliconn.close()
            except:
                pass


def main():
    t = Thread(target=newuser)
    t.start()
    TCP_IP = socket.gethostbyname(socket.gethostname())
    TCP_PORT = 2017
    buffer_size = 2048
    msg_str = []

    client_port = 3000
    client_ip = socket.gethostbyname(socket.gethostname())

    fh = open('D:\p.txt', 'r')
    userdata = fh.read()
    userdata = userdata.split('\n')
    fh.close()

    tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpserver.bind((TCP_IP,TCP_PORT))
    print('Server started on ', TCP_IP)
    active_users.append(('chandu',0))
    while True:
        
        tcpserver.listen(10)
        print('waiting for clients')
        #print(active_users)
        (conn, (ip,port)) = tcpserver.accept()
        data = conn.recv(2048).decode()
        print(data)
        #i = input()
        #msg = createmsg(type=0,action=2,sender='vardhan',receiver='vardhan',data='hey')
        #conn.send(msg.encode())
        msg_str=parse(data)
        #print(data)
        checkuser(msg_str, conn, userdata, client_port, client_ip)
        client_port += 1


'''
def main():
    active_users.append(('chandu', 0))

    TCP_IP = socket.gethostbyname(socket.gethostname())
    TCP_PORT = 2017
    tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcpserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tcpserver.bind((TCP_IP,TCP_PORT))
    tcpserver.listen(1)
    (conn, (ip,port)) = tcpserver.accept()
    data = conn.recv(2048).decode()

    msg = createmsg(type=0,action=0,sender='server',receiver='vardhan',data=(str(3000) + '/*/*/' +  str(TCP_IP)))
    
    tserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    tserver.bind((TCP_IP,3000))
    conn.send(msg.encode())

    tserver.listen(1)
    (conn1, (ip,port)) = tserver.accept()
    active_users.append(('vardhan',conn1))
    senduserlist()

    active_users.append(('budati',0))

    msg = conn1.recv(2048).decode()
    msg_str = msg.split('\n')
    
    print(msg_str)
    if(msg_str[0] == '0' and msg_str[1] == '2'):
        data = ''
        for ele in active_users:
            data += ele[0]
            data += '/*/*/'
        data = createmsg(type=0,action=2,sender='server',receiver='vardhan',data=data)
        conn1.send(data.encode())
                

    msg = conn1.recv(2048).decode()
    msg_str = msg.split('\n')

    if(msg_str[0] == '0' and msg_str[1] == '2'):
        sendmsg(sender = 'chandu', receiver = 'vardhan', data = 'yo')
 '''


main()
