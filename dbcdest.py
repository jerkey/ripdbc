#!/usr/bin/python
import os,sys

def getLine(file):
    line = file.readline()
    if not line:
        file.close()
        sys.exit()
    return line

def main():
  inFile = open(sys.argv[1],'r') # open a DBC file
  dest = sys.argv[2] # CAN destination we are looking for
  line = getLine(inFile)
  while True:
      while not (line.find('BO_ ')==0): # seek to the beginning of a CAN ID def
          line = getLine(inFile)
      spl = line.split()
      canid_dec = spl[1]
      canid_int = int(canid_dec,10) # convert from dec string to integer
      canid_hex = hex(canid_int) # convert from int to hex string '0x18'
      canid_name = spl[2] # 'GTW_12VStatus'
      canid_source = spl[4] # 'GTW'
      while len(line) > 2:
          line = getLine(inFile)
          spl = line.split()
          if len(spl) > 0 and spl[-1].find(dest)>=0 and canid_source != dest: # look for dest in listeners
              print(canid_hex+"\t"+canid_name.ljust(20)+"from "+canid_source) # output the CAN ID description and origin
              line = '' # make len(line) zero so this while loop exits

if __name__ == "__main__":
  main()
