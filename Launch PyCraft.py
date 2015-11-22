import sys
sys.stderr = open("error.log","a")
#sys.stdout = open("debug.log","w")
import easygui
from version import *
import master


master.remote_main()
