"""
port module for proteus
"""

import portColossus
from pci import Pci
from Mdio import Mdio
from I2c import I2c
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

class I2cAccess(portColossus.I2cAccess):
    """
    Proteus I2c implementation
    """
    def __init__(self, port, bar=0):
        self.i2c = I2c(port, bar, portColossus.I2C_CMD_REG)
