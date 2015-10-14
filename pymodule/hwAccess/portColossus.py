"""
Port Colossus Module
"""
import time
from pci import Pci
from Mdio import Mdio
from I2c import I2c
from l1constants import bit, invert
# Bar 0 Registers

MDIO_CMD_REG = 0x0078
MDIO_DATA_REG = 0x007c
I2C_CMD_REG = 0x0044

# Bar 1 Registers
FRAMER_PCS_PMA = 0x204
LOCAL_FAULT = bit(0)
REMOTE_FAULT = bit(1)
RX_GTH_RESET = bit(11)
RX_CORE_RESET = bit(12)

STICKY_REGISTER = 0x208
HSEC_ERROR = bit(2)
# MDIO and I2C Constants
CFP_PORT_ADDR = 0x1
GEARBOX_PORT_ADDR = 0x0
CFP_ADAPTOR_PORT_ADDR = 0xe
DEVICE_1 = 0x1
DEVICE_7 = 0x7
FEC_CONTROL = 0x8a05
GEARBOX_LOOPBACK = 0xf457
GEARBOX_COMMON_CTRL1 = 0xf402
RX_GB_RESET = bit(8)
RPTR_SYNC = 0xd0a0
SYNC_STATUS = bit(0)
SLICE_REGISTER = 0x8000
LOGIC_TO_PHY_LANE0_MAP = 0x8a08
AN_ADVERTISEMENT_3 = 0x12
AN_ADVERTISEMENT_2 = 0x11
AN_ADVERTISEMENT_1 = 0x10
AN_CONTROL = 0x0
FRONT_PANEL = 0x8a03
AN_TRIGGER = 0x8235
MAX_FW_READ_COUNT = 30

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

    def writeSelectedBits(self, address, mask, data):
        """
        function to write only selected bits
        """
        # read back value first
        value = self.read(address)
        # get all bits that are high and not in mask
        value &= invert(mask)
        # get bits that are high in mask
        value |= (data & mask)
        # write back what we want
        self.write(address, value)


class MdioAccess():
    """
    Mdio Access Class
    """
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

    def gearbox_read(self, regAddr):
        return self.mdio.read(GEARBOX_PORT_ADDR, DEVICE_1, regAddr)

    def gearbox_write(self, regAddr, data):
        self.mdio.write(GEARBOX_PORT_ADDR, DEVICE_1, regAddr, data)

    def cfp_adaptor_read(self, devAddr, regAddr):
        return self.mdio.read(CFP_ADAPTOR_PORT_ADDR, devAddr, regAddr)

    def cfp_adaptor_write(self, devAddr, regAddr, data):
        self.mdio.write(CFP_ADAPTOR_PORT_ADDR, devAddr, regAddr, data)

    def writeSelectedBits(self, devAddr, portAddr, regAddr, mask, data):
        mdio_data = self.read(devAddr, portAddr, regAddr)
        mdio_data &= invert(mask)
        mdio_data |= data
        # mdio data is only 16 bits in width
        mdio_data &= 0xffff
        self.write(devAddr, portAddr, regAddr, mdio_data)

class I2cAccess():
    """
    I2c Access Class
    """
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


class Port():
    """
    Port Handle Class
    """
    def __init__(self, port):
        """
        port class for Colossus
        """
        self.bar1 = Colossus(1, port)
        self.i2c = I2cAccess(port)
        self.mdio = MdioAccess(port)


    def setFEC(self, enable):
        """
        set FEC configuration
        """
        # get back data first
        data = self.mdio.cfp_adaptor_read(DEVICE_1, FEC_CONTROL)
        # only set the configuration if it has changed
        value = (data | bit(3)) if enable else (data & invert(bit(3)))
        self.mdio.cfp_adaptor_write(DEVICE_1, FEC_CONTROL, value)
        time.sleep(0.5)
        return ""

    def setAN(self, enable):
        """
        set AN configuration
        """
        # select lane 0
        self.mdio.cfp_adaptor_write(DEVICE_7, SLICE_REGISTER, 0x3b80)
        # set lane0 for AN DME
        self.mdio.cfp_adaptor_write(DEVICE_1, LOGIC_TO_PHY_LANE0_MAP, 0x203)

        if enable:
            # AN Adv3 bit14=1 FEC Ability
            self.mdio.cfp_adaptor_write(DEVICE_7, AN_ADVERTISEMENT_3, 0x4000)
            # AN Adv2 bit13=1 100G-CR4
            self.mdio.cfp_adaptor_write(DEVICE_7, AN_ADVERTISEMENT_2, 0x2000)
            # AN Adv1
            self.mdio.cfp_adaptor_write(DEVICE_7, AN_ADVERTISEMENT_1, 0x1)
            # Enable/Restart AN process
            self.mdio.cfp_adaptor_write(DEVICE_7, AN_CONTROL, 0x1200)
            # PHY= Front Panel
            self.mdio.cfp_adaptor_write(DEVICE_1, FRONT_PANEL, 0x1)
            # trigger FW changes
            self.mdio.cfp_adaptor_write(DEVICE_1, AN_TRIGGER, 0x1)
            data = 0xffff
            read_count = 0
            while (data & bit(0) != 0x0) and read_count < MAX_FW_READ_COUNT:
                data = self.mdio.cfp_adaptor_read(DEVICE_1, AN_TRIGGER)
                read_count += 1
            time.sleep(1)

        else:
            # reset and disable AN
            self.mdio.cfp_adaptor_write(DEVICE_7, AN_CONTROL, 0x8000)
            # trigger changes
            self.mdio.cfp_adaptor_write(DEVICE_1, AN_TRIGGER, 0x1)
            while (data & bit(0) != 0x0) and read_count < MAX_FW_READ_COUNT:
                data = self.mdio.cfp_adaptor_read(DEVICE_1, AN_TRIGGER)
                read_count += 1
            time.sleep(0.01)
            # disable AN
            self.mdio.cfp_adaptor_write(DEVICE_7, AN_CONTROL, 0x0)
            # trigger changes
            self.mdio.cfp_adaptor_write(DEVICE_1, AN_TRIGGER, 0x1)
            while (data & bit(0) != 0x0) and read_count < MAX_FW_READ_COUNT:
                data = self.mdio.cfp_adaptor_read(DEVICE_1, AN_TRIGGER)
                read_count += 1
            time.sleep(0.2)

        return ""

    def recoverLink(self):
        """
        link recovery method
        """
        retStatus = {}
        # first check link and only recovery if there are any local faults
        link_data = self.bar1.read(FRAMER_PCS_PMA)
        sticky_data = self.bar1.read(STICKY_REGISTER)
        if not bool(link_data & LOCAL_FAULT) and not bool(sticky_data & LOCAL_FAULT):
            # link is up don't recover
            retStatus["data"] = "Link Recovery done! Link is UP"
            retStatus["level"] = "success"
            return retStatus

        # link is down proceed with recovery
        self.gearboxLoopback(True)
        self.repeaterSync()
        self.gearboxLoopback(False)

        self.gearboxLoopback(True)
        self.resetRxDatapath()
        self.gearboxLoopback(False)

        # check link status and return it
        link_data = self.bar1.read(FRAMER_PCS_PMA)
        hsec_error = self.bar1.read(STICKY_REGISTER) & HSEC_ERROR
        if link_data & LOCAL_FAULT:
            retStatus["data"] = "Link Recovery failed! Detected Local Fault!"
            retStatus["level"] = "danger"
        elif link_data & REMOTE_FAULT:
            retStatus["data"] = "Link Recovery done! Detected Remote Fault!"
            retStatus["level"] = "danger"
        elif hsec_error:
            retStatus["data"] = "Link Recovery done! Detected Fpga Core Errors!"
            retStatus["level"] = "danger"
        else:
            retStatus["data"] = "Link Recovery done! Link is UP"
            retStatus["level"] = "success"

        return retStatus

    def gearboxLoopback(self, enable):
        """
        method to put gearbox in and out of loopback
        """
        value = 0x3ff if enable else 0
        print "Setting gearbox loopback to %s" % enable
        self.mdio.gearbox_write(GEARBOX_LOOPBACK, value)

    def repeaterSync(self):
        """
        method to synchronize lanes
        """
        data = self.mdio.cfp_adaptor_read(DEVICE_1, RPTR_SYNC)
        if not data & SYNC_STATUS:
            # lanes are not synced
            print "Lanes not synced! Syncing lanes!"
            self.mdio.cfp_adaptor_write(DEVICE_1, SLICE_REGISTER, 0x0bf0)
            self.mdio.cfp_adaptor_write(DEVICE_1, RPTR_SYNC, 0x7083)

    def resetRxDatapath(self):
        """
        method to reset rx datapath
        """
        # clear initial resets
        self.mdio.writeSelectedBits(0x1, 0x0, GEARBOX_COMMON_CTRL1, RX_GB_RESET, RX_GB_RESET)
        self.bar1.writeSelectedBits(FRAMER_PCS_PMA, (RX_GTH_RESET | RX_CORE_RESET), 0x0)

        """
        Reset Sequence:
        1) assert Xilinx HSEC Rx reset
        2) assert Broadcom Rx datapath reset
        3) deassert Broadcom Rx datapath reset
        4) deassert Xilinx HSEC Rx Reset
        """
        # put Rx Core in Reset
        self.bar1.writeSelectedBits(FRAMER_PCS_PMA, RX_CORE_RESET, RX_CORE_RESET)
        time.sleep(0.001)
        # put Gearbox in Rx Reset
        self.mdio.writeSelectedBits(0x1, 0x0, GEARBOX_COMMON_CTRL1, RX_GB_RESET, 0x0)
        time.sleep(0.1)
        # take GB out of Rx Reset
        self.mdio.writeSelectedBits(0x1, 0x0, GEARBOX_COMMON_CTRL1, RX_GB_RESET, RX_GB_RESET)
        time.sleep(0.2)
        print "Resetting Rx Gearbox Done!"
        # take Rx Core out of Reset
        self.bar1.writeSelectedBits(FRAMER_PCS_PMA, RX_CORE_RESET, 0x0)
        # basically waiting for GTH Done bit
        time.sleep(0.8)
        print "Resetting HSEC Rx Core done!"
