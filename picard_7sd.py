# /usr/bin/env python3
# -*- codng: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Paweł Krzemiński 
#
# Distributed under terms of the MIT license.

"""

"""
import time
import socket, sys
import selectors, logging

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment

#sel = selectors.DefaultSelector()
#logging.basicConfig(format="%(asctime)s %(message)s",
#                    filename="/home/pi/Picard/log.txt", datefmt="%y.%m.%d %H:%M:%S")

#addr = ("127.0.0.1", 65000)

class SevenSegDisplay():

    def __init__(self):
        serial = spi(port=0, device=0, gpio=noop())
        device = max7219(serial, cascaded=1)
        device.contrast(15)
        self.seg = sevensegment(device)
        self.update_clock()
        self.messages = []
        self.t0 = time.time()

    def update_clock(self):
        text = time.strftime("%H%M")
        self.seg.text = str(text)[0:8]# 7 seg can only display 8 digits

    def update(self):
        t1 = time.time()
        if len(self.messages) == 0 and ((t1 - self.t0) > 5):
            self.update_clock()
            self.t0 = time.time()
        elif len(self.messages) > 1 and (t1 - self.t0) > 2:
            self.seg.text = self.messages.pop()[0:8]
            self.t0 = time.time()



    def msg(self,mess):
        #self.messages.append(mess)
        text = mess
        self.seg.text = str(text)[0:8] # 7 seg can only display 8 digits



def main():

    def accept(sock, mask):
        conn, addr = sock.accept()
        print('accepted', conn, 'from', addr)
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, read)

    def read(conn, mask):
        try:
            data = conn.recv(1024)
        except:
            print("error")
            logging.error(sys.exc_info()[0])
            return 0

        if data:
            info = "Received data form client " + repr(data) + repr(conn)
            logging.warning(info)
            display.msg(data.decode()[0:8])
            print(data)
        else:
            logging.warning(sys.exc_info()[0])
            sel.unregister(conn)
            conn.close()

    sock = socket.socket()
    sock.bind(addr)
    sock.listen(5)
    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, accept)

    display = SSDisplay()
    #s = create_socket()
    #s.setblocking(0)
    t0 = time.time()

    while True:
        t1 = time.time()
        if (t1 - t0 ) > 20:
            display.update_clock()
            t0 = time.time()

        events = sel.select(timeout=0)
        for key, mask in events:
            callback = key.data
            callback(key.fileobj, mask)


if __name__ == '__main__':
    main()
