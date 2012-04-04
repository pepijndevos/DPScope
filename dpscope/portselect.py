from serial.tools.list_ports import comports
from Tkinter import *

def get_port(parent):
    dialog = Toplevel(parent)
    ports = [p[0] for p in comports()]
    port = [None] # weird scope rules

    def finish():
        nr = int(list.curselection()[0])
        port[0] = ports[nr]
        dialog.destroy()

    Label(dialog, text="Select serial port").pack()
    list = Listbox(dialog)
    list.pack(padx=5)
    Button(dialog, text="OK", command=finish).pack()

    for p in ports:
        list.insert(END, p)

    parent.wait_window(dialog)
    return port[0]
