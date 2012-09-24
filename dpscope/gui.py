import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from portselect import get_port
from Tkinter import *

import high

root = Tk()
root.title("DPScope")
fig = Figure()


pltr = high.Plotter(fig)

class Datalogger(high.Task):
    def __init__(self, widget, interval):
        high.Task.__init__(self, widget, interval)
        self.ch1 = []
        self.ch2 = []

    def task(self):
        data = ch1, ch2 = pltr.read_volt()
        self.ch1.append(ch1)
        self.ch2.append(ch2)
        pltr.plot([], self.ch1, [], self.ch2)

stopfn = lambda: None

def start():
    global stopfn
    if samepl_mode.get():
        dl = Datalogger(root, 100)
        stopfn = dl.stop
        dl.start()

def stop():
    stopfn()


# the plot
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.show()
canvas.get_tk_widget().pack(fill=BOTH, expand=1, side=LEFT)

# the controls
controls = Frame(root)
controls.pack(side=LEFT)
coll1 = Frame(controls)
coll1.pack(fill=BOTH, expand=1, side=LEFT)
coll2 = Frame(controls)
coll2.pack(fill=BOTH, expand=1, side=LEFT)

# all control sections
acquisition = LabelFrame(coll1, text="Acquisition")
acquisition.pack(fill=BOTH, expand=1)

levels = LabelFrame(coll1, text="Levels")
levels.pack(fill=BOTH, expand=1)

display = LabelFrame(coll2, text="Display")
display.pack(fill=BOTH, expand=1)

vertical = LabelFrame(coll2, text="Vertical")
vertical.pack(fill=BOTH, expand=1)

horizontal = LabelFrame(coll2, text="Horizontal")
horizontal.pack(fill=BOTH, expand=1)

trigger = LabelFrame(coll2, text="Trigger")
trigger.pack(fill=BOTH, expand=1)

# acquisition controls
Button(acquisition, text="Start", command=start).pack(fill=X)
Button(acquisition, text="Poll", command=pltr.poll).pack(fill=X)
Button(acquisition, text="Stop", command=stop).pack(fill=X)
Button(acquisition, text="Clear", command=pltr.plot).pack(fill=X)
Label(acquisition, text="Average").pack(fill=X)
Spinbox(acquisition, from_=1, to=100, width=4).pack(fill=X)

# level controls
Label(levels, text="Ch1").grid(sticky=E, row=0, column=0)
Label(levels, text="Ch1").grid(sticky=E, row=0, column=1)
Label(levels, text="Trg").grid(sticky=E, row=0, column=2)
Scale(levels, from_=-100, to=100, length=300).grid(sticky=E, row=1, column=0)
Scale(levels, from_=-100, to=100, length=300).grid(sticky=E, row=1, column=1)
Scale(levels, from_=-100, to=100, length=300).grid(sticky=E, row=1, column=2)

# Display controls
Checkbutton(display, text="Ch1", variable=pltr.ch1b).grid(sticky=W, row=0, column=1)
Checkbutton(display, text="Ch2", variable=pltr.ch2b).grid(sticky=W, row=1, column=1)
Checkbutton(display, text="X/Y", variable=pltr._xy).grid(sticky=W, row=2, column=1)
Checkbutton(display, text="FFT", variable=pltr._fft).grid(sticky=W, row=3, column=1)

# Vertical controls
gains = ["1 V/div", "0.5 V/div", "0.2 V/div", "0.1 V/div", "50 mV/div", "20 mV/div", "10 mV/div", "5 mV/div"]
Label(vertical, text="Scale").grid(sticky=W, row=0, column=1)
Label(vertical, text="Probe Attenuation").grid(sticky=W, row=0, column=2, columnspan=2)

Label(vertical, text="Ch1").grid(sticky=W, row=2, column=0)
ch1att = BooleanVar()
ch1gain = StringVar()
ch1gain.set(gains[0])
OptionMenu(vertical, ch1gain, *gains).grid(sticky=W, row=2, column=1)
Radiobutton(vertical, text="1:1", variable=ch1att, value=0).grid(sticky=W, row=2, column=2)
Radiobutton(vertical, text="1:10", variable=ch1att, value=1).grid(sticky=W, row=2, column=3)

Label(vertical, text="Ch2").grid(sticky=W, row=4, column=0)
ch2att = BooleanVar()
ch2gain = StringVar()
ch2gain.set(gains[0])
OptionMenu(vertical, ch2gain, *gains).grid(sticky=W, row=4, column=1)
Radiobutton(vertical, text="1:1", variable=ch2att, value=0).grid(sticky=W, row=4, column=2)
Radiobutton(vertical, text="1:10", variable=ch2att, value=1).grid(sticky=W, row=4, column=3)

# Horizontal controls
speeds = ["0.5 us/div", "1 us/div", "2 us/div", "5 us/div", "10 us/div", "20 us/div", "50 us/div", "0.1 ms/div", "0.2 ms/div", "0.5 ms/div", "1 ms/div", "2 ms/div", "5 ms/div", "10 ms/div", "20 ms/div", "50 ms/div", "0.1 s/div", "0.2 s/div", "0.5 s/div", "1 s/div"]
sample_speed = StringVar()
sample_speed.set(speeds[0])
samepl_mode = BooleanVar()
Radiobutton(horizontal, text="Scope mode", variable=samepl_mode, value=0).grid(sticky=W, row=0, column=0)
Radiobutton(horizontal, text="Datalog mode", variable=samepl_mode, value=1).grid(sticky=W, row=0, column=1)
OptionMenu(horizontal, sample_speed, *speeds).grid(sticky=W, row=1, column=0, columnspan=2)
Checkbutton(horizontal, text="Pretrigger mode").grid(sticky=W, row=2, column=0, columnspan=2)
Scale(horizontal, from_=0, to=100, length=200, orient=HORIZONTAL).grid(sticky=W, row=3, column=0, columnspan=2)

# Trigger controls
Label(trigger, text="Source").grid(sticky=W, row=0, column=0)
trigger_mode = IntVar()
Radiobutton(trigger, text="Auto", variable=trigger_mode, value=0).grid(sticky=W, row=0, column=1)
Radiobutton(trigger, text="Ch1", variable=trigger_mode, value=1).grid(sticky=W, row=0, column=2)
Radiobutton(trigger, text="Ch2", variable=trigger_mode, value=2).grid(sticky=W, row=0, column=3)

Label(trigger, text="Polarity").grid(sticky=W, row=1, column=0)
trigger_pol = BooleanVar()
Radiobutton(trigger, text="Rising", variable=trigger_pol, value=0).grid(sticky=W, row=1, column=1)
Radiobutton(trigger, text="Falling", variable=trigger_pol, value=1).grid(sticky=W, row=1, column=2)
Checkbutton(trigger, text="Noise reject").grid(sticky=W, row=1, column=3)


pltr.scope = get_port(root)
# defaults
pltr.scope.trig_source(0)
pltr.scope.adcon_from(0)

root.mainloop()
