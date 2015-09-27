#!/usr/bin/python3
#
# start pytrain
#
import os
import sys
import threading

if len(sys.argv)==1:
    sys.argv.append("10.0.0.6")

if sys.argv[1]!="10.0.0.6":
    MYDIR = os.path.dirname(sys.argv[0])
    Thread_one = threading.Thread(target=lambda:(os.system(MYDIR+"/run.sh")))
    Thread_one.start()

Thread_two = threading.Thread(target=lambda:(os.system("chromium http://%s:8000/index.html"%(sys.argv[1]))))
Thread_two.start()
