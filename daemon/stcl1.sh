#!/bin/sh
#
# Don't edit the following line for startup level
# startlevel 30
# @MessageSets : stcl1_1
#
# Description:
# stcl1d startup script
#

#-------------------------------------
# Variable initialization
#-------------------------------------
. /etc/init.d/spirent/spirent_functions

APPNAME=/usr/spirent/stcl1/daemon/stcl1d
FIFONAME=`get_fifo_name $APPNAME`
ARGS="-s $FIFONAME"
NICE=0
EXITCODE=0

#-------------------------------------
# Daemon start/stop routine
#-------------------------------------
run_start_stop $1 $APPNAME $FIFONAME $NICE "$ARGS"

exit $EXITCODE
