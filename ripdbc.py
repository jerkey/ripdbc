#!/usr/bin/python
import os,sys

def getLine(file):
    line = file.readline()
    if not line:
        file.close()
        sys.exit()
    return line

def main():
  inFile = open(sys.argv[1],'r')
  line = getLine(inFile)
  while not (line.find('BDY_messages')==0):
      line = getLine(inFile)
  while True:
      line = getLine(inFile)
      spl = line.split()
      if ((len(spl) == 4) and (spl[0]=='DCD') and (spl[2]==';') and (ord(spl[3][1]) & 32 == 0)):
          descr = spl[3][1:-1] # strip "" from name of CANid       not begin with lowercase ^^^
          line = getLine(inFile)
          spl = line.split()
          if ((len(spl) == 2) and (spl[0]=='DCD') and (len(spl[1]) >= 5) and (len(spl[1]) <= 6)):
              canid = spl[1]
              canid_dec = int(canid,16) #convert from hex string to integer
              print("BO_ "+str(canid_dec)+' '+descr+': 0 Vector__XXX')

if __name__ == "__main__":
  main()
