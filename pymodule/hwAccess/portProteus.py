"""
port module for proteus
"""
import portColossus
import time
from pci import Pci
from Mdio import Mdio
from I2c import I2c
from l1constants import bit, invert

GEARBOX_PORT_ADDR = 0x7
DEVICE_1 = 0x1
DEVICE_7 = 0x7
MODE_CONTROL_0 = 0xa101
FEC_ENABLE = bit(13)
SLICE_REGISTER = 0x8000

class Proteus(Pci):
    """
    port class implementation
    """
    def __init__(self, bar, port):
        Pci.__init__(self, '174a:0a0f', bar, port)


class MdioAccess(portColossus.MdioAccess):
    """
    Proteus Mdio implementation
    """
    def __init__(self, port, bar=0):
        self.mdio = Mdio(port, bar, portColossus.MDIO_CMD_REG, portColossus.MDIO_DATA_REG)

    def gearbox_read(self, device, regAddr):
        return self.mdio.read(GEARBOX_PORT_ADDR, device, regAddr)

    def gearbox_write(self, device, regAddr, data):
        self.mdio.write(GEARBOX_PORT_ADDR, device, regAddr, data)

class I2cAccess(portColossus.I2cAccess):
    """
    Proteus I2c implementation
    """
    def __init__(self, port, bar=0):
        self.i2c = I2c(port, bar, portColossus.I2C_CMD_REG)

class Port(portColossus.Port):
    """
    Proteus Port implementation
    """
    def __init__(self, port):
        self.bar1 = Proteus(1, port)
        self.i2c = I2cAccess(port)
        self.mdio = MdioAccess(port)

    def setFEC(self, enable):
        """
        set FEC configuration
        """
        data = 0x6800 if enable else 0x4800
        self.mdio.gearbox_write(DEVICE_1, MODE_CONTROL_0, data)
        return ""

    def setAN(self, enable):
        """
        set AN configuration
        """
        if enable:
            print "Setting Advertisment!!"
            self.mdio.gearbox_write(DEVICE_7, SLICE_REGISTER, 0x8000)
            self.mdio.gearbox_write(DEVICE_7, 0x12, 0x0)
            self.mdio.gearbox_write(DEVICE_7, 0x11, 0x2000)
            self.mdio.gearbox_write(DEVICE_7, 0x10, 0x1)
            time.sleep(0.5)
            self.mdio.gearbox_write(DEVICE_1, SLICE_REGISTER, 0x0)

            self.mdio.gearbox_write(DEVICE_7, SLICE_REGISTER, 0x8000)
            self.mdio.gearbox_write(DEVICE_7, 0xc0ba, 0x8)
            time.sleep(0.5)
            self.mdio.gearbox_write(DEVICE_1, SLICE_REGISTER, 0x0)

            self.mdio.gearbox_write(DEVICE_1, 0xa201, 0)
            self.mdio.gearbox_write(DEVICE_1, 0x822b, 0x0100)

            self.mdio.gearbox_write(DEVICE_1, 0x8235, 0x1)
            time.sleep(1)

        else:
            print "Disabling AN!!"
            self.mdio.gearbox_write(DEVICE_1, 0x822b, 0x0)
            self.mdio.gearbox_write(DEVICE_1, 0x8235, 0x1)
            time.sleep(2)
        return ""

    def recoverLink(self):
        """
        link recovery method
        """
        # first check link and only recovery if there are any local faults
        link_data = self.bar1.read(portColossus.FRAMER_PCS_PMA)
        sticky_data = self.bar1.read(portColossus.STICKY_REGISTER)
        if not bool(link_data & portColossus.LOCAL_FAULT) and not bool(sticky_data & portColossus.LOCAL_FAULT):
            return ""
        self.resetRxCore()
        return ""

    def resetRxCore(self):
        """
        method to reset Rx Core
        """
        self.bar1.writeSelectedBits(portColossus.FRAMER_PCS_PMA, portColossus.RX_CORE_RESET, portColossus.RX_CORE_RESET)
        time.sleep(0.02)
        self.bar1.writeSelectedBits(portColossus.FRAMER_PCS_PMA, portColossus.RX_CORE_RESET, 0x0)
