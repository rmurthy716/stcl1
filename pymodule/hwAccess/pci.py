from __future__ import with_statement
import mmap
import os
import time
import struct

import mmap_spirent
import popen2

class Pci:
    """
    Class for accessing a memory mapped FPGA over PCI. This just
    low level register reads/writes, without interpreting the
    register meanings in any way.
    """
    def __init__ (self, pci_device_id, resource_number, port_number=0):
       # This is for Yocto VM

       # following could be the output of lspci command for our device
       # '00:03.0 0580: 174a:0b03 -> port # 1
       # '00:04.0 0580: 174a:0b03 -> port # 2
       # we are interested in first word which is the PCI endpoint address
       r, w, e = popen2.popen3( 'lspci | grep ' + pci_device_id)

       # first line in the output is for 1st port
       # second line in the output is for 2nd port...
       while port_number is not -1:
           line = r.readline()
           port_number -= 1

       r.close()
       w.close()
       e.close()
       # port 1 on wraith uses  "/sys/bus/pci/devices/0000:00:03.0/resource2"
       dev_name =  ''.join( ('/sys/bus/pci/devices/0000:', line.split()[0], '/resource', str(resource_number) ) )
       size = os.stat(dev_name).st_size

       with open(dev_name, 'rw+') as self.file:
           self.mmap = mmap_spirent.mmap_spirent (self.file.fileno(), size, mmap.MAP_SHARED, mmap.PROT_READ | mmap.PROT_WRITE,offset=0)

    def _read_32(self, address):
        self.mmap.seek(address, os.SEEK_SET)
        result = self.mmap.read32()
        result = result % (1 << 32)     # Ensure positive
        return result

    def _write_32 (self, address, data):
        self.mmap.seek (address, os.SEEK_SET)
        if data >= 0x80000000:
            data -= 0x100000000
        self.mmap.write32(data)

    def adjust_address (self, address, offset):
        #
        # Always use a dword aligned address, adjusting the offset in
        # a little-endian way if necessary. Need to do this because the
        # icebaby PCI is broken for byte and word (16 bit) access.
        #
        # Adjust the address to a word, compensating the bit offset
        # accordingly.
        #
        offset  += (address & 3) * 8
        address &= ~3
        #
        # Make sure the offset is less than 32 - the address must include
        # the first word of the data.
        #
        address += 4 * (offset / 32)
        offset  %= 32

        return (address, offset)

    def read (self, address, length = 32, offset = 0):
        address, offset = self.adjust_address (address, offset)
        result = 0
        result_bits = 0

        while length > 0:
            data = self._read_32 (address)
            address += 4
            data >>= offset
            if offset + length >= 32:
                #
                # Starts in this word, goes at least to the top of it
                # (and perhaps beyond.)
                #
                result |= data << result_bits
                result_bits += 32 - offset
                length -= 32 - offset
            else:
                #
                # Entirely contained in this word.
                #
                mask = ~(0xFFFFFFFF << length)
                data &= mask
                result |= data << result_bits
                result_bits += length
                length = 0
        return result

    def write (self, address, data, length = 32, offset = 0):
        address, offset = self.adjust_address (address, offset)

        while length > 0:
            if offset == 0 and length >= 32:
                #
                # Easy (and common) case: a complete word. Just write it.
                #
                self._write_32 (address, data & 0xFFFFFFFF)
                length -= 32
                address += 4
                data = data >> 32
            elif offset + length >= 32:
                #
                # Starts in this word, goes at least to the top of it
                # (and perhaps beyond.)
                #
                mask = (0xFFFFFFFF << offset) & 0xFFFFFFFF
                word = self._read_32 (address)
                word &= ~mask
                word |= (data << offset) & mask
                self._write_32 (address, word)
                address += 4
                length -= (32 - offset)
                data = data >> offset
                offset = 0
            else:
                #
                # Entirely contained in this word.
                #
                mask = (0xFFFFFFFF >> (32 - length)) << offset
                word = self._read_32 (address)
                word &= ~mask
                word |= (data << offset) & mask
                self._write_32 (address, word)
                length = 0

