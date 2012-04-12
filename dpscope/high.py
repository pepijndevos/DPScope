from low import DPScope
from numpy.fft import fft
from multiprocessing.pool import ThreadPool
from Tkinter import BooleanVar

def channels(data):
    return data[0::2], data[1::2]

class Plotter(object):

    def __init__(self, fig):
        self._scope = None
        self.fig = fig
        self.plt = fig.add_subplot(111)
        self.ch1, self.ch2 = self.plt.plot([], [], [], [])
        self.pool = ThreadPool()

        self.ch1b = BooleanVar()
        self.ch1b.set(True)

        self.ch2b = BooleanVar()
        self.ch2b.set(True)

        self._fft = BooleanVar()
        self._fft.set(False)

        self._xy = BooleanVar()
        self._xy.set(False)

    @property
    def scope(self):
        return self._scope

    @scope.setter
    def scope(self, port):
        self._scope = DPScope(port)

    @property
    def both_channels(self):
        return self.ch1b.get() and self.ch2b.get()

    @property
    def xy(self):
        return self._xy.get()

    @property
    def fft(self):
        return self._fft.get()

    def poll(self):
        self.arm()
        self.plot(*self.parse(self.read()))
        self.scope.abort()
        
    def read(self, nofb=205):
        data = None
        while not data:
            data = self.scope.read_back(nofb)

        return data[1:] # need first byte?

    def parse(self, data):
        ch1 = data
        ch2 = []
        if self.both_channels:
            ch1, ch2 = channels(data)

        if self.fft:
            ch1 = fft(ch1)
            ch2 = fft(ch2)

        if self.xy:
            return ch1, ch2, [], []
        else:
            return [], ch1, [], ch2

    def reader(self, nofb=205):
       while True:
           yield self.read(nofb)

    def arm(self):
        if self.both_channels:
            self.scope.arm(0)
        else:
            self.scope.arm_fft(0, self.ch1b.get() or self.ch2b.get()*2)

    def plot(self, x1=[], y1=[], x2=[], y2=[]):
        if len(y1) and not len(x1):
            x1 = range(len(y1))

        if len(y2) and not len(x2):
            x2 = range(len(y2))

        self.ch1.set_data(x1, y1)
        self.ch2.set_data(x2, y2)

        self.plt.relim()
        self.plt.autoscale_view()
        self.fig.canvas.draw()


