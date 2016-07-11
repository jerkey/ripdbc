#!/usr/bin/env python
import dpkt,sys

if not len(sys.argv) == 2:
    print("USAGE: "+sys.argv[0]+" candata.cap")
    print("outputs CSV file for SavvyCAN to stdout")
    sys.exit(1)

capFile = open(sys.argv[1],'r')

startTime = 0 # savvyCAN does not use unixtime

print('Time Stamp,ID,Extended,Dir,Bus,LEN,D1,D2,D3,D4,D5,D6,D7,D8')

pcap = dpkt.pcap.Reader(capFile)
for ts, buf in pcap:
    if startTime == 0:
        startTime = ts
    microSeconds = int((ts - startTime) * 1000000.0)
    eth = dpkt.sll.SLL(buf)
    ip = eth.data
    udp = ip.data
    if isinstance (udp, dpkt.udp.UDP):
        if udp.sport == 20100:
            packet=''.join(x.encode('hex') for x in str(udp))
            message_id = '0000'+packet[20:24]
            message_data = packet[24:]
            message_length = len(packet[24:]) / 2 # half the number number of hex characters
            message_csv = ''
            for i in range(message_length):
                message_csv += message_data[i:i+2]+','
            print(str(microSeconds)+','+message_id+',false,Rx,0,'+str(message_length)+','+message_csv.upper())
        else:
            print "x"
    else:
        print "x"
