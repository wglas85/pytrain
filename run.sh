#!/bin/sh
#
# start pytrain
#
MYDIR=$(cd $(dirname "$0"); pwd)

PYTHONPATH=$MYDIR/src python $MYDIR/src/pytrain/Main.py

