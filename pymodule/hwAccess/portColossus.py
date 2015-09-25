"""
Port Colossus Module
"""
import time
from pci import Pci
from Mdio import Mdio
from I2c import I2c
# Bar 0 Registers

MDIO_CMD_REG = 0x0078
MDIO_DATA_REG = 0x007c
I2C_CMD_REG = 0x0044

# MDIO and I2C Constants
CFP_PORT_ADDR = 0x1
GEARBOX_PORT_ADDR = 0x0
CFP_ADAPTOR_PORT_ADDR = 0xe

QSFP_DEV_ADDR = 0x50
QSFP_BUS_SEL = 0x9

class Colossus(Pci):
    """
    Colossus PCI class
    """
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

    def __init__(self, bar, port):
        """
        find the PCI id corresponding to Colossus
        """
        for key, ids in Colossus.DEVICE_IDs.items():
            try:
                Pci.__init__(self, ids, bar, port)
                break
            except:
                continue
        self.port = port

    def read(self, address):
        """
        basic spam read
        """
        value = self._read_32(address)

        time.sleep(1 / 10000.0)    # sleep for 100 us
        return value

    def write(self, address, value):
        """
        basic spam write
        """
        if value >= 0x80000000:
            value -= 0x100000000
        self._write_32(address, value)
        time.sleep(1 / 10000.0)    # sleep for 100 us

class MdioAccess():
    def __init__(self, port, bar=0):
        """
        initialize MDIO Bar0 Class
        """
        # MDIO for Colossus on BAR0
        self.mdio = Mdio(port, bar, MDIO_CMD_REG, MDIO_DATA_REG)

    def read(self, devAddr, portAddr, regAddr):
        return self.mdio.read(devAddr, portAddr, regAddr)

    def write(self, devAddr, portAddr, regAddr, data):
        self.mdio.write(devAddr, portAddr, regAddr, data)

    def cfp_read(self, devAddr, regAddr):
        return self.mdio.read(CFP_PORT_ADDR, devAddr, regAddr)

    def cfp_write(self, devAddr, regAddr, data):
        self.mdio.write(CFP_PORT_ADDR, devAddr, regAddr, data)

    def gearbox_read(self, devAddr, regAddr):
        return self.mdio.read(GEARBOX_PORT_ADDR, devAddr, regAddr)

    def gearbox_write(self, devAddr, regAddr, data):
        return self.mdio.write(GEARBOX_PORT_ADDR, devAddr, regAddr, data)

    def cfp_adaptor_read(self, devAddr, regAddr):
        return self.mdio.read(CFP_ADAPTOR_PORT_ADDR, devAddr, regAddr)

    def cfp_adaptor_write(self, devAddr, regAddr, data):
        self.mdio.write(CFP_ADAPTOR_PORT_ADDR, devAddr, regAddr, data)

class I2cAccess():
    def __init__(self, port, bar=0):
        """
        I2C for colossus on BAR0
        """
        self.i2c = I2c(port, bar, I2C_CMD_REG)

    def read(self, devAddr, busSel, regAddr):
        return self.i2c.read(devAddr, busSel, regAddr)

    def write(self, devAddr, busSel, regAddr, regData):
        return self.i2c.write(devAddr, busSel, regAddr, regData)

    def qsfp_read(self, regAddr):
        return self.read(QSFP_DEV_ADDR, QSFP_BUS_SEL, regAddr)

    def qsfp_write(self, regAddr, regData):
        self.write(QSFP_DEV_ADDR, QSFP_BUS_SEL, regAddr, regData)
