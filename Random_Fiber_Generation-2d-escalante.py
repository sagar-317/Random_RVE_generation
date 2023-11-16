import numpy as np
import random as rand
from math import sin, cos
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

xlen=21.25e-3  
ylen=21.25e-3
# zlen=50

def checker(x, y, cx, xy):
    global r
    dmin = 2.25*r

    if (x <= r and y <= r):
        compat = np.max([np.max(np.sqrt((cx-x)**2 + (cy-y)**2) < dmin),
                         np.max(np.sqrt((cx-(x+xlen))**2 + (cy-y)**2) < dmin),
                         np.max(np.sqrt((cx-x)**2 + (cy-(y+ylen))**2) < dmin),
                         np.max(np.sqrt((cx-(x+xlen))**2 + (cy-(y+ylen))**2) < dmin)])
        region = 6

    elif (x <= r and y >= ylen-r):
        compat = np.max([np.max(np.sqrt((cx-x)**2 + (cy-y)**2) < dmin),
                         np.max(np.sqrt((cx-(x+xlen))**2 + (cy-y)**2) < dmin),
                         np.max(np.sqrt((cx-x)**2 + (cy-(y-ylen))**2) < dmin),
                         np.max(np.sqrt((cx-(x+xlen))**2 + (cy-(y-ylen))**2) < dmin)])
        region = 9

    elif (x >= xlen-r and y >= ylen-r):
        compat = np.max([np.max(np.sqrt((cx-x)**2 + (cy-y)**2) < dmin),
                         np.max(np.sqrt((cx-(x-xlen))**2 + (cy-y)**2) < dmin),

                         np.max(np.sqrt((cx-x)**2 + (cy-(y-ylen))**2) < dmin),
                         np.max(np.sqrt((cx-(x-xlen))**2 + (cy-(y-ylen))**2) < dmin)])
        region = 8

    elif (x >= xlen-r and y <= r):
        compat = np.max([np.max(np.sqrt((cx-x)**2 + (cy-y)**2) < dmin),
                         np.max(np.sqrt((cx-(x-xlen))**2 + (cy)**2) < dmin),
                         np.max(np.sqrt((cx-x)**2 + (cy-(y+ylen))**2) < dmin),
                         np.max(np.sqrt((cx-(x-xlen))**2 + (cy-(y+ylen))**2) < dmin)])
        region = 7

    elif (x > r and x < xlen-r and y <= r):
        compat = np.max([np.max(np.sqrt((cx-x)**2 + (cy-y)**2) < dmin),
                         np.max(np.sqrt((cx-(x))**2 + (cy-(y+ylen)**2) < dmin))])
        region = 2

    elif (x > r and x < xlen-r and y >= ylen-r):
        compat = np.max([np.max(np.sqrt((cx-x)**2 + (cy-y)**2) < dmin),
                         np.max(np.sqrt((cx-(x))**2 + (cy-(y-ylen))**2) < dmin)])
        region = 3

    elif (x <= r and y < ylen-r and y > r):
        compat = np.max([np.max(np.sqrt((cx-x)**2 + (cy-y)**2) < dmin),
                         np.max(np.sqrt((cx-(x+xlen))**2 + (cy-y)**2) < dmin)])
        region = 4

    elif (x >= xlen-r and y < xlen-r and y > r):
        compat = np.max([np.max(np.sqrt((cx-x)**2 + (cy-y)**2) < dmin),
                         np.max(np.sqrt((cx-(x-xlen))**2 + (cy-y)**2) < dmin)])
        region = 5

    else:
        compat = np.max(np.sqrt((cx-x)**2 + (cy-y)**2) < dmin)
        region = 1

    return compat, region


def update(x, y, nop, region):
    global cx, reg
    global cy, pn
    if region == 1:
        cx = np.append(cx, x)
        cy = np.append(cy, y)
        pn = np.append(pn, nop)
        reg = np.append(reg, region)
    if region == 2:
        cx = np.append(cx, [x, x])
        cy = np.append(cy, [y+ylen])
        pn = np.append(pn, [nop, nop])
        reg = np.append(reg, [region, region])
    if region == 3:
        cx = np.append(cx, [x, x])
        cy = np.append(cy, [y, y-ylen])
        pn = np.append(pn, [nop, nop])
        reg = np.append(reg, [region, region])
    if region == 4:
        cx = np.append(cx, [x, x+xlen])
        cy = np.append(cy, [y, y])
        pn = np.append(pn, [nop, nop])
        reg = np.append(reg, [region, region])
    if region == 5:
        cx = np.append(cx, [x, x-xlen])
        cy = np.append(cy, [y, y])
        pn = np.append(pn, [nop, nop])
        reg = np.append(reg, [region, region])
    if region == 6:
        cx = np.append(cx, [x, x, x+xlen, x+xlen])
        cy = np.append(cy, [y, y+ylen, y, y+ylen])
        pn = np.append(pn, [nop, nop, nop, nop])
        reg = np.append(reg, [region, region, region, region])
    if region == 7:
        cx = np.append(cx, [x, x, x-xlen, x-ylen])
        cy = np.append(cy, [y, y+ylen, y, y+ylen])
        pn = np.append(pn, [nop, nop, nop, nop])
        reg = np.append(reg, [region, region, region, region])
    if region == 8:
        cx = np.append(cx, [x, x, x-xlen, x-xlen])
        cy = np.append(cy, [y, y-ylen, y, y-ylen])
        pn = np.append(pn, [nop, nop, nop, nop])
        reg = np.append(reg, [region, region, region, region])
    if region == 9:
        cx = np.append(cx, [x, x, x+xlen, x+xlen])
        cy = np.append(cy, [y, y-ylen, y, y-ylen])
        pn = np.append(pn, [nop, nop, nop, nop])
        reg = np.append(reg, [region, region, region, region])


def s3reg(x, y, d):
    if (x <= d and y <= d):
        region = 5

    elif (x <= d and y >= ylen-d):
        region = 8

    elif (x >= xlen-d and y >= ylen-d):
        region = 7

    elif (x >= xlen-d and y <= d):
        region = 6

    elif (x > d and x < xlen-d and y <= d):
        region = 3

    elif (x > d and x < xlen-d and y >= ylen-d):
        region = 4

    elif (x <= d and y < ylen-d and y > d):
        region = 1

    elif (x >= xlen-d and y < ylen-d and y > d):
        region = 2

    else:
        region = 0

    return region


def stir3(x, y, reg3, nop, region):
    PI = 3.14159
    global cx
    global cy, pn, reg
    global r

    #global changes,nochange

    if reg3 == 1:
        ang = (-0.5*PI, 0.5*PI)
    if reg3 == 2:
        ang = (0.5*PI, 1.5*PI)
    if reg3 == 3:
        ang = (0, PI)
    if reg3 == 4:
        ang = (-PI, 0)
    if reg3 == 5:
        ang = (0, 0.5*PI)
    if reg3 == 6:
        ang = (0.5*PI, PI)
    if reg3 == 7:
        ang = (PI, 1.5*PI)
    if reg3 == 8:
        ang = (1.5*PI, 2*PI)

    rad = 0.75*r
    while(rad > 0):
        br = 0
        for i in range(0, 10):
            angle = rand.uniform(ang[0], ang[1])
            nx = x + rad*cos(angle)
            ny = y + rad*sin(angle)
            uncompatible, newr = checker(nx, ny, cx, cy)
            if uncompatible == 1:
                continue
            if uncompatible == 0:
                br = 1
                break

        if br == 1:
            update(nx, ny, nop, newr)
            break

        rad = rad-0.25*r
    if br == 0:
        update(x, y, nop, region)


def plotter():
    global cx, cy, r

    fig, ax = plt.subplots()
    ax.set(xlim=(0, xlen), ylim=(0, ylen))
    ax.set_aspect(1)
    plt.title("iter-"+str(iter)+" step"+str(step)+"  vf="+str(vf))
    for i in range(0, len(cx)):
        a_circle = plt.Circle((cx[i], cy[i]), r, fill=False, linewidth=0.1)
        ax.add_artist(a_circle)
    plt.savefig("iter-"+str(iter)+" step"+str(step)+".png", dpi=500)


cx = np.array([rand.uniform(0, xlen)])
cy = np.array([rand.uniform(0, ylen)])
pn = np.array([1])
reg = np.array([1])

nop = 1
r = 2.1e-3               #change radius
ngmax = 50000
vf = (3.14159*r*r)/(xlen*ylen)
vfmax = 0.50       #change volume fractiom
d = 2.8*r          #originally 3r
iter = 1

while(vf < vfmax):
    ng = 0
    step = 1
    while(ng < ngmax):
        ng = ng+1

        xtemp = rand.random()*xlen
        ytemp = rand.random()*ylen
        uncompatible, regtemp = checker(xtemp, ytemp, cx, cy)
        if uncompatible == 1:
            continue
        nop = nop+1
        update(xtemp, ytemp, nop, regtemp)
        vf = vf+3.14159*r*r/(xlen*ylen)
        if vf > vfmax:
            break
    # plotter()

    i_f = 0
    d = d+(8.5-10*vfmax)*r
    step = 3
    while(i_f < nop):
        i_f = i_f + 1
        xtemp, ytemp, regtemp = cx[0], cy[0], reg[0]
        if regtemp == 1:
            cx = cx[1:]
            cy = cy[1:]
            reg = reg[1:]
            pn = pn[1:]
        elif regtemp in [2, 3, 4, 5]:
            cx = cx[2:]
            cy = cy[2:]
            reg = reg[2:]
            pn = pn[2:]
        elif regtemp in [6, 7, 8, 9]:
            cx = cx[4:]
            cy = cy[4:]
            reg = reg[4:]
            pn = pn[4:]

        s3region = s3reg(xtemp, ytemp, d)
        if s3region == 0:
            update(xtemp, ytemp, i_f, regtemp)
            continue
        stir3(xtemp, ytemp, s3region, i_f, regtemp)
    #
    iter = iter+1

np.savetxt("RVE_Centre_Coordinate_x.txt", cx)
np.savetxt("RVE_Centre_Coordinate_y.txt", cy)


plotter()
for var in dir():
    if not (var.startswith('_') or var == "cx" or var == "cy"):
        del globals()[var]

with open('file3.txt', 'w+') as file3:
    with open('RVE_Centre_Coordinate_x.txt', 'r') as file1:
        with open('RVE_Centre_Coordinate_y.txt', 'r') as file2:
            for line1, line2 in zip(file1, file2):
                print(line1.strip(), line2.strip(), file=file3)