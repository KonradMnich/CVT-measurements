#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 22:32:26 2020

@author: konrad
"""

date = ["24072020"]*12
symmetry = ["_asym"]*6 + ["-sym"]*6
brakes = ["","_br"]*6
ratio = ["_r0", "_r16", "_r32"]*4
#source = ["_mr", "_ni"]*12
#extension = [".csv"]*24

names = []
for i in range(12):
    names += [date[i]+symmetry[i]+brakes[i]+ratio[i]] #+source[i]+extension[i]]

sym = [False, True]*6
bra = [False, True]*6
rat = [0,16,32]*4

import pandas as pd

#name,symmetric,breaks,ratios
df = pd.DataFrame()
df['name'] = names
df['symmetric'] = sym
df['breaks'] = bra
df['ratios'] = rat
#%%
df.to_csv('list.csv',index=False)