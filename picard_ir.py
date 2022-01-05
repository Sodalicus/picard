#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2021 Paweł Krzemiński
#
# Distributed under terms of the MIT license.

"""
InfraRed remote control for picard.
It one way communicates with flask app by sending HTTP Post requests,
and so it's completly separate.

Key down event values for my remote:
    69,70,71
    68,64,67
     7,21, 9
    22,25,13
    12,24,94
     8,28,90
    66,82,74

    69,70,71,68,64,67,7,21,9,22,25,13,12,24,94,8,28,90,66,82,74

"""
import evdev
import requests
import time
import socket
from picard_client import send
sock = socket.socket()
addr = ("127.0.0.1", 65000)

#appUrl = "http://127.0.0.1:5000/"
device = evdev.InputDevice('/dev/input/event0')
actions = {70 : "radio", 71 : "noise", 7 : "volumedown", 21 : "volumeup", 12 : "switch", 24: "switch"}

device_switches= [{ "dev_switch" : "1"},{ "dev_switch" : "2"}]

t0 = time.time()
diff = 1



for event in device.read_loop():
    if (event.value) in actions.keys():
        t1 = time.time()
        if (t1 - t0) > diff:
            t0 = time.time()
            if event.value == 12:
                pass
                #requests.post(appUrl+actions[event.value], data = device_switches[0])
                #print(event.value)
            elif event.value == 24:
                pass
                #requests.post(appUrl+actions[event.value], data = device_switches[1])
                #print(event.value)
            else:
                print(actions[event.value])
                send(actions[event.value], addr)
                #requests.post(appUrl+actions[event.value])
                #print(event.value)
    else:
        pass
        #print(event.value)
