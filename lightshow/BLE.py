import time
import pexpect
import subprocess
import sys
import re
import sh

# pi@192.168.44.77
# pw: musicnan5

bulb1mac = 'C4:BE:84:42:03:E6'
bulb2mac = 'C4:BE:84:41:A8:01'
bulb3mac = 'C4:BE:84:41:AB:A2'
bulb4mac = 'C4:BE:84:41:AF:E0'
bulb5mac = '04:A3:16:9E:FC:FC'
bulb6mac = '04:A3:16:9F:01:EC'
bulb7mac = '04:A3:16:9F:24:B2'
bulb8mac = '04:A3:16:9F:2C:FD'

bulb1addr = 'C4_BE_84_42_03_E6'
bulb2addr = 'C4_BE_84_41_A8_01'
bulb3addr = 'C4_BE_84_41_AB_A2'
bulb4addr = 'C4_BE_84_41_AF_E0'
bulb5addr = '04_A3_16_9E_FC_FC'
bulb6addr = '04_A3_16_9F_01_EC'
bulb7addr = '04_A3_16_9F_24_B2'
bulb8addr = '04_A3_16_9F_2C_FD'

RESONATOR_MAP = dict([
('r1_100','0xfe 0xcd 0x55'),
('r1_80','0xcb 0xa4 0x44'),
('r1_60','0x98 0x7b 0x33'),
('r1_40','0x65 0x52 0x22'),
('r1_20','0x32 0x29 0x11'),
('r2_100','0xff 0xa5 0x32'),
('r2_80','0xcc 0x84 0x28'),
('r2_60','0x99 0x63 0x1e'),
('r2_40','0x66 0x42 0x14'),
('r2_20','0x33 0x21 0x0a'),
('r3_100','0xf9 0x72 0x12'),
('r3_80','0xc7 0x5b 0x0e'),
('r3_60','0x95 0x44 0x0a'),
('r3_40','0x63 0x2d 0x07'),
('r3_20','0x31 0x16 0x03'),
('r4_100','0xd8 0x06 0x04'),
('r4_80','0xac 0x04 0x03'),
('r4_60','0x81 0x03 0x02'),
('r4_40','0x56 0x02 0x01'),
('r4_20','0x2b 0x01 0x00'),
('r5_100','0xff 0x30 0x99'),
('r5_80','0xcc 0x26 0x7a'),
('r5_60','0x99 0x1c 0x5b'),
('r5_40','0x66 0x13 0x3d'),
('r5_20','0x33 0x09 0x1e'),
('r6_100','0xed 0x23 0xc9'),
('r6_80','0xbd 0x1c 0xa0'),
('r6_60','0x8e 0x15 0x78'),
('r6_40','0x5e 0x0e 0x50'),
('r6_20','0x24 0x08 0x29'),
('r7_100','0xb8 0x29 0xcf'),
('r7_80','0x93 0x20 0xa5'),
('r7_60','0x6e 0x18 0x7c'),
('r7_40','0x49 0x10 0x52'),
('r7_20','0x24 0x08 0x29'),
('r8_100','0x8a 0x23 0xe8'),
('r8_80','0x6e 0x1c 0xb9'),
('r8_60','0x52 0x15 0x8b'),
('r8_40','0x37 0x0e 0x5c'),
('r8_20','0x1b 0x07 0x2e'),
])

class BluetoothctlError(Exception):
    """This exception is raised, when bluetoothctl fails to start."""
    pass


class Bluetoothctl:
    """A wrapper for bluetoothctl utility."""

    def __init__(self):
        out = subprocess.check_output("rfkill unblock bluetooth", shell = True)
        #self.child = pexpect.spawn("bluetoothctl", echo = True)
        print("Initializing...")
        self.child = pexpect.spawn('bluetoothctl')
        self.child.sendline('power on')
        self.child.sendline('agent on')
        self.child.sendline('default-agent')

    def get_output(self, command, pause = 0):
        """Run a command in bluetoothctl prompt, return output as a list of lines."""
        print("Sending command " + command)
        self.child.send(command + "\n")
        time.sleep(pause)
        start_failed = self.child.expect(["bluetooth", pexpect.EOF])

        if start_failed:
            raise BluetoothctlError("Bluetoothctl failed after running " + command)

        return self.child.before.split("\r\n")

    def pair(self, mac_address):
        """Try to pair with a device by mac address."""
        try:
            print("Starting pair " + mac_address)
            out = self.get_output("pair " + mac_address, 4)
            #self.child.sendline('pair C4:BE:84:42:03:E6')
            #self.child.sendline('pair ' + mac_address)
        except BluetoothctlError, e:
            print(e)
            return None
        #else:
        #    res = self.child.expect(["not available", pexpect.EOF])
        #    success = True if res == 0 else False
        #    return success

    def connect(self, mac_address):
        """Try to connect with a device by mac address."""
        try:
            self.child.sendline('connect ' + mac_address)
        except BluetoothctlError, e:
            print(e)
            return None

    def start_agent(self):
        """Start agent"""
        try:
            out = self.get_output("agent on")
        except BluetoothctlError, e:
            print(e)
            return None

    def default_agent(self):
        """Start default agent"""
        try:
            out = self.get_output("default-agent")
        except BluetoothctlError, e:
            print(e)
            return None

    def ble_select_attribute(self, mac_address):
        """Select attribute"""
        try:
            print("Trying to select attribute " + mac_address)
            self.child.sendline("select-attribute /org/bluez/hci0/dev_" + mac_address + "/service0023/char002d")
        except BluetoothctlError, e:
            print(e)
            return None

    def ble_turn_off(self):
        """Turns bulb off"""
        try:
	    print("Trying to turn off")
            self.child.sendline("write 0xcc 0x24 0x33")
        except BluetoothctlError, e:
            print(e)
            return None

    def ble_turn_on(self):
        """Turns bulb off"""
        try:
            self.child.sendline("write 0xcc 0x23 0x33")
        except BluetoothctlError, e:
            print(e)
            return None

    def ble_set_green(self):
        """Turns bulb green"""
        try:
            self.child.sendline("write 0x56 0x00 0xff 0x00 0x00 0xf0 0xaa")
        except BluetoothctlError, e:
            print(e)
            return None

    def ble_set_blue(self):
        """Turns bulb blue"""
        try:
            self.child.sendline("write 0x56 0x00 0x00 0xff 0x00 0xf0 0xaa")
        except BluetoothctlError, e:
            print(e)
            return None


if __name__ == "__main__":

    print("Init bluetooth...")
    b7 = Bluetoothctl()
    b8 = Bluetoothctl()
    #print("Ready!")
    #from sh import bluetoothctl
    b7.pair(bulb7mac)
    b8.pair(bulb8mac)

    b7.ble_select_attribute(bulb7addr)
    b7.ble_turn_on()


    b8.ble_select_attribute(bulb8addr)
    b8.ble_turn_on()

    b7.ble_select_attribute(bulb7addr)
    b7.ble_set_green()
    b8.ble_select_attribute(bulb8addr)
    b8.ble_set_green()

    time.sleep(3)
    b7.ble_select_attribute(bulb7addr)
    b7.ble_set_blue()
    b8.ble_select_attribute(bulb8addr)
    b8.ble_set_blue()
    time.sleep(3)
