#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  1 12:13:43 2018

@author:Hui Sun
Please direct any questions to: hui.sun@kellogg.northwestern.edu.
"""

import os
import sys
import random
import numpy as np
import pandas as pd
from itertools import combinations
from psychopy import core, visual, gui, event

""" CHECK BEFORE RUNNING  """
# monitor settings
win_width = 800
win_height = 600
scrn = 0
full_scrn = False
refresh_rate = 60

# exp parameters
condition = 1
max_round = 6
duration_s = 10.0
fixation_lower = 0.5
fixation_upper = 1.0
name_list = ['Alice', 'Bob', 'Cathy', 'Daniel']
target_list = ['p', 'p', 'p', 'q', 'q', 'q']
""""""

# create combinations
perm_list = []
for i in combinations(name_list, 2):
    perm_list.append((i[0], i[1]))

# shuffle
zip_list = list(zip(perm_list, target_list))
random.shuffle(zip_list)

n_trials = len(perm_list)

# window
task_win = visual.Window(size=[win_width, win_height], color = (0.3, 0.3, 0.3), colorSpace='rgb', units='pix', screen=scrn, fullscr=full_scrn)
# timing devices
global_clock = core.Clock()
local_clock = core.Clock()
ISI = core.StaticPeriod(screenHz=refresh_rate, win=task_win)

# stimuli
fixation = visual.TextStim(text='+', height=100, alignHoriz='center', alignVert='center', win=task_win)
#left_cue = visual.TextStim(text='Not Connected', height=20, alignHoriz='left', alignVert='bottom', win=task_win)
#right_cue = visual.TextStim(text='Connected', height=20, alignHoriz='right', alignVert='bottom', win=task_win)
left_cue = visual.TextStim(text='Not Connected', antialias=True, pos = [-300,-200], height=20, win=task_win)
right_cue = visual.TextStim(text='Connected',  antialias=True, pos = [300, -200], height=20, win=task_win)
feedback_wrong = visual.TextStim(text='Incorrect!',  antialias=True, height=40, color=(1,0,0), colorSpace='rgb', win=task_win)
feedback_correct = visual.TextStim(text='Correct!',  antialias=True, height=40, color=(0,1,0), colorSpace='rgb', win=task_win)

# data
data_colnames = ['subjectID','round','trial','rt','correct','name1', 'name2', 'target']

def genDF(max_round, n_trials, data_colnames):
    emp = np.zeros([max_round * n_trials, len(data_colnames)])  # Creates an empty NumPy array
    df = pd.DataFrame(data = emp, columns = data_colnames)  # Transforms the array into a data frame

    df['subjectID'] = df['subjectID'].astype(int)
    df['round'] = df['round'].astype(int)
    df['trial'] = df['trial'].astype(int)
    df['rt'] = df['rt'].astype(float)
    df['correct'] = df['correct'].astype(int)
    df['name1'] = df['name1'].astype(str)
    df['name2'] = df['name2'].astype(str)
    df['target'] = df['target'].astype(str)

    return df

def runTrial(task_data, text1, text2, target, ISI, local_clock, current_row,
             task_win = task_win,
             fixation = fixation, fixation_lower = fixation_lower, fixation_upper = fixation_upper,
             feedback_correct = feedback_correct, feedback_wrong = feedback_wrong):
    # draw fixation
    fixation.draw()
    task_win.flip()
    # start ISI timer
    this_ISI = np.random.uniform(fixation_lower, fixation_upper)
    print(this_ISI)
    ISI.start(this_ISI)
    t1 = local_clock.getTime()
    # preload stimuli
    sti1 = visual.TextStim(text=text1, height=40, pos=[-200, 0], win=task_win)
    sti2 = visual.TextStim(text=text2, height=40, pos=[200, 0], win=task_win)
    sti1.draw()
    sti2.draw()
    left_cue.draw()
    right_cue.draw()
    this_resp = None
    # stop ISI timer
    ISI.complete()
    t2 = local_clock.getTime()
    task_win.flip()
    local_clock.reset()
    while True:
        keys = event.getKeys(keyList=['p', 'q'], timeStamped=local_clock)
        for key in keys:
            # print(key)
            if key[0] == target and key[1] > 0:
                t = local_clock.getTime()
                feedback_correct.draw()
                task_win.flip()
                this_resp = 1
                task_data.at[current_row, 'rt'] = t
                task_data.at[current_row, 'correct'] = this_resp
                core.wait(1)
                break
            elif key[0] != target and key[1] > 0:
                t = local_clock.getTime()
                feedback_wrong.draw()
                task_win.flip()
                this_resp = 0
                task_data.at[current_row, 'rt'] = t
                task_data.at[current_row, 'correct'] = this_resp
                core.wait(1)
                break

        if this_resp != None:
            break

        if event.getKeys(['escape']):
            core.quit()
        if local_clock.getTime() > duration_s:
            break

    event.clearEvents()
    #print(trial_num, t2 - t1)
    if this_resp != None:
        return this_resp

gui = gui.Dlg()
gui.addField("SubjectID:")
gui.show()
subj_ID = gui.data[0]
data_path = subj_ID + ".csv"

task_data = genDF(max_round, n_trials, data_colnames)
round_pass2 = 0
round_pass1 = 0
current_round = 0
while round_pass1 * round_pass2 != 1 and current_round < max_round:
    random.shuffle(zip_list)
    resp = 1
    for current_trial in range(n_trials):
        text1 = zip_list[current_trial][0][0]
        text2 = zip_list[current_trial][0][1]
        target = zip_list[current_trial][1]
        current_row = current_round * n_trials + current_trial
        resp *= runTrial(task_data=task_data, text1 = text1, text2 = text2, target = target,
                         current_row = current_row, ISI=ISI, local_clock=local_clock)
        task_data.at[current_row, 'round'] = current_round
        task_data.at[current_row, 'trial'] = current_trial
        task_data.at[current_row, 'name1'] = text1
        task_data.at[current_row, 'name2'] = text2
        task_data.at[current_row, 'target'] = target
    if current_round == 1:
        round_pass1 = resp
    else:
        round_pass2 = round_pass1
        round_pass1 = resp
    current_round += 1

print(task_data)
task_data.to_csv(data_path)
