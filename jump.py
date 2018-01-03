#!/usr/bin/env python


import pygame
from pygame.locals import *
from sys import exit
import math
import subprocess
import shlex
import time

pygame.init()

#screen = pygame.display.set_mode((720, 1280), 0, 32)
screen = pygame.display.set_mode((720, 1280), 0, 32)
pygame.display.set_caption("jump")

background = pygame.image.load("1.png").convert()
screen.blit(background, (0,0))

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

def refresh():
    cmd = "adb shell screencap -p /sdcard/1.png"
    print cmd
    subprocess.call(shlex.split(cmd), shell=True)

    cmd = "adb pull /sdcard/1.png ."
    print cmd
    subprocess.call(shlex.split(cmd), shell=True)
    background = pygame.image.load("1.png").convert()
    print background
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
            if event.key == 32: # space
                refresh()
    curr = time.time() - last
    if curr > 1:
        curr = time.time()
        refresh()
    pygame.display.update()
