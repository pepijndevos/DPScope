import serial

class DPScope(serial.Serial):

    def __init__(self, port):
        serial.Serial.__init__(self, port, 500000, timeout=1)

    def _cmd(cmd, ack=True, ret=0):
        def cmd_impl(self, *params):
            self.write(chr(cmd))
            self.write(''.join(map(chr, params)))
            if ack:
                ackb = self.read(1)
                assert cmd == ord(ackb), "Command(%s) not the same as ack(%s)" % (cmd, ord(ackb))
            
            res = map(ord, self.read(ret))
            assert self.inWaiting() == 0, "%s unexpected unread bytes" % self.inWaiting()
            return res

        return cmd_impl
    
    # 0 bytes
    read_adc = _cmd(3, ret=2)
    ping = _cmd(4, ack=False, ret=7)
    revision = _cmd(5, ack=False, ret=2) # assume > 2.1
    abort = _cmd(6)
    read_adc_10 = _cmd(7, ret=4)
    measure_offset = _cmd(8, ret=4)
    # 1 byte
    trig_source = _cmd(21)
    trig_pol = _cmd(22)
    def read_back(self, nob):
        self.write(chr(23)+chr(nob))
        res = map(ord, self.read(2+(2*nob)))
        assert self.inWaiting() == 0, "%s unexpected unread bytes" % self.inWaiting()
        return res

    sample_rate = _cmd(24)
    noise_reject = _cmd(25)
    arm = _cmd(26)
    adcon_from = _cmd(27)
    cal_mode = _cmd(28)
    pretriggger_mode = _cmd(29)
    timer_prescale = _cmd(30)
    post_trig_cnt = _cmd(31)
    serial_tx = _cmd(32)
    status_led = _cmd(33)
    # 2 bytes
    trig_level = _cmd(41)
    pre_gain = _cmd(41)
    gain = _cmd(43)
    set_dac = _cmd(44)
    arm_fft = _cmd(45)
    set_delay = _cmd(49)
    timer_period = _cmd(51)
