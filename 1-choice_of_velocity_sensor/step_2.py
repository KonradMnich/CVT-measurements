#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 12:21:16 2020

@author: konrad

% In this script I interpolate the data to make further comutations easier
and rotate them in order to synchronize.

"""
import pandas as pd
#mport numpy as np
from Data_conversion import interpolate, synchronize

# set input and output paths
path_in = "step_1_out/"
path_out= "step_2_out/"

# read data from step 1 of curing data
serv = pd.read_csv(path_in+"v_mr.csv",usecols=[5,4,3])
pot = pd.read_csv(path_in+"x_pot.csv")
enc = pd.read_csv(path_in+"x_enc.csv")

# homodenizing sampling by interpolation and put resampled date into new dataframe
df = pd.DataFrame()
for i in range(3):
    df[str(i*3)] = serv.iloc[1:,i]
    df[str(i*3+1)] = interpolate(serv.iloc[:,i], pot.iloc[:,i])
    df[str(i*3+2)] = interpolate(serv.iloc[:,i], enc.iloc[:,i])
    '''could be done by a built in method "rolling"'''

# as the series have different lengths, fill the gaps with zeros
df.fillna(0, inplace=True)

# add new column containing sapling periods for each measurement case
df['T'] = serv.iloc[0,:].tolist() + [None]*(len(df['1'])-3)

# clear the workspace
del enc, i, pot, serv

#%%
# synchronize the series minimizing squared errors
# rearrange data into new dataframe
sync = pd.DataFrame()
for i in range(3):
    sync[str(i*3)] = df.iloc[:,3*i]
    sync[str(i*3+1)] = synchronize(df.iloc[:,3*i], df.iloc[:,3*i+1])
    sync[str(i*3+2)] = synchronize(df.iloc[:,3*i], df.iloc[:,3*i+2])

# drop last rows that contain mainly padded zeros    
sync.drop(sync.tail(50).index, inplace=True)

#%%
# add headings to the dataframe and save it to a file
headings_l1 = ["case 1 - const vel (T="+str(df['T'].iloc[0])+')']*3 +\
    ["case2 - const acc (T="+str(df['T'].iloc[1])+')']*3 +\
        ["case3 - smooth (T="+str(df['T'].iloc[2])+')']*3
headings_l2 = ("servo_x[m] potent._x[m] encoder_x[m]".split())*3
headings = [headings_l1, headings_l2]
tuples = list(zip(*headings))
index = pd.MultiIndex.from_tuples(tuples, names=['l1', 'l2'])
sync.columns=index
sync.to_csv(path_out+'all_x_data.csv')

#%%
# plots made to double check the results 
''' PREVIEW
from matplotlib import pyplot as plt

fig = plt.Figure()
ax = plt.axes()
ax.plot(df.iloc[1:,3])
ax.plot(df.iloc[1:,4])
ax.plot(df.iloc[1:,5])

#%%
fig = plt.Figure()
ax = plt.axes()
ax.plot(sync.iloc[1:,3])
ax.plot(sync.iloc[1:,4])
ax.plot(sync.iloc[1:,5])
'''