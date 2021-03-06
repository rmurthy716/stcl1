"""
Define hardware access class
"""
import logging
import sys
import os
import stat
from getHwHandle import *
from l1constants import *

logger = logging.getLogger('hwaccess')

class hw_access(object):
    """
    Hardware Access class implementation
    """

    def __init__(self, port=0):
        self.bar0 = getBar0Handle(port)
        self.bar1 = getBar1Handle(port)
        self.mdio = getMdioHandle(port)
        self.i2c  = getI2cHandle(port)
        self.port = getPort(port)
        # initialize combination operator dictionary
        # currently only used to combine numeric data (Power, Counters, etc)
        self.combination_operator_dict = {}
        self.combination_operator_dict['SLR'] = lambda data, link_data: round(((data << 8) + link_data) * 0.1, 2)


    def read(self, register):
        data = None
        address = register["address"]
        protocolInterface = register["protocolInterface"]
        protocol = protocolInterface["protocol"]
        try:
            if protocol == "MDIO":
                devAddr = protocolInterface["devAddr"]
                portAddr = protocolInterface["portAddr"]
                if "slice" in protocolInterface.keys():
                    self.mdio.write(portAddr, 0x1, 0x8000, protocolInterface["slice"])
                    logger.info("Setting slice register to 0x%x!" % protocolInterface["slice"])
                data = self.mdio.read(portAddr, devAddr, address)
                logger.info("Mdio Read of address 0x%x with data of 0x%x" % (address, data))
                if "linkedRegister" in register.keys():
                    linked_register = register["linkedRegister"]
                    linked_address = linked_register["address"]
                    linked_data = self.mdio.read(portAddr, devAddr, linked_address)
                    logger.info("Mdio Read of address 0x%x with data of 0x%x" % (linked_address, linked_data))
                    combination_operator = self.combination_operator_dict[linked_register["combinationOperator"]]
                    data = combination_operator(data, linked_data)
                    logger.info("Combination operator for Mdio read returned %d" % data)

            elif protocol == "I2C":
                devAddr = protocolInterface["devAddr"]
                busSel = protocolInterface["busSel"]
                if "page" in protocolInterface.keys():
                    self.i2c.qsfp_write(127, protocolInterface["page"])
                data = self.i2c.read(devAddr, busSel, address)
                logger.info("I2c Read of address 0x%x with data of 0x%x" % (address, data))
                if "linkedRegister" in register.keys():
                    linked_register = register["linkedRegister"]
                    linked_address = linked_register["address"]
                    linked_data = self.i2c.read(devAddr, busSel, linked_address)
                    logger.info("I2c Read of address 0x%x with data of 0x%x" % (linked_address, linked_data))
                    combination_operator = self.combination_operator_dict[linked_register["combinationOperator"]]
                    data = combination_operator(data, linked_data)
                    logger.info("Combination operator for I2c read returned %d" % data)

            elif protocol == "Bar1":
                data = self.bar1.read(address)
                logger.info("Bar1 Read of address 0x%x with data of 0x%x" % (address, data))

            elif protocol == "Bar0":
                data = self.bar0.read(address)
                logger.info("Bar0 Read of address 0x%x with data of 0x%x" % (address, data))

            else:
                logger.error("Protocol %s not supported!" % protocol)

        except:
            logger.error("Read for protocol %s failed!" % protocol)
            raise

        return data
