# dpscope

I bought a DPScope for my electronic projects, but quickly found out it had only Windows software, but a relatively simple serial protocol.

This software aims to pull data out of the device on any platform supported my matplotlib and PySerial.

## Usage

    $ python dpscope/high.py 
    0 /dev/tty.NXT-DevB-1
    1 /dev/tty.VodaGPS-SPPslave-1
    2 /dev/tty.Bluetooth-Modem
    3 /dev/tty.Bluetooth-PDA-Sync
    4 /dev/tty.usbserial-FTE0ZZ3K
    Enter port number: 4

![screenshot](https://raw.github.com/pepijndevos/DPScope/master/output.png)

## License

Copyright (C) 2012 Pepijn de Vos

Distributed under the Eclipse Public License.
