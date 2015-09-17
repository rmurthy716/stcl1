#!/mnt/spirent/ccpu/bin/python
from __future__ import with_statement

import os
import time
import sys
import exceptions
from iceman import pspam

def bit(x):
    return 0x1 << x


# Bar 0 Registers

MDIO_CMD_REG  = 0x0078
MDIO_DATA_REG = 0x007c

I2C_CMD_REG   = 0x0044

# MDIO and I2C Constants
READ_WRITE_BIT = bit(30)
PORT_ADDR_MASK = 0x1f
PORT_ADDR_SHIFT = 21
DEV_ADDR_MASK = 0x1f
DEV_ADDR_SHIFT = 16
REG_ADDR_MASK = 0xffff
DATA_MASK = 0x1ffff

mdioDoneBit = bit(31)
mdioWriteBit = bit(16)

CFP_PORT_ADDR = 0x1
GEARBOX_PORT_ADDR = 0x0
CFP_ADAPTOR_PORT_ADDR = 0xe

QSFP_DEV_ADDR = 0x50
QSFP_BUS_SEL = 0x9

i2cDoneBit = bit(31)
i2cErrorBit = bit(29)
i2cDoneMask = i2cDoneBit | i2cErrorBit


class Colossus(pspam.Pci):
    #
    # Some register addresses.
    #
    VERSION        = 0x00
    MAX_POLL_COUNT = 10
    DEVICE         = '/dev/pspam1'

    # Spirent FPGA PCI device IDs
    DEVICE_IDs = {
        "STC_DX2_100G" : '174a:0a05',     # 1x100GbE image
        "STC_FX2_100G" : '174a:0a09',     # 1x100GbE image
        "STC_DX2_40G"  : '174a:0a0a',     # 2x40Gbe  image
        "STC_DX2_10G"  : '174a:0a0b',     # 8x10GbE  image
        "NIC_DX2_100G" : '174a:0a06',     # 1x100GbE image
        "NIC_FX2_100G" : '174a:0a0c',     # 1x100GbE image
        "NIC_DX2_40G"  : '174a:0a0d',     # 2x40GbE  image
        "NIC_DX2_10G"  : '174a:0a0e',     # 8x10GbE  image
    }

    def __init__ (self, bar = 1, port = 0):
        for key, ids in Colossus.DEVICE_IDs.items():
            try:
                pspam.Pci.__init__ (self, Colossus.DEVICE, ids, bar, port)
                #print "Detected ", key, " ID ", ids
                break
            except:
                continue
        self.port = port
        self.mdio = Mdio(0, port)
        self.i2c = I2c(0, port)

    def __str__ (self):
        version = self.read (Colossus.VERSION)
        return "  FPGA version (%06X = 0x%08X)/" % (Colossus.VERSION, version)

    def read( self, address ):
        value = self._read_32(address)

        time.sleep( 1 / 10000.0 )    # sleep for 100 us
        return value

    def write( self,address, value ):
        if value >= 0x80000000:
            value -= 0x100000000
        self._write_32(address, value)
        time.sleep( 1 / 10000.0 )    # sleep for 100 us

class Mdio():
    def __init__ (self, bar = 0, port = 1):
        self.spam = Colossus(bar, port)

    def wait_done(self):
        for attempt in xrange(Colossus.MAX_POLL_COUNT):
            time.sleep(0.0001)
            data = self.spam.read (MDIO_CMD_REG)
            if  data & mdioDoneBit:
                return
        raise Exception("MDIO failure")

    def write(self, reg, data ):
        self.spam.write (MDIO_DATA_REG, data)
        self.spam.write (MDIO_CMD_REG, mdioWriteBit + reg)
        self.wait_done()

    def read(self, reg):
        self.spam.write (MDIO_CMD_REG, 0x40010000 + reg)
        self.wait_done()
        data = self.spam.read (MDIO_DATA_REG)
        return data & 0xffff

    def MdioRead(self, portAddr, devAddr, regAddr):
        # implicit assumption for clause 45
        cmd = 0x0
        cmd |= READ_WRITE_BIT # read/write bit
        cmd |= ((portAddr & PORT_ADDR_MASK) << PORT_ADDR_SHIFT)
        cmd |= ((devAddr & DEV_ADDR_MASK) << DEV_ADDR_SHIFT)
        cmd |= (regAddr & REG_ADDR_MASK)
        self.spam.write(MDIO_CMD_REG, cmd)
        self.wait_done()
        data = self.spam.read(MDIO_DATA_REG)
        return data & DATA_MASK

    def MdioWrite(self, portAddr, devAddr, regAddr, data):
        cmd = 0x0
        cmd |= ((portAddr & PORT_ADDR_MASK) << PORT_ADDR_SHIFT)
        cmd |= ((devAddr & DEV_ADDR_MASK) << DEV_ADDR_SHIFT)
        cmd |= (regAddr & REG_ADDR_MASK)
        self.spam.write(MDIO_DATA_REG, data)
        self.spam.write(MDIO_CMD_REG, cmd)
        self.wait_done()

    def cfp_read(self, devAddr, regAddr):
        return self.MdioRead(CFP_PORT_ADDR, devAddr, regAddr)

    def cfp_write(self, devAddr, regAddr, data):
        self.MdioWrite(CFP_PORT_ADDR, devAddr, regAddr, data)

    def gearbox_read(self, devAddr, regAddr):
        return self.MdioRead(GEARBOX_PORT_ADDR, devAddr, regAddr)

    def gearbox_write(self, devAddr, regAddr, data):
        return self.MdioWrite(GEARBOX_PORT_ADDR, devAddr, regAddr, data)

    def cfp_adaptor_read(self, devAddr, regAddr):
        return self.MdioRead(CFP_ADAPTOR_PORT_ADDR, devAddr, regAddr)

    def cfp_adaptor_write(self, devAddr, regAddr, data):
        self.MdioWrite(CFP_ADAPTOR_PORT_ADDR, devAddr, regAddr, data)

class I2c():
    def __init__(self, bar = 0, port = 1):
        self.spam = Colossus(bar, port)

    def buildReadCmd(self, devAddr, regAddr, busSel):
        cmd =  0x0 | 1 << 30 | ((busSel & 0xf) << 23) | ((devAddr & 0x7f) << 16) | (regAddr & 0xff)
        return cmd

    def buildWriteCmd(self, devAddr, regAddr, regData, busSel):
        cmd = 0x0 | ((busSel & 0xf) << 23) | ((devAddr & 0x7f) << 16) | ((regData & 0xff) << 8) | (regAddr & 0xff)
        return cmd

    def cmdDone(self, cmdData):
        # or the done bit and error bit
        return True if ((cmdData & i2cDoneMask) == i2cDoneBit) else False

    def waitForWriteDone(self):
        for i in range(10):
            if i >= 10:
                print "I2C Failure"
                break
            time.sleep(0.0005)
            bar0Data = self.spam.read(I2C_CMD_REG)
            if(self.cmdDone(bar0Data)):
                break

    def waitForReadDone(self):
        bar0Data = 0x0
        for i in range(10):
            if i >= 10:
                print "I2C Failure"
                break
            time.sleep(0.0005)
            bar0Data = self.spam.read(I2C_CMD_REG)
            if(self.cmdDone(bar0Data)):
                break

        return bar0Data

    def cmdRtrvData(self, cmdData):
        return ((cmdData >> 8) & 0xff)

    def write(self, devAddr,  busSel, regAddr, regData):
        bar0Data = self.buildWriteCmd(devAddr, regAddr, regData, busSel)
        self.spam.write(I2C_CMD_REG, bar0Data)
        # The QSFP+ data sheet mentions that the time needed for a write to be done is 40ms (up to 4 Bytes)
        time.sleep(0.004)
        self.waitForWriteDone()

    def read(self, devAddr, busSel, regAddr):
        bar0Data = self.buildReadCmd(devAddr, regAddr, busSel)
        self.spam.write(I2C_CMD_REG, bar0Data)
        bar0Data = self.waitForReadDone()
        return self.cmdRtrvData(bar0Data)

    def qsfp_read(self, regAddr):
        return self.read(QSFP_DEV_ADDR, QSFP_BUS_SEL, regAddr)

    def qsfp_write(self, regAddr, regData):
        self.write(QSFP_DEV_ADDR, QSFP_BUS_SEL, regAddr, regData)

# This is mainly meant as a library module but can be run stand-alone
# to display version information about the card.
#
if __name__ == "__main__":
        print Colossus(0)
