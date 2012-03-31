from low import DPScope
import matplotlib.pyplot as plt
from serial.tools.list_ports import comports

ports = comports()

for i, p in enumerate(ports):
    print i, p[1]

n = int(raw_input("Enter port number: "))
port = ports[n][0]

s = DPScope(port)
s.cal_mode(1)
s.trig_source(0)
s.arm(0)
status = 0
while not status:
    data = s.read_back(205)
    status = data[0]
s.abort()

ch1 = data[2::2]
ch2 = data[3::2]
plt.plot(ch1)
plt.plot(ch2)
plt.show()
