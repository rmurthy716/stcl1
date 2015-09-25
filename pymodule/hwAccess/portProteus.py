"""
port module for proteus
"""

import portColossus
from pci import Pci

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
        self.spam = Proteus(bar, port)

class I2cAccess(portColossus.I2cAccess):
    """
    Proteus I2c implementation
    """
    def __init__(self, port, bar=0):
        self.spam = Proteus(bar, port)
