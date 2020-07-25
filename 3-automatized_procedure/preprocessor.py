#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 24 16:41:37 2020

@author: konrad
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
        self.resample_ni()
        self.synchronize_and_append()
        
    def read_ni(self):
        l=[]
        for n in self.df_in['name']:
            df = pd.read_csv('inputs/'+n+'_ni.csv', usecols=[0,1,3],\
                             skiprows=4, names=['t','F','x'])
            # touples consisting of a data frame and a sampling period
            l += [(df[['F','x']].astype(float), df.iloc[1,0].astype(float))]
            '''for debugging'''
            plt.figure()
            df['F'].plot()
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
            df['F'] *= -200  # scaling to Newtons
            df['F'] = df['F'].rolling(10,center=True).mean().fillna(0)
            
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
            df['v'] *= -20/60/1000  # scaling rpm to m/s
            #df['x'] = [0, *np.cumsum(df['v'])*n[1]]
            df['x'] = np.cumsum(df['v'])*n[1]
            df['a'] = [0, *np.diff(df['v'])/n[1]]
            df['a'] = df['a'].rolling(10,center=True).mean().fillna(0)
            l += [[df,n[1]]]
        return l
    
    def resample_ni(self):
        for i in range(len(self.scaled_ni)):
            df = self.scaled_ni[i][0]
            T_old = self.scaled_ni[i][1]
            T_new = self.scaled_mr[i][1]
            t_old = np.cumsum([T_old]*len(df))-T_old   
            t_new = np.cumsum([T_new]*len(self.scaled_mr[i][0]))-T_new
            df_new = pd.DataFrame()
            df_new['x'] = np.interp(t_new,t_old,df['x'])
            df_new['F'] = np.interp(t_new,t_old,df['F'])
            self.scaled_ni[i][0] = df_new
            
    
    def synchronize_and_append(self):
        for i in range(len(self.df_in)):
            x_mr =  self.scaled_mr[i][0]['x'].to_numpy()
            x_ni =  self.scaled_ni[i][0]['x'].to_numpy()
            se = sum((x_mr[200:-200]-x_ni[200:-200])**2)
            for j in range(len(x_ni)):
                x_ni = np.append(x_ni,x_ni[0])
                x_ni = x_ni[1:]
                se_temp = sum((x_mr[200:-200]-x_ni[200:-200])**2)
                if se_temp < se:
                    se = se_temp
                    ind = j
            F_ni =  self.scaled_ni[i][0]['F'].tolist()
            self.scaled_mr[i][0]['F'] = F_ni[ind:] + F_ni[:ind]
            ''' for debugging purpose
            plt.figure()
            plt.plot(x_mr,label='mr')
            plt.plot(x_ni,label='before')
            plt.plot(np.concatenate((x_ni[-ind:], x_ni[:ind])))
            plt.legend(['mr','before','after'])
            '''
    
    def out(self):
        return pd.concat([n[0] for n in self.scaled_mr])
            