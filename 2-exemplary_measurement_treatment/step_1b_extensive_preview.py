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

#df = pd.read_csv(path_in+file_name+".csv")
df_plus = pd.read_csv(path_in+file_name+"_plus.csv")

sns.set_style('whitegrid')
plt.figure()
df_plus[['F [N]','x [m]','v [m/s]','a m/s^2']].plot(subplots=True)
#plt.set...