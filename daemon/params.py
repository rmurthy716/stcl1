#! /usr/bin/env python

import sys
import getopt
import mps.logger as logger
import mps.conn as mpsConn

class Usage(Exception):
    def __init__(self, msg):
        self.args = msg


class Params(object):
    def __init__(self):
        self.startup_fifo = None
        self.redirect_to = None
        self.log_level = logger.ERROR
        self.tcp_port = mpsConn.DEFAULT_MPS_PORT

        opt_chars = 'hs:f:l:p:'
        usage_msg = 'usage: ' + sys.argv[0] + ' [-' + opt_chars + """]
        \t-h prints this help
        \t-s startup fifo name
        \t-l log level
        \t-f trace file (use \"stdout\" for console)
        \t-p mps server port number
        """

        try:
            opts, args = getopt.getopt(sys.argv[1:], opt_chars)
        except getopt.error, msg:
            raise Usage(msg)

        for optname, optvalue in opts:
            print optname, optvalue
            if optname == '-h':
                print usage_msg
                sys.exit(1)

            if optname == '-s':
                self.startup_fifo = optvalue

            if optname == '-l':
                self.log_level = self.translate_log_level(optvalue)

            if optname == '-f':
                self.redirect_to = optvalue

            if optname == '-p':
                self.tcp_port = int(optvalue)

    def translate_log_level(self, level):
        if level >= 7:
            return logger.DEBUG
        elif level == 6:
            return logger.INFO
        elif level == 5:
            return logger.INFO
        elif level == 4:
            return logger.WARNING
        elif level == 3:
            return logger.ERROR
        elif level <= 2:
            return logger.CRITICAL
