"""
Mdio Base module
"""
import time
import getHwHandle
from l1constants import bit

READ_WRITE_BIT = bit(30)
PORT_ADDR_MASK = 0x1f
PORT_ADDR_SHIFT = 21
DEV_ADDR_MASK = 0x1f
DEV_ADDR_SHIFT = 16
REG_ADDR_MASK = 0xffff
DATA_MASK = 0x1ffff
mdioDoneBit = bit(31)
mdioWriteBit = bit(16)

class Mdio():
    """
    Mdio base class implementation
    """
    def __init__(self, port, bar, cmd_reg, data_reg):
        """
        initialization of MDIO class
        """
        self.port = port
        if bar:
            self.spam = getHwHandle.getBar1Handle(self.port)
        else:
            self.spam = getHwHandle.getBar0Handle(self.port)

        self.cmd_reg = cmd_reg
        self.data_reg = data_reg

    def wait_done(self):
        """
        Wait for the ready bit
        """
        doneBit = bit(31)
        for attempt in xrange(10):
            time.sleep(0.01)
            data = self.spam.read(self.cmd_reg)
            if data & doneBit:
                return

        # if the done bit does not get set raise an Exception
        print "MDIO Failure"

    def read(self, portAddr, devAddr, regAddr):
        """
        method to read MDIO register
        """
        # implicit assumption for clause 45
        cmd = 0x0
        cmd |= READ_WRITE_BIT # read/write bit
        cmd |= ((portAddr & PORT_ADDR_MASK) << PORT_ADDR_SHIFT)
        cmd |= ((devAddr & DEV_ADDR_MASK) << DEV_ADDR_SHIFT)
        cmd |= (regAddr & REG_ADDR_MASK)
        self.spam.write(self.cmd_reg, cmd)
        self.wait_done()
        data = self.spam.read(self.data_reg)
        return data & DATA_MASK

    def write(self, portAddr, devAddr, regAddr, data):
        """
        method to write to MDIO register
        """
        cmd = 0x0
        cmd |= ((portAddr & PORT_ADDR_MASK) << PORT_ADDR_SHIFT)
        cmd |= ((devAddr & DEV_ADDR_MASK) << DEV_ADDR_SHIFT)
        cmd |= (regAddr & REG_ADDR_MASK)
        self.spam.write(self.data_reg, data)
        self.spam.write(self.cmd_reg, cmd)
        self.wait_done()
