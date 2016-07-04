#!/usr/bin/python
import os,sys

canIDs = {}

def getLine(file):
    line = file.readline()
    if not line:
        file.close()
        sys.exit()
    return line

def main():
  if not len(sys.argv) == 2:
      print("USAGE: "+sys.argv[0]+" exapmle.dbc exapmle.csv")
      print("outputs to stdout")
      sys.exit(1)
  dbcFile = open(sys.argv[1],'r') # dbc file for CAN IDs
  csvFile = open(sys.argv[2],'r') # csv file to translate
  line = getLine(dbcFile)
  while not (line.find('BO_')==0): # seek to DBC defines
      line = getLine(dbcFile)
  while (line.find('BO_')==0) and line:
      spl = line.split()
      canIDs[int(spl[1])] = spl[2][0:-1] # store DBC records in RAM without trailing :
      line = getLine(dbcFile)
  dbcFile.close()
  print(getLine(csvFile)) # swallow Time Stamp,ID,Extended,Dir,Bus,LEN,D1,D2,D3...
  line = getLine(csvFile)
  startTime = int(line.split(',')[0])
  while line:
      spl = line.split(',')
      spl.append(canIDs[int(spl[1])])
      lineTime = int(spl[0])/1000.0
      print(lineTime+','+spl[-1]+','+spl[4]+','+spl[5]+','+spl[6]+','+spl[7]+','+spl[8]+','+spl[9]+','+spl[10]+','+spl[11]+','+spl[12]+','+spl[13])
      line = getLine(csvFile)
  csvFile.close()
  sys.exit(0)

if __name__ == "__main__":
  main()
