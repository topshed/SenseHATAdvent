from sense_hat import SenseHat
import datetime as dt
import random
sh = SenseHat()
sh.clear()


day = dt.date.today().day

O = (0,0,0)
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

def day2led(day):
    if day % 2 == 1:
        ledPair = (day, day -1)
    else:
        ledPair = (day, day + 1)
    return ledPair

for d in range(2*day):
    p = day2led(d)
    print(p)
    r = random.randint(50,255)
    g = random.randint(50,255)
    b = random.randint(50,255)
    cal[p[0]] = (r,g,b)
    cal[p[1]] = (r,g,b)
sh.set_pixels(cal)
