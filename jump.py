#!/usr/bin/env python

import pygame
from pygame.locals import *
from sys import exit
import math
import subprocess
import shlex
import time
import threading
import string
import Queue

pygame.init()

screen = pygame.display.set_mode((720, 1280), pygame.DOUBLEBUF, 32)
pygame.display.set_caption("jump-assistant")

background = pygame.image.load("1.png").convert()
screen.blit(background, (0, 0))

stack = []
speed = 480

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
    cmd = "adb shell input swipe %d %d %d %d %d" % (st[0], st[1], ed[0], ed[1], t * 1000)
    subprocess.call(cmd)
    print cmd

class ImageLoader(threading.Thread):
    def __init__(self, que, ev):
        threading.Thread.__init__(self)
        self.que = que
        self.ev = ev

    def run(self):
        print "start..."
        while True:
            cmd = "adb shell screencap -p /sdcard/1.png"
            proc = subprocess.Popen(shlex.split(cmd), shell=True)
            proc.wait()

            cmd = "adb pull /sdcard/1.png ."
            proc = subprocess.Popen(shlex.split(cmd), shell=True)
            proc.wait()
            img = pygame.image.load("1.png").convert()
            if img != None:
                self.que.put(img)
            if self.ev.wait(0.1) == True:
                break

ev = threading.Event()
images = Queue.Queue()
loader = ImageLoader(images, ev)
loader.start()

last = time.time()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            ev.set()
            loader.join()
            exit()
        if event.type == MOUSEBUTTONDOWN:
            stack.append(event.pos)
            if len(stack) == 2:
                do_jump()
    try:
        img = images.get_nowait()
        screen.blit(img, (0, 0))
    except:
        pass
    pygame.display.flip()