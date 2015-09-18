"""
module to create json responses
main function will create three json files
each json file will have one object 
{key = attributeName : value = attributeValue}
response will be board family json file and protocol json files
"""
import sys
sys.path.append("/usr/spirent/pymodule")
from colossus import Mdio, I2c, Colossus
import json
import time
import threading
import logging
import logging.handlers
import os

LAYER1_PATH = "/usr/spirent/stcl1"
LOGFILE_PATH = LAYER1_PATH + "/logs"
LOGFILE = LOGFILE_PATH + "/hwaccess.log"
JSON_INPUT_PATH = LAYER1_PATH + "/json/colossus.json"

def setupLogging(loglevel='INFO'):
    """
    Configures logging for hw access reads and writes
    """
    global logger
    if not os.path.exists(LOGFILE_PATH):
        # create log path if first time calling script
        os.mkdir(LOGFILE_PATH)
    logLevelNum = getattr(logging, loglevel, None)
    logFormatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger = logging.getLogger('hwaccess')
    logger.setLevel(logLevelNum)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.DEBUG)
    logger.addHandler(consoleHandler)

    fileHandler = logging.handlers.RotatingFileHandler(LOGFILE, maxBytes=0x10000, backupCount=4)
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)


def get_hw_info(protocol, json_data):
    """
    main thread function to retrieve data
    @param protocol to filter
    @param json_data to indicate which registers to read
    """
    # intialize hardware access objects
    bar1 = Colossus(1, 1)
    mdio = Mdio()
    i2c = I2c()

    # initialize return operator dictionary
    # return types correspond to types specified in default value of bits
    return_operator_dict = {}
    return_operator_dict['AND'] = lambda data, bitMap: (data & bitMap) == bitMap
    return_operator_dict['EQ'] = lambda data, bitMap: data == bitMap
    return_operator_dict['READ'] = lambda data, bitMap: data

    # initialize combination operator dictionary
    # currently only used to combine numeric data (Power, Counters, etc)
    combination_operator_dict = {}
    combination_operator_dict['SLR'] = lambda data, link_data: data >> 8 + link_data

    memory_map = json_data["memoryMap"]
    for register_map in memory_map:
        # iterate through registers
        for key in register_map.keys():
            # get to register object in register_map
            if "register" in key:
                data = 0
                register = register_map[key]
                address = register["address"]
                try:
                    # check for protocol in register key value
                    if "mdio" in key and protocol == "MDIO":
                        devAddr = register_map["devAddr"]
                        portAddr = register_map["portAddr"]
                        if "slice" in register_map.keys():
                            # if a slice value is specified write it
                            mdio.cfp_adaptor_write(0x1, 0x8000, register_map["slice"])
                        data = mdio.read(portAddr, devAddr, address)
                        logger.info("Mdio Read of address 0x%x with data of 0x%x" % (address, data))

                    elif "i2c" in key and protocol == "I2C":
                        devAddr = register_map["devAddr"]
                        busSel = register_map["busSel"]
                        if "page" in register_map.keys():
                            # if a page is specified for the qsfp write it
                            i2c.qsfp_write(127, register_map["page"])
                        data = i2c.read(devAddr, busSel, address)
                        logger.info("I2c Read of address 0x%x with data of 0x%x" % (address, data))

                    elif "bar1" in key and protocol == "Bar1":
                        data = bar1.read(address)
                        logger.info("Bar1 Read of address 0x%x with data of 0x%x" % (address, data))

                    else:
                        # if no match between keys and protocol don't do anything
                        break

                except:
                    # if data read fails for whatever reason
                    # set data to None
                    # need to set values for bits accordingly
                    e = sys.exc_info()[0]
                    logger.error("Caught error %s" % e)
                    data = None

                for attribute in register["values"]:
                    # iterate through attributes

                    # get the bitMap of the attribute
                    # For example bits[x:y]
                    bitMap = attribute["bitMap"]

                    # get the return operator
                    return_operator = return_operator_dict[attribute["returnOperator"]]

                    if data is not None:
                        # make sure data is valid (no exception occurred in read)
                        ret_val = return_operator(data, bitMap)

                        if "links" in attribute.keys():
                            link_object = attribute["links"]
                            link_register = link_object["register"]
                            link_address = link_register["address"]
                            link_data = None
                            # if there are any links go and get the data
                            if "MDIO" == protocol:
                                link_data = mdio.read(portAddr, devAddr, link_address)
                                logger.info("Mdio Read of address 0x%x with data of 0x%x" % (link_address, link_data))
                            elif "I2C" == protocol:
                                link_data = i2c.read(devAddr, busSel, link_address)
                                logger.info("I2c Read of address 0x%x with data of 0x%x" % (link_address, link_data))
                                
    return True


def main():
    """
    main function to create JSON response
    to HTTP GET requests

    -Implements retrieval of information from FPGA, PHY, and FrontEnd
    -There will be one thread per protocol (Bar1, MDIO, I2C)
    -Locking of MDIO and I2C buses will be handled by httpd to handle concurrency
    -Necessary for Multiport configurations (multiple ports and on one FPGA)

    The http server will handle the suspension of hardware manager as well
    """
    setupLogging()
    logger.info("Running createJsonResponse")
    threads = {}
    protocols = ['Bar1', 'MDIO', 'I2C']
    with open(JSON_INPUT_PATH) as f:
        json_data = json.load(f)
        while True:
            # ensure that each thread starts succesfully
            for protocol in protocols:
                # start each protocol thread
                logger.info("Starting thread for protocol %s" % protocol)
                thread = get_hw_info_thread(protocol, json_data)
                thread.start()
                threads[protocol] = thread

            if len(threads) == len(protocols):
                break

        alive = len(threads)
        while alive:
            time.sleep(0.1)
            alive = sum(1 for protocol in protocols if threads[protocol].isAlive())



class get_hw_info_thread(threading.Thread):
    """
    Thread class implementation for hardware access
    """
    def __init__(self, protocol, json_data):
        """
        Init thread with base class
        set protocol class member
        """
        threading.Thread.__init__(self)
        self.protocol = protocol
        self.json_data = json_data

    def run(self):
        """
        run method for thread
        goes to get hardware information for respective protocol
        """
        for attempts in xrange(0, 3):
            try:
                success = get_hw_info(self.protocol, self.json_data)
                if success:
                    logger.info("Thread for protocol %s is finished!" % self.protocol)
                    break
            except ZeroDivisionError, e:
                logger.error("Caught error %s" % str(e))                    
                pass

            time.sleep(0.5)

if __name__ == '__main__':
    main()
