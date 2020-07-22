#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 14:42:14 2020

@author: konrad
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

path_in = "step_1_out/"
path_out = "step_1_out/"
file_name = "smooth"

df_plus = pd.read_csv(path_in+file_name+"_plus.csv")

# find start of motion
v = df_plus['v [m/s]'].tolist()
v_mask = [n > 0 for n in v]
i_start = v_mask.index(True)
t_start = df_plus['t [s]'].iloc[i_start]

sns.set_style('whitegrid')
axs = df_plus.plot(subplots=True, sharex=True,x='t [s]',figsize=(6,8))
fig = axs[0].figure
fig.dpi = 600
axs[0].set_title("Force measured on 'random' input\n")
axs[0].plot([t_start,t_start],[0, 175],color='red')