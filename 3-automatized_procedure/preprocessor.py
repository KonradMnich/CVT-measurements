#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 16:41:37 2020

@author: konrad
"""
import pandas as pd
import numpy as np

class Preprocessor:
    def __init__(self, list_of_inputs="list_of_inputs.csv", ratios=[0,16,32],\
                 breaks=[False,True], symmetric=[False,True]):
        self.df_in = pd.read_csv(list_of_inputs)
        self.df_in = self.df_in[self.df_in['ratios'].isin(ratios) &\
                           self.df_in['breaks'].isin(breaks) &\
                           self.df_in['symmetric'].isin(symmetric)]
        self.raw_ni = self.read_ni()
        self.raw_mr = self.read_mr()
        self.scaled_ni = self.scale_ni()
        self.scaled_mr = self.scale_and_expand_mr()
        
    def read_ni(self):
        l=[]
        for n in self.df_in['name']:
            df = pd.read_csv('inputs/'+n+'_ni.csv', usecols=[0,1,3],\
                             skiprows=4, names=['t','F','x'])
            # touples consisting of a data frame and a sampling period
            l += [(df[['F','x']].astype(float), df.iloc[1,0].astype(float))]
        return l
    
    def read_mr(self):
        l=[]
        for n in self.df_in['name']:
            df = pd.read_csv('inputs/'+n+'_mr.csv', usecols=[0,1],\
                             skiprows=5, names=['t','v'])
            # touples consisting of a data frame and a sampling period
            l += [(df[['v']].astype(float), df.iloc[1,0].astype(float)/1000)]
        return l
        
    def scale_ni(self):
        l=[]
        for n in self.raw_ni:
            df = n[0]
            
            # force
            F0 = (max(df['F'])+min(df['F']))/2
            df['F'] -= F0 # shifting zero
            df['F'] *= 200  # scaling to Newtons
            
            # displacement
            x0 = np.mean(df['x'].iloc[:10])
            df['x'] -= x0 # shifting zero
            df['x'] /= 55.4 # scaling to meters
            
            l += [[df,n[1]]]
        return l
    
    def scale_and_expand_mr(self):
        l=[]
        for n in self.raw_mr:
            df = n[0]
            df['v'] *= 20/60/1000  # scaling rpm to m/s
            #df['x'] = [0, *np.cumsum(df['v'])*n[1]]
            df['x'] = np.cumsum(df['v'])*n[1]
            df['a'] = [0, *np.diff(df['v'])/n[1]]
            df['a'] = df['a'].rolling(10,center=True).mean().fillna(0)
            l += [[df,n[1]]]
        return l
    
  
            