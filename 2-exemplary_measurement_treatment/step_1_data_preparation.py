#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 11:50:51 2020

@author: konrad
"""

from reusable import DataConditioner

# names of the files available for analysis
file_names = [("r0v0a0mr.csv","r0v0a0pot.csv"),\
              ("r0a1mr.csv","r0a1pot.csv"),\
              ("r0a1bmr","r0a1bpot")]

# create the object performing computations
dc = DataConditioner("step_1_in/", "step_1_out/")
dc.read_data_mr(file_names[0][0])
dc.read_data_ni(file_names[0][1])
dc.condition()
#%%
# preview and save preprocessed data
dc.df_ready[['F [N]','x [m]','v [m/s]']].plot(subplots=True)
dc.save()
