import sys
import socket
import select
import os
from threading import *
import threading
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox

lock = threading.Lock()

def createmsg(type=0,action=0,sender='',receiver='',data=''):
    msg = str(str(type)+'\n'+str(action)+'\n'+sender+'\n'+receiver+'\n'+data)
    return msg

def parse(data=''):
    msg_str = data.split('\n')
    return msg_str



class WelcomeScreen1(Frame):
    def Adduser(self):
        

        try:
            self.parent.tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.parent.tcpserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.parent.username = self.topinput1.get()
            try:
                os.mkdir('D:\\'+self.parent.username)
                for ele in self.parent.userlist:
                    fh = open('D:\\' + self.parent.username + '\\' + ele[0] + '.txt', 'a')
                    fh.close()
            except:
                pass
            
            self.parent.tcpserver.connect((self.parent.con_IP, self.parent.con_PORT))
            self.msg = createmsg(sender=self.parent.username + '/*/*/' + self.topinput2.get() ,receiver='server')
            self.parent.tcpserver.send(self.msg.encode())
            self.msg = self.parent.tcpserver.recv(2048).decode()
            print(self.msg)
            self.msg_str = parse(self.msg)

            if(self.msg_str[0] == '0' and self.msg_str[1] == '0'):
                self.client = self.msg_str[4].split('/*/*/')
                self.parent.cli_IP = self.client[1]
                self.parent.cli_PORT = int(self.client[0])
                while True:
                    try:
                        self.parent.clientserver.connect((self.parent.cli_IP, self.parent.cli_PORT))
                        break
                    except:
                        pass

                self.msg = self.parent.clientserver.recv(2048).decode()
                print(self.msg)
                self.msg_str = parse(self.msg)
                self.parent.updatelist(self.msg_str[4])
                self.pack_forget()
                self.parent.listscreen = ListScreen(self.parent)
                self.parent.listscreen.pack()
                self.parent.parent.title(self.parent.username)
                t = Thread(target=self.parent.listen)
                t.start()
            else:
                self.parent.tcpserver.close()
                messagebox.showinfo("Error", "Wrong user name")

            

            print("hurray")
        except:
            messagebox.showinfo("Error", "Server inactive")
            self.pb_hd.pack_forget()


    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        
        self.topbar1 = Frame(self)
        self.toplabel1 = Label(self.topbar1, text="User Name : ")
        self.toplabel1.grid(row=0,column=0)
        self.topinput1 = Entry(self.topbar1, width=31)
        self.topinput1.grid(row=0,column=1,pady=3)
        self.topbar1.grid(row=0,column=0, columnspan=2)

        self.topbar2 = Frame(self)
        self.toplabel2 = Label(self.topbar2, text="Password : ")
        self.toplabel2.grid(row=0, column=0,padx=4)
        self.topinput2 = Entry(self.topbar2, show="*", width=31)
        self.topinput2.grid(row=0, column=1,pady=3)
        self.topbar2.grid(row=1, column=0, columnspan=2)

        self.connect = Button(self, text='Connect', command=self.Adduser)
        self.connect.grid(row=2, column=0, columnspan=2, pady=5)
        self.pack(pady=20, padx=3)

class WelcomeScreen2(Frame):
    def Adduser(self):

        try:
            self.parent.newserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.parent.newserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.parent.username = self.topinput1.get()# + '/*/*/' + self.topinput2.get()


            self.parent.newserver.connect((self.parent.con_IP, self.parent.con_PORT + 1))
            self.msg = createmsg(sender=self.parent.username, receiver='server', data=(self.topinput1.get() + '/*/*/' + self.topinput2.get()))
            self.parent.newserver.send(self.msg.encode())
            self.msg = self.parent.tcpserver.recv(2048).decode()
            print(self.msg)
            self.msg_str = parse(self.msg)

            if (self.msg_str[0] == '0' and self.msg_str[1] == '3'):
                messagebox.showinfo("Info", "done")
        except:
            pass
        self.parent.newserver.close()

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.topbar1 = Frame(self)
        self.toplabel1 = Label(self.topbar1, text="User Name : ")
        self.toplabel1.grid(row=0, column=0)
        self.topinput1 = Entry(self.topbar1, width=31)
        self.topinput1.grid(row=0, column=1)
        self.topbar1.grid(row=0, column=0, columnspan=2)

        self.topbar2 = Frame(self)
        self.toplabel2 = Label(self.topbar2, text="Password : ")
        self.toplabel2.grid(row=0, column=0)
        self.topinput2 = Entry(self.topbar2, width=31)
        self.topinput2.grid(row=0, column=1)
        self.topbar2.grid(row=1, column=0, columnspan=2)

        self.add = Button(self, text='Add', command=self.Adduser)
        self.add.grid(row=2, column=0, columnspan=2, pady=5)
        self.pack(pady=20, padx=3)

class ListScreen(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.tree = Treeview(self)
        self.tree.heading('#0', text='Friends online')
        self.parent.state = 'listscreen'
        for ele in self.parent.userlist:
            print(ele[0])
            if ele[0] != '' and ele[0] != self.parent.username:
                self.tree.insert('','end',ele[0],text = ele[0]+' ('+str(ele[1])+')')
        self.tree.bind("<<TreeviewSelect>>", self.OnDoubleClick)
        self.tree.pack()

    def OnDoubleClick(self, event):
        item = self.tree.selection()[0]
        self.parent.rcvr = (self.tree.item(item, "text")).split(' ')[0]
        for ele in self.parent.userlist:
            if ele[0] == self.parent.rcvr:
                self.parent.userlist.remove((ele[0], ele[1]))
                self.parent.userlist.append((ele[0], 0))
        self.pack_forget()
        self.parent.chatscreen = ChatScreen(self.parent)
        self.parent.chatscreen.updatechatscreen()
        self.parent.chatscreen.pack()
        print("you clicked on", self.tree.item(item, "text"))

class ChatScreen(Frame):
    def updatechatscreen(self):
        global lock

        lock.acquire()
        try:
            self.history.config(state='normal')
            fh = open('D:\\' + self.parent.username + '\\' + self.parent.rcvr + '.txt', 'a')
            fh.close()
            fh = open('D:\\' + self.parent.username + '\\' + self.parent.rcvr + '.txt', 'r')
            self.txt = fh.read()
            fh.close()
        finally:
            lock.release()

        self.history.delete('1.0', END)
        self.history.insert('end', self.txt)
        self.history.config(state='disabled')

    def sendentrybox(self):
        self.msg = createmsg(type=1, action=0, sender=self.parent.username, receiver=self.parent.rcvr, data=self.box.get())
        self.parent.clientserver.send(self.msg.encode())
        fh = open('D:\\' + self.parent.username + '\\' + self.parent.rcvr + '.txt', 'a')
        fh.write(self.parent.username + ' : ' + self.box.get()+'\n')
        fh.close()
        self.box.delete(0,'end')
        self.updatechatscreen()

            #self.parent.listen()
        #self.msg = self.parent.clientserver.recv(2048).decode()
        #self.parent.processmsg(self.msg)

    def backtolist(self):
        self.pack_forget()
        self.parent.listscreen = ListScreen(self.parent)
        self.parent.listscreen.pack()
        self.msg=createmsg(type=0,action=2,sender=self.parent.username,receiver='server',data='')
        self.parent.clientserver.send(self.msg.encode())

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.state = 'chatscreen'
        self.bottombar = Frame(self)
        self.box = Entry(self.bottombar, width=33)
        self.send = Button(self.bottombar, text='send', command=self.sendentrybox)
        self.box.grid(row=0, column=0, padx=2, pady=2)
        self.send.grid(row=0, column=1, padx=2, pady=2)

        self.topbar = Frame(self)
        self.toplabel = Label(self.topbar, text = self.parent.rcvr, width=33)
        self.back = Button(self.topbar, text='back', command=self.backtolist)
        self.toplabel.grid(row=0, column=0, padx=2, pady=2)
        self.back.grid(row=0, column=1, padx=2, pady=2)

        self.textbar = Frame(self)
        self.history = Text(self.textbar, width=35, height=18, wrap='word')
        self.scroll = Scrollbar(self.textbar, orient=VERTICAL, command=self.history.yview)
        self.history.config(yscrollcommand=self.scroll.set)
        self.history.grid(row=0, column=0)
        self.scroll.grid(row=0, column=1, sticky=NS)

        self.topbar.grid(row=0,column=0)

        self.textbar.grid(row=1, column=0)
        self.bottombar.grid(row=2, column=0)

class Application(Frame):
    
    def processmsg(self, msg):
        global lock

        self.msg_str = parse(data = msg)

        if (self.msg_str[0] == '0' and self.msg_str[1] == '2' and self.msg_str[2] == 'server'):
            self.updatelist(self.msg_str[4])
            if (self.state == 'listscreen'):
                self.listscreen.pack_forget()
                self.listscreen = ListScreen(self)
                self.listscreen.pack()



        elif (self.msg_str[0] == '1' and self.msg_str[1] == '0'):
            lock.acquire()
            try:
                fh = open('D:\\' + self.username+'\\' + self.msg_str[2] + '.txt', 'a')
                fh.write(self.msg_str[2] + ' : ' + self.msg_str[4]+'\n\n')
                fh.close()
            finally:
                lock.release()
            for ele in self.userlist:
                if ele[0] == self.msg_str[2]:
                    self.userlist.remove((ele[0], ele[1]))
                    self.userlist.append((ele[0], ele[1]+1))

            if (self.state == 'chatscreen' and self.rcvr == self.msg_str[2]):
                self.chatscreen.updatechatscreen()
            if (self.state == 'listscreen'):
                self.listscreen.pack_forget()
                self.listscreen = ListScreen(self)
                self.listscreen.pack()



    def listen(self):
         while True:
             try:
                self.msg = self.clientserver.recv(2048).decode()
                self.processmsg(self.msg)
             except socket.error as msg:
                messagebox.showerror('Error', 'server in active')
                self.destroy()
                self.parent.destroy()

    def updatelist(self, ulist):
        ulist = ulist.split('/*/*/')
        self.userlist = []
        for ele in ulist:
            if(ele != ''):
                self.userlist.append((ele,0))

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        self.state = 'welcomescreen'
        self.rcvr = ''
        self.username = ''
        self.userlist =[]
        #self.userlist.append(('vardhan', 0))
        self.con_IP = socket.gethostbyname(socket.gethostname())
        self.con_PORT = 2017

        self.tcpserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clientserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.buffer_size = 2048

        self.cli_IP = ''#socket.gethostname()
        self.cli_PORT = 0#3000

        #self.clientserver.connect((self.cli_IP, self.cli_PORT))#testing

        self.welcomescreen = WelcomeScreen1(self)
        #self.newuserscreen = WelcomeScreen2(self)
        self.listscreen = ListScreen(self)
        #self.listscreen.pack()
        #self.welcomescreen.pack(pady=20, padx=3)
        #self.newuserscreen.pack(pady=20, padx=3)
        self.chatscreen = ChatScreen(self)
        #self.chatscreen.pack()
        #self.notebook = Notebook(self)
        #self.notebook.add(self.welcomescreen, text="Home")
        #self.notebook.add(self.newuserscreen, text='New User')
        #self.notebook.pack()
        self.pack()
        

        
root = Tk()
root.title('MyChat')
app = Application(root)
root.mainloop()