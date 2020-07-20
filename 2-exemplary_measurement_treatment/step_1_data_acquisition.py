# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 14:21:59 2020

@author: Konrad
"""
import pandas as pd

path_in = "step_1_in/"
path_out = "step_1_out/"

# read data from data acquisition unit
df_const = pd.DataFrame()
df_const['F'] = pd.read_csv(path_in+"r0a1bpot.csv",\
                            usecols=[1]).iloc[:,0].to_numpy()
df_const['x'] = pd.read_csv(path_in+"r0a1bpot.csv",\
                            usecols=[3]).iloc[:,0].to_numpy()

# read data from servodrive
df_temp = pd.DataFrame()
df_temp['v_mr'] = pd.read_csv(path_in+"r0a1bmr.csv",\
                              usecols=[1], skiprows=1).iloc[:,0].to_numpy()
df_temp.iloc[0,0] = pd.to_numeric(df_temp.iloc[0,0])/1000

# concatenate both
df_const = pd.concat([df_const,df_temp],axis=1)

# displace automatic headings to another DataFrame "info"
info = df_const.iloc[0:3,:]
info['i'] = ['T','name','unit']
info.set_index('i',inplace=True)
info.iloc[2,2]='rpm'
df_const.drop(index=[0,1,2],inplace=True)

#%%
# scale sensor data to SI
df_const.fillna(0,inplace=True)
df_const = df_const.astype(float)
f_0 = sum(df_const['F'].iloc[0:10].tolist())/10
x_0 = sum(df_const['x'].iloc[0:10].tolist())/10
df_const['F'] = df_const['F'].apply(lambda x: -(x-f_0)*200)
df_const['x'] = df_const['x'].apply(lambda x: (x-x_0)/55.4)
df_const['v_mr'] = df_const['v_mr'].apply(lambda x: -x*20/60/1000)

# compute distance x_mr basing on v_mr 
df_const['x_mr'] =\
    df_const['v_mr'].astype(float).cumsum().apply(lambda x: x*0.00244)

# clean unused
del df_temp, x_0, f_0