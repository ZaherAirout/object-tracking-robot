# -*- coding: utf-8 -*-

import json
from controller import Controller
from server import Server

t = 0.1


def reverse():
    x.move_backward()
    # setLEDs(1, 0, 0, 1)
    # print('straight')


def forwards():
    x.move_forward()
    # setLEDs(0, 1, 1, 0)
    # print('straight')


def turnright():
    x.move_right()
    # setLEDs(0, 0, 1, 1)
    # print('left')


def turnleft():
    x.move_left()
    # setLEDs(1, 1, 0, 0)
    # print('right')


def stopall():
    x.stopall()
    # setLEDs(1, 1, 1, 1)
    # print('stop')


def execute(message):
    json_message = json.loads(message)
    FB = json_message.get("FB")
    LR = json_message.get("LR")
    print(FB + " " + LR + str(len(FB)) + str(len(LR)))
    if FB == "F":
        forwards()

    elif FB == "B":
        reverse()

    elif LR == "L":
        turnleft()

    elif LR == "R":
        turnright()

    elif LR == "S" or FB == "S":
        stopall()

import socket, json

if __name__ == '__main__':
    server = Server(host='192.168.1.18')
    x = Controller()
    print('Server is online \nHost Name : {}:{}'.format(server.HostName, server.Port))
    while True:
        message, address = server.receive()
        print("Got >>", str(message), " form : ", address)
        execute(message.decode("utf-8"))