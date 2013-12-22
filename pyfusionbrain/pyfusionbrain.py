import os
#os.environ['PYUSB_DEBUG'] = 'debug'
#os.environ['PYUSB_LOG_FILENAME'] = 'err.log'
import usb.core
import usb.util
import time
import random


class FusionBrainV3:
    """
    Wraps the FusionBrain multifunction IO device, v.3. Specifically, tested with v. 3c.

    One instance per actual device -- not more, not less.

    See /docs for more protocol details.
    """

    def __init__(self):
        self.device = usb.core.find(idVendor=0x04d8, idProduct=0x000c)
        self.device.set_configuration()
        random.seed()
        if random.randint(0,1) == 0:
            self.keepalive = True
        else:
            self.keepalive = False
        self.curr_states = [False]*12

    def dbg_device_info(self):
        """
        Print debugging.
        """
        print "configs..."
        for config in self.device:
            print str(config.bConfigurationValue)
            print "interfaces..."
            for interface in config:
                print 'interface: ' + str(interface.bInterfaceNumber)
                print '  alt setting: ' + str(interface.bAlternateSetting)
                print "  endpoints..."
                for ep in interface:
                    print '    address: ' + str(ep.bEndpointAddress)

    def _make_cmd(self, states):
        #self.dbg_dump_state(states)

        # all commands are 64-byte
        bytes_out = bytearray(64)
        for b in range(0, 64): # should be 0 by default already but not pos
            bytes_out[b] = 0

        # wake-up bit (needed since firmware update in 07)
        bytes_out[61] = 0xFF
        on = True
        self.keepalive = not self.keepalive
        for pos in range(0,12):

            # first bit is on/off state
            if states[pos]:
                bytes_out[pos] = 0x01
            else:
                bytes_out[pos] = 0x00

            # second bit is a keepalive signal, that flips each time we gen a command
            if self.keepalive is True:
                bytes_out[pos] |= 0x02

        # command assembled
        #print ''.join('%02x' % j for j in bytes_out)
        return bytes_out

    def dbg_dump_state(self, output_states):
        for output in range(0,12):
            print '  %r' % output_states[output]

    def set_output(self, idx, state):
        """
        Set the state of a digital output at a specific position (0-based), either on or off (True or False).
        """
        #self.dbg_dump_state(self.curr_states)
        self.curr_states[idx] = state
        self.set_outputs(self.curr_states)

    def set_outputs(self, output_states):
        """
        Set the states of all 12 digital outputs, either on or off (True or False).
        """
        cmd = self._make_cmd(output_states)

        # write then read it back
        self.device.write(1, cmd, 0) # endpoint data interface
        self.device.read(129, 64, 0, 10) # endpoint size interface timeout
        self.curr_states = states

if __name__ == '__main__':
    fb = FusionBrainV3()
    states = [True]*12
    fb.set_outputs(states)
    time.sleep(5)