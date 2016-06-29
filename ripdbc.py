#!/usr/bin/python
import os
import time
import serial

def filename(i):
  return str(i) + '.rad'

def open_chrome():
  return serial.Serial('/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0', 57600)

def open_kosmo():
  return serial.Serial('/dev/serial/by-id/usb-FTDI_FT232R_USB_UART_A5005Y58-if00-port0', 115200)

def open_file():
  logdir = 'data'
  try:
    os.mkdir(logdir)
  except:
    pass
  files = os.listdir(logdir)

  i=0
  while (True):
    if not (filename(i) in files):
      break
    i += 1

  return open(logdir + '/' + filename(i), 'w')

def parse_packet(packet):
  length = len(packet)
  result = 0
  for i in range(length):
    result |= (packet[length - 1 - i] & 0x7F) << 7*i
  return result

def read_packet(port):
  while True:
    data = ord(port.read(1))
    if (data & 0x80) != 0:
      packet = [data] + map(ord, port.read(2))
      return parse_packet(packet)

def main():
  #outfile = open_file()
  port = open_kosmo() # the detector
  chrome = open_chrome() # the LED panel

  lasttime = time.time()
  count = 0
  chrome.write("127")
  time.sleep(1)
  while True:
    data=read_packet(port)
    if data > 600000:
      print data
      smallData = (data>>12) & 0x1FF
      print str(smallData)
      chrome.write(str(smallData))
      time.sleep(0.05)
  #  outfile.write(str(read_packet(port)))
  #  outfile.write('\n')
      count += 1
    if time.time() - lasttime  > 60:
      lasttime = time.time()
  #    outfile.write('time ')
  #    outfile.write(str(int(time.time())))
  #    outfile.write('\n')
      print count
      count = 0
    #outfile.flush()

  #outfile.close()
  port.close()
  chrome.close()

if __name__ == "__main__":
  main()
