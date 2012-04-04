import serial
import struct

class DPScope(serial.Serial):


    def __init__(self, port):
        serial.Serial.__init__(self, port, 500000, timeout=1)

    def _ack(self, cmd):
        ackb = self.read(1)
        assert cmd == ord(ackb), "Command(%s) not the same as ack(%s)" % (cmd, ord(ackb))

    def _cmd(cmd, ack=True, postack=False, ret='', args=''):
        def cmd_impl(self, *params):
            endian = '!' #big
            arglen = struct.calcsize(endian+args)
            assert len(params) == arglen, "Wrong number of arguments, requires %s" % arglen
            self.write(chr(cmd))
            self.write(struct.pack(endian+args, *params))

            if ack:
                self._ack(cmd)
            
            retlen = struct.calcsize(endian+ret)
            res = struct.unpack(endian+ret, self.read(retlen))

            if postack:
                self._ack(cmd)

            assert self.inWaiting() == 0, "%s unexpected unread bytes" % self.inWaiting()
            return res

        return cmd_impl
    
    # 0 bytes
    read_adc = _cmd(3, ret='BB')
    ping = _cmd(4, ack=False, ret='7s')
    revision = _cmd(5, ack=False, ret='BB') # assume > 2.1
    abort = _cmd(6)
    read_adc_10 = _cmd(7, ret='HH', postack=True)
    measure_offset = _cmd(8, ret='HH', postack=True)
    # 1 byte
    trig_source = _cmd(21, args='B')
    trig_pol = _cmd(22, args='B')
    def read_back(self, nob):
        self.write(chr(23)+chr(nob))
        status = self.read()
        res = None
        if status:
            res = map(ord, self.read(1+(2*nob)))
        assert self.inWaiting() == 0, "%s unexpected unread bytes" % self.inWaiting()
        return res

    sample_rate = _cmd(24, args='B')
    noise_reject = _cmd(25, args='B')
    arm = _cmd(26, args='B')
    adcon_from = _cmd(27, args='B')
    cal_mode = _cmd(28, args='B')
    pretriggger_mode = _cmd(29, args='B')
    timer_prescale = _cmd(30, args='B')
    post_trig_cnt = _cmd(31, args='B')
    serial_tx = _cmd(32, args='B')
    status_led = _cmd(33, args='B')
    # 2 bytes
    trig_level = _cmd(41, args='H')
    pre_gain = _cmd(41, args='BB')
    gain = _cmd(43, args='BB')
    set_dac = _cmd(44, args='H') # weirdness
    arm_fft = _cmd(45, args='BB')
    set_delay = _cmd(49, args='H')
    timer_period = _cmd(51, args='H')
