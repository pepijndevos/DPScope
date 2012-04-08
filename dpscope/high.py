from low import DPScope
from numpy.fft import fft

def channels(data):
    return data[1::2], data[2::2]

# scope modes
A = 1
B = 2
AB = 3
XY = 4
AFFT = 5
BFFT = 6

class Plotter(object):

    def __init__(self, port, fig):
        self.scope = DPScope(port)
        self.fig = fig
        self.plt = fig.add_subplot(111)
        self.ch1, self.ch2 = self.plt.plot([], [], [], [])

        self.mode = AB
        #self.scope.trig_source(0)
        #self.scope.cal_mode(1)
        
    def read(self, nofb=205):
        data = None
        while not data:
            data = self.scope.read_back(nofb)

        if self.mode in [AB, XY]:
            return channels(data)
        elif self.mode in [AFFT, BFFT]:
            return fft(data[1:]), []
        elif self.mode in [A, B]:
            return data[1:], []

    def reader(self, nofb=205):
       while True:
           yield self.read(nofb)

    def arm(self):
        if self.mode in [AB, XY]:
            self.scope.arm(0)
        elif self.mode in [AFFT, A]:
            self.scope.arm_fft(0, 1)
        elif self.mode in [BFFT, B]:
            self.scope.arm_fft(0, 2)

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

    def poll(self):
        self.arm()
        d1, d2 = self.read()
        if self.mode == XY:
            self.plot(x1=d1, y1=d2)
        else:
            self.plot(y1=d1, y2=d2)
        self.scope.abort()

