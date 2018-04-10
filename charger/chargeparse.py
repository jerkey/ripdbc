#!/usr/bin/env python3
# based on cantldr.py by jerkey
# opens ks_can2serial canbus logs generated by https://github.com/jerkey/ks_can/blob/teslalog/ks_can2serial.ino
inFile = open('/tmp/can2serial.txt')
RESET  = '\033[0m' # https://misc.flogisoft.com/bash/tip_colors_and_formatting
GREEN  = '\033[32m'
RED    = '\033[31m'
YELLOW = '\033[33m'

ids = [530,546,770,924,930] # list of CAN IDs we care about
lastMsg = ['                                                                     '] * len(ids) # empty so it's not too short to compare with

def parseCan(id,data):
    message = ''
    if id==530:
        BMS_contactorState = int(data[5],16) # lower 4 bits of third byte
        BMS_state = int(data[4],16) # high 4 bits of third byte
        BMS_contactorStateText = {6:"BMS_CTRSET_CLEANING",5:"BMS_CTRSET_WELD",4:"BMS_CTRSET_SNA",3:"BMS_CTRSET_OPENING",2:"BMS_CTRSET_CLOSED",1:"BMS_CTRSET_PRECHARGE",0:"BMS_CTRSET_OPEN"}
        BMS_stateText = {15:"BMS_SNA",8:"BMS_WELD",7:"BMS_FAULT",6:"BMS_CLEARFAULT",5:"BMS_CHARGERVOLTAGE",4:"BMS_FASTCHARGE",3:"BMS_CHARGER",2:"BMS_SUPPORT",1:"BMS_DRIVE",0:"BMS_STANDBY"}
        message += 'BMS_contactorState:'+BMS_contactorStateText.get(BMS_contactorState,' ').ljust(20) + ' BMS_state:' + BMS_stateText.get(BMS_state,' ').ljust(18)
    else:
        message = data
    return message

for line in inFile: # '268:00000000B3000000 16\n' is what a line looks like
    if line.find('CAN')!=0: # swallow the init lines from ks_can2serial.ino
        id = int(line.split(':')[0],16)
        if id in ids: # we ignore CAN IDs not in our list
            idIndex = ids.index(id)
            if lastMsg[idIndex].split(' ')[0] != line.split(' ')[0]: # ignore messages that haven't changed since we last saw them
                print(str(id)+'\t',end='')
                print(parseCan(id,line[4:20]),end='')
                for i in range(4,len(line.split(' ')[0])): # print character by character, colored according to same or changed
                    if lastMsg[idIndex][i]==line[i]:
                        print(RESET+line[i],end='')
                    else:
                        print(RED+line[i],end='')
                for i in range(len(line[4:].split(' ')),16): # pad data with spaces out to 16 characters
                        print(' ',end='')
                linetime = int(line[:-1].split(' ')[1]) # get the time in milliseconds from the log
                mins = int(linetime / (1000*60))
                secs = linetime % 60000 / 1000
                lastMsg[idIndex] = line # store the latest line to compare with for next time
                print('\t'+YELLOW+str(mins).zfill(3)+':',end='') # print the number of minutes:
                if secs < 10:
                    print('0',end='')
                print(str(secs)+RESET) # print the number of seconds (a float) and ANSI RESET

