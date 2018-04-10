# opens ks_can2serial canbus logs
# '268:00000000B3000000 16\n'
filename='/home/user/hack/tesla/canhack/charger/chargetwice.log'

ids = [530,546,770,924,930] # list of CAN IDs we care about
lastMsg = [''] * len(ids)

inFile = open(filename)

for line in inFile:
    if line.find('CAN')!=0:
        id = int(line.split(':')[0],16)
        if id in ids:
            idIndex = ids.index(id)
            if lastMsg[idIndex].split(' ')[0] != line.split(' ')[0]:
                lastMsg[idIndex] = line
                print line[:-1] # remove the trailing newline from the line
