"""
helper class to retrieve board specific
hardware object handles
"""
import sys
sys.path.append("/usr/spirent/bin/pysysmgr")
import portColossus
import portProteus
#import iceman
#import wraith
import phxhal

boardFamily = phxhal.getBoardFamilyName()

def getBar0Handle(port):
    """
    function to get Bar0 handle
    """
    if boardFamily == 'COLOSSUS':
        return portColossus.Colossus(0, port)

    elif boardFamily == 'PROTEUS':
        return portProteus.Proteus(0, port)

    elif boardFamily == 'WRAITH':
        return Wraith(0, port)

    elif boardFamily == 'ICEMAN':
        return Iceman(0, port)

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
        return wraith.Wraith(2, port)
    
    elif boardFamily == 'ICEMAN':
        return iceman.Iceman(1, port)
            
def getMdioHandle(port):
    """
    function to get Mdio handle
    """
    if boardFamily == 'COLOSSUS':
        return portColossus.Mdio(port)

    elif boardFamily == 'PROTEUS':
        return portProteus.Mdio(port)

    elif boardFamily == 'WRAITH':
        return wraith.Mdio(port)

    elif boardFamily == 'ICEMAN':
        return iceman.Mdio(port)
            
def getI2cHandle(port):
    """
    function to get I2c handle
    """
    if boardFamily == 'COLOSSUS':
        return portColossus.I2c(port)

    elif boardFamily == 'PROTEUS':
        return portProteus.I2c(port)
    
    elif boardFamily == 'WRAITH':
        return wraith.I2c(port)

    elif boardFamily == 'ICEMAN':
        return iceman.I2c(port)
            
