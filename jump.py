#!/usr/bin/env python
#-*-: coding=utf-8 -*-

usage = '''
*******************************************************
pip install pygame --user -U

1. 开发者选项中开启 "允许通过 USB 调试修改权限或模拟点击"
*******************************************************
'''

print usage

import pygame
from pygame.locals import *
from sys import exit
import math
import subprocess
import shlex
import time

# android screen
results = str(subprocess.Popen(['adb shell wm size'],stdout=subprocess.PIPE, shell=True).communicate()[0]).strip()
res = results.replace('Physical size: ', '').split('x')
phonewidth, phoneheight = int(res[0]), int(res[1])

#
height = 640
width = height * phonewidth / phoneheight
scale = float(height) / float(phoneheight)

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("jump: 退出(esc) 点击起点和终点")

background = pygame.image.load("1.png").convert()
background = pygame.transform.scale(background, (width, height))
screen.blit(background, (0,0))

stack = []
speed = 480


def toPhone(x):
    return x/scale

def sqr(x):
    return x * x

def dis(p1, p2):
    return math.sqrt(sqr(p1[0] - p2[0]) + sqr(p1[1] - p2[1]))

def do_jump():
    st = stack[0]
    ed = stack[1]
    d = dis(st, ed)
    t = d / speed
    print t

    stack.pop()
    stack.pop()

    # adb shell input swipe x y x y time(ms)
    cmd = "adb shell input swipe %d %d %d %d %d" % (toPhone(st[0]),
        toPhone(st[1]),
        toPhone(ed[0]),
        toPhone(ed[1]), t * 1000)
    # print (cmd)
    subprocess.call(cmd, shell=True)

def refresh():
    cmd = "adb shell /system/bin/screencap -p /sdcard/1.png"
    # print cmd
    subprocess.call(cmd, shell=True)

    cmd = "adb pull /sdcard/1.png 1.png"
    # print cmd
    subprocess.call(cmd, shell=True)
    background = pygame.image.load("1.png").convert()
    background = pygame.transform.scale(background, (width, height))
    # print background
    screen.blit(background, (0,0))
    pygame.display.flip()

last = time.time()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        if event.type == MOUSEBUTTONDOWN:
            stack.append(event.pos)
            if len(stack) == 2:
                do_jump()
        if event.type == KEYDOWN:
            if event.key == 27: # esc
                exit(0)
            if event.key == 32: # space
                refresh()
    curr = time.time() - last
    if curr > 1:
        curr = time.time()
        refresh()
    pygame.display.update()
