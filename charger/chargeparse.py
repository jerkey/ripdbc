# opens ks_can2serial canbus logs
# '268:00000000B3000000 16\n'
filename='/home/user/hack/tesla/canhack/charger/chargetwice.log'
#https://misc.flogisoft.com/bash/tip_colors_and_formatting
RESET  = '\033[0m'
GREEN  = '\033[32m'
RED    = '\033[31m'
YELLOW = '\033[33m'

ids = [530,546,770,924,930] # list of CAN IDs we care about
lastMsg = ['                                                                     '] * len(ids)

inFile = open(filename)

for line in inFile:
    if line.find('CAN')!=0:
        id = int(line.split(':')[0],16)
        if id in ids:
            idIndex = ids.index(id)
            if lastMsg[idIndex].split(' ')[0] != line.split(' ')[0]:
                print(str(id)+'\t',end='')
                for i in range(4,len(line.split(' ')[0])):
                    if lastMsg[idIndex][i]==line[i]:
                        print(RESET+line[i],end='')
                    else:
                        print(RED+line[i],end='')
                linetime = int(line[:-1].split(' ')[1])
                mins = int(linetime / (1000*60))
                secs = linetime % 60000 / 1000
                lastMsg[idIndex] = line
                print('\t'+YELLOW+str(mins).zfill(3)+':',end='')
                if secs < 10:
                    print('0',end='')
                print(str(secs)+RESET)
