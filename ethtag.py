#!/usr/bin/env python
import dpkt,sys
import binascii
import json
import caneton

if not len(sys.argv) == 3:
  print("USAGE: "+sys.argv[0]+" candata.cap dbcfile.json")
  print("outputs to stdout")
  sys.exit(1)
f = open(sys.argv[1])
with open(sys.argv[2]) as dbc_file:
        dbc_json = json.loads(dbc_file.read())

message_data = binascii.unhexlify('01000000009e7fe0')
pcap = dpkt.pcap.Reader(f)
for ts, buf in pcap:
   print ts,
   eth = dpkt.sll.SLL(buf)
   ip = eth.data
   udp = ip.data
   if isinstance (udp, dpkt.udp.UDP):
      if udp.sport == 20100:
            # print len(udp),''.join(x.encode('hex') for x in str(udp))
            packet=''.join(x.encode('hex') for x in str(udp))
            message_id = int(packet[20:24],16)
            message_data = binascii.unhexlify(packet[24:])
            message_length = len(packet[24:]) / 2 # half the number number of hex characters
            try:
                message = caneton.message_decode(message_id, message_length, message_data, dbc_json)
                print(message)
            except:
                print(packet+'    decode failed ID: 0x'+packet[20:24])
          
      else:
         print "x"
   else:
      print "x"
