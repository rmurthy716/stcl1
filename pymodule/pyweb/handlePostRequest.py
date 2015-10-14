"""
Module to handle post requests from browser.
"""
import logging
import sys
import json
sys.path.append("/usr/spirent/stcl1/pymodule/hwAccess")
logger = logging.getLogger('hwaccess')

def setFEC(hw_access_handle, data):
    """
    set Forward Error Correction configuration
    """
    enableString = data["Value"][0]
    # javascript bool values not compatible with python
    enable = True if enableString == "true" else False
    logger.info("Setting FEC to %s" % enable)
    return hw_access_handle.port.setFEC(enable)

def setAN(hw_access_handle, data):
    """
    set Auto Negotiation Configuration
    """
    enableString = data["Value"][0]
    enable = True if enableString == "true" else False
    return hw_access_handle.port.setAN(enable)

def mdioRead(hw_access_handle, data):
    """
    read through mdio
    """
    retStatus = {}
    devAddr = int(data["mdioDevAddr"][0], 16)
    portAddr = int(data["mdioPortAddr"][0], 16)
    regAddr = int(data["mdioRegAddr"][0], 16)
    data = hw_access_handle.mdio.read(portAddr, devAddr, regAddr)
    logger.info("Mdio read returned 0x%x" % data)
    if str(data):
        retStatus["data"] = "MDIO Read of 0x%x = 0x%x" % (regAddr, data)
        retStatus["level"] = "success"
    else:
        retStatus["data"] = "MDIO Access Failure!"
        retStatus["level"] = "danger"

    return json.dumps(retStatus)

def mdioWrite(hw_access_handle, data):
    """
    write through mdio
    """
    retStatus = {}
    devAddr = int(data["mdioDevAddr"][0], 16)
    portAddr = int(data["mdioPortAddr"][0], 16)
    regAddr = int(data["mdioRegAddr"][0], 16)
    try:
        writeData = int(data["mdioData"][0], 16)
    except:
        writeData = ""
    if str(writeData):
        try:
            hw_access_handle.mdio.write(portAddr, devAddr, regAddr, writeData)
            retStatus["data"] = "MDIO Write to 0x%x succeeded with value of 0x%x" % (regAddr, writeData)
            retStatus["level"] = "success"
        except:
            retStatus["data"] = "MDIO Access Failure"
            retStatus["level"] = "danger"
    else:
        retStatus["data"] = "Write Data is invalid!"
        retStatus["level"] = "danger"

    return json.dumps(retStatus)

def i2cRead(hw_access_handle, data):
    """
    read through i2c
    """
    retStatus = {}
    devAddr = int(data["i2cDevAddr"][0], 16)
    busSel = int(data["i2cBusSel"][0], 16)
    regAddr = int(data["i2cRegAddr"][0], 10)
    data = hw_access_handle.i2c.read(devAddr, busSel, regAddr)
    logger.info("I2c read returned 0x%x" % data)
    if str(data):
        retStatus["data"] = "I2C Read of %d = 0x%x" % (regAddr, data)
        retStatus["level"] = "success"
    else:
        retStatus["data"] = "I2C Access Failure"
        retStatus["level"] = "danger"

    return json.dumps(retStatus)

def i2cWrite(hw_access_handle, data):
    """
    write through i2c
    """
    retStatus = {}
    devAddr = int(data["i2cDevAddr"][0], 16)
    busSel = int(data["i2cBusSel"][0], 16)
    regAddr = int(data["i2cRegAddr"][0], 10)
    try:
        writeData = int(data["i2cData"][0], 16)
    except:
        writeData = ""
    if str(writeData):
        try:
            hw_access_handle.i2c.write(devAddr, busSel, regAddr, writeData)
            retStatus["data"] = "I2C Write Succeded to %d with value of 0x%x" % (regAddr, writeData)
            retStatus["level"] = "success"
        except:
            retStatus["data"] = "I2C Access Failure"
            retStatus["level"] = "danger"
    else:
        retStatus["data"] = "Write Data is invalid!"
        retStatus["level"] = "danger"

    return json.dumps(retStatus)

def bar1Read(hw_access_handle, data):
    """
    read through bar1
    """
    retStatus = {}
    regAddr = int(data["bar1Addr"][0], 16)
    data = hw_access_handle.bar1.read(regAddr)
    logger.info("Bar1 read returned 0x%x" % data)
    if str(data):
        retStatus["data"] = "Bar1 Read of 0x%x = 0x%x" % (regAddr, data)
        retStatus["level"] = "success"
    else:
        retStatus["data"] = "Bar 1 PCI Failure"
        retStatus["level"] = "danger"

    return json.dumps(retStatus)

def bar1Write(hw_access_handle, data):
    """
    write through bar1
    """
    retStatus = {}
    regAddr = int(data["bar1Addr"][0], 16)
    try:
        writeData = int(data["bar1Data"][0], 16)
    except:
        writeData = ""
    if str(writeData):
        try:
            hw_access_handle.bar1.write(regAddr, writeData)
            retStatus["data"] = "Bar 1 Write to 0x%x succeded with value of 0x%x" % (regAddr, writeData)
            retStatus["level"] = "success"
        except:
            retStatus["data"] = "Bar 1 PCI Failure"
            retStatus["level"] = "danger"
    else:
        retStatus["data"] = "Write Data is invalid"
        retStatus["level"] = "danger"

    return json.dumps(retStatus)

def recoverLink(hw_access_handle, data):
    """
    port specific link recovery
    """
    return json.dumps(hw_access_handle.port.recoverLink())

def handlePostRequest(data, hw_access_handle):
    postFunctions = {}
    postFunctions["FEC"] = setFEC
    postFunctions["AN"] = setAN
    postFunctions["MdioRead"] = mdioRead
    postFunctions["MdioWrite"] = mdioWrite
    postFunctions["I2cRead"] = i2cRead
    postFunctions["I2cWrite"] = i2cWrite
    postFunctions["Bar1Read"] = bar1Read
    postFunctions["Bar1Write"] = bar1Write
    postFunctions["RecoverLink"] = recoverLink

    # unfortunately in jQuery each post request value is in an array

    if data["Attribute"][0] in postFunctions.keys():
        postFunction = postFunctions[data["Attribute"][0]]
        return postFunction(hw_access_handle, data)
    else:
        logger.error("Unsupported post request for attribute %s" % data["Attribute"][0])
        return "Error Unsupported Post Function"
