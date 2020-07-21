#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:50:51 2020

@author: konrad
"""

from reusable import DataConditioner
import matplotlib.pyplot as plt

# names of the files available for analysis
file_names = [("r0v0a0mr.csv","r0v0a0pot.csv"),\
              ("r0a1mr.csv","r0a1pot.csv"),\
              ("r0a1bmr.csv","r0a1bpot.csv")]

# create the object performing computations
dc = DataConditioner("step_1_in/", "step_1_out/")
dc.read_data_mr(file_names[2][0])
dc.read_data_ni(file_names[2][1])
dc.condition()
#%%
# preview and save preprocessed data
dc.df_basic[['F [N]','x [m]','v [m/s]']].plot(subplots=True)

#%% add acceleration, filter force and acceleration and preview
# adjust averaging window for the force
dc.assemble_plus(10,10)
plt.figure()
dc.df_basic['F [N]'].plot()
dc.df_plus['F [N]'].plot(title="Force")
#%%
# adjust averaging window for the acceleration
dc.assemble_plus(1,10)
dc.df_plus['a [m/s^2]'].plot()
dc.assemble_plus(10,10)
dc.df_plus['a [m/s^2]'].plot(title="acceleration")

#%% save
dc.save("smooth.csv")
dc.save_plus("smooth_plus.csv")