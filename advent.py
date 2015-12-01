import pygame
from pygame.locals import *
from sense_hat import SenseHat
import datetime as dt
import random
import time
import twodigit as td
import threading
import animations as ani

#Set up pygame
pygame.init()
#create a small window 
pygame.display.set_mode((50, 40))

#initialise sensehat and clear LED matrix
sh = SenseHat()
sh.clear()

#Get thh date
day = dt.date.today().day
#Advent calendar ends on Xmas Eve
if day > 24:
    day = 24
day = 5 #testing
#Lists of pngs and animations for each day
pngs = [2,3,4,6,7,8,9,11,12,13,14,16,17,18,19,21,22]
anis = [1,5,10,15,20,23,24]

#define LED grid
O = (0,0,0)
global cal
cal = [
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,

O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, O, O, O, O, O
]

def day2led(day): # calc which 2 LEDs should be lit
    if day % 2 == 1:
        ledPair = (day, day -1)
    else:
        ledPair = (day, day + 1)
    return ledPair

def setDay(): #Create colour grid
    day = dt.date.today().day
    if day > 24:
        day = 24
    day = 5 #testing
    print('drawing grid')
    global x
    global y
    global x1
    global new_x
    global new_y
    global new_x1
    # pick some colours
    r = random.randint(50,200)
    g = random.randint(50,200)
    b = random.randint(50,200)
    for d in range(2*day):
        p = day2led(d)
        if d == 0:
            r = random.randint(50,200)
            g = random.randint(50,200)
            b = random.randint(50,200)
        else:
            # try to get non-similar adjacent day colours 
            while abs(r-r_prev) < 20 and abs(g-g_prev) <20 and abs(b-b_prev) <20:
                r = random.randint(50,200)
                g = random.randint(50,200)
                b = random.randint(50,200)
            
        cal[p[0]] = (r,g,b)
        cal[p[1]] = (r,g,b)
        r_prev = r
        g_prev = g
        b_prev = b
    # draw grid on LED matrix
    sh.set_pixels(cal)
 
    # Calc x and y for a given day value
    y = round((day*2)/8)-1
    if y <= 0:
        y = 0
    x = (2*day - 8*y -2)%8
    x1 = x+1
    new_y = y
    new_x = x
    new_x1 = x1

def DayWatch(): # check to see if its is a brand new day
    while True:
        oldday = dt.date.today().day
        time.sleep(60)
        newday = dt.date.today().day
        #print('checked day')
        if newday != oldday:
            setDay()
            


running = True
# start daywatch as seperate thread
DayWatchThread = threading.Thread(target=DayWatch)
DayWatchThread.start()
setDay()
pos = (x1 - x/2) +8*y/2

print(x,y,pos)
# set starting position for red LED cursor
if x == 0 and y != 0:
    y = y+1
    new_y = y

sh.set_pixel(x, y, 255, 0,0)
sh.set_pixel(x1, y, 255, 0,0)

while running:
    # get all key presses
    for event in pygame.event.get():

        if event.type == KEYDOWN:

            pos = (x1 - x/2) +8*y/2
            
            print('pos: '+ str(pos) + ' x: ' + str(x) + ' y: ' + str(y))
            # cursor navigation
            if event.key == K_DOWN and y < 7:
                new_y = y + 1
            elif event.key == K_UP and y > 0:
                new_y = y - 1
            elif event.key == K_RIGHT and x < 6:
                new_x = x + 2
                new_x1 = x1 +2
            elif event.key == K_LEFT and x > 0:
                new_x = x - 2
                new_x1 = x1 -2
            elif event.key == K_RETURN:
                print('press')
                # display a png or animation
                if pos in pngs:
                    sh.set_rotation(90)
                    sh.load_image("pngs/dec"+str(int(pos))+".png")
                    time.sleep(5)
                    sh.set_rotation(0)
                    sh.set_pixels(cal)
                elif pos in anis: # days with animations
                    if int(pos) == 5:
                        ani.play5()
                    elif int(pos) == 10:
                        ani.play10()
                    elif int(pos) == 15:
                        ani.play15()
                    elif int(pos) == 1:
                        ani.play1()
                    elif int(pos) == 20:
                        ani.play20()
                    elif int(pos) == 23:

                        ani.play23()
                    elif int(pos) == 24:
                        ani.play24()
                    sh.set_pixels(cal)
            # new cursor position
            new_pos = (new_x1 - new_x/2) +8*new_y/2
            if new_pos <= day:
                x = new_x
                x1 = new_x1
                y = new_y
                pos2 = '%02d' %new_pos
                td.display2digits(pos2)

                sh.set_pixels(cal)
                sh.set_pixel(x, y, 255, 0,0)
                sh.set_pixel(x1, y, 255, 0,0)
        #print(x,y)

        #print(pos)
        if event.type == QUIT:
            running = False
            print("BYE")
