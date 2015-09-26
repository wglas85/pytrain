#!/usr/bin/python3
#
# start pytrain
#
import os
import sys

MYDIR = os.path.dirname(sys.argv[0])

os.system(MYDIR+"/run.sh")
if len(sys.argv)==1:
    sys.argv.append("10.0.0.6")
os.system("chromium http://%s:8000/index.html"%(sys.argv[1]))
