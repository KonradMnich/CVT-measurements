#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 01:42:30 2020

@author: konrad
"""


import pandas as pd
import numpy as np

class Data_conversion:
    def __init__(self, in_path="raw_data/", out_path="step_1_out/"):
        self.df = pd.DataFrame()
        self.in_path = in_path
        self.out_path = out_path
        
    def get_series(self, name_in, title, fun, col=1):
        df = pd.read_csv(self.in_path+name_in,skiprows=5)
        T = (df.iloc[1,0]-df.iloc[0,0])
        self.df[title]=df.iloc[:,col]
        self.df[title]=self.df[title].apply(\
                            lambda x: x-np.mean(self.df[title].iloc[1:10]))
        self.df[title]=self.df[title].apply(fun)
        self.df[title].loc[0] = T
    
    def save(self,file_name='default_name.csv'):
        self.df.to_csv(self.out_path + file_name)
        
    def rpm2mps(x):
        return -x*20/1000/60
    
    def r2m(x):
        return x*3.1415*40/1000
    
    def V2m(x):
        return x/55.4
    
    def cumtrapz(self,col):
        v = self.df[col].tolist()
        w = [v[0]/1000,0]
        for i in range(1,len(v)-1):
            w.append(w[i]+(v[i]+v[i+1])*v[0]/2/1000)
        self.df["integrated_"+col] = pd.Series(w)
        