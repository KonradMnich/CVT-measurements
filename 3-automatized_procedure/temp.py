#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 22:32:26 2020

@author: konrad
"""

date = ["24072020"]*24
symmetry = ["_asym","-sym"]*12
brakes = ["","_br"]*12
ratio = ["_r0", "_r16", "_r32"]*8
#source = ["_mr", "_ni"]*12
#extension = [".csv"]*24

names = []
for i in range(24):
    names += [date[i]+symmetry[i]+brakes[i]+ratio[i]] #+source[i]+extension[i]]

sym = [False, True]*12
bra = [False, True]*12
rat = [0,16,32]*8

import pandas as pd

#name,symmetric,breaks,ratios
df = pd.DataFrame()
df['name'] = names
df['symmetric'] = sym
df['breaks'] = bra
df['ratios'] = rat
#%%
df.to_csv('list.csv',index=False)