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
          descr = spl[3] # name of CAN data              spl[3] not begin with lowercase ^^^
          line = getLine(inFile)
          spl = line.split()
          if ((len(spl) == 2) and (spl[0]=='DCD') and (len(spl[1]) >= 5) and (len(spl[1]) <= 6)):
              canid = spl[1]
              print(canid+'\t'+descr)

if __name__ == "__main__":
  main()
