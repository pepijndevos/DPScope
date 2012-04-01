from serial.tools.list_ports import comports
from Tkinter import *

def get_port():
    root = Tk()
    ports = [p[0] for p in comports()]
    port = [None] # weird scope rules

    def finish():
        nr = int(list.curselection()[0])
        port[0] = ports[nr]
        root.destroy()

    Label(root, text="Select serial port").pack()
    list = Listbox(root)
    list.pack(padx=5)
    Button(root, text="OK", command=finish).pack()

    for p in ports:
        list.insert(END, p)

    root.wait_window(root)
    return port[0]
