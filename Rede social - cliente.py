#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import select
import time
import socket

read_list = [sys.stdin]
timeout = 1 # segundos

def EnviaTag(linein, udpenvia, dest):
  global last_work_time
  msg = linein
  udpenvia.sendto(msg, dest)
  #print("Enviou: ", linein)

def RecebeMensagem(udprecebe):
  global last_work_time
  udprecebe.settimeout(0.2)
  try:
    msgr, server = udprecebe.recvfrom(1024)
    print(msgr)
  except:
    time.sleep(0.1)
  #udp.close()

def main(PortaCliente, IPServidor, PortaServidor):
  global read_list
  HOST = IPServidor
  PORT = PortaServidor
  udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  udp.bind(("0.0.0.0", PortaCliente))
  dest = (HOST, PORT)

  while read_list:
    ready = select.select(read_list, [], [], timeout)[0]
    if not ready:
        RecebeMensagem(udp)
    else:
      for file in ready:
        line = file.readline()
        if not line:
          read_list.remove(file)
        elif line.rstrip():
          EnviaTag(line, udp, dest)

try:
    PortaCliente = int(sys.argv[1])
    IPServidor = sys.argv[2]
    PortaServidor = int(sys.argv[3])
    main(PortaCliente, IPServidor, PortaServidor)
except KeyboardInterrupt:
  pass