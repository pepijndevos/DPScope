from low import DPScope

def read(nofb):
    data = None
    while not data:
        data = s.read_back(nofb)
    return data

def reader(nofb):
   while True:
       yield read(nofb)

def channels(data):
    return data[1::2], data[2::2]
