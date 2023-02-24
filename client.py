import socket
import threading
from tkinter import *
import tkinter
from tkinter import simpledialog

class Chat:
    def __init__(self) -> None:
        HOST = 'localhost'
        PORT = 8000
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        login = Tk()
        login.withdraw()
        self.window_loaded = False
        self.active = True

        self.client_name = simpledialog.askstring('Name', 'Tipe your name:', parent=login)
        self.room_name = simpledialog.askstring('Room', 'Tipe the room name:', parent=login)
        thread = threading.Thread(target=self.connect)
        thread.start()
        self.window()


    def window(self):
        self.root = Tk()
        self.root.geometry("800x800")
        self.root.title("Chat")
        self.text_box = Text(self.root)
        self.text_box.place(relx=0.05, rely=0.01, width=700, height=600)

        self.tipe_message = Entry(self.root)
        self.tipe_message.place(relx=0.05, rely=0.9, width=500, height=50)
        self.btn_send = Button(self.root, text='Send', command=self.send_message)
        self.btn_send.place(relx=0.7, rely=0.9, width=100, height=50)
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.mainloop()

    def close(self):
        self.root.destroy()
        self.client.close()


    def connect(self):
        while True:
            received = self.client.recv(1024)
            if received == b'room':
                self.client.send(self.room_name.encode())
                self.client.send(self.client_name.encode())
            else:
                try:
                    self.text_box.insert('end', received.decode())
                except:
                    pass


    def send_message(self):
        message = self.tipe_message.get()
        self.client.send(message.encode())
        self.tipe_message.delete(0, END)

chat = Chat()