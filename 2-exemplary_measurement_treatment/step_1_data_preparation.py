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
              ("r0a1bmr.csv","r0a1bpot.csv"),\
              ("22.07.2020/v100xa10mr.csv","22.07.2020/v100xa10ni.csv")]
file_name = '22.07.2020/a2mr10'

# create the object performing computations
dc = DataConditioner("step_1_in/", "step_1_out/")
dc.read_data_mr(file_name+"mr.csv")
dc.read_data_ni(file_name+"ni.csv")
dc.condition()
#%%
# preview and save preprocessed data
dc.df_basic[['F [N]','x [m]','v [m/s]']].plot(subplots=True)

#%% add acceleration, filter force and acceleration and preview
# adjust averaging window for the force
dc.assemble_plus(1,5)
plt.figure()
dc.df_basic['F [N]'].plot()
dc.df_plus['F [N]'].plot(title="Force")

#%%
# adjust averaging window for the acceleration
dc.assemble_plus(1,5)
dc.df_plus['a [m/s^2]'].plot()
dc.assemble_plus(10,5)
dc.df_plus['a [m/s^2]'].plot(title="acceleration")

#%% save
name = "a2mr10"
dc.save(name+".csv")
dc.save_plus(name+"_plus.csv")