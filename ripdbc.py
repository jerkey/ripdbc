#!/usr/bin/python
import os,sys

def main():
  inFile = open(sys.argv[1],'r')
  line = inFile.readline()
  print(1)
  while line.find('CANBusList')==-1:
      line = inFile.readline()
  print(2)
  while line.find('BDY_messages')==-1:
      line = inFile.readline()

  print(3)
  while True:
      line = inFile.readline()
      if not line:
          inFile.close()
          break
      spl = line.split()
      if ((len(spl) == 4) and (spl[0]=='DCD') and (spl[2]==';') and (ord(spl[3][1]) & 32 == 0)):
          descr = spl[3] # name of CAN data              spl[3] not begin with lowercase ^^^
          line = inFile.readline()
          spl = line.split()
          if ((len(spl) == 2) and (spl[0]=='DCD') and (len(spl[1]) >= 5) and (len(spl[1]) <= 6)):
              canid = spl[1]
              print(canid+'\t'+descr)

if __name__ == "__main__":
  main()
