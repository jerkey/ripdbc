#!/usr/bin/python
import os,sys

canIDs = {}
IDusage = {}
jC = '\t' # what to join the output fields with

def main():
  if not len(sys.argv) == 3:
      print("USAGE: "+sys.argv[0]+" exapmle.dbc exapmle.csv")
      print("outputs to stdout")
      sys.exit(1)
  dbcFile = open(sys.argv[1],'r') # dbc file for CAN IDs
  csvFile = open(sys.argv[2],'r') # csv file to translate
  line = dbcFile.readline()
  while not (line.find('BO_')==0): # seek to DBC defines
      line = dbcFile.readline()
  while (line.find('BO_')==0) and line:
      spl = line.split()
      canIDs[int(spl[1])] = spl[2][0:-1] # store DBC records in RAM without trailing :
      line = dbcFile.readline()
  dbcFile.close()
  csvFile.readline() # swallow Time Stamp,ID,Extended,Dir,Bus,LEN,D1,D2,D3...
  line = csvFile.readline()
  startTime = int(line.split(',')[0])
  while line:
      spl = line.split(',')
      canID = int(spl[1],16)
      if canIDs.has_key(canID):
          spl.append(canIDs[canID].ljust(25))
      else:
          spl.append('Unknown: '+spl[1].ljust(15))
      if IDusage.has_key(canID):
          IDusage[canID]+=1 # we saw this ID again
          spl.append(IDusage[canID]) # so we can print it
      else:
          IDusage[canID]=1 # first time this canID
          spl.append('first') # so we can print it
      lineTime = (int(spl[0]) - startTime) / 1000000.0
      print(str(lineTime).ljust(8)+jC+spl[-2]+jC+'bus'+spl[4]+jC+spl[5]+jC+spl[6]+jC+spl[7]+jC+spl[8]+jC+spl[9]+jC+spl[10]+jC+spl[11]+jC+spl[12]+jC+spl[13]+jC+str(spl[-1]))
      line = csvFile.readline()
  csvFile.close()
  sys.exit(0)

if __name__ == "__main__":
  main()
