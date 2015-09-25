"""
I2c base module
"""
import time
import getHwHandle
from l1constants import bit

i2cDoneBit = bit(31)
i2cErrorBit = bit(29)
i2cDoneMask = i2cDoneBit | i2cErrorBit
READ_WRITE_BIT = bit(30)
class I2c():
    """
    I2c base class implementation
    """
    def __init__(self, port, bar, cmd_reg):
        """
        Initialization of I2c class
        """
        self.port = port
        if bar:
            self.spam = getHwHandle.getBar1Handle(self.port)
        else:
            self.spam = getHwHandle.getBar0Handle(self.port)

        self.cmd_reg = cmd_reg

    def buildReadCmd(self, devAddr, regAddr, busSel):
        """
        helper function to build i2c read cmd
        """
        cmd = 0x0 | READ_WRITE_BIT | ((busSel & 0xf) << 23) | ((devAddr & 0x7f) << 16) | (regAddr & 0xff)
        return cmd

    def buildWriteCmd(self, devAddr, regAddr, regData, busSel):
        """
        helper function to build i2c write cmd
        """
        cmd = 0x0 | ((busSel & 0xf) << 23) | ((devAddr & 0x7f) << 16) | ((regData & 0xff) << 8)
        cmd |= (regAddr & 0xff)
        return cmd

    def cmdDone(self, cmdData):
        """
        helper function to wait for ready bit
        also checks error bit
        """
        # or the done bit and error bit
        return True if ((cmdData & i2cDoneMask) == i2cDoneBit) else False

    def waitForReadDone(self):
        """
        wait for read cmd done
        """
        data = 0x0
        for i in range(10):
            if i >= 10:
                print "I2C Failure"
                break
            time.sleep(0.0005)
            data = self.spam.read(self.cmd_reg)
            if(self.cmdDone(data)):
                break

        return data

    def waitForWriteDone(self):
        """
        wait for write cmd done
        """
        for i in range(10):
            if i >= 10:
                print "I2C Failure"
                break
            time.sleep(0.0005)
            data = self.spam.read(self.cmd_reg)
            if(self.cmdDone(data)):
                break

    def cmdRtrvData(self, cmdData):
        """
        extract data from cmd reg
        """
        return ((cmdData >> 8) & 0xff)

    def write(self, devAddr, busSel, regAddr, regData):
        """
        main write function
        """
        data = self.buildWriteCmd(devAddr, regAddr, regData, busSel)
        self.spam.write(self.cmd_reg, data)
        # The QSFP+ data sheet mentions that the time needed for a write to be done is 40ms (up to 4 Bytes)
        time.sleep(0.004)
        self.waitForWriteDone()

    def read(self, devAddr, busSel, regAddr):
        """
        main read function
        """
        data = self.buildReadCmd(devAddr, regAddr, busSel)
        self.spam.write(self.cmd_reg, data)
        data = self.waitForReadDone()
        return self.cmdRtrvData(data)
