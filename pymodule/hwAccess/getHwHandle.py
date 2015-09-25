"""
helper class to retrieve board specific
hardware object handles
"""
import sys
import portColossus
import portProteus
#import iceman
#import wraith
import phxhal
from l1constants import boardFamily

def getBar0Handle(port):
    """
    function to get Bar0 handle
    """
    if boardFamily == 'COLOSSUS':
        return portColossus.Colossus(0, port)

    elif boardFamily == 'PROTEUS':
        return portProteus.Proteus(0, port)

    elif boardFamily == 'WRAITH':
        return portWraith.Wraith(0, port)

    elif boardFamily == 'ICEMAN':
        return portIceman.Iceman(0, port)

def getBar1Handle(port):
    """
    function to get Bar1 handle
    """
    if boardFamily == 'COLOSSUS':
        return portColossus.Colossus(1, port)
    
    elif boardFamily == 'PROTEUS':
        return portProteus.Proteus(1, port)
    
    elif boardFamily == 'WRAITH':
        # Wraith is weird and uses bar2 
        return portWraith.Wraith(2, port)
    
    elif boardFamily == 'ICEMAN':
        return portIceman.Iceman(1, port)
            
def getMdioHandle(port):
    """
    function to get Mdio handle
    """
    if boardFamily == 'COLOSSUS':
        return portColossus.MdioAccess(port)

    elif boardFamily == 'PROTEUS':
        return portProteus.MdioAccess(port)

    elif boardFamily == 'WRAITH':
        return portWraith.MdioAccess(port)

    elif boardFamily == 'ICEMAN':
        return portIceman.MdioAccess(port)
            
def getI2cHandle(port):
    """
    function to get I2c handle
    """
    if boardFamily == 'COLOSSUS':
        return portColossus.I2cAccess(port)

    elif boardFamily == 'PROTEUS':
        return portProteus.I2cAccess(port)
    
    elif boardFamily == 'WRAITH':
        return portWraith.I2cAccess(port)

    elif boardFamily == 'ICEMAN':
        return portIceman.I2cAccess(port)
            
