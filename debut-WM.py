#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 7 2018

@author: huisun
"""

import os
import sys
import random
import numpy as np
import pandas as pd
from itertools import combinations
from psychopy import core, visual, gui, event
import pygame

""" CHECK BEFORE RUNNING  """
# monitor settings
win_width = 800
win_height = 600
scrn = 0
full_scrn = False
refresh_rate = 60

win = visual.Window(size = [win_width, win_height], units='pix', color = 'black')

# experiment settings

# grid
grid_row = 4
grid_col = 4
grid_size = 60
margin = 20
gap = grid_size + margin
canvas_size = [win_width/2, win_height/2]
loc = [0,0]
target_color = (0.9,0.5,-1) # yellow
nontarget_color = (1,1,1) # white


# array of coordinates for each element
xys = []
for x in range(grid_row):
    for y in range(grid_col):
        xys.append((gap * x - 3/2*gap,
                    gap * y - 3/2*gap))


level = 3

target = [[0,0],[1,1],[2,2]]
for item in target:
    index = grid_row*item[1] + grid_col - 1 - item[0]
    # color coordinates are different from target coordinates
    # "colors" mark cells from the bottom left to top right, populate first column then next
    # "target" mark cells from the top left to bottom right, populate first row then next
colors = [nontarget_color] * (grid_col * grid_row)
colors[index] = target_color

print(colors)

# array of rgbs for each element (2D)
"""
colors = [(0.9, 0.9, 0.9),(0.9, 0.9, 0.9), (0.9, 0.9, 0.9), (0.9, 0.9, 0.9),
          (0.9, 0.9, 0.9),(0.2, 0.9, 0.9), (0.9, 0.9, 0.9), (0.9, 0.9, 0.9),
          (0.9, 0.9, 0.9),(0.9, 0.9, 0.9),(0.9, 0.9, 0.9),(0.9, 0.9, 0.9),
          (0.9, 0.9, 0.9),(0.9, 0.9, 0.9),(0.2, 0.9, 0.9),(0.9, 0.9, 0.9)]
"""

stim = visual.ElementArrayStim(win,
                               xys=xys,
                               fieldPos=loc,
                               colors=colors,
                               nElements=grid_row * grid_col,
                               elementMask=None,
                               elementTex=None,
                               sizes=(grid_size,grid_size))

stim.size = (canvas_size[0], canvas_size[1])

for i in range(60):
    stim.draw()
    win.flip()

core.wait(1)