"""
Module to handle post requests from browser.
"""
import logging
import sys
sys.path.append("/usr/spirent/stcl1/pymodule/hwAccess")
from l1constants import bit, invert

logger = logging.getLogger('hwaccess')

def setFEC(hw_access_handle, enable):
    """
    set Forward Error Correction configuration
    """
    # initialize paramters
    devAddr = 0x1
    portAddr = 0xe
    regAddr = 0x8a05

    # get back data first
    data = hw_access_handle.mdio.read(portAddr, devAddr, regAddr)
    status = bool(data & bit(3))
    if status != enable:
        # only set the configuration if it has changed
        value = (data | bit(3)) if enable else (data & invert(bit(3)))
        logger.info("Setting FEC to %s" % enable)
        hw_access_handle.mdio.write(portAddr, devAddr, regAddr, value)

def setAN(hw_access_handle, enable):
    """
    set Auto Negotiation Configuration
    """
    return

def handlePostRequest(data, hw_access_handle):
    postFunctions = {}
    postFunctions["FEC"] = setFEC
    postFunctions["AN"] = setAN

    # unfortunately in jQuery each post request value is in an array

    if data["Attribute"][0] in postFunctions.keys():
        postFunction = postFunctions[data["Attribute"][0]]
        enableString = data["Value"][0]
        # javascript bool values not compatible with python
        enable = True if enableString == "true" else False
        postFunction(hw_access_handle, enable)
    else:
        logger.error("Unsupported post request for attribute %s" % data["Attribute"][0])
